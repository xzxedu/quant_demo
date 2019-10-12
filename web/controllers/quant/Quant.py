# -*- coding: utf-8 -*-
from common.libs.Helper import ops_render, getCurrentDate, iPagination, getDictFilterField
from common.models.quant.QuantStockChangeLog import QuantStockChangeLog
from flask import Blueprint, request, jsonify, redirect
from common.libs.quant.QuantService import QuantService
from common.models.quant.QuantCat import QuantCat
from common.libs.UrlManager import UrlManager
from common.models.quant.Quant import Quant
from application import app, db
from decimal import Decimal
from sqlalchemy import  or_

route_quant = Blueprint('quant_page', __name__)

@route_quant.route("/index")
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = Quant.query
    if 'mix_kw' in req:
        rule = or_(Quant.name.ilike("%{0}%".format(req['mix_kw'])), Quant.tags.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Quant.status == int( req['status'] ) )

    if 'cat_id' in req and int(req['cat_id']) > 0:
        query = query.filter(Quant.cat_id == int(req['cat_id']))

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    list = query.order_by(Quant.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()

    cat_mapping = getDictFilterField(QuantCat, QuantCat.id, "id", [])
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['cat_mapping'] = cat_mapping
    resp_data['current'] = 'index'
    return ops_render( "quant/index.html",resp_data )

@route_quant.route("/info")
def info():
    resp_data = {}
    req = request.args
    id = int(req.get("id", 0))
    reback_url = UrlManager.buildUrl("/quant/index")

    if id < 1:
        return redirect(reback_url)

    info = Quant.query.filter_by(id=id).first()
    if not info:
        return redirect(reback_url)

    stock_change_list = QuantStockChangeLog.query.filter(QuantStockChangeLog.quant_id == id)\
        .order_by(QuantStockChangeLog.id.desc()).all()

    resp_data['info'] = info
    resp_data['stock_change_list'] = stock_change_list
    resp_data['current'] = 'index'
    return ops_render("quant/info.html", resp_data)


@route_quant.route("/set", methods=["GET", "POST"])
def set():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        id = int(req.get('id', 0))
        info = Quant.query.filter_by(id=id).first()
        if info and info.status != 1:
            return redirect(UrlManager.buildUrl("/quant/index"))

        cat_list = QuantCat.query.all()
        resp_data['info'] = info
        resp_data['cat_list'] = cat_list
        resp_data['current'] = 'index'
        return ops_render("quant/set.html", resp_data)

    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req and req['id'] else 0
    cat_id = int(req['cat_id']) if 'cat_id' in req else 0
    name = req['name'] if 'name' in req else ''
    price = req['price'] if 'price' in req else ''
    main_image = req['main_image'] if 'main_image' in req else ''
    summary = req['summary'] if 'summary' in req else ''
    stock = int(req['stock']) if 'stock' in req else ''
    tags = req['tags'] if 'tags' in req else ''

    if cat_id < 1:
        resp['code'] = -1
        resp['msg'] = "请选择分类"
        return jsonify(resp)

    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的名称"
        return jsonify(resp)

    if not price or len(price) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的价格"
        return jsonify(resp)

    price = Decimal(price).quantize(Decimal('0.00'))
    if price <= 0:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的价格"
        return jsonify(resp)

    if main_image is None or len(main_image) < 3:
        resp['code'] = -1
        resp['msg'] = "请上传封面图"
        return jsonify(resp)

    if summary is None or len(summary) < 3:
        resp['code'] = -1
        resp['msg'] = "请输入相应描述，并不能少于10个字符"
        return jsonify(resp)

    if stock < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的剩余量"
        return jsonify(resp)

    if tags is None or len(tags) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入标签，便于搜索"
        return jsonify(resp)

    quant_info = Quant.query.filter_by(id=id).first()
    before_stock = 0 # 改变之前的剩余量
    if quant_info:
        model_quant = quant_info
        before_stock = model_quant.stock
    else:
        model_quant = Quant()
        model_quant.status = 1
        model_quant.created_time = getCurrentDate()

    model_quant.cat_id = cat_id
    model_quant.name = name
    model_quant.price = price
    model_quant.main_image = main_image
    model_quant.summary = summary
    model_quant.stock = stock
    model_quant.tags = tags
    model_quant.updated_time = getCurrentDate()

    db.session.add(model_quant)
    ret = db.session.commit()

    model_stock_change = QuantStockChangeLog()
    model_stock_change.quant_id = model_quant.id
    model_stock_change.unit = int(stock) - int(before_stock)
    model_stock_change.total_stock = stock
    model_stock_change.note = ''
    model_stock_change.created_time = getCurrentDate()

    db.session.add(model_quant)
    db.session.commit()

    QuantService.setStockChangeLog(model_quant.id, int(stock) - int(before_stock), "后台修改")
    return jsonify(resp)

@route_quant.route("/cat")
def cat():
    resp_data = {}
    req = request.values
    query = QuantCat.query

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(QuantCat.status == int(req['status']))
    list = query.order_by(QuantCat.weight.desc(), QuantCat.id.desc()).all()
    resp_data['list'] = list
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['current'] = 'cat'
    return ops_render("quant/cat.html", resp_data)

@route_quant.route( "/cat-set", methods = ["GET", "POST"] )
def catSet():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        id = int(req.get("id", 0))
        info = None
        if id:
            info = QuantCat.query.filter_by(id=id).first()
        resp_data['info'] = info
        resp_data['current'] = 'cat'
        return ops_render("quant/cat_set.html", resp_data)

    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    name = req['name'] if 'name' in req else ''
    weight = int(req['weight']) if ('weight' in req and int(req['weight']) > 0) else 1

    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的分类名称"
        return jsonify(resp)
    quant_cat_info = QuantCat.query.filter_by(id=id).first()
    if quant_cat_info:
        model_quant_cat = quant_cat_info
    else:
        model_quant_cat = QuantCat()
        model_quant_cat.created_time = getCurrentDate()
    model_quant_cat.name = name
    model_quant_cat.weight = weight
    model_quant_cat.updated_time = getCurrentDate()

    db.session.add(model_quant_cat)
    db.session.commit()
    return jsonify(resp)

@route_quant.route("/cat-ops", methods = ["POST"])
def ops():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''

    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号"
        return jsonify(resp)

    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = " 操作有误，请重试"
        return jsonify(resp)

    quant_cat_info = QuantCat.query.filter_by(id=id).first()
    if not quant_cat_info:
        resp['code'] = -1
        resp['msg'] = "指定账号不存在"
        return jsonify(resp)

    if act == "remove":
        quant_cat_info.status = 0
    elif act == "recover":
        quant_cat_info.status = 1

    quant_cat_info.update_time = getCurrentDate()
    db.session.add(quant_cat_info)
    db.session.commit()
    return jsonify(resp)
