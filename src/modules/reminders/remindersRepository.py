from asyncio.log import logger
from datetime import datetime, timedelta
from src.db.models.Operations import Operations
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
      query = (
        session
        .query(Reminder)
        .join(Account, Account.id == Reminder.account_id)
        .filter(Reminder.is_active == True)
        .filter(Reminder.next_time < datetime.now())
        .order_by(Reminder.created_at)
      )

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
  def getAll(session: Session, tg_id: int):
    try:
      reminders = (
          session.query(Reminder)
          .join(Account, Reminder.account_id == Account.id)
          .filter(Account.id == tg_id)
          .order_by(Reminder.created_at.desc())
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
      next_time = RemindersRepository.calculateNextTime(data.day_of_week, int(data.hour))
      reminder = Reminder(
        account_id = data.account_id,
        day_of_week = data.day_of_week,
        hour = data.hour,
        is_active = data.is_active,
        next_time = next_time,
      )
      session.add(reminder)
      session.commit()
      return reminder
    except Exception as e:
      logger.error(f"create reminder error: {str(e)}")
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
      reminder = session.query(Reminder).where(Reminder.id == data.id).one()
      if not reminder: raise Exception('There is not reminder')
      
      if hasattr(data, 'day_of_week'):
        reminder.day_of_week = data.day_of_week if not None else None
      if hasattr(data, 'hour'):
        reminder.hour = data.hour if not None else None
      if hasattr(data, 'is_active'):
        reminder.is_active = data.is_active
      reminder.next_time = RemindersRepository.calculateNextTime(data.day_of_week, int(data.hour))

      session.commit()
      return reminder
    except SQLAlchemyError as e:
      logger.error(f"{str(e)}")
      raise Exception(e)
    except Exception as e:
      raise Exception(e)
    
  @staticmethod
  def get_operations_by_date_range(session: Session, start_date: datetime, end_date: datetime):
      return session.query(Operations)\
          .filter(Operations.created_at >= start_date)\
          .filter(Operations.created_at <= end_date)\
          .order_by(Operations.created_at)\
          .all()