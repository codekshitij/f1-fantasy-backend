"""Drop hashed_password from users

Revision ID: 36b27f43fa63
Revises: c958e2b21638
Create Date: 2025-03-29 23:16:23.690569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36b27f43fa63'
down_revision: Union[str, None] = 'c958e2b21638'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'hashed_password')

def downgrade() -> None:
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=True))
