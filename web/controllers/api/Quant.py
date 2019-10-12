# -*- coding: utf-8 -*-
from common.models.member.MemberCart import MemberCart
from common.models.quant.QuantCat import QuantCat
from common.libs.UrlManager import UrlManager
from common.models.quant.Quant import Quant
from web.controllers.api import route_api
from flask import request, jsonify, g
from application import app, db
from sqlalchemy import or_
import requests, json

@route_api.route("/quant/index")
def quantIndex():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    cat_list = QuantCat.query.filter_by(status=1).order_by(QuantCat.weight.desc()).all()
    data_cat_list = []
    data_cat_list.append({
        'id': 0,
        'name': '全部'
    })
    if cat_list:
        for item in cat_list:
            tmp_data = {
                "id": item.id,
                "name": item.name
            }
            data_cat_list.append(tmp_data)
    resp['data']['cat_list'] = data_cat_list

    quant_list = Quant.query.filter_by(status=1)\
        .order_by(Quant.total_count.desc(), Quant.id.desc()).limit(3).all()
    data_quant_list = []
    if quant_list:
        for item in quant_list:
            tmp_data = {
                "id": item.id,
                "pic_url": UrlManager.buildImageUrl(item.main_image)
            }
            data_quant_list.append(tmp_data)
    resp['data']['banner_list'] = data_quant_list
    return jsonify(resp)

@route_api.route("/quant/search")
def quantSearch():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    cat_id = int(req['cat_id']) if 'cat' in req else 0
    mix_kw = str(req['mix_kw']) if 'mix_kw' in req else ''
    p = int(req['p']) if 'p' in req else 1
    if p < 1:
        p = 1

    query = Quant.query.filter_by(status=1)
    page_size = 10
    offset = (p-1) * page_size
    if cat_id > 0:
        query = query.filter(Quant.cat_id == cat_id)

    if mix_kw in req:
        rule = or_(Quant.name.ilike("%{0}%".format(mix_kw))), Quant.tags.ilike("%{0}%".format(mix_kw))
        query = query.filter(rule)

    quant_list = query.order_by(Quant.total_count.desc(), Quant.id.desc())\
        .offset(offset).limit(page_size).all()
    data_quant_list = []
    if quant_list:
        for item in quant_list:
            tmp_data = {
                'id': item.id,
                'name': "%s" % (item.name),
                'price': str(item.price),
                'min_price': str(item.price),
                'pic_url': UrlManager.buildImageUrl(item.main_image)
            }
            data_quant_list.append(tmp_data)

    resp['data']['list'] = data_quant_list
    resp['data']['has_more'] = 0 if len(data_quant_list) < page_size else 1
    return jsonify(resp)

@route_api.route("/quant/info")
def quantInfo():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req else 0
    quant_info = Quant.query.filter_by(id=id).first()
    if not quant_info and not quant_info.status:
        resp['code'] = -1
        resp['msg'] = "该产品已下架 "
        return jsonify(resp)

    member_info = g.member_info
    cart_number = 0
    if member_info:
        cart_number = MemberCart.query.filter_by(member_id=member_info.id).count()
    resp['data']['info'] = {
        "id": quant_info.id,
        "name": quant_info.name,
        "summary": quant_info.summary,
        "total_count": quant_info.total_count,
        "comment_count": quant_info.comment_count,
        "main_image": UrlManager.buildImageUrl(quant_info.main_image),
        "price": str(quant_info.price),
        "stock": quant_info.stock,
        "pics": [UrlManager.buildImageUrl(quant_info.main_image)]
    }
    resp['data']['cart_number'] = cart_number
    return jsonify(resp)

