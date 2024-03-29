# -*- coding: utf-8 -*-
from common.models.member.MemberCart import MemberCart
from common.libs.Helper import getCurrentDate
from application import app, db

class CartService():

    @staticmethod
    def deleteItem(member_id=0, items=None):
        if member_id < 1 or not items:
            return False
        for item in items:
            MemberCart.query.filter_by(quant_id=item['id'], member_id=member_id).delete()
        db.session.commit()
        return True
    @staticmethod
    def setItems(member_id=0, quant_id=0, number=0):
        if member_id < 1 or quant_id < 1 or number < 1:
            return False

        cart_info = MemberCart.query.filter_by(quant_id=quant_id, member_id=member_id).first()
        if cart_info:
            model_cart = cart_info
        else:
            model_cart = MemberCart()
            model_cart.member_id = member_id
            model_cart.created_time = getCurrentDate()

        model_cart.quant_id = quant_id
        model_cart.quantity = number
        model_cart.updated_time = getCurrentDate()
        db.session.add(model_cart)
        db.session.commit()
        return True