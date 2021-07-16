#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@date: 2021/7/8 0008
"""

from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element

transaction_detail = Element('transaction/detail')


class TransactionDetailPage(WebPage):

    def complete_transfer_house(self):
        if 'done' not in self.get_element_attribute(transaction_detail['综合办理按钮'], 'class'):
            raise Exception("不能办理过户流程")
        self.is_click(transaction_detail['综合办理按钮'])
        self.is_click(transaction_detail['完成按钮'])
        sleep()

    def close_case(self):
        if 'done' not in self.get_element_attribute(transaction_detail['结案按钮'], 'class'):
            raise Exception("不能办理结案流程")
        self.is_click(transaction_detail['结案按钮'])
        self.is_click(transaction_detail['完成按钮'])
        sleep()
