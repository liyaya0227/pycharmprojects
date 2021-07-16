#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@time: 2021/06/22
"""

from page.webpage import WebPage
from utils.timeutil import sleep
from common.readelement import Element

customer_table = Element('customer/table')


class CustomerTablePage(WebPage):

    def click_add_button(self):
        self.is_click(customer_table['录入客源按钮'])

    def input_search_text(self, search_text):
        self.input_text(customer_table['搜索输入框'], search_text)

    def click_search_button(self):
        self.is_click(customer_table['查询按钮'])

    def click_all_tab(self):
        self.is_click(customer_table['全部标签'])

    def click_sale_tab(self):
        self.is_click(customer_table['买二手标签'])

    def click_rent_tab(self):
        self.is_click(customer_table['租赁标签'])

    def click_new_house_tab(self):
        self.is_click(customer_table['新房标签'])

    def click_made_deal_tab(self):
        self.is_click(customer_table['已成交标签'])

    def choose_customer_wish(self, customer_wish):
        if customer_wish == '不限':
            self.is_click(customer_table['意愿等级_不限'])
        elif customer_wish == '三星':
            self.is_click(customer_table['意愿等级_三星'])
        elif customer_wish == '二星':
            self.is_click(customer_table['意愿等级_二星'])
        elif customer_wish == '一星':
            self.is_click(customer_table['意愿等级_一星'])
        else:
            raise ValueError('传值错误')

    def go_customer_detail_by_row(self, row=1):
        locator = 'xpath', \
                  "//div[not(contains(@style,'display'))]//div[contains(@class,'customesList')]//table/tbody/tr["\
                  + str(row) + "]/td[2]/a/div"
        self.is_click(locator)
        sleep(1)

    def get_customer_table_count(self):
        locator = 'xpath', "//div[not(contains(@style,'display'))]/div[contains(@class,'customesList')]//table/tbody/tr"
        table_count = self.find_elements(locator)
        if table_count[0].text == '暂无数据':
            return 0
        return len(table_count)
