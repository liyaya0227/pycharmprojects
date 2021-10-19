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

table = Element('jrcw/web/receipt/table')


class ReceiptTablePage(WebPage):

    def input_receipt_code_search(self, receipt_code):
        """输入收款单据号"""
        self.input_text(table['收款单据号搜索输入框'], receipt_code)

    def input_project_code_search(self, project_code):
        """输入项目单据号"""
        self.input_text(table['项目单据号搜索输入框'], project_code)

    def input_order_code_search(self, order_code):
        """输入订单编号"""
        self.input_text(table['订单编号搜索输入框'], order_code)

    def input_bank_serial_number_search(self, bank_serial_number):
        """输入订单编号"""
        self.input_text(table['银行流水号搜索输入框'], bank_serial_number)

    def choose_city_search(self, city):
        """选择城市"""
        self.is_click(table['城市搜索输入框'])
        locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                           "//label[contains(text(), '城市')]/parent::div//ul/li[text()='" + city + "']"
        self.is_click(locator)

    def choose_collection_channel_search(self, collection_channel):
        """选择收款渠道"""
        self.is_click(table['收款渠道搜索下拉框'])
        locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt ')]" \
                           "//label[contains(text(), '收款渠道')]/parent::div//ul/li[text()='" + collection_channel + "']"
        self.is_click(locator)

    def input_create_time_search(self, create_time):
        """输入创建时间"""
        self.input_text(table['创建时间搜索输入框'], create_time)

    def input_pay_time_search(self, pay_time):
        """输入支付时间"""
        self.input_text(table['支付时间搜索输入框'], pay_time)

    def click_search_button(self):
        """点击查询按钮"""
        self.is_click(table['查询按钮'])

    def click_reset_button(self):
        """点击重置按钮"""
        self.is_click(table['重置按钮'])

    def click_export_button(self):
        """点击导出按钮"""
        self.is_click(table['导出按钮'])

    def get_table_total_count(self):
        """获取列表总条数"""
        text = self.element_text(table['总计标签'])
        return re.search(r"总计(.+?)条", text).group(1)

    def get_table_total_collection_money(self):
        """获取总收款金额"""
        text = self.element_text(table['总计标签'])
        return re.search(r"总收款金额 (.+?)元", text).group(1)

    def get_table_total_pay_money(self):
        """获取总支付金额"""
        text = self.element_text(table['总计标签'])
        return re.search(r"总支付金额 (.+?)元", text).group(1)

    def __get_table_column_by_name(self, name):
        """获取列表头的列数"""
        table_header_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                                        "/div[contains(@class,'table')]//div[@class='ivu-table-header']//table" \
                                        "/thead/tr/th//span"
        return self.find_elements(table_header_locator).index(name)

    def get_table_data(self):
        """获取收款单列表信息"""
        table_data = []
        table_row_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                                     "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table/tbody/tr"
        for i in range(len(self.find_elements(table_row_locator))):
            receipt_code_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                                            "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table/tbody" \
                                            "/tr[" + str(i+1) + "]/td[" + self.__get_table_column_by_name('收款信息') \
                                   + "]//span[contains(text(),'收款单据号')]/parent::p"
            project_code_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                                            "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table/tbody" \
                                            "/tr[" + str(i+1) + "]/td[" + self.__get_table_column_by_name('收款信息') \
                                   + "]//span[contains(text(),'项目单据号')]/parent::p"
            receipt_info = {
                'receipt_code': self.element_text(receipt_code_locator)[7:],
                'project_code': self.element_text(project_code_locator)[7:]
            }
            order_code_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                                          "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table/tbody" \
                                          "/tr[" + str(i+1) + "]/td[" + self.__get_table_column_by_name('订单信息') \
                                 + "]//p[1]/a"
            business_type_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                                             "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table" \
                                             "/tbody/tr[" + str(i+1) + "]/td[" + self.__get_table_column_by_name('订单信息') \
                                    + "]//p[2]"
            product_name_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                                            "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table" \
                                            "/tbody/tr[" + str(i+1) + "]/td[" + self.__get_table_column_by_name('订单信息') \
                                   + "]//p[3]"
            fee_type_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                                        "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table/tbody" \
                                        "/tr[" + str(i+1) + "]/td[" + self.__get_table_column_by_name('订单信息') \
                               + "]//p[4]/span"
            order_info = {
                'order_code': self.element_text(order_code_locator),
                'business_type': self.element_text(business_type_locator),
                'product_name': self.element_text(product_name_locator),
                'fee_type': self.element_text(fee_type_locator)
            }
            city_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                                    "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table/tbody" \
                                    "/tr[" + str(i+1) + "]/td[" + self.__get_table_column_by_name('城市') + "]//p"
            payer_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                                     "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table/tbody" \
                                     "/tr[" + str(i+1) + "]/td[" + self.__get_table_column_by_name('付款方') + "]//span"
            collection_channel_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                                                  "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table" \
                                                  "/tbody/tr[" + str(i) + "]/td[" +\
                                         self.__get_table_column_by_name('付款方') + "]//div[not(@class)]"
            pay_money_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                                         "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table" \
                                         "/tbody/tr[" + str(i+1) + "]/td[" + self.__get_table_column_by_name('付款金额') \
                                + "]/div/div"
            collected_money_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                                               "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table" \
                                               "/tbody/tr[" + str(i+1) + "]/td[" \
                                      + self.__get_table_column_by_name('收款金额') + "]/div/div"
            service_charge_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                                              "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table" \
                                              "/tbody/tr[" + str(i+1) + "]/td[" + self.__get_table_column_by_name('手续费') \
                                     + "]/div/div"
            pay_time_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                                        "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table/tbody" \
                                        "/tr[" + str(i+1) + "]/td[" + self.__get_table_column_by_name('时间') \
                               + "]//span[contains(text(),'支付时间')]/parent::p"
            create_time_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                                           "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table/tbody" \
                                           "/tr[" + str(i+1) + "]/td[" + self.__get_table_column_by_name('时间') \
                                  + "]//span[contains(text(),'创建时间')]/parent::p"
            date_info = {
                'pay_time': self.element_text(pay_time_locator)[6:],
                'create_time': self.element_text(create_time_locator)[6:]
            }
            row_data = {
                'receipt_info': receipt_info,
                'order_info': order_info,
                'city': self.element_text(city_locator),
                'payer': self.element_text(payer_locator),
                'collection_channel': self.element_text(collection_channel_locator),
                'pay_money': self.element_text(pay_money_locator)[1:],
                'collected_money': self.element_text(collected_money_locator)[1:],
                'service_charge': self.element_text(service_charge_locator)[1:],
                'date_info': date_info
            }
            table_data.append(row_data)
        return table_data

    def click_detail_button_by_row(self, row=1):
        """点击详情按钮"""
        detail_button_locator = 'xpath', "//div[@class='ivu-layout']//div[contains(@class, 'receipt')]" \
                                         "/div[contains(@class,'table')]//div[@class='ivu-table-body']/table" \
                                         "/tbody/tr[" + str(row) + "]/td[" + self.__get_table_column_by_name('操作') \
                                + "]//a[text()='详情']"
        self.is_click(detail_button_locator)
