from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        expiration_date = request.args.get('expiration_date')
        original_url = request.args.get('url')
        con = db_utils.db_connect()
        cursor = con.cursor()

        with con:
            insert_url_sql = "INSERT INTO Url (ORIGINAL, EXPIRATION_DATE) VALUES (?, ?)"
            cursor.execute(insert_url_sql, (original_url, 90 if expiration_date is None else expiration_date))
            return shortener.shorten(cursor.lastrowid + 1)


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    db_utils.create_url_table()
    # con = db_utils.db_connect()
    # cursor = con.cursor()
    # with con:
    #     product_sql = "INSERT INTO Url (ORIGINAL, EXPIRATION_DATE) VALUES (?, ?)"
    #     cursor.execute(product_sql, ('string', 90))
    app.run(debug=True)
