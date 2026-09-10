"""SQLite-backed storage for accepted ExtractedFact rows."""

import json
import sqlite3
from pathlib import Path

from extraction.schemas import ExtractedFact

SCHEMA = """
CREATE TABLE IF NOT EXISTS extracted_facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    institution TEXT NOT NULL,
    report_year INTEGER,
    metric TEXT NOT NULL,
    dimension TEXT,
    dimension_value TEXT,
    numeric_value REAL,
    unit TEXT,
    status TEXT NOT NULL,
    source_url TEXT NOT NULL,
    source_excerpt TEXT,
    hallucination_check_passed INTEGER,
    created_at TEXT DEFAULT (datetime('now'))
);
"""


class FactStore:
    def __init__(self, db_path: Path):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self._conn = sqlite3.connect(str(db_path))
        self._conn.execute(SCHEMA)
        self._conn.commit()

    def save(self, fact: ExtractedFact) -> int:
        cursor = self._conn.execute(
            """
            INSERT INTO extracted_facts
                (institution, report_year, metric, dimension, dimension_value,
                 numeric_value, unit, status, source_url, source_excerpt,
                 hallucination_check_passed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                fact.institution,
                fact.report_year,
                fact.metric,
                fact.dimension,
                fact.dimension_value,
                fact.numeric_value,
                fact.unit,
                fact.status,
                fact.source_url,
                fact.source_excerpt,
                int(bool(fact.hallucination_check_passed)),
            ),
        )
        self._conn.commit()
        return cursor.lastrowid

    def save_many(self, facts: list[ExtractedFact]) -> list[int]:
        return [self.save(f) for f in facts]

    def all(self) -> list[dict]:
        cursor = self._conn.execute("SELECT * FROM extracted_facts ORDER BY id")
        columns = [c[0] for c in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def by_institution(self, institution: str) -> list[dict]:
        cursor = self._conn.execute(
            "SELECT * FROM extracted_facts WHERE institution = ? ORDER BY id", (institution,)
        )
        columns = [c[0] for c in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def close(self) -> None:
        self._conn.close()
