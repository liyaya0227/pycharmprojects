#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/8/24 0024
"""

from page.webpage import WebPage
from common.readelement import Element

table = Element('jrgj/web/contractreport/table')


class ContractReportTablePage(WebPage):

    def input_contract_code_search(self, contract_code):  # 输入合同编码搜索
        self.input_text(table['合同编号搜索框'], contract_code)

    def click_search_button(self):  # 点击搜索按钮
        self.click_element(table['搜索按钮'], sleep_time=1)

    def click_reset_button(self):  # 点击重置按钮
        self.click_element(table['重置按钮'])

    def get_table_data(self):  # 获取列表所有数据
        last_page_num = self.get_element_text(table['最后页数'])
        data = []
        for _ in range(int(last_page_num)):
            table_rows = self.find_elements(table['列表行数'])
            for m in range(len(table_rows)):
                row_data = self.get_table_row_data(m+1)
                data.append(row_data)
            self.click_element(table['下一页按钮'], sleep_time=1)
        return data

    def get_table_row_data(self, row=1):
        row_data = {}
        contract_info_locator = 'xpath', \
                                "//div[@style]/div[contains(@class,'contractReport')]//table/tbody/tr[" \
                                + str(row + 1) + "]/td[" + str(self.__get_column_by_title('合同信息')) + "]"
        row_data['合同信息'] = self.get_element_text(contract_info_locator).split('\n')
        trade_type_locator = 'xpath', "//div[@style]/div[contains(@class,'contractReport')]//table/tbody/tr[" \
                             + str(row + 1) + "]/td[" + str(self.__get_column_by_title('交易类型')) + "]"
        trade_type = self.get_element_text(trade_type_locator)
        row_data['交易类型'] = trade_type
        contract_price_locator = 'xpath', \
                                 "//div[@style]/div[contains(@class,'contractReport')]//table/tbody/tr[" \
                                 + str(row + 1) + "]/td[" + str(self.__get_column_by_title('合同价格')) + "]"
        row_data['合同价格'] = self.get_element_text(contract_price_locator).replace(',', '')
        receivable_commission_locator = 'xpath', \
                                        "//div[@style]/div[contains(@class,'contractReport')]//table/tbody/tr[" \
                                        + str(row + 1) + "]/td[" + str(self.__get_column_by_title('应收佣金')) + "]"
        row_data['应收佣金'] = self.get_element_text(receivable_commission_locator).replace(',', '')
        received_commission_locator = 'xpath', \
                                      "//div[@style]/div[contains(@class,'contractReport')]//table/tbody/tr[" \
                                      + str(row + 1) + "]/td[" + str(self.__get_column_by_title('已收佣金')) + "]"
        row_data['已收佣金'] = self.get_element_text(received_commission_locator).replace(',', '')
        not_received_commission_locator = 'xpath', \
                                          "//div[@style]/div[contains(@class,'contractReport')]//table/tbody/" \
                                          "tr[" + str(row + 1) + "]/td[" \
                                          + str(self.__get_column_by_title('未收佣金')) + "]"
        row_data['未收佣金'] = self.get_element_text(not_received_commission_locator).replace(',', '')
        role_info_locator = 'xpath', \
                            "//div[@style]/div[contains(@class,'contractReport')]//table/tbody/tr[" \
                            + str(row + 1) + "]/td[" + str(self.__get_column_by_title('角色类型-占比-门店-角色人')) + "]"
        row_data['角色类型-占比-门店-角色人'] = self.get_element_text(role_info_locator).split('\n')
        achievement_money_locator = 'xpath', \
                                    "//div[@style]/div[contains(@class,'contractReport')]//table/tbody/tr[" \
                                    + str(row + 1) + "]/td[" + str(self.__get_column_by_title('业绩金额')) + "]"
        row_data['业绩金额'] = self.get_element_text(achievement_money_locator).split('\n')
        od_om_locator = 'xpath', "//div[@style]/div[contains(@class,'contractReport')]//table/tbody/tr[" \
                        + str(row + 1) + "]/td[" + str(self.__get_column_by_title('大区OD/小区OM')) + "]"
        row_data['大区OD/小区OM'] = self.get_element_text(od_om_locator).split('\n')
        return row_data

    def __get_column_by_title(self, title):  # 根据列表头获取index
        title_list = self.find_elements(table['列表头'])
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele) + 1
