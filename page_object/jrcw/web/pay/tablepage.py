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

table = Element('jrcw/web/pay/table')


class PayTablePage(WebPage):

    def input_pay_code_search(self, pay_code):
        """输入付款单据号"""
        self.input_text(table['付款单据号搜索输入框'], pay_code)

    def input_order_code_search(self, order_code):
        """输入订单编号"""
        self.input_text(table['订单编号搜索输入框'], order_code)

    def input_pay_shop_search(self, pay_shop):
        """输入签约门店"""
        self.input_text(table['付款门店搜索输入框'], pay_shop)

    def input_create_time_search(self, create_time):
        """输入创建时间"""
        self.input_text(table['创建时间搜索输入框'], create_time)

    def input_pay_time_search(self, pay_time):
        """输入付款时间"""
        self.input_text(table['付款时间搜索输入框'], pay_time)

    def input_reconciliation_code_search(self, reconciliation_code):
        """输入对账单据号"""
        self.input_text(table['对账单据号搜索输入框'], reconciliation_code)

    def choose_pay_status_search(self, pay_status):
        """选择付款状态"""
        self.click_element(table['付款状态搜索输入框'])
        locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'paylist')]" \
                           "//label[contains(text(), '付款状态')]/parent::div//ul/li[text()='" + pay_status + "']"
        self.click_element(locator)

    def choose_city_search(self, city):
        """选择城市"""
        self.click_element(table['城市搜索输入框'])
        locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'paylist')]" \
                           "//label[contains(text(), '城市')]/parent::div//ul/li[text()='" + city + "']"
        self.click_element(locator)

    def input_pay_company_search(self, pay_company):
        """输入付款公司"""
        self.input_text(table['付款公司搜素输入框'], pay_company)

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

    def get_table_total_pending_pay_money(self):
        """获取列表总条数"""
        text = self.get_element_text(table['总计标签'])
        return re.search(r"待付款金额 (.+?)元", text).group(1)

    def get_table_data(self):
        """获取列表信息"""
        table_data = []
        table_row_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'paylist')]" \
                                     "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table/tbody/tr"
        for i in range(len(self.find_elements(table_row_locator))):
            common_locator = "//div[@class='ivu-layout']//div[contains(@class, 'paylist')]" \
                             "//div[@class='ivu-table-body']//table/tbody/tr[" + str(i+1) + "]"
            project_type_locator = 'xpath', common_locator + "/td[" + self.__get_table_column_by_name('付款单信息') \
                                   + "]//span[contains(text(),'项目类型')]/parent::p"
            pay_code_locator = 'xpath', common_locator + "/td[" + self.__get_table_column_by_name('付款单信息') \
                               + "]//span[contains(text(),'付款单据号')]/parent::p"
            reconciliation_code_locator = 'xpath', common_locator + "/td[" + self.__get_table_column_by_name('付款单信息') \
                                          + "]//span[contains(text(),'对账单据号')]/parent::p"
            pay_info = {
                'project_type_': self.get_element_text(project_type_locator)[7:],
                'project_code': self.get_element_text(pay_code_locator)[8:],
                'version': self.get_element_text(reconciliation_code_locator)[8:]
            }
            account_name_locator = 'xpath', common_locator + "/td[" + self.__get_table_column_by_name('主体信息') \
                                   + "]//span[contains(text(),'账户名称')]/parent::p"
            shop_locator = 'xpath', common_locator + "/td[" + self.__get_table_column_by_name('主体信息') \
                                   + "]//span[contains(text(),'收款门店/商户')]/parent::p"
            company_locator = 'xpath', common_locator + "/td[" + self.__get_table_column_by_name('主体信息') \
                              + "]//span[contains(text(),'收款公司')]/parent::p"
            city_locator = 'xpath', common_locator + "/td[" + self.__get_table_column_by_name('主体信息') \
                           + "]//span[contains(text(),'收款城市')]/parent::p"
            pay_operator_locator = 'xpath', common_locator + "/td[" + self.__get_table_column_by_name('主体信息') \
                                   + "]//span[contains(text(),'付款操作人')]/parent::p"
            subject_info = {
                'account_name': self.get_element_text(account_name_locator)[6:],
                'store': self.get_element_text(shop_locator)[9:],
                'company': self.get_element_text(company_locator)[6:],
                'city': self.get_element_text(city_locator)[6:],
                'pay_operator': self.get_element_text(pay_operator_locator)[7:]
            }
            payable_money_locator = 'xpath', common_locator + "/td[" + self.__get_table_column_by_name('金额') \
                                    + "]//span[contains(text(),'应付金额')]/parent::p/span[2]"
            paid_money_locator = 'xpath', common_locator + "/td[" + self.__get_table_column_by_name('金额') \
                                 + "]//span[contains(text(),'实际金额')]/parent::p/span[2]"
            money_info = {
                'payable_money': self.get_element_text(payable_money_locator)[1:].replace(',', ''),
                'paid_money': self.get_element_text(paid_money_locator)[1:].replace(',', '')
            }
            pay_type_locator = 'xpath', common_locator + "/td[" + self.__get_table_column_by_name('状态') \
                                    + "]//span[contains(text(),'付款方式')]/parent::p]"
            pay_status_locator = 'xpath', common_locator + "/td[" + self.__get_table_column_by_name('状态') \
                                 + "]//span[contains(text(),'付款状态')]/parent::p"
            status_info = {
                'pay_type': self.get_element_text(pay_type_locator)[6:],
                'pay_status': self.get_element_text(pay_status_locator)[6:]
            }
            create_time_locator = 'xpath', common_locator + "/td[" + self.__get_table_column_by_name('日期') \
                               + "]//span[contains(text(),'付款创建')]/parent::p]"
            pay_time_locator = 'xpath', common_locator + "/td[" + self.__get_table_column_by_name('日期') \
                                 + "]//span[contains(text(),'付款日期')]/parent::p"
            date_info = {
                'create_time': self.get_element_text(create_time_locator)[6:],
                'pay_time': self.get_element_text(pay_time_locator)[6:]
            }
            row_data = {
                'pay_info': pay_info,
                'subject_info': subject_info,
                'money': money_info,
                'status': status_info,
                'date': date_info
            }
            table_data.append(row_data)
        return table_data

    def click_detail_button_by_row(self, row=1):
        """点击详情按钮"""
        detail_button_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'paylist')]" \
                                         "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                                + "]/td[" + self.__get_table_column_by_name('操作') + "]//a[text()='详情']"
        self.click_element(detail_button_locator)

    def click_pay_button_by_row(self, row=1):
        """点击付款按钮"""
        detail_button_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'paylist')]" \
                                         "//div[@class='ivu-table-body']//table/tbody/tr[" + str(row) \
                                + "]/td[" + self.__get_table_column_by_name('操作') + "]//a[text()='付款']"
        self.click_element(detail_button_locator)

    def __get_table_column_by_name(self, name):
        """获取列表头的列数"""
        table_header_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'paylist')]//div" \
                                        "//div[@class='ivu-table-header']//table/thead/tr/th//span"
        return str(list(map(lambda x: x.text, self.find_elements(table_header_locator))).index(name) + 1)

    def tip_pop_click_confirm_button(self):
        self.click_element(table['弹窗提示_确定按钮'])
