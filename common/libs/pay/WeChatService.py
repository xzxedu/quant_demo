# -*- coding: utf-8 -*-
from application import app, db
import xml.etree.ElementTree as ET
from common.libs.Helper import getCurrentDate
import hashlib, requests, uuid, json, datetime
from common.models.pay.OauthAccessToken import OauthAccessToken

class WeChatService():
    def __init__(self, merchant_key=None):
        self.merchant_key = merchant_key

    def create_sign(self, pay_data):
        """
        生产签名, 加密
        :param pay_data:
        :return:
        """
        stringA = "".join(["{0}={1}".format(k, pay_data.get(k)) for k in sorted(pay_data)])
        stringSignTemp = '{0}&key={1}'.format(stringA, self.merchant_key)
        sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
        return sign.upper()

    # def get_pay_info(self, pay_data=None):
    #     """
    #     获取支付信息
    #     """
    #     sign = self.create_sign(pay_data)
    #     pay_data['sign'] = sign
    #     xml_data = self.dict_to_xml(pay_data)
    #     headers = {
    #         'Content-Type': 'application/xml'
    #     }
    #     url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    #     r = requests.post(url=url, data=xml_data.encode("utf-8"), headers=headers)
    #     r.encoding = "utf-8"
    #     if r.status_code == 200:
    #         prepay_id = self.xml_to_dict(r.text).get("prepay_id")
    #         pay_sign_data = {
    #             'appId': pay_data.get('appid'),
    #             'timeStamp': pay_data.get('out_trade_no'),
    #             'nonceStr': pay_data.get('nonce_str'),
    #             'package': 'prepay_id={0}'.format(prepay_id),
    #             'signType': ' MD5'
    #         }
    #         pay_sign = self.create_sign(pay_sign_data)
    #         pay_sign_data.pop('appId')
    #         pay_sign_data['paySign'] = pay_sign
    #         pay_sign_data['prepay_id'] = prepay_id
    #
    #         return pay_sign_data
    #     return False

    def get_pay_info(self, pay_data=None):
        """
        缺少mchID，模拟获取支付信息
        """
        sign = self.create_sign(pay_data)
        pay_data['sign'] = sign
        prepay_id = 'wx12220608745169b44b8f43db0304588791'
        pay_sign_data = {
            'appId': pay_data.get('appid'),
            'timeStamp': pay_data.get('out_trade_no'),
            'nonceStr': pay_data.get('nonce_str'),
            'package': 'prepay_id=wx12220608745169b44b8f43db0304588791',
            'signType': ' MD5'
        }
        pay_sign = self.create_sign(pay_sign_data)
        pay_sign_data.pop('appId')
        pay_sign_data['paySign'] = pay_sign
        pay_sign_data['prepay_id'] = prepay_id

        return pay_sign_data
        #return False

    def dict_to_xml(self, dict_data):
        """
        dict to xml
        :param dict_data:
        :return:
        """
        xml = ["<xml>"]
        for k, v in dict_data.items():
            xml.append("<{0}>{1}</{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    def xml_to_dict(self, xml_data):
        """
        xml to dict
        :param xml_data:
        :return:
        """
        xml_dict = {}
        root = ET.fromstring(xml_data)
        for child in root:
            xml_dict[child.tag] = child.text
        return xml_dict

    def get_nonce_str(self):
        """
        获取随机字符串
        :return:
        """
        return str(uuid.uuid4()).replace('-', '')

    def getAccessToken(self):
        token = None
        # find if oauthaccesstoken has non-expired token
        token_info = OauthAccessToken.query.filter(OauthAccessToken.expired_time >= getCurrentDate()).first()
        if token_info:
            token = token_info.access_token
            return token

        config_mina = app.config['MINA_APP']
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}" \
            .format(config_mina['appid'], config_mina['appkey'])

        r = requests.get(url=url)
        if r.status_code != 200 or not r.text:
            return token

        data = json.loads(r.text)
        now = datetime.datetime.now()
        date = now + datetime.timedelta(seconds=data['expires_in'] - 200)
        model_token = OauthAccessToken()
        model_token.access_token = data['access_token']
        model_token.expired_time = date.strftime("%Y-%m-%d %H:%M:%S")
        model_token.created_time = getCurrentDate()
        db.session.add(model_token)
        db.session.commit()

        return data['access_token']



