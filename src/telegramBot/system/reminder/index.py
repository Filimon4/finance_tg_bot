import asyncio
from asyncio.log import logger
import logging
import random
from typing import Optional
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
                reminder.next_time = RemindersRepository.calculateNextTime(reminder.day_of_week, reminder.hour)
            
            session.commit()
            yield data_reminders['reminders']
            page += 1


    def __init__(self):
        logger.info('-- Start ReminderSystem')
        self._fetch_interval = 3600
        self._loop = asyncio.new_event_loop()
        self._task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()

    def _setup_scheduler(self):
        # schedule.every(self._fetch_interval).seconds.do(self._startFetching_sync)
        if not self._task or self._task.done():
            self._task = asyncio.create_task(self._run_periodically())

    async def _run_periodically(self):
        while not self._stop_event.is_set():
            try:
                await self.startFetching()  # Ваш метод для обработки напоминаний
            except Exception as e:
                logging.error(f"ReminderSystem error: {e}")
            await asyncio.sleep(self._fetch_interval)

    async def sendReminder(self, reminder) -> bool:
        try:
            user_id = reminder.account.id
            reminder_messages = [
                "🔔 Напоминание: Не забудь внести последние расходы! Финансы любят порядок.",
                "⏰ Время обновить записи! Занеси последние траты для точного учёта.",
                "💡 Ты давно не добавлял расходы. Не упусти важные детали!",
                "📊 Поддерживай свой бюджет в актуальном состоянии. Добавь последние траты!",
                "💰 Маленькие расходы складываются в большие суммы. Запиши их сейчас!",
                "📝 Не откладывай на потом - внеси расходы пока они свежи в памяти!",
                "🧐 Проверь, все ли траты занесены? Сейчас самое время обновить записи!",
                "🤖 Ваш финансовый помощник напоминает: пора добавить последние расходы!"
            ]
            
            random_message = random.choice(reminder_messages)
            await MainBotTg.send_message(text=random_message, chat_id=user_id)
            return True
        except Exception as e:
            return False

    async def startFetching(self):
        try:
            with DB.get_session() as session:
                for reminders in self.paginatedRemindersGenerator(session):
                    for reminder in reminders:
                        await self.sendReminder(reminder)
        except Exception as e:
            logger.error(f"{str(e)}")
        except SQLAlchemyError as e:
            logger.error(f"{str(e)}")

Reminder = ReminderSystem()