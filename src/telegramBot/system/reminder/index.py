from asyncio.log import logger
import schedule
import time
from typing import Generator

from src.telegramBot import MainBotTg
from src.db.index import DB
from sqlalchemy.orm import Session
from src.modules.reminders.remindersRepository import RemindersRepository
from sqlalchemy.exc import SQLAlchemyError

import json

class ReminderSystem:

    def paginatedRemindersGenerator(self, session: Session, page_size: int = 40):
        page = 1
        while True:
            data_reminders = RemindersRepository.getPaginatedReminders(session, page, page_size)
            if not data_reminders['reminders']:
                break

            for reminder in data_reminders['reminders']:
                if reminder.next_time is None:
                    reminder.next_time = RemindersRepository.calculateNextTime(reminder.day_of_week, reminder.hour)
            
            session.commit() # Сохраняем все изменения разом
            yield data_reminders['reminders']
            page += 1


    def __init__(self):
        logger.info('-- Start ReminderSystem')
        self._fetch_interval = 1  # интервал проверки в минутах
        self._setup_scheduler()

    def _setup_scheduler(self):
        schedule.every(self._fetch_interval).minutes.do(self.startFetching)

    def sendReminder(self, reminder) -> bool:
        try:
            user_id = reminder['account']['id']
            MainBotTg.send_message(text='Напоминание', chat_id=user_id)
            return True
        except Exception as e:
            print(f"Ошибка при отправке напоминания: {e}")
            return False

    def startFetching(self):
        try:
            with DB.get_session() as session:
                for reminder in self.paginatedRemindersGenerator(session):
                    print(reminder)
                    self.sendReminder(reminder)
        except SQLAlchemyError as e:
            print(e)

Reminder = ReminderSystem()