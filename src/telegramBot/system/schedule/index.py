import time
import schedule


class ScheduleSystem:

    def __init__(self):
        self.start()

    def start(self):
        while True:
            print('run pending')
            schedule.run_pending()
            time.sleep(1)


Schedule = ScheduleSystem()