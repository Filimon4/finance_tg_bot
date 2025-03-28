from datetime import datetime
from sqlalchemy import and_, extract, func, select, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.db.models.Operations import Operations
from src.modules.finance.types import OperationType 


class OperationsRepository:
    @staticmethod
    def create(
        db: Session,
        account_id: int,
        category_id: int,
        amount: float,
        type: str,
        to_account_id: int,
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
    async def get_paginate_operations(db: Session, limit: int = 100):
        query = select(Operations).order_by(Operations.created_at.desc()).limit(limit)
        return db.execute(query).scalars().all()

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
        
    @staticmethod
    async def getOperationsStat(db: Session, cash_account_id: int):
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        
        income_query = select(func.sum(Operations.amount)).where(
            Operations.type == OperationType.INCOME,
            Operations.created_at >= start_of_month
        )
        
        expense_query = select(func.sum(Operations.amount)).where(
            Operations.type == OperationType.EXPENSIVE,
            Operations.created_at >= start_of_month
        )

        income = db.execute(income_query).scalar() or 0
        expense = db.execute(expense_query).scalar() or 0

        print('cash invome expense')
        print(cash_account_id, income, expense)

        return {
            "total_balance": float(income - expense), #float(total_income - total_expense),
            "monthly_income": float(income), #float(monthly_income),
            "monthly_expense": float(expense), #float(monthly_expense)
        }