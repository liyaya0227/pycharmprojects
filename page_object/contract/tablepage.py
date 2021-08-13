#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/7/2 0002
"""

from utils.timeutil import sleep
from utils.sqlutil import update_sql
from page.webpage import WebPage
from common.readelement import Element

table = Element('contract/table')


class ContractTablePage(WebPage):

    def click_sale_contract_tab(self):
        self.is_click(table['买卖合同列表标签'])

    def click_sale_contract_examine_tab(self):
        self.is_click(table['签前审核列表标签'])

    def click_rent_contract_tab(self):
        self.is_click(table['租赁合同列表标签'])

    def click_rent_contract_examine_tab(self):
        self.is_click(table['租赁合同审核列表标签'])

    def click_create_order_button(self):
        self.is_click(table['创建订单按钮'])

    def click_wait_examine(self):
        self.is_click(table['待审核标签'])

    def click_had_examine(self):
        self.is_click(table['已处理标签'])

    def input_contract_code_search(self, contract_code):
        self.input_text(table['合同编号搜索框'], contract_code)

    def input_house_code_search(self, house_code):
        self.input_text(table['房源编号搜索框'], house_code)

    def input_customer_code_search(self, customer_code):
        self.input_text(table['客源编号搜索框'], customer_code)

    def click_reset_button(self):
        self.is_click(table['重置按钮'])

    def click_search_button(self):
        self.is_click(table['查询按钮'])

    def delete_contract_by_row(self, row=1):
        locator = 'xpath', "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                  str(row) + "]/td[" + str(self.__get_column_by_title('操作') + 1) + "]//span[contains(text(),'删除')]"
        self.is_click(locator)

    def go_contract_detail_by_row(self, row=1):
        locator = 'xpath', "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                  str(row) + "]/td[" + str(self.__get_column_by_title('合同编号') + 1) + "]//a"
        self.is_click(locator)

    def pass_examine_by_row(self, row=1):
        locator = 'xpath', "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                  str(row) + "]/td[" + str(self.__get_column_by_title('审核状态') + 1) + "]//span[text()='通过']"
        self.is_click(locator)
        sleep(2)

    def legal_examine_by_row(self, row=1):
        locator = 'xpath', "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                  str(row) + "]/td[" + str(self.__get_column_by_title('审核状态') + 1) + "]//a[text()='审核']"
        self.is_click(locator)

    def get_contract_detail_by_row(self, row=1, flag='买卖'):
        contract_detail = {}
        contract_code_locator = 'xpath', \
                                "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                                str(row) + "]/td[" + str(self.__get_column_by_title('合同编号') + 1) + "]//a"
        contract_detail['contract_code'] = self.element_text(contract_code_locator)
        house_code_locator = 'xpath', \
                             "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                             str(row) + "]/td[" + str(self.__get_column_by_title('房源编号/物业地址') + 1) + "]/a"
        contract_detail['house_code'] = self.element_text(house_code_locator)
        customer_code_locator = 'xpath', \
                                "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                                str(row) + "]/td[" + str(self.__get_column_by_title('客户编号/姓名') + 1) + "]/a"
        contract_detail['customer_code'] = self.element_text(customer_code_locator)
        customer_name_locator = 'xpath', \
                                "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                                str(row) + "]/td[" + str(self.__get_column_by_title('客户编号/姓名') + 1) + "]/div"
        contract_detail['customer_name'] = self.element_text(customer_name_locator)
        trade_type_locator = 'xpath', \
                             "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                             str(row) + "]/td[" + str(self.__get_column_by_title('交易类型') + 1) + "]"
        contract_detail['trade_type'] = self.element_text(trade_type_locator)
        contract_status_locator = 'xpath', \
                                  "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                                  str(row) + "]/td[" + str(self.__get_column_by_title('合同状态') + 1) + "]"
        contract_detail['contract_status'] = self.element_text(contract_status_locator)
        agency_fee_locator = 'xpath', \
                             "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                             str(row) + "]/td[" + str(self.__get_column_by_title('代理费待收款') + 1) + "]/p[1]"
        contract_detail['agency_fee'] = self.element_text(agency_fee_locator)
        agency_fee_status_locator = 'xpath', \
                                    "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                                    str(row) + "]/td[" + str(self.__get_column_by_title('代理费待收款') + 1) + "]/p[2]"
        contract_detail['agency_fee_status'] = self.element_text(agency_fee_status_locator)
        achievement_status_locator = 'xpath', \
                                     "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                                     str(row) + "]/td[" + str(self.__get_column_by_title('业绩状态') + 1) + "]"
        contract_detail['achievement_status'] = self.element_text(achievement_status_locator)
        if flag == '买卖':
            pre_examine_locator = 'xpath', \
                                  "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                                  str(row) + "]/td[" + str(self.__get_column_by_title('签前审核') + 1) + "]"
            contract_detail['pre_examine'] = self.element_text(pre_examine_locator)

            change_rescind_locator = 'xpath', \
                                     "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                                     str(row) + "]/td[" + str(self.__get_column_by_title('更变/解约') + 1) + "]"
            contract_detail['change_rescind'] = self.element_text(change_rescind_locator)

        elif flag == '租赁':
            attachment_examine_locator = 'xpath', \
                                         "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                                         str(row) + "]/td[" + str(self.__get_column_by_title('备件审核') + 1) + "]"
            contract_detail['attachment_examine'] = self.element_text(attachment_examine_locator)
        else:
            raise ValueError('传值错误')
        return contract_detail

    def click_dialog_confirm_button(self):
        self.is_click(table['弹窗_确认按钮'])

    def click_dialog_cancel_button(self):
        self.is_click(table['弹窗_取消按钮'])

    def get_contract_table_count(self):
        value = self.element_text(table['合同列表总数'])
        return int(value)

    @staticmethod
    def update_agency_fee(contract_code):
        sql = "update contract_order set is_all_pay='1' where contract_no='" + contract_code + "'"
        update_sql(sql)

    def __get_column_by_title(self, title):
        locator = 'xpath', \
                  "//div[not(contains(@style,'display'))]/div[@class='sign-less']//table/thead//th"
        title_list = self.find_elements(locator)
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele)
