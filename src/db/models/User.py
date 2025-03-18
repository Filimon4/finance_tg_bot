from sqlalchemy import Column, Integer, TIMESTAMP, func
from ..index import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, default=func.now())
