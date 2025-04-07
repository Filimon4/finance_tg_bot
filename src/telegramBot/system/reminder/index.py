from asyncio.log import logger
import schedule
import time
from typing import Generator

class ReminderSystem:
    def __init__(self):
        logger.info('-- Start ReminderSystem')
        self._fetch_interval = 1  # интервал проверки в минутах
        self._setup_scheduler()

    def _setup_scheduler(self):
        schedule.every(self._fetch_interval).minutes.do(self.startFetching)

    def getAvailableReminder(self) -> Generator:
        current_time = time.time()
        for reminder in self._reminders:
            if reminder['time'] <= current_time and not reminder['sent']:
                yield reminder

    def sendReminder(self, reminder: dict) -> bool:
        try:
            print(f"Отправка напоминания пользователю {reminder['user_id']}: {reminder['message']}")
            
            return True
        except Exception as e:
            print(f"Ошибка при отправке напоминания: {e}")
            return False

    async def startFetching(self):
        print(f"Запуск проверки напоминаний в {time.strftime('%Y-%m-%d %H:%M:%S')}")
        # for reminder in self.getAvailableReminder():
        #     self.sendReminder(reminder)

Reminder = ReminderSystem()