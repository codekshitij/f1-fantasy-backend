"""Fix missing password field

Revision ID: 4ac9026ffc4c
Revises: 11333bf83d7d
Create Date: 2025-02-21 11:48:53.513681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String


# Revision identifiers, used by Alembic.
revision: str = "4ac9026ffc4c"
down_revision: Union[str, None] = "11333bf83d7d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

users_table = table("users", column("password", String))


def upgrade() -> None:
    # ✅ Step 1: First, add the password column as NULLABLE
    op.add_column("users", sa.Column("password", sa.String(), nullable=True))

    # ✅ Step 2: Update all existing users with a default password
    op.execute(users_table.update().values(password="temp_password"))

    # ✅ Step 3: Alter the column to make it NOT NULL
    op.alter_column("users", "password", nullable=False)


def downgrade() -> None:
    # Drop the password column in case of rollback
    op.drop_column("users", "password")
