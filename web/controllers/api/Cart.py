# -*- coding: utf-8 -*-
from common.libs.Helper import selectFilterObj, getDictFilterField
from common.models.member.UserBuyHistory import UserBuyHistory
from common.libs.member.CartService import CartService
from common.models.member.MemberCart import MemberCart
from common.libs.Helper import getCurrentDate
from common.libs.UrlManager import UrlManager
from common.models.quant.Quant import Quant
from web.controllers.api import route_api
from flask import request, jsonify, g
from application import db
import json

@route_api.route("/cart/index")
def cartIndex():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    member_info = g.member_info
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "获取失败，未登录"
        return jsonify(resp)
    cart_list = MemberCart.query.filter_by(member_id=member_info.id).all()
    data_cart_list=[]
    if cart_list:
        quant_ids = selectFilterObj(cart_list, "quant_id")
        quant_map = getDictFilterField(Quant, Quant.id, "id", quant_ids)
        for item in cart_list:
            tmp_quant_info = quant_map[item.quant_id]
            tmp_data = {
                "id": item.id,
                "quant_id": item.quant_id,
                "number": item.quantity,
                "name": tmp_quant_info.name,
                "price": str(tmp_quant_info.price),
                "pic_url": UrlManager.buildImageUrl(tmp_quant_info.main_image),
                "active": True
            }
            data_cart_list.append(tmp_data)
    resp['data']['list'] = data_cart_list
    return jsonify(resp)

@route_api.route("/cart/set", methods=["POST"])
def setCart():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    quant_id = int(req['id']) if 'id' in req else 0
    number = int(req['number']) if 'number' in req else 0

    if quant_id < 1 or number < 1:
        resp['code'] = -1
        resp['msg'] = "添加到购物车失败-1"
        return jsonify(resp)

    member_info = g.member_info
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "添加到购物车失败-2"
        return jsonify(resp)

    quant_info = Quant.query.filter_by(id=quant_id).first()
    if not quant_info:
        resp['code'] = -1
        resp['msg'] = "添加到购物车失败-3"
        return jsonify(resp)

    if quant_info.stock < number:
        resp['code'] = -1
        resp['msg'] = "剩余量不足，添加购物车失败"
        return jsonify(resp)

    ret = CartService.setItems(member_id=member_info.id, quant_id=quant_id, number=number)
    if not ret:
        resp['code'] = -1
        resp['msg'] = "添加到购物车失败-4"
        return jsonify(resp)
    """
    添加到用户的购物记录（临时模拟，其实应该是在确认收获后添加）
    """
    history_model = UserBuyHistory()
    history_model.openid = req['openid']
    history_model.nickname = member_info.nickname
    history_model.cat_id = quant_info.cat_id
    history_model.product = quant_info.name
    history_model.price = str(quant_info.price)
    history_model.buy_count = number
    history_model.updated_time = getCurrentDate()

    db.session.add(history_model)
    db.session.commit()

    return jsonify(resp)

@route_api.route("/cart/del", methods=["POST"])
def delCart():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    params_goods = req['goods'] if 'goods' in req else None
    items = []
    if params_goods:
        items = json.loads(params_goods)

    if not items or len(items) < 1:
        return jsonify(resp)

    member_info = g.member_info
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "删除购物车失败-1"
        return jsonify(resp)

    ret = CartService.deleteItem(member_id=member_info.id, items=items)
    if not ret:
        resp['code'] = -1
        resp['msg'] = "删除购物车失败-2"
        return jsonify(resp)

    return jsonify(resp)
