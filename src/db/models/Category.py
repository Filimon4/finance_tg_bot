from sqlalchemy import (
    TIMESTAMP,
    VARCHAR,
    Column,
    Enum,
    ForeignKey,
    Integer,
    UniqueConstraint,
    func,
)

from sqlalchemy.orm import relationship

from src.modules.finance.types import TransactionType

from ..index import Base



class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    base_type = Column(Enum(TransactionType), nullable=True)
    created_at = Column(TIMESTAMP, default=func.now())
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)

    account = relationship("Account", back_populates="categories")

    operations = relationship("Operations", back_populates="category")

    __table_args__ = (
        UniqueConstraint("name", "account_id", name="uq_category_name_per_account"),
    )
