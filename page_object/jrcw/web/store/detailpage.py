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

detail = Element('jrcw/web/store/detail')


class StoreDetailPage(WebPage):

    def get_store_info1(self):
        """获取门店/商户信息"""
        return {
            'store_code': self.get_element_text(detail['门店/商户信息_门店/商户编号标签']),
            'city': self.get_element_text(detail['门店/商户信息_所在城市标签']),
            'create_time': self.get_element_text(detail['门店/商户信息_新增时间标签']),
            'store_name': self.get_element_text(detail['门店/商户信息_门店/商户名称标签']),
            'brand': self.get_element_text(detail['门店/商户信息_所属品牌标签']),
            'last_edit_time': self.get_element_text(detail['门店/商户信息_最后一次编辑时间标签']),
            'company_code': self.get_element_text(detail['门店/商户信息_公司编号标签']),
            'district': self.get_element_text(detail['门店/商户信息_所属商圈标签']),
            'company': self.get_element_text(detail['门店/商户信息_公司名称标签']),
            'region': self.get_element_text(detail['门店/商户信息_所属大区标签']),
            'shop_attribute': self.get_element_text(detail['门店/商户信息_门店/商户属性标签'])
        }

    def get_store_info2(self):
        """获取门店/商户信息"""
        return {
            'type': self.get_element_text(detail['门店/商户信息_类型标签']),
            'accounting_model': self.get_element_text(detail['门店/商户信息_核算模式标签']),
            'settlement_model': self.get_element_text(detail['门店/商户信息_结算模式标签']),
            'settlement_period': self.get_element_text(detail['门店/商户信息_结算周期标签'])
        }

    def get_account_info(self):
        """获取账户信息"""
        return {
            'account_type': self.get_element_text(detail['账户信息_账户类型单元格']),
            'bank_address': self.get_element_text(detail['账户信息_银行所在地单元格']),
            'opening_bank': self.get_element_text(detail['账户信息_开户行单元格']),
            'account_name': self.get_element_text(detail['账户信息_账户名称单元格']),
            'account_number': self.get_element_text(detail['账户信息_账户账号单元格'])
        }

    def click_close_button(self):
        """点击关闭按钮"""
        self.click_element(detail['关闭按钮'])

    def click_edit_button(self):
        """点击编辑按钮"""
        self.click_element(detail['编辑按钮'])
