import schedule
from flask import Flask

import cleaner_expired
from database import init_db

app = Flask(__name__)
init_db()

if __name__ == '__main__':
    schedule.every().second.do(cleaner_expired.delete_expired)
    stop_run_continuously = cleaner_expired.run_continuously()

    app.run()

import routes
