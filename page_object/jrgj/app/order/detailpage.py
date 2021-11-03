#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@date: 2021/8/11 0011
"""

from page.androidpage import AndroidPage
from common.readelement import Element

order_detail = Element('jrgj/app/order/detail')


class AppOrderDetailPage(AndroidPage):

    def get_house_code(self):  # 获取房源编号
        value = self.get_element_text(order_detail['房源编号标签'])
        return value.split('：')[1]

    def click_start_shot_button(self):  # 点击开始拍摄按钮
        self.click_element(order_detail['开始拍摄按钮'])

    def click_end_shot_button(self):  # 点击结束拍摄按钮
        self.click_element(order_detail['结束拍摄按钮'])

