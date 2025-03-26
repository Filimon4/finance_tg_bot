from sqlalchemy import select, text
from db import DB
from db.models.Account import Account


class AccountRepository:

    @classmethod
    async def getOrCreateUserById(cls, id: int) -> Account:
        try:
            user = await AccountRepository.getUserById(id)
            if not user:
                user = await AccountRepository.create(id)
            return user
        except Exception as e:
            print(e)
            return None

    @classmethod
    async def getUserById(cls, id: int) -> Account:
        try:
            session = DB.getSession()
            query = select(Account.id).where(Account.id == id)
            result = session.execute(query)
            return result.scalar()
        except Exception as e:
            print(e)
            return None
        
    @classmethod
    async def create(cls, tg_id: int) -> Account:
        try:
            session = DB.getSession()
            session.add_all([Account(
                id=tg_id,
            )])
            session.commit()
        except Exception as e:
            print(e)
            return None
        
    @classmethod
    async def delete(cls, tg_id: int) -> Account:
        try:
            account = AccountRepository.getUserById(tg_id)
            if not account: raise "There is not such account"
            session = DB.getSession()
            session.delete(account)
            session.commit()
            return True
        except Exception as e:
            print(e)
            return False
