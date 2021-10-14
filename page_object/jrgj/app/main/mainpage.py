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

main = Element('jrgj/app/main/main')


class AppMainPage(AndroidPage):

    def click_order_button(self):
        self.is_click(main['订单按钮'])

    def click_message_button(self):
        self.is_click(main['消息按钮'])

    def click_mine_button(self):
        self.is_click(main['我的按钮'])

    def close_top_view(self):
        if self.find_element(main['经纪人荣誉殿堂_关闭按钮'], wait_time=5):
            self.is_click(main['经纪人荣誉殿堂_关闭按钮'])
