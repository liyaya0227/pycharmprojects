#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/7/8 0008
"""

from page.webpage import WebPage
from common.readelement import Element

transaction_table = Element('jrgj/web/transaction/table')


class TransactionTablePage(WebPage):

    def click_transaction_code_tab(self):
        self.is_click(transaction_table['交易编号标签'])

    def click_contract_code_tab(self):
        self.is_click(transaction_table['合同编号标签'])

    def input_search_text(self, search_value):
        self.input_text(transaction_table['搜索输入框'], search_value)

    def click_search_button(self):
        self.is_click(transaction_table['搜索按钮'])

    def go_to_transaction_detail_by_row(self, row=1):
        locator = "xpath", \
                  "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']" \
                  "//div[@class='ant-table-wrapper']//table//tbody/tr[" + str(row) + "]/td[" + \
                  str(self.__get_column_by_title('交易编号') + 1) + "]//div"
        self.is_click(locator)

    def get_table_count(self):
        locator = "xpath",\
                  "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']" \
                  "//div[@class='ant-table-wrapper']//table//tbody/tr"
        table_row = self.find_elements(locator)
        return len(table_row)

    def get_order_detail_by_row(self, row=1):
        order_detail = {}
        transaction_code_locator = "xpath",\
                                   "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']" \
                                   "//div[@class='ant-table-wrapper']//table//tbody/tr[" + str(row) + "]/td[" + \
                                   str(self.__get_column_by_title('交易编号') + 1) + "]//div"
        order_detail['transaction_code'] = self.element_text(transaction_code_locator)
        buyer_locator = "xpath",\
                        "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']" \
                        "//div[@class='ant-table-wrapper']//table//tbody/tr[" + str(row) + "]/td[" + \
                        str(self.__get_column_by_title('买方') + 1) + "]/div"
        order_detail['buyer'] = self.element_text(buyer_locator)
        seller_locator = "xpath", \
                         "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']" \
                         "//div[@class='ant-table-wrapper']//table//tbody/tr[" + str(row) + "]/td[" + \
                         str(self.__get_column_by_title('卖方') + 1) + "]/div"
        order_detail['seller'] = self.element_text(seller_locator)
        agent_locator = "xpath", \
                        "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']" \
                        "//div[@class='ant-table-wrapper']//table//tbody/tr[" + str(row) + "]/td[" + \
                        str(self.__get_column_by_title('经纪人') + 1) + "]/div"
        order_detail['agent'] = self.element_text(agent_locator)
        property_address_locator = "xpath", \
                                   "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']" \
                                   "//div[@class='ant-table-wrapper']//table//tbody/tr[" + str(row) + "]/td[" + \
                                   str(self.__get_column_by_title('物业地址') + 1) + "]/div"
        order_detail['property_address'] = self.element_text(property_address_locator)
        contract_code_locator = "xpath", \
                                "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']" \
                                "//div[@class='ant-table-wrapper']//table//tbody/tr[" + str(row) + "]/td[" + \
                                str(self.__get_column_by_title('合同编号') + 1) + "]/div"
        order_detail['contract_code'] = self.element_text(contract_code_locator)
        commission_locator = "xpath", \
                             "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']" \
                             "//div[@class='ant-table-wrapper']//table//tbody/tr[" + str(row) + "]/td[" + \
                             str(self.__get_column_by_title('佣金') + 1) + "]/div"
        order_detail['commission'] = self.element_text(commission_locator)
        return order_detail

    def __get_column_by_title(self, title):
        locator = 'xpath', \
                  "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']//table/thead//th"
        title_list = self.find_elements(locator)
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele)
