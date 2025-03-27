from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, time
from typing import List, Optional
from src.db.models.Reminder import Reminder
from ..reminders_types import DayOfWeek


class ReminderRepository:
    @staticmethod
    def create(
        db: Session,
        account_id: int,
        day_of_week: DayOfWeek,
        reminder_time: time,
        is_active: bool = True,
    ) -> Optional[Reminder]:
        """Создание нового напоминания"""
        try:
            new_reminder = Reminder(
                account_id=account_id,
                day_of_week=day_of_week,
                time=datetime.combine(datetime.today(), reminder_time),
                is_active=is_active,
            )
            db.add(new_reminder)
            db.commit()
            db.refresh(new_reminder)
            return new_reminder
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error creating reminder: {e}")
            return None

    @staticmethod
    def get(db: Session, reminder_id: int) -> Optional[Reminder]:
        """Получение напоминания по ID"""
        try:
            return db.query(Reminder).filter(Reminder.id == reminder_id).first()
        except SQLAlchemyError as e:
            print(f"Error getting reminder: {e}")
            return None

    @staticmethod
    def get_by_account(db: Session, account_id: int) -> List[Reminder]:
        """Получение всех напоминаний пользователя"""
        try:
            return (
                db.query(Reminder)
                .filter(Reminder.account_id == account_id)
                .all()
            )
        except SQLAlchemyError as e:
            print(f"Error getting reminders by account: {e}")
            return []

    @staticmethod
    def update(db: Session, reminder_id: int, **kwargs) -> Optional[Reminder]:
        """Обновление напоминания"""
        try:
            reminder = (
                db.query(Reminder).filter(Reminder.id == reminder_id).first()
            )
            if reminder:
                for key, value in kwargs.items():
                    setattr(reminder, key, value)
                db.commit()
                db.refresh(reminder)
            return reminder
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error updating reminder: {e}")
            return None

    @staticmethod
    def delete(db: Session, reminder_id: int) -> bool:
        """Удаление напоминания"""
        try:
            reminder = (
                db.query(Reminder).filter(Reminder.id == reminder_id).first()
            )
            if reminder:
                db.delete(reminder)
                db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error deleting reminder: {e}")
            return False

    @staticmethod
    def count_by_account(db: Session, account_id: int) -> int:
        """Подсчет количества напоминаний пользователя"""
        try:
            return (
                db.query(Reminder)
                .filter(Reminder.account_id == account_id)
                .count()
            )
        except SQLAlchemyError as e:
            print(f"Error counting reminders: {e}")
            return 0
