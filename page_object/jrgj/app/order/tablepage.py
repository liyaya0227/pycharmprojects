#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/8/10 0010
"""
from common_enum.calendar import *
from page.androidpage import AndroidPage
from common.readelement import Element
from utils.timeutil import sleep

order_table = Element('jrgj/app/order/table')


class AppOrderTablePage(AndroidPage):

    def click_search_button(self):  # 点击搜索按钮
        self.click_element(order_table['搜索按钮'])

    def input_search_content(self, search_content):  # 输入搜索内容，按回车
        self.click_element(order_table['搜索输入框'])
        self.input_text_into_element(order_table['搜索输入框'], search_content)
        self.send_enter_key()

    def go_order_detail_by_index(self, index=1):  # 根据index，进入订单详情
        locator_xpath = "//*[@class='android.widget.TextView' and contains(@text,'订单编号')]" \
                        "/parent::android.view.ViewGroup/parent::android.view.ViewGroup" \
                        "/*[@class='android.view.ViewGroup' and @index='" + str(index) + "']"
        self.click_element(('xpath', locator_xpath))
        sleep(4)

    def get_shot_status_by_index(self, index=1):  # 根据index，获取订单状态
        locator = 'xpath', \
                  "//*[@class='android.widget.TextView' and contains(@text,'订单编号')]/parent::android.view.ViewGroup" \
                  "/parent::android.view.ViewGroup/*[@class='android.view.ViewGroup' and @index='" + str(index) + "']" \
                  "/*[@class='android.view.ViewGroup' and @index='1']/*[@class='android.widget.TextView']"
        return self.get_element_text(locator)

    def show_calendar(self):
        self.click_element(order_table['日历下拉按钮'])

    def choose_date(self, date):
        day = int(date.split(' ')[0])
        month = date.split(' ')[1]
        year = date.split(' ')[2]
        date = str(day) + ' ' + CalendarNameEnum[CalendarCodeEnum(month).name].value + ' ' + year
        self.show_calendar()
        locator = 'xpath', \
                  "//*[@class='android.widget.Button' and contains(@content-desc,'" + date + "')]"
        self.click_element(locator)
        sleep(2)
