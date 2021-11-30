#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/11/26 0026
"""
from page.webpage import WebPage
from common.readelement import Element
from utils.timeutil import sleep

table = Element('jrgj/web/sharepool/table')


class SharePoolTablePage(WebPage):

    def click_store_share_pool_tab(self):
        """点击门店共享池标签"""
        self.click_element(table['门店共享池标签'])

    def click_region_share_pool_tab(self):
        """点击区域共享池标签"""
        self.click_element(table['区域共享池标签'])

    def click_sale_tab(self):
        """点击买卖标签"""
        self.click_element(table['买卖标签'])

    def click_rent_tab(self):
        """点击租赁标签"""
        self.click_element(table['租赁标签'])

    def input_house_code_search(self, house_code):
        """输入房源编号搜索框"""
        self.input_text_into_element(table['房源编号搜索输入框'], house_code)
        sleep(2)

    def click_search_button(self):
        """点击搜索按钮"""
        self.click_element(table['搜索按钮'])

    def click_reset_button(self):
        """点击重置按钮"""
        self.click_element(table['重置按钮'])

    def dialog_click_confirm_button(self):
        """弹窗，点击确定按钮"""
        self.click_element(table['弹窗_确定按钮'])

    def claim_house_by_row(self, row=1):
        """根据行数，认领房源"""
        locator = 'xpath', "//div[not(contains(@style,'display'))]/div[contains(@class,'sharedPool')]" \
                  "//div[contains(@class, 'dataPlateHouseList')]//table/tbody//tr[" + str(row) + "]/td[" \
                  + self.__get_column_by_title('操作') + "]/span[text()='认领']"
        self.click_element(locator)
        self.dialog_click_confirm_button()

    def __get_column_by_title(self, title):
        locator = 'xpath', \
                  "//div[not(contains(@style,'display'))]/div[contains(@class,'sharedPool')]" \
                  "//div[contains(@class, 'dataPlateHouseList')]//table/thead//th"
        return str(list(map(lambda x: x.text, self.find_elements(locator))).index(title) + 1)

    def get_table_count(self):
        locator = 'xpath', \
                  "//div[not(contains(@style,'display'))]/div[contains(@class,'sharedPool')]" \
                  "//div[contains(@class, 'dataPlateHouseList')]//table/tbody//tr[@data-row-key]"
        table_count = self.find_elements(locator)
        if not table_count:
            return 0
        return len(table_count)
