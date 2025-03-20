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
from sqlalchemy.orm import Session
from src.modules.finance.types import OperationType
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

    # CRUD операции

    @classmethod
    def create(
        cls,
        db: Session,
        account_id: int,
        to_account_id: int,
        category_id: int,
        amount: float,
        type: OperationType,
        description: str = None,
    ):
        """
        Создание новой операции.
        """
        new_operation = cls(
            account_id=account_id,
            to_account_id=to_account_id,
            category_id=category_id,
            amount=amount,
            type=type,
            description=description,
        )
        db.add(new_operation)
        db.commit()
        db.refresh(new_operation)
        return new_operation

    @classmethod
    def get(cls, db: Session, operation_id: int):
        """
        Получение операции по ID.
        """
        return db.query(cls).filter(cls.id == operation_id).first()

    @classmethod
    def update(cls, db: Session, operation_id: int, **kwargs):
        """
        Обновление операции по ID.
        """
        operation = db.query(cls).filter(cls.id == operation_id).first()
        if operation:
            for key, value in kwargs.items():
                setattr(operation, key, value)
            db.commit()
            db.refresh(operation)
        return operation

    @classmethod
    def delete(cls, db: Session, operation_id: int):
        """
        Удаление операции по ID.
        """
        operation = db.query(cls).filter(cls.id == operation_id).first()
        if operation:
            db.delete(operation)
            db.commit()
        return operation
