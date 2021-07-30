#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/7/8 0008
"""

from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element

transaction_table = Element('transaction/table')


class TransactionTablePage(WebPage):

    def click_transaction_code_tab(self):
        self.is_click(transaction_table['交易编号标签'])
        sleep()

    def click_contract_code_tab(self):
        self.is_click(transaction_table['合同编号标签'])
        sleep()

    def input_search_text(self, search_value):
        self.input_text(transaction_table['搜索输入框'], search_value)
        sleep()

    def click_search_button(self):
        self.is_click(transaction_table['搜索按钮'])

    def go_to_transaction_detail_by_row(self, row=1):
        locator = "xpath", \
                  "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']" \
                  "//div[@class='ant-table-wrapper']//table//tbody/tr[" + str(row) + "]/td[2]//div"
        self.is_click(locator)
        sleep()

    def get_table_count(self):
        locator = "xpath",\
                  "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']" \
                  "//div[@class='ant-table-wrapper']//table//tbody/tr"
        table_row = self.find_elements(locator)
        return len(table_row)

    def get_order_detail_by_row(self, row=1):
        order_table = self.find_element(transaction_table['订单列表'])
        order_detail = {}
        transaction_code = order_table.find_element_by_xpath(
            "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']"
            "//div[@class='ant-table-wrapper']//table//tbody/tr[" + str(row) + "]/td[2]//div")
        order_detail['transaction_code'] = transaction_code.text
        buyer = order_table.find_element_by_xpath(
            "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']"
            "//div[@class='ant-table-wrapper']//table//tbody/tr[" + str(row) + "]/td[4]/div")
        order_detail['buyer'] = buyer.text
        seller = order_table.find_element_by_xpath(
            "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']"
            "//div[@class='ant-table-wrapper']//table//tbody/tr[" + str(row) + "]/td[5]/div")
        order_detail['seller'] = seller.text
        agent = order_table.find_element_by_xpath(
            "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']"
            "//div[@class='ant-table-wrapper']//table//tbody/tr[" + str(row) + "]/td[6]/div")
        order_detail['agent'] = agent.text
        property_address = order_table.find_element_by_xpath(
            "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']"
            "//div[@class='ant-table-wrapper']//table//tbody/tr[" + str(row) + "]/td[7]/div")
        order_detail['property_address'] = property_address.text
        contract_code = order_table.find_element_by_xpath(
            "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']"
            "//div[@class='ant-table-wrapper']//table//tbody/tr[" + str(row) + "]/td[2]//div")
        order_detail['contract_code'] = contract_code.text
        commission = order_table.find_element_by_xpath(
            "//div[@style='']/div[@class='onTheWay-transaction' or @class='final-transaction']"
            "//div[@class='ant-table-wrapper']//table//tbody/tr[" + str(row) + "]/td[11]//div")
        order_detail['commission'] = commission.text
        return order_detail
