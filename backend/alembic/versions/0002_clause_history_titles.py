"""add clause history titles

Revision ID: 0002_clause_history_titles
Revises: 0001
Create Date: 2026-09-11 15:50:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "0002_clause_history_titles"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "clauses",
        sa.Column(
            "title",
            sa.String(length=255),
            nullable=False,
            server_default="Generated arbitration clause",
        ),
    )
    op.alter_column("clauses", "title", server_default=None)


def downgrade() -> None:
    op.drop_column("clauses", "title")
