from sqlalchemy.orm import Session
from src.db.models.Reminder import Reminder, ReminderCreateDTO, ReminderUpdateDTO
from sqlalchemy.exc import SQLAlchemyError

class RemindersRepository:

  @staticmethod
  def getAll(session: Session):
    try:
      return session.query(Reminder).all()
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
      deleted = session.query(Reminder).where(Reminder.id == id).delete()
      session.commit()
      return deleted
    except Exception as e:
      raise Exception(e)
    
  @staticmethod
  def update(session: Session, data: ReminderUpdateDTO):
    try:
      print(data)
      reminder = session.query(Reminder).where(Reminder.id == data.id).scalar()
      print(reminder)
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