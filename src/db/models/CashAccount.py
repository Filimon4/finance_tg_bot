from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, VARCHAR, func
from ..index import Base
from sqlalchemy.orm import relationship


class CashAccount(Base):
    __tablename__ = "cash_account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    currency_id = Column(Integer, ForeignKey("currency.id"), nullable=False)
    account = relationship("Account", back_populates="cash_accounts")
    currency = relationship("Currency", back_populates="cash_accounts")
    outgoing_operations = relationship(
        "Operations",
        foreign_keys="[Operations.cash_account_id]",
        back_populates="account",
        cascade=True
    )
    incoming_operations = relationship(
        "Operations",
        foreign_keys="[Operations.to_cash_account_id]",
        back_populates="to_account",
        cascade=True
    )
