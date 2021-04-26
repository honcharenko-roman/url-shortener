from datetime import timedelta, date

from flask import request, redirect

import cleaner_expired
import shortener
from database import db_session
from models import Url
from urlshortener import app


@app.route('/shorten', methods=['GET'])
def shorten_url():
    cleaner_expired.delete_expired()

    args = request.args
    days_to_expire = int(args['days_to_expire'])
    original_url = args['url']

    used_ids = db_session.query(Url.id).all()
    used_ids = [shortener.unshort(i[0]) for i in used_ids]

    encoded_id = 1 if not used_ids else max(used_ids) + 1

    user = Url(
        id=shortener.shorten(encoded_id),
        original=original_url,
        expiration_date=date.today() + timedelta(days=days_to_expire)
    )
    db_session.add(user)
    db_session.commit()

    return shortener.shorten(encoded_id)


@app.route('/<short_url>', methods=['GET'])
def restore_url(short_url):
    restored_url = db_session.query(Url).filter(Url.id == short_url)
    return redirect(restored_url[0]) if restored_url else 'NoSuchOriginalLinkError'
