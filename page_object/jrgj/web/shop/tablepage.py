#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/8/27 0027
"""

from page.webpage import WebPage
from common.readelement import Element

table = Element('jrgj/web/store/table')


class ShopTablePage(WebPage):

    def input_shop_name_search(self, phone):
        self.input_text(table['门店搜索框'], phone, clear=True)

    def click_search_button(self):
        self.is_click(table['搜索按钮'], sleep_time=1)

    def get_brand_by_shop_code(self, shop_code):
        locator = 'xpath', \
                  "//div[@style='' or not(@style)]/div[@class='filiale-management-less']//table" \
                  "/tbody//td[" + str(self.__get_column_by_title('门店名称')) + "]/div[text()='" \
                  + shop_code + "']/ancestor::tr/td[" + str(self.__get_column_by_title('品牌')) + "]/span"
        return self.element_text(locator)

    def get_company_by_shop_code(self, shop_code):
        locator = 'xpath', \
                  "//div[@style='' or not(@style)]/div[@class='filiale-management-less']//table" \
                  "/tbody//td[" + str(self.__get_column_by_title('门店名称')) + "]/div[text()='" \
                  + shop_code + "']/ancestor::tr/td[" + str(self.__get_column_by_title('公司名称')) + "]//span[not(@class)]"
        return self.element_text(locator)

    def edit_shop_info_by_shop_code(self, shop_code):
        edit_locator = 'xpath', \
                       "//div[@style='' or not(@style)]/div[@class='filiale-management-less']//table" \
                       "/tbody//td[" + str(self.__get_column_by_title('门店名称')) + "]/div[text()='" \
                       + shop_code + "']/ancestor::tr/td[" + str(self.__get_column_by_title('操作')) \
                       + "]//a[text()='编辑']"
        self.is_click(edit_locator, sleep_time=1)

    def __get_column_by_title(self, title):  # 根据列表头获取index
        title_list = self.find_elements(table['列表头'])
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele) + 1
