from sqlalchemy import Column, Integer, Text

from database import Base


class Url(Base):
    __tablename__ = 'urls'

    id = Column(Text, primary_key=True)
    original = Column(Text, nullable=False)
    expiration_date = Column(Integer, nullable=False)

    def __init__(self, id=None, original=None, expiration_date=None):
        self.id = id
        self.original = original
        self.expiration_date = expiration_date

    def __repr__(self):
        return '<Url %r>' % self.id
