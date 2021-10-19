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

detail = Element('jrcw/web/reconciliation/detail')


class ReconciliationDetailPage(WebPage):

    def get_reconciliation_code(self):
        """获取对账单据号"""
        return self.element_text(detail['对账单据号标签'])

    def get_reconciliation_info(self):
        """获取对账单信息"""
        return {
            'reconciliation_code': self.element_text(detail['对账单信息_对账单号标签']),
            'create_person': self.element_text(detail['对账单信息_创建人标签'])[4:],
            'create_time': self.element_text(detail['对账单信息_单据生成日期标签'])[7:],
            'reconciliation_status': self.element_text(detail['对账单信息_对账状态标签'])[5:],
            'settlement_model': self.element_text(detail['对账单信息_结算模式标签']),
            'finance_examine_person': self.element_text(detail['对账单信息_财务审核人标签'])[6:],
            'finance_examine_time': self.element_text(detail['对账单信息_财务审核时间标签'])[7:],
            'accounting_model': self.element_text(detail['对账单信息_核算模式标签'])[5:]
        }

    def get_reconciliation_money(self):
        """对账单金额"""
        return {
            'receivable_money': self.element_text(detail['对账单金额_应收对账总金额标签'])[1:],
            'payable_money': self.element_text(detail['对账单金额_应付对账总金额标签'])[1:]
        }

    def get_shop_info(self):
        """门店/商户账户信息"""
        return {
            'store': self.element_text(detail['门店/商户账户信息_门店/商户标签'])[6:],
            'account_type': self.element_text(detail['门店/商户账户信息_账户类型标签'])[5:],
            'pay_type': self.element_text(detail['门店/商户账户信息_支付方式标签'])[5:],
            'company': self.element_text(detail['门店/商户账户信息_公司标签'])[3:],
            'bank': self.element_text(detail['门店/商户账户信息_开户行银行标签'])[5:],
            'bank_address': self.element_text(detail['门店/商户账户信息_开户行所在地标签'])[7:],
            'bank_account_name': self.element_text(detail['门店/商户账户信息_开户行账户名称标签'])[8:],
            'city': self.element_text(detail['门店/商户账户信息_城市标签'])[3:],
            'bank_account': self.element_text(detail['门店/商户账户信息_开户行账号标签'])[6:-2]
        }
