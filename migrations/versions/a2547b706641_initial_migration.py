"""Initial Migration

Revision ID: a2547b706641
Revises: None
Create Date: 2016-12-18 18:07:38.262173

"""

# revision identifiers, used by Alembic.
revision = "a2547b706641"
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "agencies",
        sa.Column("ein", sa.String(length=4), nullable=False),
        sa.Column("parent_ein", sa.String(length=3), nullable=True),
        sa.Column("categories", postgresql.ARRAY(sa.String(length=256)), nullable=True),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("next_request_number", sa.Integer(), nullable=True),
        sa.Column("default_email", sa.String(length=254), nullable=True),
        sa.Column("appeals_email", sa.String(length=254), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("ein"),
    )
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=True),
        sa.Column("permissions", sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "reasons",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "type", sa.Enum("closing", "denial", name="reason_type"), nullable=False
        ),
        sa.Column("agency_ein", sa.String(length=4), nullable=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["agency_ein"], ["agencies.ein"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "requests",
        sa.Column("id", sa.String(length=19), nullable=False),
        sa.Column("agency_ein", sa.String(length=4), nullable=True),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("title", sa.String(length=90), nullable=True),
        sa.Column("description", sa.String(length=5000), nullable=True),
        sa.Column("date_created", sa.DateTime(), nullable=True),
        sa.Column("date_submitted", sa.DateTime(), nullable=True),
        sa.Column("due_date", sa.DateTime(), nullable=True),
        sa.Column(
            "submission",
            sa.Enum(
                "Direct Input",
                "Fax",
                "Phone",
                "Email",
                "Mail",
                "In-Person",
                "311",
                name="submission",
            ),
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "Open", "In Progress", "Due Soon", "Overdue", "Closed", name="status"
            ),
            nullable=False,
        ),
        sa.Column("privacy", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column("agency_description", sa.String(length=5000), nullable=True),
        sa.Column("agency_description_release_date", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["agency_ein"], ["agencies.ein"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("guid", sa.String(length=64), nullable=False),
        sa.Column(
            "auth_user_type",
            sa.Enum(
                "Saml2In:NYC Employees",
                "LDAP:NYC Employees",
                "FacebookSSO",
                "MSLiveSSO",
                "YahooSSO",
                "LinkedInSSO",
                "GoogleSSO",
                "EDIRSSO",
                "AnonymousUser",
                name="auth_user_type",
            ),
            nullable=False,
        ),
        sa.Column("agency_ein", sa.String(length=4), nullable=True),
        sa.Column("is_super", sa.Boolean(), nullable=False),
        sa.Column("is_agency_admin", sa.Boolean(), nullable=False),
        sa.Column("is_agency_active", sa.Boolean(), nullable=False),
        sa.Column("first_name", sa.String(length=32), nullable=False),
        sa.Column("middle_initial", sa.String(length=1), nullable=True),
        sa.Column("last_name", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=True),
        sa.Column("email_validated", sa.Boolean(), nullable=False),
        sa.Column("terms_of_use_accepted", sa.Boolean(), nullable=True),
        sa.Column("title", sa.String(length=64), nullable=True),
        sa.Column("organization", sa.String(length=128), nullable=True),
        sa.Column("phone_number", sa.String(length=25), nullable=True),
        sa.Column("fax_number", sa.String(length=25), nullable=True),
        sa.Column(
            "mailing_address", postgresql.JSON(astext_type=sa.Text()), nullable=True
        ),
        sa.ForeignKeyConstraint(["agency_ein"], ["agencies.ein"]),
        sa.PrimaryKeyConstraint("guid", "auth_user_type"),
    )
    op.create_table(
        "responses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("request_id", sa.String(length=19), nullable=True),
        sa.Column(
            "privacy",
            sa.Enum("private", "release_private", "release_public", name="privacy"),
            nullable=True,
        ),
        sa.Column("date_modified", sa.DateTime(), nullable=True),
        sa.Column("release_date", sa.DateTime(), nullable=True),
        sa.Column("deleted", sa.Boolean(), nullable=False),
        sa.Column(
            "type",
            sa.Enum(
                "notes",
                "links",
                "files",
                "instructions",
                "determinations",
                "emails",
                name="type",
            ),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["request_id"], ["requests.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_requests",
        sa.Column("user_guid", sa.String(length=64), nullable=False),
        sa.Column(
            "auth_user_type",
            sa.Enum(
                "Saml2In:NYC Employees",
                "LDAP:NYC Employees",
                "FacebookSSO",
                "MSLiveSSO",
                "YahooSSO",
                "LinkedInSSO",
                "GoogleSSO",
                "EDIRSSO",
                "AnonymousUser",
                name="auth_user_type",
            ),
            nullable=False,
        ),
        sa.Column("request_id", sa.String(length=19), nullable=False),
        sa.Column(
            "request_user_type",
            sa.Enum("requester", "agency", name="request_user_type"),
            nullable=True,
        ),
        sa.Column("permissions", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(["request_id"], ["requests.id"]),
        sa.ForeignKeyConstraint(
            ["user_guid", "auth_user_type"], ["users.guid", "users.auth_user_type"]
        ),
        sa.PrimaryKeyConstraint("user_guid", "auth_user_type", "request_id"),
    )
    op.create_table(
        "determinations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "dtype",
            sa.Enum(
                "denial",
                "acknowledgment",
                "extension",
                "closing",
                "re-opening",
                name="determination_type",
            ),
            nullable=False,
        ),
        sa.Column("reason", sa.String(), nullable=True),
        sa.Column("date", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["id"], ["responses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "emails",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("to", sa.String(), nullable=True),
        sa.Column("cc", sa.String(), nullable=True),
        sa.Column("bcc", sa.String(), nullable=True),
        sa.Column("subject", sa.String(length=5000), nullable=True),
        sa.Column("body", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["id"], ["responses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("request_id", sa.String(length=19), nullable=True),
        sa.Column("user_guid", sa.String(length=64), nullable=True),
        sa.Column(
            "auth_user_type",
            sa.Enum(
                "Saml2In:NYC Employees",
                "LDAP:NYC Employees",
                "FacebookSSO",
                "MSLiveSSO",
                "YahooSSO",
                "LinkedInSSO",
                "GoogleSSO",
                "EDIRSSO",
                "AnonymousUser",
                name="auth_user_type",
            ),
            nullable=True,
        ),
        sa.Column("response_id", sa.Integer(), nullable=True),
        sa.Column("type", sa.String(length=64), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column(
            "previous_value", postgresql.JSON(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("new_value", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(["request_id"], ["requests.id"]),
        sa.ForeignKeyConstraint(["response_id"], ["responses.id"]),
        sa.ForeignKeyConstraint(
            ["user_guid", "auth_user_type"], ["users.guid", "users.auth_user_type"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "files",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("mime_type", sa.String(), nullable=True),
        sa.Column("size", sa.Integer(), nullable=True),
        sa.Column("hash", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["id"], ["responses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "instructions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["id"], ["responses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "links",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["id"], ["responses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(length=5000), nullable=True),
        sa.ForeignKeyConstraint(["id"], ["responses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "response_tokens",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(), nullable=False),
        sa.Column("response_id", sa.Integer(), nullable=False),
        sa.Column("expiration_date", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["response_id"], ["responses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("response_tokens")
    op.drop_table("notes")
    op.drop_table("links")
    op.drop_table("instructions")
    op.drop_table("files")
    op.drop_table("events")
    op.drop_table("emails")
    op.drop_table("determinations")
    op.drop_table("user_requests")
    op.drop_table("responses")
    op.drop_table("users")
    op.drop_table("requests")
    op.drop_table("reasons")
    op.drop_table("roles")
    op.drop_table("agencies")
    ### end Alembic commands ###
