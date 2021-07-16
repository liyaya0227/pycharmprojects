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
        sleep()

    def click_search_button(self):
        self.is_click(table['查询按钮'])
        sleep()

    def delete_contract_by_row(self, row, flag='买卖'):
        contract_tb = self.find_element(table['合同列表'])
        if flag == '买卖':
            locator = "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row)\
                      + "]/td[11]//span[contains(text(),'删除')]"
        elif flag == '租赁':
            locator = "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row)\
                      + "]/td[10]//span[contains(text(),'删除')]"
        contract = contract_tb.find_element_by_xpath(locator)
        contract.click()
        sleep()

    def go_contract_detail_by_row(self, row=1, flag='买卖'):
        contract_tb = self.find_element(table['合同列表'])
        if flag == '买卖':
            locator = "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row)\
                      + "]/td[1]//div"
        elif flag == '租赁':
            locator = "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row)\
                      + "]/td[1]//a"
        else:
            raise ValueError('传值错误')
        contract = contract_tb.find_element_by_xpath(locator)
        contract.click()
        sleep()

    def pass_examine_by_row(self, row=1, flag='买卖'):
        contract_tb = self.find_element(table['合同列表'])
        if flag == '买卖':
            locator = "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row)\
                      + "]/td[10]//span[text()='通过']"
        elif flag == '租赁':
            locator = "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row)\
                      + "]/td[8]//span[text()='通过']"
        else:
            raise ValueError('传值错误')
        contract = contract_tb.find_element_by_xpath(locator)
        contract.click()
        sleep(2)

    def legal_examine_by_row(self, row=1):
        contract_tb = self.find_element(table['合同列表'])
        contract = contract_tb.find_element_by_xpath(
            "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row)
            + "]/td[10]//a[text()='审核']")
        contract.click()
        sleep()

    def get_contract_detail_by_row(self, row=1, flag='买卖'):
        contract_tb = self.find_element(table['合同列表'])
        contract_detail = {}
        house_code = contract_tb.find_element_by_xpath(
            "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row) + "]/td[2]/a")
        contract_detail['house_code'] = house_code.text
        customer_code = contract_tb.find_element_by_xpath(
            "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row) + "]/td[3]/a")
        contract_detail['customer_code'] = customer_code.text
        trade_type = contract_tb.find_element_by_xpath(
            "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row) + "]/td[4]")
        contract_detail['trade_type'] = trade_type.text
        contract_status = contract_tb.find_element_by_xpath(
            "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row) + "]/td[6]")
        contract_detail['contract_status'] = contract_status.text
        if flag == '买卖':
            contract_code = contract_tb.find_element_by_xpath(
                "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row) + "]/td[1]//div")
            contract_detail['contract_code'] = contract_code.text
            customer_name = contract_tb.find_element_by_xpath(
                "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row) + "]/td[3]/div")
            contract_detail['customer_name'] = customer_name.text
            pre_examine = contract_tb.find_element_by_xpath(
                "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row) + "]/td[7]")
            contract_detail['pre_examine'] = pre_examine.text
            change_rescind = contract_tb.find_element_by_xpath(
                "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row) + "]/td[8]")
            contract_detail['change_rescind'] = change_rescind.text
            agency_fee = contract_tb.find_element_by_xpath(
                "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row) + "]/td[9]/p[1]")
            contract_detail['agency_fee'] = agency_fee.text
            agency_fee_status = contract_tb.find_element_by_xpath(
                "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row) + "]/td[9]/p[2]")
            contract_detail['agency_fee_status'] = agency_fee_status.text
            achievement_status = contract_tb.find_element_by_xpath(
                "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row) + "]/td[10]")
            contract_detail['achievement_status'] = achievement_status.text
        elif flag == '租赁':
            contract_code = contract_tb.find_element_by_xpath(
                "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row) + "]/td[1]//a")
            contract_detail['contract_code'] = contract_code.text
            attachment_examine = contract_tb.find_element_by_xpath(
                "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row) + "]/td[7]")
            contract_detail['attachment_examine'] = attachment_examine.text
            agency_fee = contract_tb.find_element_by_xpath(
                "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row) + "]/td[8]/p[1]")
            contract_detail['agency_fee'] = agency_fee.text
            agency_fee_status = contract_tb.find_element_by_xpath(
                "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row) + "]/td[8]/p[2]")
            contract_detail['agency_fee_status'] = agency_fee_status.text
            achievement_status = contract_tb.find_element_by_xpath(
                "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + str(row) + "]/td[9]")
            contract_detail['achievement_status'] = achievement_status.text
        else:
            raise ValueError('传值错误')
        return contract_detail

    def click_dialog_confirm_button(self):
        self.is_click(table['弹窗_确认按钮'])
        sleep()

    def click_dialog_cancel_button(self):
        self.is_click(table['弹窗_取消按钮'])
        sleep()

    def get_contract_table_count(self):
        value = self.element_text(table['合同列表总数'])
        return int(value)

    @staticmethod
    def update_agency_fee(contract_code):
        sql = "update contract_order set is_all_pay='1' where contract_no='" + contract_code + "'"
        update_sql(sql)

