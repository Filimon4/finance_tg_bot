from pydantic import BaseModel
from sqlalchemy import (
    CheckConstraint,
    Column,
    Index,
    Integer,
    Enum,
    TIMESTAMP,
    Boolean,
    func,
    ForeignKey,
    TIME
)

from src.modules.reminders.remindersTypes import DayOfWeek
from sqlalchemy.orm import relationship
from datetime import time

from ..index import Base

class ReminderCreateDTO(BaseModel):
    account_id: int
    day_of_week: DayOfWeek
    hour: str
    is_active: bool

class ReminderUpdateDTO(BaseModel):
    id: int
    day_of_week: DayOfWeek | None
    hour: str | None
    is_active: bool | None

class Reminder(Base):
    __tablename__ = "reminder"


    id = Column(Integer, primary_key=True, autoincrement=True)
    day_of_week = Column(Enum(DayOfWeek), nullable=False)
    hour = Column(Integer, nullable=False, server_default="0", default=0)
    next_time = Column(TIMESTAMP, nullable=True)
    is_active = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=func.now())
    account_id = Column(Integer, ForeignKey("account.id"))
    
    account = relationship("Account", back_populates="reminders")

    __table_args__ = (
        CheckConstraint("hour >= 0 and hour <= 24", 
                      name="ck_hour_reminder"),
        Index("ix_reminder_active_next", "is_active", "next_time"),
    )
