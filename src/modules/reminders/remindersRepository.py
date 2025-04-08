from datetime import datetime, timedelta
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.db.models.Account import Account
from src.modules.reminders.remindersTypes import DayOfWeek
from src.db.models.Reminder import Reminder, ReminderCreateDTO, ReminderUpdateDTO
from sqlalchemy.exc import SQLAlchemyError

class ReminderDeleteData(BaseModel):
  id: int

class RemindersRepository:

  @staticmethod
  def calculateNextTime(day_of_week: DayOfWeek, hour: int) -> datetime:
      """Вычисляет следующее время срабатывания напоминания на основе дня недели и часа."""
      now = datetime.now()
      current_weekday = now.weekday() 
      target_weekday = DayOfWeek.get_weekday_number(day_of_week) 

      days_ahead = (target_weekday - current_weekday) % 7

      if days_ahead == 0 and now.hour >= hour:
          days_ahead = 7

      next_date = now + timedelta(days=days_ahead)
      next_time = datetime(
          year=next_date.year,
          month=next_date.month,
          day=next_date.day,
          hour=hour,
          minute=0,
          second=0,
      )

      return next_time

  @staticmethod
  def getPaginatedReminders(session: Session, page: int = 1, limit: int = 40):
    try:
      query = session.query(Reminder).join(Account, Account.id == Reminder.account_id).filter(Reminder.is_active == True).order_by(Reminder.created_at)
      offset = (max(page, 1) - 1) * limit
      reminders = query.offset(offset).limit(limit).all()
      return {
          "reminders": reminders,
          "page": page,
          "limit": limit,
      }
    except Exception as e:
      raise Exception(e)
    except SQLAlchemyError as e:
      raise Exception(e)

  @staticmethod
  def getAll(session: Session):
    try:
      page = max(1, page)
      offset = (page - 1) * limit
      reminders = (
          session.query(Reminder)
          .join(Account, Reminder.account_id == Account.id)
          .filter(Account.id == tg_id)
          .order_by(Reminder.created_at.desc())
          .offset(offset)
          .limit(limit)
          .all()
      )
      return reminders
    except Exception as e:
      raise Exception(e)
  
  @staticmethod
  def getById(session: Session, id: int):
    try:
      return session.query(Reminder).filter(Reminder.id == id).first()
    except Exception as e:
      raise Exception(e)
    
  @staticmethod
  def getAllById(session: Session, id: int):
    try:
      return session.query(Reminder).filter(Reminder.account_id == id).all()
    except SQLAlchemyError as e:
      raise Exception(e)
    except Exception as e:
      raise Exception(e)
    
  @staticmethod
  def create(session: Session, data: ReminderCreateDTO):
    try:
      reminder = Reminder(
        account_id = data.account_id,
        day_of_week = data.day_of_week,
        hour = data.hour,
        is_active = data.is_active,
      )
      session.add(reminder)
      session.commit()
      return reminder
    except Exception as e:
      raise Exception(e)

  @staticmethod
  def delete(session: Session, id: int):
    try:
      deleted_count = session.query(Reminder).where(Reminder.id == id).delete()
      session.commit()
      return deleted_count > 0
    except SQLAlchemyError as e:
      raise Exception(e)
    except Exception as e:
      raise Exception(e)
    
  @staticmethod
  def update(session: Session, data: ReminderUpdateDTO):
    try:
      reminder = session.query(Reminder).where(Reminder.id == data.id).scalar()
      if not reminder: raise Exception('There is not reminder')
      
      if hasattr(data, 'day_of_week'):
        reminder.day_of_week = data.day_of_week if not None else None
      if hasattr(data, 'hour'):
        reminder.hour = data.hour if not None else None
      if hasattr(data, 'is_acitve'):
        reminder.is_acitve = data.is_acitve if not None else None

      session.commit()

      return reminder
    except SQLAlchemyError as e:
      print(e)
      raise Exception(e)
    except Exception as e:
      raise Exception(e)