from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from src.db.models import Category


class CategoryRepository:
    @staticmethod
    def create(
        db: Session, name: str, base_type: str, account_id: int
    ) -> Optional[Category]:
        """Создание новой категории"""
        try:
            category = Category(
                name=name, base_type=base_type, account_id=account_id
            )
            db.add(category)
            db.commit()
            db.refresh(category)
            return category
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @staticmethod
    def get(db: Session, category_id: int) -> Optional[Category]:
        """Получение категории по ID"""
        try:
            return db.query(Category).filter(Category.id == category_id).first()
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Category]:
        """Получение категории по имени"""
        try:
            return db.query(Category).filter(Category.name == name).first()
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update(db: Session, category_id: int, **kwargs) -> Optional[Category]:
        """Обновление категории"""
        try:
            category = (
                db.query(Category).filter(Category.id == category_id).first()
            )
            if category:
                for key, value in kwargs.items():
                    setattr(category, key, value)
                db.commit()
                db.refresh(category)
            return category
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @staticmethod
    def delete(db: Session, category_id: int) -> bool:
        """Удаление категории"""
        try:
            category = (
                db.query(Category).filter(Category.id == category_id).first()
            )
            if category:
                db.delete(category)
                db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.rollback()
            raise e
