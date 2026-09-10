"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-09-09

"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True, index=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "seats",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(120), nullable=False, unique=True),
        sa.Column("country", sa.String(120), nullable=False),
        sa.Column("ny_convention_member", sa.Boolean, default=True),
        sa.Column("supervisory_court", sa.String(255), nullable=True),
        sa.Column("governing_statute", sa.String(255), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
    )

    op.create_table(
        "institutions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("short_code", sa.String(20), nullable=False, unique=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("website_url", sa.String(500), nullable=True),
        sa.Column("home_seat_id", sa.Integer, sa.ForeignKey("seats.id"), nullable=True),
    )

    op.create_table(
        "institution_rules",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("institution_id", sa.Integer, sa.ForeignKey("institutions.id"), nullable=False),
        sa.Column("rules_name", sa.String(255), nullable=False),
        sa.Column("version_year", sa.Integer, nullable=True),
        sa.Column("effective_date", sa.Date, nullable=True),
        sa.Column("summary", sa.Text, nullable=True),
        sa.Column("source_url", sa.String(500), nullable=False),
        sa.Column("last_checked_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "annual_report_stats",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("institution_id", sa.Integer, sa.ForeignKey("institutions.id"), nullable=False),
        sa.Column("report_year", sa.Integer, nullable=False),
        sa.Column("new_cases_filed", sa.Integer, nullable=True),
        sa.Column("avg_claim_value_usd", sa.Float, nullable=True),
        sa.Column("avg_duration_months", sa.Float, nullable=True),
        sa.Column("source_url", sa.String(500), nullable=False),
        sa.Column("verified", sa.Boolean, default=False),
        sa.Column("notes", sa.Text, nullable=True),
    )

    op.create_table(
        "fee_schedules",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("institution_id", sa.Integer, sa.ForeignKey("institutions.id"), nullable=False),
        sa.Column("schedule_name", sa.String(255), nullable=False),
        sa.Column("currency", sa.String(10), default="USD"),
        sa.Column("admin_fee_tiers", sa.JSON, nullable=False),
        sa.Column("tribunal_fee_tiers", sa.JSON, nullable=False),
        sa.Column("typical_duration_months_min", sa.Integer, nullable=True),
        sa.Column("typical_duration_months_max", sa.Integer, nullable=True),
        sa.Column("source_url", sa.String(500), nullable=False),
        sa.Column("verified", sa.Boolean, default=False),
    )

    op.create_table(
        "seat_institution_ratings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("seat_id", sa.Integer, sa.ForeignKey("seats.id"), nullable=False),
        sa.Column("institution_id", sa.Integer, sa.ForeignKey("institutions.id"), nullable=False),
        sa.Column("speed_score", sa.Integer, nullable=False),
        sa.Column("cost_score", sa.Integer, nullable=False),
        sa.Column("neutrality_score", sa.Integer, nullable=False),
        sa.Column("enforceability_score", sa.Integer, nullable=False),
        sa.Column("rationale", sa.Text, nullable=True),
    )

    op.create_table(
        "contract_uploads",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=True),
        sa.Column("filename", sa.String(500), nullable=False),
        sa.Column("storage_path", sa.String(1000), nullable=False),
        sa.Column("status", sa.String(30), default="processed"),
        sa.Column("extracted_parties", sa.JSON, nullable=True),
        sa.Column("extracted_scope", sa.String(2000), nullable=True),
        sa.Column("extracted_claim_quantum", sa.Float, nullable=True),
        sa.Column("extracted_claim_currency", sa.String(10), nullable=True),
        sa.Column("extracted_governing_law", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "seat_allocation_requests",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=True),
        sa.Column("contract_upload_id", sa.Integer, sa.ForeignKey("contract_uploads.id"), nullable=True),
        sa.Column("arbitration_type", sa.String(20), nullable=False),
        sa.Column("parties", sa.JSON, nullable=True),
        sa.Column("scope", sa.Text, nullable=True),
        sa.Column("claim_quantum", sa.Float, nullable=True),
        sa.Column("claim_currency", sa.String(10), nullable=True),
        sa.Column("governing_law", sa.String(255), nullable=True),
        sa.Column("priority_speed", sa.Float, default=0.25),
        sa.Column("priority_cost", sa.Float, default=0.25),
        sa.Column("priority_neutrality", sa.Float, default=0.25),
        sa.Column("priority_enforceability", sa.Float, default=0.25),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "seat_allocation_results",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "request_id", sa.Integer, sa.ForeignKey("seat_allocation_requests.id"), nullable=False
        ),
        sa.Column("rank", sa.Integer, nullable=False),
        sa.Column("seat_id", sa.Integer, sa.ForeignKey("seats.id"), nullable=False),
        sa.Column("institution_id", sa.Integer, sa.ForeignKey("institutions.id"), nullable=False),
        sa.Column("score", sa.Float, nullable=False),
        sa.Column("rationale", sa.Text, nullable=False),
        sa.Column("pros", sa.JSON, nullable=False),
        sa.Column("cons", sa.JSON, nullable=False),
        sa.Column("citations", sa.JSON, nullable=False),
    )

    op.create_table(
        "clauses",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=True),
        sa.Column(
            "source_seat_allocation_result_id",
            sa.Integer,
            sa.ForeignKey("seat_allocation_results.id"),
            nullable=True,
        ),
        sa.Column("seat_id", sa.Integer, sa.ForeignKey("seats.id"), nullable=False),
        sa.Column("institution_id", sa.Integer, sa.ForeignKey("institutions.id"), nullable=False),
        sa.Column("num_arbitrators", sa.String(30), nullable=False),
        sa.Column("appointment_mechanism", sa.String(50), nullable=False),
        sa.Column("language", sa.String(60), nullable=False),
        sa.Column("governing_law_contract", sa.String(255), nullable=False),
        sa.Column("governing_law_arbitration", sa.String(255), nullable=False),
        sa.Column("party_details", sa.JSON, nullable=True),
        sa.Column("generated_text", sa.Text, nullable=False),
        sa.Column("pathology_check_notes", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "cost_estimates",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=True),
        sa.Column("institution_id", sa.Integer, sa.ForeignKey("institutions.id"), nullable=False),
        sa.Column("claim_amount", sa.Float, nullable=False),
        sa.Column("currency", sa.String(10), default="USD"),
        sa.Column("estimated_admin_fee", sa.Float, nullable=False),
        sa.Column("estimated_tribunal_fee_min", sa.Float, nullable=False),
        sa.Column("estimated_tribunal_fee_max", sa.Float, nullable=False),
        sa.Column("estimated_duration_months_min", sa.Integer, nullable=False),
        sa.Column("estimated_duration_months_max", sa.Integer, nullable=False),
        sa.Column("breakdown", sa.JSON, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("cost_estimates")
    op.drop_table("clauses")
    op.drop_table("seat_allocation_results")
    op.drop_table("seat_allocation_requests")
    op.drop_table("contract_uploads")
    op.drop_table("seat_institution_ratings")
    op.drop_table("fee_schedules")
    op.drop_table("annual_report_stats")
    op.drop_table("institution_rules")
    op.drop_table("institutions")
    op.drop_table("seats")
    op.drop_table("users")
