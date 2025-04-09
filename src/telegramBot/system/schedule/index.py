import time
import schedule
import threading

class ScheduleSystem:
    def __init__(self):
        self._running = False
        self._thread = None
        self.start()

    def _run_continuously(self):
        while self._running:
            schedule.run_pending()
            time.sleep(5)

    def start(self):
        print('--- ScheduleSystem start')
        if self._running:
            return
            
        self._running = True
        self._thread = threading.Thread(target=self._run_continuously)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread is not None:
            self._thread.join()

Schedule = ScheduleSystem()