#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/10/13 0013
"""
import re
from page.webpage import WebPage
from common.readelement import Element

table = Element('jrcw/web/saleorder/table')


class SaleOrderTablePage(WebPage):

    def input_sale_order_code_search(self, sale_order_code):
        """输入销售单据号"""
        self.input_text(table['销售单据号搜索输入框'], sale_order_code)

    def input_project_code_search(self, project_code):
        """输入项目单据号"""
        self.input_text(table['项目单据号搜索输入框'], project_code)

    def input_order_code_search(self, order_code):
        """输入订单号"""
        self.input_text(table['订单号搜索输入框'], order_code)

    def choose_city_search(self, city):
        """选择城市"""
        self.input_text(table['城市搜索下拉框'], city)

    def input_sign_shop_search(self, sign_shop):
        """输入签约门店"""
        self.input_text(table['签约门店搜索输入框'], sign_shop)

    def input_sign_company_search(self, sign_company):
        """输入签约公司"""
        self.input_text(table['签约公司搜素输入框'], sign_company)

    def input_order_time_search(self, order_time):
        """输入下单时间"""
        self.input_text(table['下单时间搜索输入框'], order_time)

    def input_create_time_search(self, create_time):
        """输入创建时间"""
        self.input_text(table['创建时间搜索输入框'], create_time)

    def choose_pay_status_search(self, pay_status):
        """选择支付状态"""
        self.is_click(table['支付状态搜索下拉框'])
        self.input_text(table['支付状态搜索下拉框'], pay_status)

    def click_search_button(self):
        """点击查询按钮"""
        self.is_click(table['查询按钮'])

    def click_reset_button(self):
        """点击重置按钮"""
        self.is_click(table['重置按钮'])

    def click_import_button(self):
        """点击导出按钮"""
        self.is_click(table['导出按钮'])

    def get_table_total_count(self):
        """获取列表总条数"""
        text = self.element_text(table['总计标签'])
        return re.search(r"总计(.+?)条", text).group(1)

    def get_table_total_receivable_money(self):
        """获取列表总条数"""
        text = self.element_text(table['总计标签'])
        return re.search(r"应收金额 (.+?)元", text).group(1)

    def get_row_detail_info(self, row=1):
        """获取列表行信息"""
        sale_order_code_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'sale')]" \
                                           "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                                  + "]/td[" + self.__get_table_column_by_name('销售单信息') \
                                  + "]//span[contains(text(),'销售单据号'])/parent::p"
        sale_order_code = self.element_text(sale_order_code_locator)[7:]
        project_code_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'sale')]" \
                                        "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                               + "]/td[" + self.__get_table_column_by_name('销售单信息') \
                               + "]//span[contains(text(),'项目单据号'])/parent::p"
        project_code = self.element_text(project_code_locator)[7:]
        version_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'sale')]" \
                                   "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                          + "]/td[" + self.__get_table_column_by_name('销售单信息') \
                          + "]//span[contains(text(),'版本号'])/parent::p"
        version = self.element_text(version_locator)[5:]
        sale_order_info = {
            'sale_order_code': sale_order_code,
            'project_code': project_code,
            'version': version
        }
        order_code_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'sale')]" \
                                      "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                             + "]/td[" + self.__get_table_column_by_name('产品信息') \
                             + "]//span[contains(text(),'订单编号'])/parent::p"
        order_code = self.element_text(order_code_locator)[6:]
        product_name_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'sale')]" \
                                        "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                               + "]/td[" + self.__get_table_column_by_name('产品信息') \
                               + "]//span[contains(text(),'产品名称'])/parent::p"
        product_name = self.element_text(product_name_locator)[6:]
        city_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'sale')]" \
                                "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                       + "]/td[" + self.__get_table_column_by_name('产品信息') + "]//span[contains(text(),'城市'])/parent::p"
        city = self.element_text(city_locator)[4:]
        product_info = {
            'order_code': order_code,
            'product_name': product_name,
            'city': city
        }
        receivable_money_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'sale')]" \
                                            "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                                   + "]/td[" + self.__get_table_column_by_name('应收金额') + "]//span"
        receivable_money = self.element_text(receivable_money_locator)[1:].replace(',', '')
        create_time_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'sale')]" \
                                       "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                              + "]/td[" + self.__get_table_column_by_name('日期') \
                              + "]//span[contains(text(),'创建')]/parent::p"
        create_time = self.element_text(create_time_locator)[6:]
        order_time_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'sale')]" \
                                      "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                             + "]/td[" + self.__get_table_column_by_name('日期') \
                             + "]//span[contains(text(),'下单')]/parent::p"
        order_time = self.element_text(order_time_locator)[6:]
        date_info = {
            'create_time': create_time,
            'order_time': order_time
        }
        pay_status_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'sale')]" \
                                      "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                             + "]/td[" + self.__get_table_column_by_name('支付状态') + "]//span[not(@class)]"
        pay_status = self.element_text(pay_status_locator)
        return {
            'sale_order_info': sale_order_info,
            'product_info': product_info,
            'receivable_money': receivable_money,
            'date_info': date_info,
            'pay_status': pay_status
        }

    def click_detail_button_by_row(self, row=1):
        """点击详情按钮"""
        detail_button_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'sale')]" \
                                         "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                                + "]/td[" + self.__get_table_column_by_name('操作') + "]//a[text()='详情']"
        self.is_click(detail_button_locator)

    def __get_table_column_by_name(self, name):
        """获取列表头的列数"""
        table_header_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'sale')]//div" \
                                        "//div[@class='ivu-table-header']//table/thead/tr/th//span"
        return self.find_elements(table_header_locator).index(name)
