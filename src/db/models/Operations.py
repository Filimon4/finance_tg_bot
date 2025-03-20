from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    TIMESTAMP,
    func,
    Enum,
)

from modules.finance.types import OperationType

from ..index import Base


class Operations(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, autoincrement=True)

    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    to_account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)

    amount = Column(Numeric(15, 2), nullable=False)
    description = Column(Text, nullable=True)

    type = Column(Enum(OperationType), nullable=False)

    created_at = Column(TIMESTAMP, default=func.now())
