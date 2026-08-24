"""add user email

Revision ID: 87fa4b969efa
Revises: 3ec3c44de271
Create Date: 2026-08-24 21:06:49.158741

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87fa4b969efa'
down_revision: Union[str, Sequence[str], None] = '3ec3c44de271'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("email", sa.String(length=255), nullable=True),
    )

    op.execute(
        """
        UPDATE users
        SET email = user_id || '@ledgercore.local'
        WHERE email IS NULL
        """
    )

    op.alter_column(
        "users",
        "email",
        existing_type=sa.String(length=255),
        nullable=False,
    )

    op.create_unique_constraint(
        "uq_users_email",
        "users",
        ["email"],
    )
        
def downgrade() -> None:
    op.drop_constraint(
        "uq_users_email",
        "users",
        type_="unique",
    )

    op.drop_column("users", "email")
