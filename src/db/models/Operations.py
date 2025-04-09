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
    cash_account_id = Column(Integer, ForeignKey("cash_account.id"), nullable=False)
    to_cash_account_id = Column(Integer, ForeignKey("cash_account.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=True)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=True)

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
            '(to_cash_account_id IS NOT NULL AND category_id IS NULL)',
            name='check_account_category_null_logic'
        ),
        CheckConstraint(
            'to_cash_account_id IS NULL OR type = "transfer"',
            name='check_transfer_type_constraint'
        ),
    )

    @validates('to_cash_account_id', 'category_id')
    def validate_account_and_category(self, key, value):
        if key == 'to_cash_account_id':
            if value is None and self.category_id is None:
                raise ValueError("Если to_cash_account_id не указан, category_id обязателен")
        elif key == 'category_id':
            if value is None and self.to_cash_account_id is None:
                raise ValueError("Если category_id не указан, to_cash_account_id обязателен")
        return value
