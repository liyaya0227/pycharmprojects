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

order_table = Element('jrgj/app/order/table')


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

    def show_calendar(self):
        self.is_click(order_table['日历下拉按钮'])

    # def swipe_down_calendar(self):
    #     self.move_element_to_offset(order_table['搜索输入框'])

    def choose_date(self, date):
        day = int(date.split(' ')[0])
        month = date.split(' ')[1]
        year = date.split(' ')[2]
        if month == '01':
            month = '一月'
        elif month == '02':
            month = '二月'
        elif month == '03':
            month = '三月'
        elif month == '04':
            month = '四月'
        elif month == '05':
            month = '五月'
        elif month == '06':
            month = '六月'
        elif month == '07':
            month = '七月'
        elif month == '08':
            month = '八月'
        elif month == '09':
            month = '九月'
        elif month == '10':
            month = '十月'
        elif month == '11':
            month = '十一月'
        elif month == '12':
            month = '十二月'
        date = str(day) + ' ' + month + ' ' + year
        self.show_calendar()
        locator = 'xpath', \
                  "//*[@class='android.widget.Button' and contains(@content-desc,'" + date + "')]"
        self.is_click(locator)
