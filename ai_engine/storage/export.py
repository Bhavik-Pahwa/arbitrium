"""Exports accepted facts to a JSON bundle shaped for manual/human review
and eventual loading into the backend's data model. Deliberately not an
automatic write into backend Postgres — see docs/project/ai-engine-checklist.md
design decision 2.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from storage.fact_store import FactStore


def export_bundle(fact_store: FactStore, output_path: Path) -> dict:
    rows = fact_store.all()

    by_institution: dict[str, list[dict]] = {}
    for row in rows:
        by_institution.setdefault(row["institution"], []).append(
            {
                "report_year": row["report_year"],
                "metric": row["metric"],
                "dimension": row["dimension"],
                "dimension_value": row["dimension_value"],
                "numeric_value": row["numeric_value"],
                "unit": row["unit"],
                "status": row["status"],
                "source_url": row["source_url"],
                "source_excerpt": row["source_excerpt"],
                "hallucination_check_passed": bool(row["hallucination_check_passed"]),
            }
        )

    bundle = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "institutions": by_institution,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    return bundle
