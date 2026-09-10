import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_optional, get_db
from app.core.config import settings
from app.models import ContractUpload, SeatAllocationRequest, SeatAllocationResult, User
from app.schemas.contract_upload import ContractUploadRead
from app.schemas.seat_allocation import (
    SeatAllocationAnalyzeRequest,
    SeatAllocationResponse,
    SeatAllocationResultRead,
)
from app.services import contract_parser, recommendation_engine

router = APIRouter(prefix="/seat-allocation", tags=["seat-allocation"])

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@router.post("/upload-contract", response_model=ContractUploadRead)
async def upload_contract(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only .pdf and .docx files are supported")

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    storage_path = upload_dir / f"{uuid.uuid4().hex}{suffix}"
    contents = await file.read()
    storage_path.write_bytes(contents)

    try:
        extraction = contract_parser.parse(str(storage_path))
        status = "processed"
    except Exception:
        extraction = contract_parser.ExtractionResult()
        status = "extraction_failed"

    upload = ContractUpload(
        user_id=current_user.id if current_user else None,
        filename=file.filename,
        storage_path=str(storage_path),
        status=status,
        extracted_parties=extraction.parties,
        extracted_scope=extraction.scope,
        extracted_claim_quantum=extraction.claim_quantum,
        extracted_claim_currency=extraction.claim_currency,
        extracted_governing_law=extraction.governing_law,
    )
    db.add(upload)
    db.commit()
    db.refresh(upload)
    return upload


@router.post("/analyze", response_model=SeatAllocationResponse)
def analyze(
    payload: SeatAllocationAnalyzeRequest,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    weights = {
        "priority_speed": payload.priority_speed,
        "priority_cost": payload.priority_cost,
        "priority_neutrality": payload.priority_neutrality,
        "priority_enforceability": payload.priority_enforceability,
    }

    candidates = recommendation_engine.recommend(
        db, payload.arbitration_type, payload.governing_law, weights
    )
    if not candidates:
        raise HTTPException(status_code=422, detail="No eligible seats found for the supplied inputs")

    request_row = SeatAllocationRequest(
        user_id=current_user.id if current_user else None,
        contract_upload_id=payload.contract_upload_id,
        arbitration_type=payload.arbitration_type,
        parties=[p.model_dump() for p in payload.parties],
        scope=payload.scope,
        claim_quantum=payload.claim_quantum,
        claim_currency=payload.claim_currency,
        governing_law=payload.governing_law,
        **weights,
    )
    db.add(request_row)
    db.flush()

    for rank, candidate in enumerate(candidates, start=1):
        db.add(
            SeatAllocationResult(
                request_id=request_row.id,
                rank=rank,
                seat_id=candidate.seat.id,
                institution_id=candidate.institution.id,
                score=candidate.score,
                rationale=candidate.rationale,
                pros=candidate.pros,
                cons=candidate.cons,
                citations=candidate.citations,
            )
        )
    db.commit()
    db.refresh(request_row)

    return SeatAllocationResponse(
        request_id=request_row.id,
        arbitration_type=request_row.arbitration_type,
        created_at=request_row.created_at,
        results=[SeatAllocationResultRead.model_validate(r) for r in request_row.results],
    )


@router.get("/{request_id}", response_model=SeatAllocationResponse)
def get_seat_allocation(request_id: int, db: Session = Depends(get_db)):
    request_row = db.get(SeatAllocationRequest, request_id)
    if not request_row:
        raise HTTPException(status_code=404, detail="Seat allocation request not found")
    return SeatAllocationResponse(
        request_id=request_row.id,
        arbitration_type=request_row.arbitration_type,
        created_at=request_row.created_at,
        results=[SeatAllocationResultRead.model_validate(r) for r in request_row.results],
    )
