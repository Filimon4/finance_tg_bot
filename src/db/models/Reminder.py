from pydantic import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    Enum,
    TIMESTAMP,
    Boolean,
    func,
    ForeignKey,
)

from src.modules.reminders.remindersTypes import DayOfWeek
from sqlalchemy.orm import relationship
from datetime import time

from ..index import Base

class ReminderCreateDTO(BaseModel):
    account_id: int
    day_of_week: DayOfWeek
    time: str
    is_acitve: bool

class ReminderUpdateDTO(BaseModel):
    id: int
    day_of_week: DayOfWeek | None
    time: str | None
    is_acitve: bool | None

class Reminder(Base):
    __tablename__ = "reminder"

    account_id = Column(Integer, ForeignKey("account.id"))
    account = relationship("Account", back_populates="reminders")

    id = Column(Integer, primary_key=True, autoincrement=True)
    day_of_week = Column(Enum(DayOfWeek), nullable=False)
    time = Column(TIMESTAMP, nullable=False)
    next_time = Column(TIMESTAMP, nullable=True)
    is_acitve = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=func.now())
