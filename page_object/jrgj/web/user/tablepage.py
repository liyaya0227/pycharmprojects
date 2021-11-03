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

table = Element('jrgj/web/user/table')


class UserTablePage(WebPage):

    def input_phone_search(self, phone):
        self.input_text(table['电话搜索框'], phone)

    def click_search_button(self):
        self.click_element(table['搜索按钮'], sleep_time=1)

    def get_shop_info_by_row(self, row=1):
        code_locator = 'xpath', \
                       "//div[@style='' or not(@style)]/div[@class='user-management-less']" \
                       "/div[@class='user-management-list']//table/tbody/tr[" + str(row) \
                       + "]/td[" + str(self.__get_column_by_title('门店信息')) + "]/div/p"
        shop_code = self.get_element_text(code_locator)
        name_locator = 'xpath', \
                       "//div[@style='' or not(@style)]/div[@class='user-management-less']" \
                       "/div[@class='user-management-list']//table/tbody/tr[" + str(row) \
                       + "]/td[" + str(self.__get_column_by_title('门店信息')) + "]/div"
        shop_name = self.get_element_text(name_locator)
        return {"门店号": shop_code, "门店名": shop_name.split(shop_code)[1].replace('\n', '')}

    def get_shop_group_info_by_row(self, row=1):
        name_locator = 'xpath', \
                       "//div[@style='' or not(@style)]/div[@class='user-management-less']" \
                       "/div[@class='user-management-list']//table/tbody/tr[" + str(row) \
                       + "]/td[" + str(self.__get_column_by_title('店组名称')) + "]/span"
        return self.get_element_text(name_locator)

    def __get_column_by_title(self, title):  # 根据列表头获取index
        title_list = self.find_elements(table['列表头'])
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele) + 1
