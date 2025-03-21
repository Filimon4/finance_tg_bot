from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.Operations import Operations


class OperationsRepository:
    @staticmethod
    def create(
        db: Session,
        account_id: int,
        to_account_id: int,
        category_id: int,
        amount: float,
        type: str,
        description: str = None,
    ):
        """
        Создание новой операции.
        """
        try:
            new_operation = Operations(
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
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Ошибка при создании операции: {e}")
            return None

    @staticmethod
    def get(db: Session, operation_id: int):
        """
        Получение операции по ID.
        """
        try:
            return (
                db.query(Operations)
                .filter(Operations.id == operation_id)
                .first()
            )
        except SQLAlchemyError as e:
            print(f"Ошибка при получении операции: {e}")
            return None

    @staticmethod
    def update(db: Session, operation_id: int, **kwargs):
        """
        Обновление операции по ID.
        """
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
            print(f"Ошибка при обновлении операции: {e}")
            return None

    @staticmethod
    def delete(db: Session, operation_id: int):
        """
        Удаление операции по ID.
        """
        try:
            operation = (
                db.query(Operations)
                .filter(Operations.id == operation_id)
                .first()
            )
            if operation:
                db.delete(operation)
                db.commit()
            return operation
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Ошибка при удалении операции: {e}")
            return None
