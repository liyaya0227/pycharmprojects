#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/8/10 0010
"""

from page.androidpage import AndroidPage
from common.readelement import Element

order_table = Element('app/order/table')


class AppOrderTablePage(AndroidPage):

    def click_search_button(self):  # 点击搜索按钮
        self.is_click(order_table['搜索按钮'])

    def input_search_content(self, search_content):  # 输入搜索内容，按回车
        self.is_click(order_table['搜索输入框'])
        self.input_text_with_enter(order_table['搜索输入框'], search_content)

    def go_order_detail_by_index(self, index=1):  # 根据index，进入订单详情
        locator = 'xpath', \
                  "//*[@class='android.widget.TextView' and contains(@text,'订单编号')]/parent::android.view.ViewGroup" \
                  "/parent::android.view.ViewGroup/*[@class='android.view.ViewGroup' and @index='" + str(index) + "']"
        self.is_click(locator)

    def get_shot_status_by_index(self, index=1):  # 根据index，获取订单状态
        locator = 'xpath', \
                  "//*[@class='android.widget.TextView' and contains(@text,'订单编号')]/parent::android.view.ViewGroup" \
                  "/parent::android.view.ViewGroup/*[@class='android.view.ViewGroup' and @index='" + str(index) + "']" \
                  "/*[@class='android.view.ViewGroup' and @index='1']/*[@class='android.widget.TextView']"
        return self.get_element_attribute(locator)

    def choose_date(self, date):
        month = date.split(' ')[1]
        if month == '01':
            date = date.replace(month, '一月')
        if month == '02':
            date = date.replace(month, '二月')
        if month == '03':
            date = date.replace(month, '三月')
        if month == '04':
            date = date.replace(month, '四月')
        if month == '05':
            date = date.replace(month, '五月')
        if month == '06':
            date = date.replace(month, '六月')
        if month == '07':
            date = date.replace(month, '七月')
        if month == '08':
            date = date.replace(month, '八月')
        if month == '09':
            date = date.replace(month, '九月')
        if month == '10':
            date = date.replace(month, '十月')
        if month == '11':
            date = date.replace(month, '十一月')
        if month == '12':
            date = date.replace(month, '十二月')
        locator = 'xpath', \
                  "//*[@class='android.widget.Button' and contains(@content-desc,'" + date + "')]"
        self.is_click(locator)
