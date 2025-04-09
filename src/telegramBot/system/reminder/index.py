import asyncio
from asyncio.log import logger
import schedule

from src.telegramBot import MainBotTg
from src.db.index import DB
from sqlalchemy.orm import Session
from src.modules.reminders.remindersRepository import RemindersRepository
from sqlalchemy.exc import SQLAlchemyError

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
            
            session.commit()
            yield data_reminders['reminders']
            page += 1


    def __init__(self):
        logger.info('-- Start ReminderSystem')
        self._fetch_interval = 60
        self._loop = asyncio.new_event_loop()  # Создаем свой event loop
        self._setup_scheduler()

    def _setup_scheduler(self):
        schedule.every(self._fetch_interval).minutes.do(self._startFetching_sync)

    def _startFetching_sync(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self.startFetching())

    async def sendReminder(self, reminder) -> bool:
        try:
            user_id = reminder.account.id
            await MainBotTg.send_message(text='🔔 Напоминание: ', chat_id=user_id)
            return True
        except Exception as e:
            print(f"Ошибка при отправке напоминания: {e}")
            return False

    async def startFetching(self):
        try:
            with DB.get_session() as session:
                for reminders in self.paginatedRemindersGenerator(session):
                    for reminder in reminders:
                        await self.sendReminder(reminder)
        except SQLAlchemyError as e:
            print(e)

Reminder = ReminderSystem()