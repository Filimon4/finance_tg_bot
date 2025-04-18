from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    TIMESTAMP,
    func,
    Enum,
)

from src.modules.finance.types import OperationType
from sqlalchemy.orm import relationship, validates
from ..index import Base

class Operations(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    category_id = Column(Integer, ForeignKey("category.id", ondelete="SET NULL"), nullable=True)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=True)
    cash_account_id = Column(Integer, ForeignKey("cash_account.id", ondelete="CASCADE"), nullable=False)
    to_cash_account_id = Column(Integer, ForeignKey("cash_account.id", ondelete="SET NULL"), nullable=True)
    exchange_rate = Column(Numeric(15,2), server_default=None, default=None, nullable=True)
    linked_operation_id = Column(Integer, ForeignKey("operations.id", ondelete="CASCADE"), nullable=True)

    # Relationships
    cash_account = relationship(
        "CashAccount",
        foreign_keys=[cash_account_id],
        back_populates="outgoing_operations",
    )
    to_account = relationship(
        "CashAccount",
        foreign_keys=[to_cash_account_id],
        back_populates="incoming_operations",
    )
    category = relationship("Category", back_populates="operations")
    account = relationship("Account", back_populates="operations")  # This one stays as 'account'

    amount = Column(Numeric(15, 2), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(Enum(OperationType), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())

    __table_args__ = (
        CheckConstraint(
            '(to_cash_account_id IS NULL AND category_id IS NOT NULL) OR '
            '(to_cash_account_id IS NOT NULL AND category_id IS NULL) OR '
            '(to_cash_account_id IS NULL AND category_id IS NULL)',
            name='check_account_category_null_logic'
        ),
        CheckConstraint(
            'to_cash_account_id IS NULL OR type = \'transfer\'',
            name='check_transfer_type_constraint'
        ),
    )