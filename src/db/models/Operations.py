from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    TIMESTAMP,
    func,
    Enum,
)

from src.modules.finance.types import OperationType
from sqlalchemy.orm import relationship
from ..index import Base


class Operations(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cash_account_id = Column(Integer, ForeignKey("cash_account.id"), nullable=False)
    to_cash_account_id = Column(Integer, ForeignKey("cash_account.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
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
