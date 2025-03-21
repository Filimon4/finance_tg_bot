from sqlalchemy import (
    TIMESTAMP,
    VARCHAR,
    Column,
    Enum,
    ForeignKey,
    Integer,
    func,
)

from sqlalchemy.orm import relationship

from systems.finance.types import TransactionType
from ..index import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False, unique=True)
    base_type = Column(Enum(TransactionType), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())

    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    account = relationship("Account", back_populates="category")

    category_operations = relationship("Operations", back_populates="category")
