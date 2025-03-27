from sqlalchemy.orm import Session
from datetime import datetime, time
from typing import Dict, Optional
from .remindersRepository import ReminderRepository
from ..reminders_types import DayOfWeek


class ReminderService:
    MAX_REMINDERS_PER_WEEK = 3

    @classmethod
    def create_reminder(
        cls,
        db: Session,
        account_id: int,
        day_of_week: DayOfWeek,
        time_str: str,
        is_active: bool = True,
    ) -> Dict[str, str]:

        if (
            ReminderRepository.count_by_account(db, account_id)
            >= cls.MAX_REMINDERS_PER_WEEK
        ):
            return {
                "success": False,
                "message": f"Нельзя создать более {cls.MAX_REMINDERS_PER_WEEK} напоминаний в неделю",
            }

        try:
            hours, minutes = map(int, time_str.split(":"))
            reminder_time = time(hours, minutes)
        except ValueError:
            return {
                "success": False,
                "message": "Неверный формат времени. Используйте HH:MM",
            }

        # Создание напоминания
        reminder = ReminderRepository.create(
            db=db,
            account_id=account_id,
            day_of_week=day_of_week,
            reminder_time=reminder_time,
            is_active=is_active,
        )

        if not reminder:
            return {
                "success": False,
                "message": "Ошибка при создании напоминания",
            }

        return {
            "success": True,
            "message": f"Напоминание создано: {day_of_week.name} в {time_str}",
            "reminder_id": reminder.id,
        }

    @classmethod
    def get_user_reminders(cls, db: Session, account_id: int) -> Dict[str, str]:
        """Получение всех напоминаний пользователя"""
        reminders = ReminderRepository.get_by_account(db, account_id)
        return {
            "success": True,
            "reminders": [
                {
                    "id": r.id,
                    "day": r.day_of_week.name,
                    "time": r.time.strftime("%H:%M"),
                    "is_active": r.is_active,
                }
                for r in reminders
            ],
        }

    @classmethod
    def update_reminder(
        cls, db: Session, reminder_id: int, account_id: int, **kwargs
    ) -> Dict[str, str]:
        """Обновление напоминания"""
        reminder = ReminderRepository.get(db, reminder_id)
        if not reminder or reminder.account_id != account_id:
            return {
                "success": False,
                "message": "Напоминание не найдено или не принадлежит вам",
            }

        updated = ReminderRepository.update(db, reminder_id, **kwargs)
        if not updated:
            return {
                "success": False,
                "message": "Ошибка при обновлении напоминания",
            }

        return {"success": True, "message": "Напоминание успешно обновлено"}

    @classmethod
    def delete_reminder(
        cls, db: Session, reminder_id: int, account_id: int
    ) -> Dict[str, str]:
        """Удаление напоминания"""
        reminder = ReminderRepository.get(db, reminder_id)
        if not reminder or reminder.account_id != account_id:
            return {
                "success": False,
                "message": "Напоминание не найдено или не принадлежит вам",
            }

        if ReminderRepository.delete(db, reminder_id):
            return {"success": True, "message": "Напоминание удалено"}
        return {"success": False, "message": "Ошибка при удалении напоминания"}
