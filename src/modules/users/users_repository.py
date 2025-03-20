from sqlalchemy import text
from db import DB, Account


class UserRepository:

    @classmethod
    async def getUserById(cls, id: int) -> Account:
        try:
            session = DB.getSession()
            user = session.query(Account).filter(Account.id == id).one()
            session.commit()
            return user
        except Exception as e:
            print(e)
            return None
