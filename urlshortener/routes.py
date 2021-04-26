from datetime import timedelta, date

import requests
from flask import request, redirect

import shortener
from database import db_session
from models import Url
from urlshortener import app


@app.route('/shorten', methods=['GET'])
def shorten_url():
    args = request.args
    days_to_expire = int(args['days_to_expire'])
    original_url = args['url']

    try:
        requests.get(original_url)
    except requests.exceptions.ConnectionError as e:
        return 'Wrong URL'
    if days_to_expire < 0 or days_to_expire > 365:
        return "Wrong expired date"

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

    return f"You can go at {request.host_url}{shortener.shorten(encoded_id)}"


@app.route('/<short_url>', methods=['GET'])
def restore_url(short_url):
    restored_url = db_session.query(Url).filter(Url.id == short_url).first()
    return redirect(restored_url.original) if restored_url else 'No such original link error'
