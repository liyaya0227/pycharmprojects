#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: mainpage.py
@date: 2021/10/13 0013
"""
from page.webpage import WebPage
from common.readelement import Element

main = Element('jrcw/web/main/main')


class MainPage(WebPage):

    def click_homepage_overview_label(self):
        self.click_element(main['首页概览标签'], sleep_time=0.5)

    def click_sale_label(self):
        if 'active' not in self.get_element_attribute(main['客户结算管理标签'], 'class'):
            self.click_element(main['客户结算管理标签'], sleep_time=0.5)
        self.click_element(main['销售单标签'], sleep_time=0.5)

    def click_settlement_label(self):
        if 'active' not in self.get_element_attribute(main['结算中心标签'], 'class'):
            self.click_element(main['结算中心标签'], sleep_time=0.5)
        self.click_element(main['结算单标签'], sleep_time=0.5)

    def click_reconciliation_label(self):
        if 'active' not in self.get_element_attribute(main['结算中心标签'], 'class'):
            self.click_element(main['结算中心标签'], sleep_time=0.5)
        self.click_element(main['对账单标签'], sleep_time=0.5)

    def click_receipt_label(self):
        if 'active' not in self.get_element_attribute(main['资金管理标签'], 'class'):
            self.click_element(main['资金管理标签'], sleep_time=0.5)
        self.click_element(main['收款单标签'], sleep_time=0.5)

    def click_pay_label(self):
        if 'active' not in self.get_element_attribute(main['资金管理标签'], 'class'):
            self.click_element(main['资金管理标签'], sleep_time=0.5)
        self.click_element(main['付款单标签'], sleep_time=0.5)

    def log_out(self):
        """退出财务系统"""
        self.click_element(main['登录用户名标签'], sleep_time=0.5)
        self.click_element(main['退出登录按钮'])

    def close_notice(self):
        """关闭右上角通知"""
        if self.element_is_exist(main['通知关闭按钮']):
            self.click_element(main['通知关闭按钮'])
