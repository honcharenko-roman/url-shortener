import threading
import time
from datetime import date

import schedule

from database import db_session
from models import Url


def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def delete_expired():
    expired_list = Url.query.filter(Url.expiration_date < date.today()).all()
    [db_session.delete(expired_record) for expired_record in expired_list]
