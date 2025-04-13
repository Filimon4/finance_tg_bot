"""Contstraints

Revision ID: 3d44f51bf882
Revises: 
Create Date: 2025-04-10 08:37:47.719108

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '30cd4647d315'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_check_constraint(
        'check_account_category_null_logic',
        'operations',
        '(to_cash_account_id IS NULL AND category_id IS NOT NULL) OR '
        '(to_cash_account_id IS NOT NULL AND category_id IS NULL) OR '
        '(to_cash_account_id IS NULL AND category_id IS NULL)'
    )

    op.create_check_constraint(
        'check_transfer_type_constraint',
        'operations',
        "to_cash_account_id IS NULL OR type = 'TRANSFER'"
    )

    op.create_check_constraint(
        'ck_main_cash_account',
        'cash_account',
        'main IS FALSE OR (main IS TRUE AND account_id IS NOT NULL)'
    )

    op.create_check_constraint(
        'ck_hour_reminder',
        'reminder',
        'hour >= 0 and hour <= 24'
    )

def downgrade():
    op.drop_constraint('check_account_category_null_logic', 'operations', type_='check')
    op.drop_constraint('check_transfer_type_constraint', 'operations', type_='check')
    
    op.drop_constraint('ck_main_cash_account', 'cash_account', type_='check')
    
    op.drop_constraint('ck_hour_reminder', 'reminder', type_='check')