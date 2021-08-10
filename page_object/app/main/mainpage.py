#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: mainpage.py
@date: 2021/8/9 0009
"""

from page.androidpage import AndroidPage
from common.readelement import Element

main = Element('app/main/main')


class AppMainPage(AndroidPage):

    def click_order_button(self):
        self.is_click(main['订单按钮'])

    def click_message_button(self):
        self.is_click(main['消息按钮'])

    def click_mine_button(self):
        self.is_click(main['我的按钮'])
