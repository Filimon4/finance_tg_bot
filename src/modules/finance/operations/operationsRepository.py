from asyncio.log import logger
import datetime
from fastapi import HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import and_, extract, func, select, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.db.models.CashAccount import CashAccount
from src.db.models.Category import Category
from src.db.models.Account import Account
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.db.models.Operations import Operations
from src.modules.finance.types import OperationType 

class OperationCreateDTO(BaseModel):
    account_id: int
    name: str | None
    cash_account_id: int
    to_cash_account_id: int | None
    category_id: int | None
    amount: int
    description: str | None
    type: OperationType
    date: datetime.datetime

class OperationUpdateDTO(BaseModel):
    id: int
    name: str | None
    cash_account_id: int | None
    to_cash_account_id: int | None
    category_id: int | None
    amount: int | None
    description: str | None
    type: OperationType | None

class OperationsRepository:
    
    @staticmethod
    def getPaginatedOperations(session: Session, user_id: int, start_time: datetime, end_time: datetime, page: int = 1, limit: int = 40, ):
        try:
            query = (
                session
                .query(Operations)
                .filter(Operations.account_id == user_id)
                .filter(Operations.created_at >= start_time)
                .filter(Operations.created_at <= end_time)
                .order_by(Operations.created_at)
            )

            offset = (max(page, 1) - 1) * limit
            operations = query.offset(offset).limit(limit).all()
            return {
                "operations": operations,
                "page": page,
                "limit": limit,
            }
        except Exception as e:
            raise Exception(e)
        except SQLAlchemyError as e:
            raise Exception(e)

    @staticmethod
    def create( session: Session, data: OperationCreateDTO):
        try:
            if data.to_cash_account_id is not None and data.category_id is not None:
                raise ValueError("Недопустимые данные: to_cash_account_id и category_id не могут быть заполнены одновременно")
            
            if data.to_cash_account_id is not None and data.type != OperationType.TRANSFER:
                raise ValueError("Недопустимые данные: to_cash_account_id может быть указан только для операций типа TRANSFER")

            operationData = {
                'account_id': data.account_id,
                'name': data.name if data.name is not None else '',
                'cash_account_id': data.cash_account_id,
                'category_id': data.category_id,
                'to_cash_account_id': data.to_cash_account_id,
                'amount': data.amount,
                'description': data.description if data.description else '',
                'type': data.type,
                'created_at': data.date if data.date is not None else datetime.now()
            }
            operation = Operations(**operationData)
            session.add(operation)
            session.commit()
            return operation
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при создании операции: {str(e)}")
            return None

    @staticmethod
    def getOperationsByCashAccount(session: Session, cash_account_id: int, page: int = 1, limit: int = 100):
        try:
            cashAccount = CashAccountRepository.get(session, cash_account_id)
            if not cashAccount:
                raise HTTPException(status_code=404, detail="Account not found")
            query = session.query(Operations).filter(
                Operations.cash_account_id == cashAccount.id
            )

            offset = (page - 1) * limit
            query = session.query(Operations).filter(
                Operations.cash_account_id == cash_account_id,
            ).order_by(
                Operations.created_at.desc()
            ).offset(offset).limit(limit)
            totalRows = query.count()

            return {
                'operations': query.all(),
                'total': totalRows
            }
        except Exception as e:
            raise Exception(e)
        
    @staticmethod
    def getOperations(session: Session, tg_id: int, page: int = 1, limit: int = 100):
        try:
            page = max(1, page)
            offset = (page - 1) * limit
            
            operations = (
                session.query(Operations)
                .join(Account, Operations.account_id == Account.id)
                .filter(Account.id == tg_id)
                .order_by(Operations.created_at.desc())
                .offset(offset)
                .limit(limit)
                .all()
            )
            return operations
            
        except Exception as e:
            raise Exception(f"Failed to get operations: {str(e)}")
        
    @staticmethod
    def getOperationById(session: Session, id: int):
        try:
            operation = (
                session.query(Operations)
                .filter(Operations.id == id)
                .one()
            )
            return operation
        except Exception as e:
            raise Exception(f"Failed to get operations: {str(e)}")

    @staticmethod
    def update(session: Session, data: OperationUpdateDTO):
        try:
            operation = session.query(Operations).filter(Operations.id == data.id).first()
            if not operation: raise Exception("There is not operation")

            if data.to_cash_account_id is not None and data.category_id is not None:
                raise ValueError("Недопустимые данные: to_cash_account_id и category_id не могут быть заполнены одновременно")
            
            if data.to_cash_account_id is not None and data.type != OperationType.TRANSFER:
                raise ValueError("Недопустимые данные: to_cash_account_id может быть указан только для операций типа TRANSFER")

            if hasattr(data, 'amount'):
                operation.amount = data.amount if data.amount is not None else None
            if hasattr(data, 'cash_account_id'):
                operation.cash_account_id = data.cash_account_id if data.cash_account_id is not None else None
            if hasattr(data, 'to_cash_account_id'):
                operation.to_cash_account_id = data.to_cash_account_id if data.to_cash_account_id is not None else None
            if hasattr(data, 'category_id'):
                operation.category_id = data.category_id if data.category_id is not None else None
            if hasattr(data, 'description'):
                operation.description = data.description if data.description is not None else None
            if hasattr(data, 'type'):
                operation.type = data.type if data.type is not None else None
            if hasattr(data, 'name'):
                operation.name = data.name if data.name is not None else None

            session.commit()
            return operation
        except Exception as e:
            raise Exception(e)
    
    @staticmethod
    def delete(session: Session, oper_id: int):
        try:
            operation = session.query(Operations).filter(Operations.id == oper_id).first()
            if not operation: raise Exception("There is not operation")
            session.delete(operation)
            session.commit()
            return True
        except Exception as e:
            raise Exception(e)