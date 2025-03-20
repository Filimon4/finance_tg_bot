from sqlalchemy import (
    TIMESTAMP,
    VARCHAR,
    Column,
    Enum,
    ForeignKey,
    Integer,
    func,
)
from sqlalchemy.orm import relationship, Session
from src.modules.finance.types import TransactionType
from ..index import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False, unique=True)
    base_type = Column(Enum(TransactionType), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())

    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    account = relationship("Account", back_populates="category")

    category_operations = relationship("Operations", back_populates="category")

    # CRUD операции

    @classmethod
    def create(
        cls, db: Session, name: str, base_type: TransactionType, account_id: int
    ):
        """
        Создание новой категории.
        """
        new_category = cls(
            name=name, base_type=base_type, account_id=account_id
        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category

    @classmethod
    def get(cls, db: Session, category_id: int):
        """
        Получение категории по ID.
        """
        return db.query(cls).filter(cls.id == category_id).first()

    @classmethod
    def update(cls, db: Session, category_id: int, **kwargs):
        """
        Обновление категории по ID.
        """
        category = db.query(cls).filter(cls.id == category_id).first()
        if category:
            for key, value in kwargs.items():
                setattr(category, key, value)
            db.commit()
            db.refresh(category)
        return category

    @classmethod
    def delete(cls, db: Session, category_id: int):
        """
        Удаление категории по ID.
        """
        category = db.query(cls).filter(cls.id == category_id).first()
        if category:
            db.delete(category)
            db.commit()
        return category
