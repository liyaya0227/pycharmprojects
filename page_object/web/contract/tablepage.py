#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/7/2 0002
"""

from utils.sqlutil import update_sql
from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element

table = Element('web/contract/table')


class ContractTablePage(WebPage):

    def click_sale_contract_tab(self):  # 点击买卖合同列表标签
        self.is_click(table['买卖合同列表标签'])

    def click_sale_contract_examine_tab(self):  # 点击签前审核列表标签
        self.is_click(table['签前审核列表标签'])

    def click_rent_contract_tab(self):  # 点击租赁合同列表标签
        self.is_click(table['租赁合同列表标签'])

    def click_rent_contract_examine_tab(self):  # 点击租赁合同审核列表标签
        self.is_click(table['租赁合同审核列表标签'])

    def click_create_order_button(self):  # 点击创建订单按钮
        self.is_click(table['创建订单按钮'])

    def click_wait_examine(self):  # 点击待审核标签
        self.is_click(table['待审核标签'])

    def click_had_examine(self):  # 点击已处理标签
        self.is_click(table['已处理标签'])

    def input_contract_code_search(self, contract_code):  # 输入合同编号搜索框
        self.input_text(table['合同编号搜索框'], contract_code)

    def input_house_code_search(self, house_code):  # 输入房源编号搜索框
        self.input_text(table['房源编号搜索框'], house_code)

    def input_customer_code_search(self, customer_code):  # 输入客源编号搜索框
        self.input_text(table['客源编号搜索框'], customer_code)

    def click_reset_button(self):  # 点击重置按钮
        self.is_click(table['重置按钮'])

    def click_search_button(self):  # 点击搜索按钮
        self.is_click(table['查询按钮'], sleep_time=1)

    def delete_contract_by_row(self, row=1):  # 根据行数，点击删除合同按钮
        self.wait_page_loading_complete()
        locator = 'xpath', "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                  str(row) + "]/td[" + str(self.__get_column_by_title('操作') + 1) + "]//span[contains(text(),'删除')]"
        self.is_click(locator, sleep_time=1)

    def contract_offline_collection_by_row(self, row=1):  # 根据行数，点击线下付款按钮
        locator = 'xpath', "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                  str(row) + "]/td[" + str(self.__get_column_by_title('操作') + 1) + "]//a[text()='线下收款']"
        self.is_click(locator, sleep_time=1)

    def offline_collection_dialog_choose_payer(self, payer):  # 线下付款弹窗，选择支付方
        self.is_click(table['线下收款弹窗_请选择付款方选择框'], sleep_time=0.5)
        payer_list = self.find_elements(table['下拉框'])
        for payer_ele in payer_list:
            if payer_ele.text == payer:
                payer_ele.click()
                break

    def offline_collection_dialog_input_payer_time(self, payer_time):  # 线下付款弹窗，输入支付时间
        self.input_text(table['线下收款弹窗_支付时间输入框'], payer_time, enter=True)

    def offline_collection_dialog_input_bank_serial(self, bank_serial):  # 线下付款弹窗，输入银行流水号
        self.input_text(table['线下收款弹窗_银行流水号输入框'], bank_serial)

    def offline_collection_dialog_get_pay_money(self):  # 线下付款弹窗，获取支付金额
        return self.get_element_attribute(table['线下收款弹窗_支付金额输入框'], 'value')

    def offline_collection_dialog_get_pay_time(self):  # 线下付款弹窗，获取支付时间
        return self.get_element_attribute(table['线下收款弹窗_支付时间输入框'], 'value')

    def offline_collection_dialog_upload_bank_receipt(self, bank_receipts):  # 线下付款弹窗，上传银行回单
        for bank_receipt in bank_receipts:
            self.input_text(table['线下收款弹窗_银行回单_上传图片按钮'], bank_receipt)

    def offline_collection_dialog_get_pay_money_by_payer(self, payer):  # 线下付款弹窗，获取付款人待付金额
        locator = 'xpath', \
                  "//div[contains(@class,'payModal') and not(@style='display: none;')]//div[@class='ant-modal-body']" \
                  "//table//td[text()='" + payer + "']/parent::tr/td[3]"
        return self.element_text(locator)

    def dialog_click_confirm_button(self):  # 弹窗，点击确定按钮
        self.is_click(table['弹窗_确定按钮'], sleep_time=2)
        while self.element_is_exist(table['弹窗_确定按钮']):
            sleep(0.5)

    def dialog_click_cancel_button(self):  # 弹窗，点击取消按钮
        self.is_click(table['弹窗_取消按钮'])

    def go_contract_detail_by_row(self, row=1):  # 根据行数，进入合同详情
        locator = 'xpath', "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                  str(row) + "]/td[" + str(self.__get_column_by_title('合同编号') + 1) + "]//a"
        self.is_click(locator, sleep_time=1)

    def pass_examine_by_row(self, row=1):  # 根据行数，点击审核通过
        locator = 'xpath', "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                  str(row) + "]/td[" + str(self.__get_column_by_title('审核状态') + 1) + "]//span[text()='通过']"
        self.is_click(locator, sleep_time=1)

    def legal_examine_by_row(self, row=1):  # 根据行数，点击审核按钮（法务）
        locator = 'xpath', "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                  str(row) + "]/td[" + str(self.__get_column_by_title('审核状态') + 1) + "]//a[text()='审核']"
        self.is_click(locator)

    def get_contract_detail_by_row(self, row=1, flag='买卖'):  # 根据行数，获取合同列表各字段
        contract_detail = {}
        contract_code_locator = 'xpath', \
                                "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                                str(row) + "]/td[" + str(self.__get_column_by_title('合同编号') + 1) + "]//a"
        contract_detail['contract_code'] = self.element_text(contract_code_locator)
        house_code_locator = 'xpath', \
                             "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                             str(row) + "]/td[" + str(self.__get_column_by_title('房源编号/物业地址') + 1) + "]/a"
        contract_detail['house_code'] = self.element_text(house_code_locator)
        house_address_locator = 'xpath', \
                                "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" \
                                + str(row) + "]/td[" + str(self.__get_column_by_title('房源编号/物业地址') + 1) + "]/div"
        contract_detail['house_address'] = self.element_text(house_address_locator)
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
        contract_detail['agency_fee'] = self.element_text(agency_fee_locator).replace(',', '')
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
                                     str(row) + "]/td[" + str(self.__get_column_by_title('变更/解约') + 1) + "]"
            contract_detail['change_rescind'] = self.element_text(change_rescind_locator)

        elif flag == '租赁':
            attachment_examine_locator = 'xpath', \
                                         "//div[@style='' or not(@style)]/div[@class='sign-less']//table/tbody/tr[" + \
                                         str(row) + "]/td[" + str(self.__get_column_by_title('备件审核') + 1) + "]"
            contract_detail['attachment_examine'] = self.element_text(attachment_examine_locator)
        else:
            raise ValueError('传值错误')
        return contract_detail

    def tooltip_click_confirm_button(self):  # 提示窗，点击确定按钮
        self.is_click(table['提示_确定按钮'])

    def tooltip_click_cancel_button(self):  # 提示窗，点击取消按钮
        self.is_click(table['提示_取消按钮'])

    def get_contract_table_count(self):  # 获取合同总数
        value = self.element_text(table['合同列表总数'])
        return int(value)

    @staticmethod
    def update_agency_fee(contract_code):  # 修改数据库，佣金已支付
        sql = "update contract_order set is_all_pay='1' where contract_no='" + contract_code + "'"
        update_sql(sql)

    def __get_column_by_title(self, title):  # 根据标签获取列数
        locator = 'xpath', \
                  "//div[not(contains(@style,'display'))]/div[@class='sign-less']//table/thead//th"
        title_list = self.find_elements(locator)
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele)
