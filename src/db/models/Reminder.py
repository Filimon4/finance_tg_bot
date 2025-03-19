from sqlalchemy import Column, Integer, Enum, TIMESTAMP, Boolean, func, ForeignKey
from ..index import Base
from src.modules.reminders import DayOfWeek

class Reminder(Base):
    __tablename__ = "reminder"

    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)

    id = Column(Integer, primary_key=True, autoincrement=True)
    day_of_week = Column(Enum(DayOfWeek), nullable=False)
    time = Column(TIMESTAMP, nullable=False)
    next_time = Column(TIMESTAMP, nullable=True)
    is_acitve = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=func.now())

