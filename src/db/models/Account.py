from sqlalchemy import Column, Integer, TIMESTAMP, func
from sqlalchemy.orm import relationship
from ..index import Base


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, default=func.now())
    categories = relationship("Category", back_populates="account")
    cash_accounts = relationship("CashAccount", back_populates="account")
    reminders = relationship("Reminder", back_populates="account")
