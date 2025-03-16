from sqlalchemy import Column, Integer
from ..index import Base

class User(Base):
  __tablename__ = 'user'

  id = Column(Integer, primary_key=True, autoincrement=True)
  
