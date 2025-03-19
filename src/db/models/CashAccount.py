from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, VARCHAR, func
from ..index import Base


class CashAccount(Base):
    __tablename__ = "cash_account"

    id = Column(Integer, primary_key=True, autoincrement=True)

    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    currency_id = Column(Integer, ForeignKey("currency.id"), nullable=False)

    name = Column(VARCHAR(255), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
