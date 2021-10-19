#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@date: 2021/10/15 0015
"""
from page.webpage import WebPage
from common.readelement import Element

detail = Element('jrcw/web/pay/detail')


class PayDetailPage(WebPage):

    def get_pay_code(self):
        """获取付款单据号"""
        return self.element_text(detail['付款单据号标签'])

    def get_pay_info(self):
        """获取付款单信息"""
        return {
            'pay_order': self.element_text(detail['付款单信息_付款单据号标签']),
            'create_person': self.element_text(detail['付款单信息_创建人标签'])[4:],
            'pay_status': self.element_text(detail['付款单信息_付款状态标签']),
            'reconciliation_code': self.element_text(detail['付款单信息_对账单据号标签']),
            'project_type': self.element_text(detail['付款单信息_项目类型标签'])[5:],
            'payer': self.element_text(detail['付款单信息_付款人标签'])[4:],
            'store': self.element_text(detail['付款单信息_对账门店/商户标签'])[8:],
            'pay_type': self.element_text(detail['付款单信息_付款方式标签'])[5:],
            'serial_number': self.element_text(detail['付款单信息_流水号标签'])[4:],
            'shop_code': self.element_text(detail['付款单信息_门店/商户编号标签'])[8:],
            'create_time': self.element_text(detail['付款单信息_创建日期标签'])[5:],
            'payable_money': self.element_text(detail['付款单信息_应付金额标签'])[1:],
            'company': self.element_text(detail['付款单信息_所属公司标签'])[5:],
            'pay_time': self.element_text(detail['付款单信息_付款日期标签'])[5:],
            'paid_money': self.element_text(detail['付款单信息_实际付款金额标签'])[1:],
            'city': self.element_text(detail['付款单信息_所在城市标签'])[5:]
        }

    def get_receipt_account_info(self):
        """获取付款单信息"""
        return {
            'account_type': self.element_text(detail['收款账户信息_账户类型单元格']),
            'bank_address': self.element_text(detail['收款账户信息_银行所在地单元格']),
            'opening_bank': self.element_text(detail['收款账户信息_开户行单元格']),
            'account_name': self.element_text(detail['收款账户信息_账户名称单元格']),
            'account_number': self.element_text(detail['收款账户信息_账户账号单元格'])
        }
