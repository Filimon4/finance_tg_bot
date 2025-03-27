from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.db.models.CashAccount import CashAccount
from src.db.models.Account import Account


class CashAccountRepository:
    @staticmethod
    def create(db: Session):
        """
        Создание нового аккаунта.
        """
        try:
            new_account = CashAccount()
            db.add(new_account)
            db.commit()
            db.refresh(new_account)
            return new_account
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Ошибка при создании аккаунта: {e}")
            return None

    @staticmethod
    async def get(db: Session, user_id: int):
        """
        Получение аккаунта по ID.
        """
        try:
            query = select(CashAccount).where(CashAccount.account_id == user_id)
            result = db.execute(query)
            return result.scalar()
        except SQLAlchemyError as e:
            print(f"Ошибка при получении аккаунта: {e}")
            return None

    @staticmethod
    def getAllAccounts(db: Session):
        """
        Получение аккаунта по ID.
        """
        try:
            return db.query(CashAccount).all()
        except SQLAlchemyError as e:
            print(f"Ошибка при получении аккаунта: {e}")
            return None

    @staticmethod
    def update(db: Session, account_id: int, **kwargs):
        """
        Обновление аккаунта по ID.
        """
        try:
            account = (
                db.query(CashAccount)
                .filter(CashAccount.id == account_id)
                .first()
            )
            if account:
                for key, value in kwargs.items():
                    setattr(account, key, value)
                db.commit()
                db.refresh(account)
            return account
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Ошибка при обновлении аккаунта: {e}")
            return None

    @staticmethod
    def delete(db: Session, account_id: int):
        """
        Удаление аккаунта по ID.
        """
        try:
            account = (
                db.query(CashAccount)
                .filter(CashAccount.id == account_id)
                .first()
            )
            if account:
                db.delete(account)
                db.commit()
            return account
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Ошибка при удалении аккаунта: {e}")
            return None
