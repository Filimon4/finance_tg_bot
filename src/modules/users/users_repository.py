from sqlalchemy import text
from db import DB, Account

class UserRepository:

  @classmethod
  async def getUserById(cls, id: int):
    session = DB.getSession()
    sql = session.execute(f"SELECT * FROM 'user' WHERE 'user'.id = {id}")
    print(sql)
    return None
