from fastapi import HTTPException
from sqlalchemy import Result, Select, func, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.db.models import Category, Operations
from src.modules.finance.types import OperationType
from src.db.models.CashAccount import CashAccount
from src.db.models.Account import Account

from pydantic import BaseModel

class CashAccountCreate(BaseModel):
    name: str
    account_id: int
    currency_id: int
    
class CashAccountRepository:

    @staticmethod
    def getOverview(session: Session, tg_id: int):
        try:
            expenses = session.query(
                Operations.category_id,
                Category.name.label("category_name"),
                func.sum(Operations.amount).label("total_amount")
            ).join(
                Category, Operations.category_id == Category.id
            ).join(
                CashAccount, Operations.cash_account_id == CashAccount.id
            ).filter(
                Operations.type == OperationType.EXPENSIVE,
                CashAccount.account_id == tg_id
            ).group_by(
                Operations.category_id,
                Category.name
            ).all()

            result = [
                {
                    "category_id": category_id,
                    "category_name": category_name,
                    "total_spent": float(total_amount)
                }
                for category_id, category_name, total_amount in expenses
            ]

            return result
        except SQLAlchemyError as e:
            print(f"Ошибка при создании аккаунта: {e}")
            return None

    @staticmethod
    def get(session: Session, id: int):
        try:
            query = select(CashAccount).where(CashAccount.id == id)
            result = session.execute(query)
            return result.scalar()
        except SQLAlchemyError as e:
            print(f"Ошибка при получении аккаунта: {e}")
            return None

    @staticmethod
    def getAll(session: Session, skip: int, limit: int):
        try:
            query: Select = select(CashAccount).offset(skip).limit(limit)
            accounts_result: Result = session.execute(query)
            return accounts_result.scalars().all()
        except SQLAlchemyError as e:
            print(f"Ошибка при получении аккаунта: {e}")
            return None
        
    @staticmethod
    def getAll(session: Session, skip: int, limit: int):
        try:
            query: Select = select(CashAccount).offset(skip).limit(limit)
            accounts_result: Result = session.execute(query)
            return accounts_result.scalars().all()
        except SQLAlchemyError as e:
            print(f"Ошибка при получении аккаунта: {e}")
            return None
        
    @staticmethod
    def getCashAccountOverview(session: Session, id: int):
        try:
            account = session.query(CashAccount).filter(CashAccount.id == id).first()
            if not account:
                raise 'Нету такого счёта'
            
            total_income = (
                session.query(func.sum(Operations.amount))
                .filter(Operations.cash_account_id == id, Operations.type == OperationType.INCOME)
                .scalar() or 0
            )
            total_expense = (
                session.query(func.sum(Operations.amount))
                .filter(Operations.cash_account_id == id, Operations.type == OperationType.EXPENSIVE)
                .scalar() or 0
            )
            return {
                account: account,
                total_income: total_income,
                total_expense: total_expense
            }
        except SQLAlchemyError as e:
            print(f"Ошибка при получении аккаунта: {e}")
            return None
        
    

