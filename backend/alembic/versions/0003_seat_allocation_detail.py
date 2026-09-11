"""add seat allocation detail fields

Revision ID: 0003_seat_allocation_detail
Revises: 0002_clause_history_titles
Create Date: 2026-09-11 16:20:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "0003_seat_allocation_detail"
down_revision: str | None = "0002_clause_history_titles"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "seat_allocation_results",
        sa.Column("factor_scores", sa.JSON(), nullable=False, server_default="[]"),
    )
    op.add_column(
        "seat_allocation_results",
        sa.Column("priority_factors", sa.JSON(), nullable=False, server_default="[]"),
    )
    op.add_column(
        "seat_allocation_results",
        sa.Column("seat_reasons", sa.JSON(), nullable=False, server_default="[]"),
    )
    op.add_column("seat_allocation_results", sa.Column("better_if", sa.Text(), nullable=True))
    op.alter_column("seat_allocation_results", "factor_scores", server_default=None)
    op.alter_column("seat_allocation_results", "priority_factors", server_default=None)
    op.alter_column("seat_allocation_results", "seat_reasons", server_default=None)


def downgrade() -> None:
    op.drop_column("seat_allocation_results", "better_if")
    op.drop_column("seat_allocation_results", "seat_reasons")
    op.drop_column("seat_allocation_results", "priority_factors")
    op.drop_column("seat_allocation_results", "factor_scores")
