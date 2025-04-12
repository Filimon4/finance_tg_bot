from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, func
from sqlalchemy.orm import relationship
from ..index import Base


class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(VARCHAR(255), nullable=False, unique=True)
    symbol_native = Column(VARCHAR(255), nullable=True, unique=True)
    code = Column(VARCHAR(255), nullable=False, unique=True)
    name = Column(VARCHAR(255), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, default=func.now())
    cash_accounts = relationship("CashAccount", back_populates="currency")
