from enum import Enum
from sqlalchemy import VARCHAR, Column, Integer
from ..index import Base

class CashAccount:
    __tablename__ = "cash_account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False, unique=True)
    base_type = Column(Enum, )
