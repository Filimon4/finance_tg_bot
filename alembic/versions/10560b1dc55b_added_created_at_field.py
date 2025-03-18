"""Added created_at field

Revision ID: 10560b1dc55b
Revises: ba981ab4e40d
Create Date: 2025-03-18 23:52:22.005088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10560b1dc55b'
down_revision: Union[str, None] = 'ba981ab4e40d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('created_at', sa.TIMESTAMP(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'created_at')
    # ### end Alembic commands ###
