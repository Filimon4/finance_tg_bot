from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.modules.finance.types import OperationType, TransactionType
from src.db.models.Operations import Operations
from src.db.models import Category

from pydantic import BaseModel

class CategoryCreateDTO(BaseModel):
    name: str
    base_type: TransactionType
    account_id: int

class CategoryUpdateDTO(BaseModel):
    id: int
    name: str
    base_type: TransactionType

class CategoryDeleteDTO(BaseModel):
    id: int

class CategoryRepository:
    @staticmethod
    def create(session: Session, data: CategoryCreateDTO):
        """
        Создание новой категории.
        """
        try:
            new_category = Category(
                name=data.name, base_type=data.base_type or None, account_id=data.account_id
            )
            session.add(new_category)
            session.commit()
            return new_category
        except Exception as e:
            print(e)
            return None 
        except SQLAlchemyError as e:
            print(e)
            return None

    @staticmethod
    def get(session: Session, category_id: int):
        try:
            return session.query(Category).filter(Category.id == category_id).first()
        except SQLAlchemyError as e:
            print(f"Ошибка при получении категории: {e}")
            return None
        
    @staticmethod
    def getByName(session: Session, name: str):
        try:
            return session.query(Category).filter(Category.name == name).first()
        except SQLAlchemyError as e:
            return None
        
    @staticmethod
    def getAll(session: Session, tg_id: int):
        try:
            return session.query(Category).filter(Category.account_id == tg_id).all()
        except SQLAlchemyError as e:
            print(f"Ошибка при получении категории: {e}")
            return None

    @staticmethod
    def update(session: Session, data: CategoryUpdateDTO):
        try:
            category = session.query(Category).filter(
                Category.id == data.id,
            ).first()

            if not category:
                raise HTTPException(
                    status_code=404,
                    detail="Category not found or access denied"
                )

            if hasattr(data, 'name'):
                category.name = data.name if data.name is not None else None
            if hasattr(data, 'base_type'):
                category.base_type = data.base_type if data.base_type is not None else None
             
            session.commit()

            return category
        except HTTPException:
            raise 
        except SQLAlchemyError as e:
            print(f"Database error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Database error occurred"
            )
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )

    @staticmethod
    def delete(session: Session, category_id: int):
        try:
            category = session.query(Category).filter(Category.id == category_id).first()
            if not category: raise Exception('There is not category')
            session.delete(category)
            session.commit()
            return True
        except Exception as e:
            print(e)
            return False
        except SQLAlchemyError as e:
            print(e)
            return False
        
    @staticmethod
    def getCategoryOverview(session: Session, tg_id: int, category_id: int):
        try:
            category = CategoryRepository.get(session, category_id)
            if not category:
                raise Exception("Категория не найдена")
            
            total_income = session.query(
                func.coalesce(func.sum(Operations.amount), 0)
            ).filter(
                Operations.category_id == category.id, Operations.type == OperationType.INCOME
            ).scalar() or 0

            total_expenses = session.query(
                func.coalesce(func.sum(Operations.amount), 0)
            ).filter(
                Operations.category_id == category.id, Operations.type == OperationType.EXPENSIVE
            ).scalar() or 0

            return {
                'total_income': float(total_income),
                'total_expenses': float(total_expenses),
                'balance': float(float(total_income) - float(total_expenses))
            }
        except SQLAlchemyError as e:
            print(e)
            return None

