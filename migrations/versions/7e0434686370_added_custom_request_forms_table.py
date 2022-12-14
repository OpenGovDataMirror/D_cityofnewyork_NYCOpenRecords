"""Added custom_request_forms table

Revision ID: 7e0434686370
Revises: 445e50628f6b
Create Date: 2018-04-30 20:07:13.242319

"""

# revision identifiers, used by Alembic.
revision = "7e0434686370"
down_revision = "445e50628f6b"

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "custom_request_forms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("agency_ein", sa.String(length=4), nullable=False),
        sa.Column("form_name", sa.String(), nullable=False),
        sa.Column("form_description", sa.String(), nullable=False),
        sa.Column(
            "field_definitions", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("repeatable", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["agency_ein"], ["agencies.ein"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "requests",
        sa.Column(
            "custom_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("requests", "custom_metadata")
    op.drop_table("custom_request_forms")
    ### end Alembic commands ###
