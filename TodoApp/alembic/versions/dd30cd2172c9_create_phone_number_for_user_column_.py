"""Create phone number for user column table

Revision ID: dd30cd2172c9
Revises: 
Create Date: 2025-02-25 16:45:17.573165

"""
from typing import Sequence, Union

from alembic import op #op in Alembic stands for operations, and it provides a set of high-level commands to modify the database schema within migration scripts. Instead of writing raw SQL, you use op to perform schema changes in a database-agnostic way.
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd30cd2172c9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
    
