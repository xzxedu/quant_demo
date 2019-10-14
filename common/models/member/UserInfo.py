# coding: utf-8
from sqlalchemy import Column, DateTime, Index, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db

class UserInfo(db.Model):

    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue())
    sex = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    reg_ip = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    mob_brand = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    mob_model = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    mob_language = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue())
    mob_version = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    mob_system = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    mob_platform = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    wx_share_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())