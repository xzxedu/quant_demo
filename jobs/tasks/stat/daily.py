# -*- coding: utf-8 -*-
from common.models.quant.QuantSaleChangeLog import QuantSaleChangeLog
from common.models.stat.StatDailyMember import StatDailyMember
from common.models.quant.WxShareHistory import WxShareHistory
from common.libs.Helper import getFormatDate, getCurrentDate
from common.models.stat.StatDailyQuant import StatDailyQuant
from common.models.stat.StatDailySite import StatDailySite
from common.models.member.Member import Member
from common.models.pay.PayOrder import PayOrder
from application import app, db
from sqlalchemy import func
import random
"""
python manager.py runjob -m stat/daily -a member|quant|site -p 2019-09-01
"""
class JobTask():
    def __init__(self):
        pass

    def run(self, params):
        act = params['act'] if 'act' in params else ''
        date = params['param'][0] if params['param'] and len(params['param']) else getFormatDate(format="%Y-%m-%d")
        if not act:
            return

        date_from = date + " 00:00:00"
        date_to = date + " 23:59:59"
        func_params = {
            'act': act,
            'date': date,
            'date_from': date_from,
            'date_to': date_to
        }
        if act == "member":
            self.statMember(func_params)
        elif act == "quant":
            self.statQuant(func_params)
        elif act == "site":
            self.statSite(func_params)
        elif act == "test":
            self.test()

        app.logger.info("it's over")
        return

    """
    会员统计
    """
    def statMember(self, params):
        act = params['act']
        date = params['date']
        date_from = params['date_from']
        date_to = params['date_to']
        app.logger.info("act:{0},from:{1},to:{2}".format(act, date_from, date_to))

        member_list = Member.query.all()
        if not member_list:
            app.logger.info("no member list")
            return

        for member_info in member_list:
            tmp_stat_member = StatDailyMember.query.filter_by(date=date, member_id=member_info.id).first()
            if tmp_stat_member:
                tmp_model_stat_member = tmp_stat_member
            else:
                tmp_model_stat_member = StatDailyMember()
                tmp_model_stat_member.date = date
                tmp_model_stat_member.member_id = member_info.id
                tmp_model_stat_member.created_time = getCurrentDate()

            tmp_stat_pay = db.session.query(func.sum(PayOrder.total_price).label("total_pay_money")) \
                    .filter(PayOrder.member_id == member_info.id, PayOrder.status == 1)\
                    .filter(PayOrder.created_time >= date_from, PayOrder.created_time <= date_to).first()
            tmp_stat_share_count = WxShareHistory.query.filter(PayOrder.member_id == member_info.id)\
                    .filter(PayOrder.created_time >= date_from, PayOrder.created_time <= date_to).count()

            tmp_model_stat_member.total_shared_count = tmp_stat_share_count
            tmp_model_stat_member.total_pay_money = tmp_stat_pay[0] if tmp_stat_pay[0] else 0.00
            '''
            为了测试效果模拟数据
            '''
            tmp_model_stat_member.total_shared_count = random.randint(50, 100)
            tmp_model_stat_member.total_pay_money = random.randint(1000, 1010)
            tmp_model_stat_member.updated_time = getCurrentDate()
            db.session.add(tmp_model_stat_member)
            db.session.commit()

        return

    '''
    Quant统计
    '''
    def statQuant(self, params):
        act = params['act']
        date = params['date']
        date_from = params['date_from']
        date_to = params['date_to']
        app.logger.info("act:{0},from:{1},to:{2}".format(act, date_from, date_to))

        stat_quant_list = db.session.query(QuantSaleChangeLog.quant_id, func.sum(QuantSaleChangeLog.quantity).label("total_count"),
                         func.sum(QuantSaleChangeLog.price).label("total_pay_money")) \
            .filter(QuantSaleChangeLog.created_time >= date_from, QuantSaleChangeLog.created_time <= date_to)\
            .group_by(QuantSaleChangeLog.quant_id).all()

        if not stat_quant_list:
            app.logger.info("no data")
            return

        for item in stat_quant_list:
            tmp_quant_id = item[0]
            tmp_stat_quant = StatDailyQuant.query.filter_by(date=date, quant_id=tmp_quant_id).first()
            if tmp_stat_quant:
                tmp_model_stat_quant = tmp_stat_quant
            else:
                tmp_model_stat_quant = StatDailyQuant()
                tmp_model_stat_quant.date = date
                tmp_model_stat_quant.quant_id = tmp_quant_id
                tmp_model_stat_quant.created_time = getCurrentDate()

            tmp_model_stat_quant.total_count = item[1]
            tmp_model_stat_quant.total_pay_money = item[2]
            tmp_model_stat_quant.updated_time = getCurrentDate()

            '''
            为了测试效果模拟数据
            '''
            tmp_model_stat_quant.total_count = random.randint(50, 100)
            tmp_model_stat_quant.total_pay_money = random.randint(1000, 1010)

            db.session.add(tmp_model_stat_quant)
            db.session.commit()

        return

    """
    site统计
    """
    def statSite(self, params):
        act = params['act']
        date = params['date']
        date_from = params['date_from']
        date_to = params['date_to']
        app.logger.info("act:{0},from:{1},to:{2}".format(act, date_from, date_to))

        # 查询总支付金额
        stat_pay = db.session.query(func.sum(PayOrder.total_price).label("total_pay_money")) \
            .filter(PayOrder.status == 1) \
            .filter(PayOrder.created_time >= date_from, PayOrder.created_time <= date_to).first()

        stat_member_count = Member.query.count()
        stat_new_member_count = Member.query.filter(Member.created_time >= date_from,
                            Member.created_time <= date_to).count()

        stat_order_count = PayOrder.query.filter_by(status=1)\
            .filter(PayOrder.created_time >= date_from, PayOrder.created_time <= date_to)\
            .count()

        stat_share_count = WxShareHistory.query.filter(WxShareHistory.created_time >= date_from
            , WxShareHistory.created_time <= date_to).count()

        tmp_stat_site = StatDailySite.query.filter_by(date=date).first()
        if tmp_stat_site:
            tmp_model_stat_site = tmp_stat_site
        else:
            tmp_model_stat_site = StatDailySite()
            tmp_model_stat_site.date = date
            tmp_model_stat_site.created_time = getCurrentDate()

        tmp_model_stat_site.total_pay_money = stat_pay[0] if stat_pay[0] else 0.00
        tmp_model_stat_site.total_new_member_count = stat_new_member_count
        tmp_model_stat_site.total_member_count = stat_member_count
        tmp_model_stat_site.total_order_count = stat_order_count
        tmp_model_stat_site.total_shared_count = stat_share_count
        tmp_model_stat_site.updated_time = getCurrentDate()
        '''
        为了测试效果模拟数据
        '''
        tmp_model_stat_site.total_pay_money = random.randint(1000, 1010)
        tmp_model_stat_site.total_new_member_count = random.randint(50, 100)
        tmp_model_stat_site.total_member_count += tmp_model_stat_site.total_new_member_count
        tmp_model_stat_site.total_order_count = random.randint(900, 1000)
        tmp_model_stat_site.total_shared_count = random.randint(1000, 2000)
        db.session.add(tmp_model_stat_site)
        db.session.commit()

    def test(self):
        import datetime
        from common.libs.Helper import getFormatDate
        now = datetime.datetime.now()
        for i in reversed(range(1, 30)):
            date_before = now + datetime.timedelta(days=-i)
            date = getFormatDate(date=date_before, format="%Y-%m-%d")
            tmp_params = {
                'act': 'test',
                'date': date,
                'date_from': date + " 00:00:00",
                'date_to':  date + " 23:59:59"
            }
            self.testQuant(date)
            self.statQuant(tmp_params)
            self.statMember(tmp_params)
            self.statSite(tmp_params)

    def testQuant(self, date):
        from common.models.quant.Quant import Quant
        list = Quant.query.all()
        if list:
            for item in list:
                model = QuantSaleChangeLog()
                model.quant_id = item.id
                model.quantity = random.randint(1, 10)
                model.price = model.quantity * item.price
                model.member_id = 1
                model.created_time = date + " " + getFormatDate(format="%H:%M:%S")
                db.session.add(model)
                db.session.commit()
