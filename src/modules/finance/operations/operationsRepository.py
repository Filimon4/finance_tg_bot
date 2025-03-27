from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from src.db.models.Operations import Operations


class OperationRepository:
    @staticmethod
    def create(
        db: Session,
        account_id: int,
        to_account_id: int,
        category_id: int,
        amount: float,
        operation_type: str,  # Переименовано для избежания конфликта с type()
        description: Optional[str] = None,
    ) -> Optional[Operations]:
        """Создание новой операции"""
        try:
            operation = Operations(
                account_id=account_id,
                to_account_id=to_account_id,
                category_id=category_id,
                amount=amount,
                type=operation_type,
                description=description,
            )
            db.add(operation)
            db.commit()
            db.refresh(operation)
            return operation
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @staticmethod
    def get(db: Session, operation_id: int) -> Optional[Operations]:
        """Получение операции по ID"""
        try:
            return (
                db.query(Operations)
                .filter(Operations.id == operation_id)
                .first()
            )
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update(
        db: Session, operation_id: int, **kwargs
    ) -> Optional[Operations]:
        """Обновление операции"""
        try:
            operation = (
                db.query(Operations)
                .filter(Operations.id == operation_id)
                .first()
            )
            if operation:
                for key, value in kwargs.items():
                    setattr(operation, key, value)
                db.commit()
                db.refresh(operation)
            return operation
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @staticmethod
    def delete(db: Session, operation_id: int) -> bool:
        """Удаление операции"""
        try:
            operation = (
                db.query(Operations)
                .filter(Operations.id == operation_id)
                .first()
            )
            if operation:
                db.delete(operation)
                db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.rollback()
            raise e
