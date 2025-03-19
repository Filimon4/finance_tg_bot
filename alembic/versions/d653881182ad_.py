"""empty message

Revision ID: d653881182ad
Revises: 6b14058784b5
Create Date: 2025-03-20 01:12:42.609651

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d653881182ad"
down_revision: Union[str, None] = "6b14058784b5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "account",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "category",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(length=255), nullable=False),
        sa.Column(
            "base_type",
            sa.Enum("INCOME", "EXPENSIVE", name="transactiontype"),
            nullable=False,
        ),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["account.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("category")
    op.drop_table("account")
    # ### end Alembic commands ###
