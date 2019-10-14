# -*- coding: utf-8 -*-
from common.models.member.OauthMemberBind import OauthMemberBind
from common.models.quant.WxShareHistory import WxShareHistory
from common.libs.member.MemberService import MemberService
from common.models.member.UserInfo import UserInfo
from common.models.member.Member import Member
from common.libs.Helper import getCurrentDate
from web.controllers.api import route_api
from flask import request, jsonify, g
from application import db, app

@route_api.route("/member/login", methods = [ "GET","POST" ])
def login():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = "需要code"
        return jsonify(resp)

    openid = MemberService.getWeChatOpenId(code)

    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错"
        return jsonify(resp)

    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''
    reg_ip = req['reg_ip'] if 'reg_ip' in req else request.remote_addr
    '''
        判断是否已经测试过，注册了直接返回一些信息
    '''
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        model_member = Member()
        model_member.nickname = nickname
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = MemberService.geneSalt()
        model_member.reg_ip = reg_ip
        model_member.updated_time = model_member.created_time = getCurrentDate()
        db.session.add(model_member)
        db.session.commit()

        # 放入user_info table里
        model_user = UserInfo()
        model_user.id = model_member.id
        model_user.nickname = nickname
        model_user.sex = sex
        model_user.reg_ip = reg_ip
        db.session.add(model_user)
        db.session.commit()

        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''
        model_bind.updated_time = model_bind.created_time = getCurrentDate()
        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token, 'openid': openid}
    return jsonify(resp)


@route_api.route("/member/check-reg", methods=["GET", "POST"])
def checkReg():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = "需要code"
        return jsonify(resp)

    openid = MemberService.getWeChatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错"
        return jsonify(resp)

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = "未绑定"
        return jsonify(resp)

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "未查询到绑定信息"
        return jsonify(resp)

    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}
    return jsonify(resp)

@route_api.route("/member/share", methods=[ "POST" ])
def memberShare():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    url = req['url'] if 'url' in req else ''
    member_info = g.member_info
    model_share = WxShareHistory()
    if member_info:
        model_share.member_id = member_info.id
    model_share.share_url = url
    model_share.created_time = getCurrentDate()
    db.session.add(model_share)
    db.session.commit()
    return jsonify(resp)

@route_api.route("/member/info")
def memberInfo():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    member_info = g.member_info
    resp['data']['info'] = {
        "nickname": member_info.nickname,
        "avatar_url": member_info.avatar
    }
    return jsonify(resp)

@route_api.route("/member/systemInfo", methods=["POST"])
def systemInfo():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    openid = req['openid']
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错"
        return jsonify(resp)

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错-1"
        return jsonify(resp)

    user = db.session.query(UserInfo).filter_by(id=bind_info.member_id).first()
    if user is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错-2"
        return jsonify(resp)

    user.mob_brand = req['brand']
    user.mob_model = req['model']
    user.mob_language = req['language']
    user.mob_version = req['version']
    user.mob_system = req['system']
    user.mob_platform = req['platform']

    db.session.add(user)
    db.session.commit()
    return jsonify(resp)
