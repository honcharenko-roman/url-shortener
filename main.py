from flask import Flask, request, redirect
from flask_restful import Resource, Api

import db_utils
import shortener

app = Flask(__name__)
api = Api(app)


class UrlShortenerAPI(Resource):

    def get(self):
        expiration_date = request.args.get('expiration_date')
        original_url = request.args.get('url')
        con = db_utils.db_connect()
        cursor = con.cursor()

        shorted_original_urls = [original_url[0] for original_url in cursor.execute("SELECT ORIGINAL FROM Url")]

        with con:
            if original_url in shorted_original_urls:
                select_url_sql = 'SELECT ID FROM Url WHERE ORIGINAL=?'
                return cursor.execute(select_url_sql, (original_url,)).fetchone()[0]
            else:
                cursor.execute("SELECT ID FROM URL ORDER BY ID DESC LIMIT 1")
                saved_id = cursor.fetchone()
                saved_id = (shortener.unshort(saved_id[0]) + 1) if saved_id is not None else 1

                insert_url_sql = "INSERT INTO Url (ID, ORIGINAL, EXPIRATION_DATE) VALUES (?, ?, ?)"
                cursor.execute(insert_url_sql,
                               (shortener.shorten(saved_id),
                                original_url,
                                90 if expiration_date is None else expiration_date))

                return shortener.shorten(saved_id)

    @app.route('/<short_url>', methods=['GET'])
    def restore_url(short_url):
        con = db_utils.db_connect()
        cursor = con.cursor()
        with con:
            select_url_sql = 'SELECT ORIGINAL FROM Url WHERE ID=?'
            return redirect(cursor.execute(select_url_sql, (short_url,)).fetchone()[0])


api.add_resource(UrlShortenerAPI, '/shorten')

if __name__ == '__main__':
    db_utils.create_url_table()
    app.run(debug=True)
