#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/10/14 0014
"""
import re
from page.webpage import WebPage
from common.readelement import Element

table = Element('jrcw/web/reconciliation/table')


class ReconciliationTablePage(WebPage):

    def input_reconciliation_code_search(self, reconciliation_code):
        """输入对账单据号"""
        self.input_text(table['对账单据号搜索输入框'], reconciliation_code)

    def input_order_code_search(self, order_code):
        """输入订单编号"""
        self.input_text(table['订单编号搜索输入框'], order_code)

    def input_reconciliation_shop_search(self, reconciliation_shop):
        """输入对账门店/商户"""
        self.input_text(table['对账门店/商户搜索输入框'], reconciliation_shop)

    def input_create_time_search(self, create_time):
        """输入单据创建时间"""
        self.input_text(table['单据创建时间搜索输入框'], create_time)

    def input_finance_examine_time_search(self, finance_examine_time):
        """输入财务审核时间"""
        self.input_text(table['财务审核时间搜索输入框'], finance_examine_time)

    def choose_city_search(self, city):
        """选择城市"""
        self.click_element(table['城市搜索输入框'])
        locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'reconciliation')]" \
                           "//label[contains(text(), '城市')]/parent::div//ul/li[text()='" + city + "']"
        self.click_element(locator)

    def choose_reconciliation_status_search(self, reconciliation_status):
        """选择对账状态"""
        self.click_element(table['对账状态搜索输入框'])
        locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'reconciliation')]" \
                           "//label[contains(text(), '城市')]/parent::div//ul/li[text()='" + reconciliation_status + "']"
        self.click_element(locator)

    def click_search_button(self):
        """点击查询按钮"""
        self.click_element(table['查询按钮'])

    def click_reset_button(self):
        """点击重置按钮"""
        self.click_element(table['重置按钮'])

    def click_export_button(self):
        """点击导出按钮"""
        self.click_element(table['导出按钮'])

    def get_table_total_count(self):
        """获取列表总条数"""
        text = self.get_element_text(table['总计标签'])
        return re.search(r"总计(.+?)条", text).group(1)

    def get_table_total_payable_money(self):
        """获取列表总应付金额"""
        text = self.get_element_text(table['总计标签'])
        return re.search(r"应付金额 (.+?)元", text).group(1)

    def get_table_total_receivable_money(self):
        """获取列表总应收金额"""
        text = self.get_element_text(table['总计标签'])
        return re.search(r"应收金额 (.+?)元", text).group(1)

    def get_table_data(self):
        """获取对账单列表信息"""
        table_data = []
        table_row_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'reconciliation')]" \
                                     "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table/tbody/tr"
        for i in range(len(self.find_elements(table_row_locator))):
            reconciliation_code_locator = 'xpath', "//div[@class='ivu-layout']" \
                                                   "//div[contains(@class, 'reconciliation')]" \
                                                   "/div[contains(@class,'table')]//div[@class='ivu-table-body']" \
                                                   "/table/tbody/tr[" + str(i+1) + "]/td[" \
                                          + self.__get_table_column_by_name('对账单信息') + "]//p[1]/span[2]"
            shop_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'reconciliation')]" \
                                    "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table/tbody/tr[" \
                           + str(i+1) + "]/td[" + self.__get_table_column_by_name('对账单信息') + "]//p[2]/span[2]"
            shop_code_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'reconciliation')]" \
                                         "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table/tbody" \
                                         "/tr[" + str(i + 1) + "]/td[" + self.__get_table_column_by_name('对账单信息') \
                                + "]//p[3]/span[2]"
            company_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'reconciliation')]" \
                                       "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table/tbody/tr[" \
                              + str(i + 1) + "]/td[" + self.__get_table_column_by_name('对账单信息') + "]//p[4]/span[2]"
            city_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'reconciliation')]" \
                                    "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table/tbody/tr[" \
                           + str(i + 1) + "]/td[" + self.__get_table_column_by_name('对账单信息') + "]//p[5]/span[2]"
            reconciliation_info = {
                'reconciliation_code': self.get_element_text(reconciliation_code_locator),
                'store': self.get_element_text(shop_locator),
                'shop_code': self.get_element_text(shop_code_locator),
                'company': self.get_element_text(company_locator),
                'city': self.get_element_text(city_locator),
            }
            receivable_money_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'reconciliation')]" \
                                                "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table" \
                                                "/tbody/tr[" + str(i + 1) + "]/td[" \
                                       + self.__get_table_column_by_name('对账金额') + "]//p[1]/span[2]"
            payable_money_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'reconciliation')]" \
                                             "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table" \
                                             "/tbody/tr[" + str(i + 1) + "]/td[" \
                                    + self.__get_table_column_by_name('对账金额') + "]//p[2]/span[2]"
            reconciliation_money_info = {
                'receivable_money': self.get_element_text(receivable_money_locator),
                'payable_money': self.get_element_text(payable_money_locator)
            }
            accounting_model_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'reconciliation')]" \
                                                "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table" \
                                                "/tbody/tr[" + str(i+1) + "]/td[" \
                                       + self.__get_table_column_by_name('状态') + "]//p[1]/span[2]"
            settlement_model_locator = 'xpath',  "//div[@class='ivu-layout']//div[contains(@class, 'reconciliation')]" \
                                                 "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table" \
                                                 "/tbody/tr[" + str(i+1) + "]/td[" \
                                       + self.__get_table_column_by_name('状态') + "]//p[2]/span[2]"
            reconciliation_status_locator = 'xpath', "//div[@class='ivu-layout']" \
                                                     "//div[contains(@class, 'reconciliation')]" \
                                                     "/div[contains(@class,'table')]//div[@class='ivu-table-body']" \
                                                     "/table/tbody/tr[" + str(i+1) + "]/td[" \
                                            + self.__get_table_column_by_name('状态') + "]//p[3]/span[2]"
            status_info = {
                'accounting_model': self.get_element_text(accounting_model_locator),
                'settlement_model': self.get_element_text(settlement_model_locator),
                'reconciliation_status': self.get_element_text(reconciliation_status_locator)
            }
            create_time_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'reconciliation')]" \
                                           "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table/tbody" \
                                           "/tr[" + str(i + 1) + "]/td[" + self.__get_table_column_by_name('日期') \
                                  + "]//span[2]"
            row_data = {
                'reconciliation_info': reconciliation_info,
                'reconciliation_money_info': reconciliation_money_info,
                'status_info': status_info,
                'date_info': self.get_element_text(create_time_locator)
            }
            table_data.append(row_data)
        return table_data

    def click_detail_button_by_row(self, row=1):
        """点击详情按钮"""
        detail_button_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'reconciliation')]" \
                                         "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                                + "]/td[" + self.__get_table_column_by_name('操作') + "]//a[text()='详情']"
        self.click_element(detail_button_locator)

    def click_examine_button_by_row(self, row=1):
        """点击详情按钮"""
        examine_button_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'reconciliation')]" \
                                          "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                                 + "]/td[" + self.__get_table_column_by_name('操作') + "]//a[text()='审核']"
        self.click_element(examine_button_locator)

    def __get_table_column_by_name(self, name):
        """获取列表头的列数"""
        table_header_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'reconciliation')]//div" \
                                        "//div[@class='ivu-table-header']//table/thead/tr/th//span"
        return str(list(map(lambda x: x.text, self.find_elements(table_header_locator))).index(name) + 1)
