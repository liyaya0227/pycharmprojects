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
from utils.timeutil import sleep

main = Element('jrgj/app/main/main')


class AppMainPage(AndroidPage):

    def click_order_button(self):
        self.click_element(main['订单按钮'])

    def click_house_button(self):
        self.click_element(main['房源按钮'])

    def click_customer_button(self):
        self.click_element(main['客源按钮'])

    def click_message_button(self):
        self.click_element(main['消息按钮'])
        sleep(2)

    def click_mine_button(self):
        self.click_element(main['我的按钮'])
        sleep(1)

    def close_top_view(self):
        if self.check_element_exist(main['经纪人荣誉殿堂_关闭按钮'], timeout=5):
            self.click_element(main['经纪人荣誉殿堂_关闭按钮'])
            sleep(2)
