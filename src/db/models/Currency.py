from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, func
from sqlalchemy.orm import relationship
from ..index import Base


class Currency(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(VARCHAR(3), nullable=False)
    name = Column(VARCHAR(255), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    cash_accounts = relationship("CashAccount", back_populates="currency")
