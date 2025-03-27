from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ....db.models.Account import Account


class AccountRepository:
    @staticmethod
    def create(db: Session):
        """
        Создание нового аккаунта.
        """
        try:
            new_account = Account()
            db.add(new_account)
            db.commit()
            db.refresh(new_account)
            return new_account
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Ошибка при создании аккаунта: {e}")
            return None

    @staticmethod
    def get(db: Session, account_id: int):
        """
        Получение аккаунта по ID.
        """
        try:
            return db.query(Account).filter(Account.id == account_id).first()
        except SQLAlchemyError as e:
            print(f"Ошибка при получении аккаунта: {e}")
            return None

    @staticmethod
    def update(db: Session, account_id: int, **kwargs):
        """
        Обновление аккаунта по ID.
        """
        try:
            account = db.query(Account).filter(Account.id == account_id).first()
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
            account = db.query(Account).filter(Account.id == account_id).first()
            if account:
                db.delete(account)
                db.commit()
            return account
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Ошибка при удалении аккаунта: {e}")
            return None
