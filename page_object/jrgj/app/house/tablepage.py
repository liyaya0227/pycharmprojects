#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/11/12 0012
"""
from page.androidpage import AndroidPage
from common.readelement import Element

house_table = Element('jrgj/app/house/table')


class AppHouseTablePage(AndroidPage):

    def click_sale_tab(self):
        """点击二手标签"""
        self.click_element(house_table['二手标签'])

    def click_rent_tab(self):
        """点击租赁标签"""
        self.click_element(house_table['租赁标签'])

    def click_new_tab(self):
        """点击新房标签"""
        self.click_element(house_table['新房标签'])

    def click_search_button(self):
        """点击搜索按钮"""
        self.click_element(house_table['搜索按钮'])

    def input_search_content(self, search_content):
        """输入搜索内容，按回车"""
        self.click_element(house_table['搜索输入框'])
        self.input_text_into_element(house_table['搜索输入框'], search_content)
        self.send_enter_key()

    def get_table_count(self):
        """获取列表数据条数"""
        return self.get_element_text(house_table['搜索输入框'])[3:-1]

    def go_house_detail_by_row(self, row=1):
        """进入房源详情"""
        locator_xpath = "//*[@class='android.view.ViewGroup' and @index='2']//*[@class='android.widget.ScrollView']" \
                        "//*[@class='android.view.ViewGroup']*[@class='android.view.ViewGroup' and @index='" \
                        + str(row-1) + "']"
        self.click_element(("xpath", locator_xpath))
