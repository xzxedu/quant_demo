# -*- coding: utf-8 -*-
from common.models.quant.QuantStockChangeLog import QuantStockChangeLog
from common.libs.Helper import getCurrentDate
from common.models.quant.Quant import Quant
from application import db

class QuantService():
    @staticmethod
    def setStockChangeLog(quant_id=0, quantity=0, note=''):
        if quant_id < 1:
            return False

        quant_info = Quant.query.filter_by(id=quant_id).first()
        if not quant_info:
            return False

        model_stock_change = QuantStockChangeLog()
        model_stock_change.quant_id = quant_id
        model_stock_change.unit = quantity
        model_stock_change.total_stock = quant_info.stock
        model_stock_change.note = note
        model_stock_change.created_time = getCurrentDate()

        db.session.add(model_stock_change)
        db.session.commit()
        return True
