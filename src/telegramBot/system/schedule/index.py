import time
import schedule


class ScheduleSystem:

    def __init__(self):
        self.start()

    def start(self):
        while True:
            schedule.run_pending()
            time.sleep(5)


Schedule = ScheduleSystem()