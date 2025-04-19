"""Add password column to users table

Revision ID: f204b86a174a
Revises: 9960180983e9
Create Date: 2025-04-18 19:46:21.634161
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f204b86a174a'
down_revision: Union[str, None] = '9960180983e9'  # Ось тут вказуємо попередню ревізію
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('password', sa.String(), nullable=False))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'password')
