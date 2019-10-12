# -*- coding: utf-8 -*-
from flask import Blueprint, request
from common.libs.Helper import ops_render
from application import app
from common.libs.Helper import getFormatDate, iPagination, getDictFilterField, selectFilterObj
from common.models.stat.StatDailySite import StatDailySite
from common.models.stat.StatDailyQuant import StatDailyQuant
from common.models.stat.StatDailyMember import StatDailyMember
from common.models.member.Member import Member
from common.models.quant.Quant import Quant
import datetime

route_stat = Blueprint('stat_page', __name__)

@route_stat.route("/index")
def index():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if 'date_from' in req else default_date_from
    date_to = req['date_to'] if 'date_to' in req else default_date_to
    query = StatDailySite.query.filter(StatDailySite.date >= date_from) \
        .filter(StatDailySite.date <= date_to)

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']

    list = query.order_by(StatDailySite.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['current'] = 'index'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }
    return ops_render("stat/index.html", resp_data)

@route_stat.route( "/quant" )
def quant():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if 'date_from' in req else default_date_from
    date_to = req['date_to'] if 'date_to' in req else default_date_to
    query = StatDailyQuant.query.filter(StatDailyQuant.date >= date_from) \
        .filter(StatDailyQuant.date <= date_to)

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']

    list = query.order_by(StatDailyQuant.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()
    date_list = []
    if list:
        quant_map = getDictFilterField(Quant, Quant.id, "id", selectFilterObj(list, "quant_id"))
        for item in list:
            tmp_quant_info = quant_map[item.quant_id] if item.quant_id in quant_map else {}
            tmp_data = {
                "date": item.date,
                "total_count": item.total_count,
                "total_pay_money": item.total_pay_money,
                'quant_info': tmp_quant_info
            }
            date_list.append(tmp_data)

    resp_data['list'] = date_list
    resp_data['pages'] = pages
    resp_data['current'] = 'quant'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }
    return ops_render("stat/quant.html", resp_data)

@route_stat.route( "/member" )
def memebr():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if 'date_from' in req else default_date_from
    date_to = req['date_to'] if 'date_to' in req else default_date_to
    query = StatDailyMember.query.filter(StatDailyMember.date >= date_from) \
        .filter(StatDailyMember.date <= date_to)

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']

    list = query.order_by(StatDailyMember.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()
    date_list = []
    if list:
        member_map = getDictFilterField(Member, Member.id, "id", selectFilterObj(list, "member_id"))
        for item in list:
            tmp_member_info = member_map[item.member_id] if item.member_id in member_map else {}
            tmp_data = {
                "date": item.date,
                "total_pay_money": item.total_pay_money,
                "total_shared_count": item.total_shared_count,
                'member_info': tmp_member_info
            }
            date_list.append(tmp_data)

    resp_data['list'] = date_list
    resp_data['pages'] = pages
    resp_data['current'] = 'member'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }
    return ops_render("stat/member.html", resp_data)

@route_stat.route("/share")
def share():
    now = datetime.datetime.now()
    date_before_30days = now + datetime.timedelta(days=-30)
    default_date_from = getFormatDate(date=date_before_30days, format="%Y-%m-%d")
    default_date_to = getFormatDate(date=now, format="%Y-%m-%d")

    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    date_from = req['date_from'] if 'date_from' in req else default_date_from
    date_to = req['date_to'] if 'date_to' in req else default_date_to
    query = StatDailySite.query.filter(StatDailySite.date >= date_from) \
        .filter(StatDailySite.date <= date_to)

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']

    list = query.order_by(StatDailySite.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['current'] = 'quant'
    resp_data['search_con'] = {
        'date_from': date_from,
        'date_to': date_to
    }
    return ops_render("stat/share.html", resp_data)
