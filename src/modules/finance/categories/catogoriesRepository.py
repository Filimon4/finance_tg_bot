from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.Category import Category


class CategoryRepository:
    @staticmethod
    def create(db: Session, name: str, base_type: str, account_id: int):
        """
        Создание новой категории.
        """
        try:
            new_category = Category(
                name=name, base_type=base_type, account_id=account_id
            )
            db.add(new_category)
            db.commit()
            db.refresh(new_category)
            return new_category
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Ошибка при создании категории: {e}")
            return None

    @staticmethod
    def get(db: Session, category_id: int):
        """
        Получение категории по ID.
        """
        try:
            return db.query(Category).filter(Category.id == category_id).first()
        except SQLAlchemyError as e:
            print(f"Ошибка при получении категории: {e}")
            return None

    @staticmethod
    def update(db: Session, category_id: int, **kwargs):
        """
        Обновление категории по ID.
        """
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
            print(f"Ошибка при обновлении категории: {e}")
            return None

    @staticmethod
    def delete(db: Session, category_id: int):
        """
        Удаление категории по ID.
        """
        try:
            category = (
                db.query(Category).filter(Category.id == category_id).first()
            )
            if category:
                db.delete(category)
                db.commit()
            return category
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Ошибка при удалении категории: {e}")
            return None
