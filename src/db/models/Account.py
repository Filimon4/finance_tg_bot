from sqlalchemy import Column, Integer, TIMESTAMP, func
from sqlalchemy.orm import relationship, Session
from ..index import Base


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, default=func.now())
    cash_accounts = relationship("Category", back_populates="account")
    category_accounts = relationship("CashAccount", back_populates="account")
    reminder_accounts = relationship("Reminder", back_populates="account")

    # CRUD операции

    @classmethod
    def create(cls, db: Session):
        """
        Создание нового аккаунта.
        """
        new_account = cls()
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        return new_account

    @classmethod
    def get(cls, db: Session, account_id: int):
        """
        Получение аккаунта по ID.
        """
        return db.query(cls).filter(cls.id == account_id).first()

    @classmethod
    def update(cls, db: Session, account_id: int, **kwargs):
        """
        Обновление аккаунта по ID.
        """
        account = db.query(cls).filter(cls.id == account_id).first()
        if account:
            for key, value in kwargs.items():
                setattr(account, key, value)
            db.commit()
            db.refresh(account)
        return account

    @classmethod
    def delete(cls, db: Session, account_id: int):
        """
        Удаление аккаунта по ID.
        """
        account = db.query(cls).filter(cls.id == account_id).first()
        if account:
            db.delete(account)
            db.commit()
        return account
