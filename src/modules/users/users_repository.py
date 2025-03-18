from sqlalchemy import text
from db import DB, User

class UserRepository:

  @classmethod
  async def getUserById(cls, id: int):
    return None
