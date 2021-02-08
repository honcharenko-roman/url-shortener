from datetime import timedelta, date

import schedule
from flask import Flask, request, redirect
from flask_restful import Resource, Api

import cleaner_expired
import db_utils
import shortener

app = Flask(__name__)
api = Api(app)


class UrlShortenerAPI(Resource):

    def get(self):
        days_to_expire = request.args.get('days_to_expire')
        days_to_expire = 90 if days_to_expire is None else int(days_to_expire)
        days_to_expire = 365 if days_to_expire > 365 else days_to_expire

        original_url = request.args.get('url')

        con = db_utils.db_connect()
        cursor = con.cursor()

        with con:
            used_ids = cursor.execute('SELECT ID FROM Url').fetchall()
            if used_ids:
                used_ids = [shortener.unshort(i[0]) for i in used_ids]

            encoded_id = 1 if used_ids is None else max(used_ids) + 1

            cursor.execute("INSERT INTO Url (ID, ORIGINAL, EXPIRATION_DATE) VALUES (?, ?, ?)",
                           (shortener.shorten(encoded_id),
                            original_url,
                            date.today() + timedelta(days=days_to_expire)))

            return shortener.shorten(encoded_id)

    @app.route('/<short_url>', methods=['GET'])
    def restore_url(short_url):
        con = db_utils.db_connect()
        cursor = con.cursor()
        with con:
            restored_url = cursor.execute('SELECT ORIGINAL FROM Url WHERE ID=?',
                                          (short_url,)).fetchone()
            return redirect(restored_url[0]) if restored_url else 'NoSuchOriginalLinkError'


api.add_resource(UrlShortenerAPI, '/shorten')

if __name__ == '__main__':
    db_utils.create_url_table()

    schedule.every().day.do(cleaner_expired.delete_expired)
    stop_run_continuously = cleaner_expired.run_continuously()

    app.run(debug=True)
