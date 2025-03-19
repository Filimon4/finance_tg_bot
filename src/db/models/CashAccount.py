from sqlalchemy import TIMESTAMP, VARCHAR, Column, Enum, ForeignKey, Integer, func

from ..index import Base
from sqlalchemy.orm import relationship
from ...modules.finance.types import TransactionType

class CashAccount(Base):
    __tablename__ = "cash_account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False, unique=True)
    base_type = Column(Enum(TransactionType), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)

    account = relationship("Account", back_populates="cash_account")
