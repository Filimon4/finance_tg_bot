from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import and_, extract, func, select, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.db.models.Operations import Operations
from src.modules.finance.types import OperationType 

class OperationCreateDTO(BaseModel):
    cash_account_id: int
    to_cash_account_id: int
    category_id: int
    amount: int
    description: str
    type: OperationType

class OperationsRepository:
    @staticmethod
    def create(
        session: Session,

    ):
        try:
            pass
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Ошибка при создании операции: {e}")
            return None

    @staticmethod
    async def getAll(session: Session, cash_account_id: int):
        pass