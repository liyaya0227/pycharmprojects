#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/10/15 0015
"""
from page.webpage import WebPage
from common.readelement import Element

table = Element('jrcw/web/store/table')


class StoreTablePage(WebPage):

    def input_store_name_search(self, store_name):
        """输入门店/商户名称"""
        self.input_text(table['门店/商户名称搜索输入框'], store_name)

    def choose_store_type_search(self, store_type):
        """选择类型"""
        self.input_text(table['类型下拉框'], store_type)

    def input_company_name_search(self, company_name):
        """输入公司"""
        self.input_text(table['公司搜索输入框'], company_name)

    def input_district_name_search(self, district_name):
        """输入商圈"""
        self.input_text(table['商圈搜索输入框'], district_name)

    def input_region_name_search(self, region_name):
        """输入大区"""
        self.input_text(table['大区搜索输入框'], region_name)

    def click_search_button(self):
        """点击查询按钮"""
        self.click_element(table['查询按钮'])

    def click_reset_button(self):
        """点击重置按钮"""
        self.click_element(table['重置按钮'])

    def get_row_detail_info(self, row=1):
        """获取列表行信息"""
        common_xpath = "//div[@class='ivu-layout']//div[contains(@class, 'storelist')]//div" \
                       "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) + "]"
        store_locator = 'xpath', common_xpath + "/td[" + self.__get_table_column_by_name('门店/商户名称') + "]/div/div"
        store_code_locator = 'xpath', common_xpath + "/td[" + self.__get_table_column_by_name('门店/商户编号') + "]/div/div"
        city_locator = 'xpath', common_xpath + "/td[" + self.__get_table_column_by_name('城市') + "]//span"
        store_type_locator = 'xpath', common_xpath + "/td[" + self.__get_table_column_by_name('类型') + "]/div/div"
        district_locator = 'xpath', common_xpath + "/td[" + self.__get_table_column_by_name('商圈') + "]/div/div"
        region_locator = 'xpath', common_xpath + "/td[" + self.__get_table_column_by_name('大区') + "]/div/div"
        return {
            'store': self.get_element_text(store_locator),
            'store_code': self.get_element_text(store_code_locator),
            'city': self.get_element_text(city_locator),
            'store_type': self.get_element_text(store_type_locator),
            'district': self.get_element_text(district_locator),
            'region': self.get_element_text(region_locator)
        }

    def click_edit_button_by_row(self, row=1):
        """点击编辑按钮"""
        detail_button_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'storelist')]" \
                                         "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                                + "]/td[" + self.__get_table_column_by_name('操作') + "]//a[text()='编辑']"
        self.click_element(detail_button_locator)

    def click_detail_button_by_row(self, row=1):
        """点击详情按钮"""
        detail_button_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'storelist')]" \
                                         "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                                + "]/td[" + self.__get_table_column_by_name('操作') + "]//a[text()='详情']"
        self.click_element(detail_button_locator)

    def click_delete_button_by_row(self, row=1):
        """点击删除按钮"""
        detail_button_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'storelist')]" \
                                         "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                                + "]/td[" + self.__get_table_column_by_name('操作') + "]//a[text()='删除']"
        self.click_element(detail_button_locator)

    def __get_table_column_by_name(self, name):
        """获取列表头的列数"""
        return str([*map(lambda x:x.text, self.find_elements(table['列表头']))].index(name) + 1)

