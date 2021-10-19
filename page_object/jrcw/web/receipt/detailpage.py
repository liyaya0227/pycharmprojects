#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@date: 2021/10/14 0014
"""
from page.webpage import WebPage
from common.readelement import Element

detail = Element('jrcw/web/receipt/detail')


class ReceiptDetailPage(WebPage):

    def get_receipt_code(self):
        """获取收款单据号"""
        return self.element_text(detail['收款单据号标签'])

    def get_project_code(self):
        """获取项目收款单据号"""
        return self.element_text(detail['项目收款单据号标签'])

    def get_receipt_detail(self):
        """获取收款明细"""
        return {
            'order_code': self.element_text(detail['收款明细_订单编号标签']),
            'payer': self.element_text(detail['收款明细_付款方标签'])[4:],
            'pay_money': self.element_text(detail['收款明细_支付金额标签'])[1:],
            'bank_serial_number': self.element_text(detail['收款明细_银行流水号标签'])[6:],
            'service_charge': self.element_text(detail['收款明细_手续费标签'])[1:],
            'common_serial_number': self.element_text(detail['收款明细_公共流水号标签'])[6:],
            'receipt_money': self.element_text(detail['收款明细_收款金额标签'])[1:],
            'receipt_account': self.element_text(detail['收款明细_收款账户标签'])[5:],
            'collection_channel': self.element_text(detail['收款明细_收款渠道标签'])[5:],
            'receipt_account_name': self.element_text(detail['收款明细_收款账户名标签'])[6:],
            'product_type': self.element_text(detail['收款明细_产品类型标签'])[5:],
            'create_pay_time': self.element_text(detail['收款明细_创建支付时间标签'])[7:],
            'fee_type': self.element_text(detail['收款明细_收款类型标签'])[5:],
            'complete_pay_time': self.element_text(detail['收款明细_支付完成时间标签'])[7:],
            'submit_person': self.element_text(detail['收款明细_提交人标签'])[4:],
            'city': self.element_text(detail['收款明细_收款城市标签'])[5:],
            'receipt_company': self.element_text(detail['收款明细_收款公司标签'])[5:],
            'product_name': self.element_text(detail['收款明细_产品名称标签'])[5:]
        }

    def get_payment_detail(self):
        """获取收款明细"""
        return {
            'fee_type': self.element_text(detail['款项明细_收款类型单元格']),
            'receipt_money': self.element_text(detail['款项明细_收款金额单元格'])[1:],
            'receipt_account_name': self.element_text(detail['款项明细_收款账户名单元格']),
            'receipt_company': self.element_text(detail['款项明细_收款公司单元格'])
        }

    def click_close_button(self):
        self.is_click(detail['关闭按钮'])
