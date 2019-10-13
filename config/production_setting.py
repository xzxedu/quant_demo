# 生产环境的配置
# -*- coding: utf-8 -*-

DEBUG = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql://root:wechatdemo123@127.0.0.1/quant_db?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = "utf8mb4"

APP = {
    'domain':'https://xzx.faithforfuture.com'
}

RELEASE_VERSION="20190929001"
