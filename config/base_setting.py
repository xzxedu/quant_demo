# 基础配置（端口号）
SERVER_PORT = 8999

# 生产环境下
DEBUG = False
SQLALCHEMY_ECHO = False
AUTH_COOKIE_NAME = "quant_cookie"

## 过滤url
IGNORE_URLS = [
    "^/user/login",
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^favicon.ico"
]

API_IGNORE_URLS = [
    "^/api"
]

# how many to display in a page
PAGE_SIZE = 10
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    "1": "正常",
    "0": "已删除"
}
# 'paykey': '微信商户的api key',
# 'mch_id': '微信商户的id',
MINA_APP = {
    'appid': 'wx76aec7d8d5f5083f',
    'appkey': 'de369b1d7fcb9d07cecb30a7ea30fbf1',
    'paykey': 'wx76aec7d8d5f5083f',  # fake
    'mch_id': '1443337302',  #fake
    'callback_url': '/api/order/callback'
}

UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/static/upload/'
}

APP = {
    'domain': 'http://192.168.1.105:8999'
}

PAY_STATUS_MAPPING = {
    "1": "已支付",
    "-8": "待支付",
    "0": "已关闭"
}

PAY_STATUS_DISPLAY_MAPPING = {
    "0": "订单关闭",
    "1": "支付成功",
    "-8": "待支付",
    "-7": "待发货",
    "-6": "待确认",
    "-5": "待评价"
}

