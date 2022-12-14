"""agency_description to agency_request_summary

Revision ID: cf62ec87d973
Revises: 971f341c0204
Create Date: 2017-05-31 16:29:17.341283

"""

# revision identifiers, used by Alembic.
revision = "cf62ec87d973"
down_revision = "58a5abdd94ac"

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "requests",
        sa.Column("agency_request_summary", sa.String(length=5000), nullable=True),
    )
    op.add_column(
        "requests",
        sa.Column("agency_request_summary_release_date", sa.DateTime(), nullable=True),
    )
    op.drop_column("requests", "agency_description_release_date")
    op.drop_column("requests", "agency_description")
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "requests",
        sa.Column(
            "agency_description",
            sa.VARCHAR(length=5000),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "requests",
        sa.Column(
            "agency_description_release_date",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column("requests", "agency_request_summary_release_date")
    op.drop_column("requests", "agency_request_summary")
    ### end Alembic commands ###
