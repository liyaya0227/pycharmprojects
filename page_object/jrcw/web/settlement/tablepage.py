#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/10/14 0013
"""
import re
from page.webpage import WebPage
from common.readelement import Element

table = Element('jrcw/web/settlement/table')


class SettlementTablePage(WebPage):

    def input_settlement_code_search(self, settlement_code):
        """输入销售单据号"""
        self.input_text(table['结算单据号搜索输入框'], settlement_code)

    def input_project_code_search(self, project_code):
        """输入项目单据号"""
        self.input_text(table['项目单据号搜索输入框'], project_code)

    def input_order_code_search(self, order_code):
        """输入订单号"""
        self.input_text(table['订单编号搜索输入框'], order_code)

    def choose_city_search(self, city):
        """选择城市"""
        self.click_element(table['城市搜索输入框'])
        locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                           "//label[contains(text(), '城市')]/parent::div//ul/li[text()='" + city + "']"
        self.click_element(locator)

    def input_settlement_company_search(self, settlement_company):
        """输入结算公司"""
        self.input_text(table['结算公司搜索输入框'], settlement_company)

    def input_settlement_shop_search(self, settlement_shop):
        """输入结算门店"""
        self.input_text(table['结算门店搜索输入框'], settlement_shop)

    def choose_settlement_model_search(self, settlement_model):
        """选择结算模式"""
        self.click_element(table['结算模式输入框'])
        locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                           "//label[contains(text(), '结算模式')]/parent::div//ul/li[text()='" + settlement_model + "']"
        self.click_element(locator)

    def choose_fee_type_search(self, fee_type):
        """选择款项类型"""
        self.click_element(table['款项类型输入框'])
        locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                           "//label[contains(text(), '款项类型')]/parent::div//ul/li[text()='" + fee_type + "']"
        self.click_element(locator)

    def choose_reconciliation_status_search(self, reconciliation_status):
        """选择对账状态"""
        self.click_element(table['对账状态输入框'])
        locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                           "//label[contains(text(), '对账状态')]/parent::div//ul/li[text()='" \
                  + reconciliation_status + "']"
        self.click_element(locator)

    def input_expect_settlement_time_search(self, expect_settlement_time):
        """输入预计结算时间"""
        self.input_text(table['预计结算时间搜索输入框'], expect_settlement_time)

    def input_create_time_search(self, create_time):
        """输入创建时间"""
        self.input_text(table['创建时间搜索输入框'], create_time)

    def input_order_time_search(self, order_time):
        """输入下单时间"""
        self.input_text(table['下单时间搜索输入框'], order_time)

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

    def get_table_total_settlement_money(self):
        """获取列表总条数"""
        text = self.get_element_text(table['总计标签'])
        return re.search(r"总结算金额 (.+?)元", text).group(1)

    def get_table_data(self):
        """获取列表信息"""
        table_data = []
        table_row_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                                     "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table/tbody/tr"
        for i in range(len(self.find_elements(table_row_locator))):
            settlement_code_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                                         "//div[@class='ivu-table-body']//table/tbody/tr[" + str(i+1) \
                                      + "]/td[" + self.__get_table_column_by_name('结算单信息') \
                                      + "]//span[contains(text(),'结算单据号')]/parent::p"
            project_code_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                                            "//div[@class='ivu-table-body']//table/tbody/tr[" + str(i+1) \
                                   + "]/td[" + self.__get_table_column_by_name('结算单信息') \
                                   + "]//span[contains(text(),'项目单据号')]/parent::p"
            version_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                                       "//div[@class='ivu-table-body']//table/tbody/tr[" + str(i+1) \
                              + "]/td[" + self.__get_table_column_by_name('结算单信息') \
                              + "]//span[contains(text(),'结算版本号')]/parent::p"
            settlement_order_info = {
                'settlement_code': self.get_element_text(settlement_code_locator)[7:],
                'project_code': self.get_element_text(project_code_locator)[7:],
                'settlement_version': self.get_element_text(version_locator)[7:]
            }
            order_code_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                                          "//div[@class='ivu-table-body']//table/tbody/tr[" + str(i+1) \
                                 + "]/td[" + self.__get_table_column_by_name('订单信息') + "]//p[1]/a"
            business_type_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                                             "//div[@class='ivu-table-body']//table/tbody/tr[" + str(i+1) \
                                    + "]/td[" + self.__get_table_column_by_name('订单信息') + "]//p[2]"
            product_name_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                                            "//div[@class='ivu-table-body']//table/tbody/tr[" + str(i+1) + "]/td[" \
                                   + self.__get_table_column_by_name('订单信息') + "]//div[@class='ivu-tooltip-rel']"
            fee_type_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                                        "//div[@class='ivu-table-body']//table/tbody/tr[" + str(i + 1) \
                               + "]/td[" + self.__get_table_column_by_name('订单信息') + "]//p[3]/span"
            order_info = {
                'order_code': self.get_element_text(order_code_locator),
                'business_type': self.get_element_text(business_type_locator),
                'product_name': self.get_element_text(product_name_locator),
                'fee_type': self.get_element_text(fee_type_locator)
            }
            city_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                                    "//div[@class='ivu-table-body']//table/tbody/tr[" + str(i+1) + "]/td[" \
                           + self.__get_table_column_by_name('城市') + "]//p"
            settlement_shop_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                                               "//div[@class='ivu-table-body']//table/tbody/tr[" + str(i + 1) \
                                      + "]/td[" + self.__get_table_column_by_name('结算信息') \
                                      + "]//span[contains(text(),'结算门店/商户')]/parent::p/span[2]"
            settlement_company_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                                                  "//div[@class='ivu-table-body']//table/tbody/tr[" + str(i + 1) \
                                         + "]/td[" + self.__get_table_column_by_name('结算信息') \
                                         + "]//span[contains(text(),'结算公司')]/parent::p/span[2]"
            settlement_model_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                                                "//div[@class='ivu-table-body']//table/tbody/tr[" + str(i + 1) \
                                       + "]/td[" + self.__get_table_column_by_name('结算信息') \
                                       + "]//span[contains(text(),'结算模式')]/parent::p/span[2]"
            settlement_info = {
                'settlement_shop': self.get_element_text(settlement_shop_locator),
                'settlement_company': self.get_element_text(settlement_company_locator),
                'settlement_model': self.get_element_text(settlement_model_locator)
            }
            settlement_money_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                                                "//div[@class='ivu-table-body']//table/tbody/tr[" + str(i + 1) \
                                       + "]/td[" + self.__get_table_column_by_name('结算金额') + "]/div/div"
            service_charge_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                                              "//div[@class='ivu-table-body']//table/tbody/tr[" + str(i+1) \
                                     + "]/td[" + self.__get_table_column_by_name('手续费') + "]/div/div"
            order_time_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'sale')]" \
                                          "//div[@class='ivu-table-body']//table/tbody/tr[" + str(i+1) \
                                 + "]/td[" + self.__get_table_column_by_name('日期') \
                                 + "]//span[contains(text(),'下单')]/parent::p"
            expect_settlement_time_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'sale')]" \
                                                      "//div[@class='ivu-table-body']//table/tbody/tr[" + str(i+1) \
                                             + "]/td[" + self.__get_table_column_by_name('日期') \
                                             + "]//span[contains(text(),'预计结算')]/parent::p"
            date_info = {
                'order_time': self.get_element_text(order_time_locator)[6:],
                'expect_settlement_time': self.get_element_text(expect_settlement_time_locator)[8:]
            }
            reconciliation_status_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]"\
                                                     "//div[@class='ivu-table-body']//table/tbody/tr[" + str(i+1) \
                                            + "]/td[" + self.__get_table_column_by_name('对账状态') + "]//span[not(@class)]"
            row_data = {
                'settlement_order_info': settlement_order_info,
                'order_info': order_info,
                'city': self.get_element_text(city_locator),
                'settlement_info': settlement_info,
                'settlement_money': self.get_element_text(settlement_money_locator)[1:],
                'service_charge': self.get_element_text(service_charge_locator)[1:],
                'date_info': date_info,
                'reconciliation_status': self.get_element_text(reconciliation_status_locator)
            }
            table_data.append(row_data)
        return table_data

    def click_detail_button_by_row(self, row=1):
        """点击详情按钮"""
        detail_button_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]" \
                                         "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                                + "]/td[" + self.__get_table_column_by_name('操作') + "]//a[text()='详情']"
        self.click_element(detail_button_locator)

    def __get_table_column_by_name(self, name):
        """获取列表头的列数"""
        table_header_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]//div" \
                                        "//div[@class='ivu-table-header']//table/thead/tr/th//span"
        return str(list(map(lambda x: x.text, self.find_elements(table_header_locator))).index(name) + 1)

    def get_table_settlement_code(self):
        """获取列表所有结算单据号"""
        table_row_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]//div" \
                                     "//div[@class='ivu-table-body']//table/tbody/tr"
        row = len(self.find_elements(table_row_locator))
        settlement_code_list = []
        for r in range(row):
            settlement_code_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'settlement')]//div" \
                                               "//div[@class='ivu-table-body']//table/tbody/tr[" + str(r+1) \
                                      + "]/td[1]//p[1]"
            settlement_code_list.append(self.get_element_text(settlement_code_locator)[7:])
        return settlement_code_list
