from sqlalchemy import Column, Integer, TIMESTAMP, func
from ..index import Base
from sqlalchemy.orm import relationship


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, default=func.now())
    cash_accounts = relationship("Category", back_populates="account")
    category_accounts = relationship("CashAccount", back_populates="account")
    reminder_accounts = relationship("Reminder", back_populates="account")
