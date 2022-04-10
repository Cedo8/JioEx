from . import db
from flask_login import UserMixin
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # For Profile
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    twitter_handle = db.Column(db.String(150))
    tele_handle = db.Column(db.String(150))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    interests = db.Column(MutableList.as_mutable(PickleType), default=[])
    message = db.Column(db.String(10000))

    # For algorithm processing
    last_scrape = db.Column(db.DATE)
    longitude = db.Column(db.REAL)
    latitude = db.Column(db.REAL)
    fitness = db.Column(db.FLOAT)
    positive_post = db.Column(db.FLOAT)
    neutral_post = db.Column(db.FLOAT)
    negative_post = db.Column(db.FLOAT)

