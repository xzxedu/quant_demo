# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db, app

class UserBuyHistory(db.Model):

    __tablename__ = 'user_buy_history'

    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    nickname = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    cat_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    product = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    buy_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
