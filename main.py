from datetime import timedelta, date

from flask import Flask, request
from flask_restful import Resource, Api

import db_utils
import shortener

app = Flask(__name__)
api = Api(app)


class UrlShortenerAPI(Resource):

    def get(self):
        days_to_expire = request.args.get('days_to_expire')
        days_to_expire = 90 if days_to_expire is None else days_to_expire

        original_url = request.args.get('url')

        con = db_utils.db_connect()
        cursor = con.cursor()

        with con:
            last_inserted_id = cursor.execute("SELECT ID FROM URL ORDER BY ID DESC LIMIT 1").fetchone()
            encoded_id = 1 if last_inserted_id is None else shortener.unshort(last_inserted_id[0]) + 1

            cursor.execute("INSERT INTO Url (ID, ORIGINAL, EXPIRATION_DATE) VALUES (?, ?, ?)",
                           (shortener.shorten(encoded_id),
                            original_url,
                            date.today() + timedelta(days=int(days_to_expire))))

            return shortener.shorten(encoded_id)

    @app.route('/<short_url>', methods=['GET'])
    def restore_url(short_url):
        con = db_utils.db_connect()
        cursor = con.cursor()
        with con:
            restored_url = cursor.execute('SELECT ORIGINAL FROM Url WHERE ID=?',
                                          (short_url,)).fetchone()
            return restored_url[0] if restored_url else 'NoSuchOriginalLinkError'


api.add_resource(UrlShortenerAPI, '/shorten')

if __name__ == '__main__':
    db_utils.create_url_table()

    # schedule.every().day.do(cleaner_expired.delete_expired)
    # stop_run_continuously = cleaner_expired.run_continuously()

    app.run(debug=True)
