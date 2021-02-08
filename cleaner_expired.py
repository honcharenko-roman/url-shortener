import threading
import time
from datetime import date

import schedule

import db_utils


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
    con = db_utils.db_connect()
    cursor = con.cursor()
    with con:
        select_expired_sql = 'SELECT ID FROM Url WHERE EXPIRATION_DATE < ?'
        expired_list = cursor.execute(select_expired_sql, (date.today(),)).fetchall()
        if expired_list:
            expired_list = [i[0] for i in expired_list]
            for expired_record in expired_list:
                delete_sql = 'DELETE FROM Url WHERE ID=?;'
                cursor.execute(delete_sql, (expired_record,))
