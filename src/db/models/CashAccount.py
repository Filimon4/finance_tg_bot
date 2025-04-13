from sqlalchemy import TIMESTAMP, CheckConstraint, Column, ForeignKey, Index, Integer, VARCHAR, UniqueConstraint, func, BOOLEAN
from ..index import Base
from sqlalchemy.orm import relationship


class CashAccount(Base):
    __tablename__ = "cash_account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    main = Column(BOOLEAN, server_default="false", default=False)
    created_at = Column(TIMESTAMP, default=func.now())
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    currency_id = Column(Integer, ForeignKey("currency.id"), nullable=False)
    account = relationship("Account", back_populates="cash_accounts")
    currency = relationship("Currency", back_populates="cash_accounts")
    outgoing_operations = relationship(
        "Operations",
        foreign_keys="[Operations.cash_account_id]",
        back_populates="cash_account",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    
    incoming_operations = relationship(
        "Operations",
        foreign_keys="[Operations.to_cash_account_id]",
        back_populates="to_account",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    __table_args__ = (
        UniqueConstraint("name", "account_id", name="uq_cash_account_name_per_account"),
        CheckConstraint("main IS FALSE OR (main IS TRUE AND account_id IS NOT NULL)", 
                      name="ck_main_cash_account"),
        Index("ix_unique_main_account", account_id, unique=True, 
             postgresql_where=(main == True)),
    )
