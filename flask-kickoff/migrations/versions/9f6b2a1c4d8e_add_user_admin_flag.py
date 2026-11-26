"""add user admin flag

Revision ID: 9f6b2a1c4d8e
Revises: 4d85e27fa27d
Create Date: 2026-11-26 08:45:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9f6b2a1c4d8e"
down_revision: str | Sequence[str] | None = "4d85e27fa27d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "User",
        sa.Column("is_admin", sa.Boolean(), server_default=sa.false(), nullable=False),
    )


def downgrade() -> None:
    with op.batch_alter_table("User") as batch_op:
        batch_op.drop_column("is_admin")
