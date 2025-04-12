"""Your changes

Revision ID: ad3524ae0676
Revises: 3d44f51bf882
Create Date: 2025-04-11 16:50:44.465310

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad3524ae0676'
down_revision: Union[str, None] = '3d44f51bf882'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('currency', sa.Column('symbol', sa.VARCHAR(length=1), nullable=True))
    op.create_unique_constraint(None, 'currency', ['symbol'])
    op.create_unique_constraint(None, 'currency', ['code'])
    op.create_unique_constraint(None, 'currency', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'currency', type_='unique')
    op.drop_constraint(None, 'currency', type_='unique')
    op.drop_constraint(None, 'currency', type_='unique')
    op.drop_column('currency', 'symbol')
    # ### end Alembic commands ###
