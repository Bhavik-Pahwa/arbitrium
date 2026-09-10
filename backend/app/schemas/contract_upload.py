from pydantic import BaseModel, ConfigDict


class ContractUploadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    status: str
    extracted_parties: list | None
    extracted_scope: str | None
    extracted_claim_quantum: float | None
    extracted_claim_currency: str | None
    extracted_governing_law: str | None
