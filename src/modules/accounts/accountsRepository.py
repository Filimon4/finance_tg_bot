from sqlalchemy import select, text
from sqlalchemy.orm import Session
from src.db.models.Account import Account


class AccountRepository:

    @classmethod
    async def getOrCreateUserById(cls, db: Session, id: int) -> Account:
        try:
            user = await AccountRepository.getUserById(db, id)
            if not user:
                user = await AccountRepository.create(db, id)
            return user
        except Exception as e:
            print(e)
            return None

    @classmethod
    async def getUserById(cls, db: Session, id: int) -> Account:
        try:
            query = select(Account).where(Account.id == id)
            result = db.execute(query)
            return result.scalar()
        except Exception as e:
            print(e)
            return None

    @classmethod
    async def create(cls, db: Session, tg_id: int) -> Account:
        try:
            db.add_all(
                [
                    Account(
                        id=tg_id,
                    )
                ]
            )
            db.commit()
        except Exception as e:
            print(e)
            return None

    @classmethod
    async def delete(db: Session, tg_id: int) -> Account:
        try:
            account = AccountRepository.getUserById(tg_id)
            if not account:
                raise "There is not such account"
            session = db.getSession()
            session.delete(account)
            session.commit()
            return True
        except Exception as e:
            print(e)
            return False
