#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/8/30 0030
"""

from page.webpage import WebPage
from common.readelement import Element

table = Element('jrgj/web/receivedachievementreport/table')


class ReceivedAchievementReportTablePage(WebPage):

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
                                "//div[@style]/div[contains(@class,'achievementReport')]//table/tbody/tr[" \
                                + str(row + 1) + "]/td[" + str(self.__get_column_by_title('合同信息')) + "]/p"
        contract_info_list = self.find_elements(contract_info_locator)
        contract_info = []
        for contract_info_ele in contract_info_list:
            contract_info.append(contract_info_ele.text)
        row_data['合同信息'] = contract_info
        trade_type_locator = 'xpath', "//div[@style]/div[contains(@class,'achievementReport')]//table/tbody/tr[" \
                             + str(row + 1) + "]/td[" + str(self.__get_column_by_title('交易类型')) + "]"
        row_data['交易类型'] = self.get_element_text(trade_type_locator)
        pay_price_locator = 'xpath', \
                            "//div[@style]/div[contains(@class,'achievementReport')]//table/tbody/tr[" \
                            + str(row + 1) + "]/td[" + str(self.__get_column_by_title('付款金额')) + "]"
        row_data['付款金额'] = self.get_element_text(pay_price_locator).replace(',', '')
        pay_time_locator = 'xpath', \
                           "//div[@style]/div[contains(@class,'achievementReport')]//table/tbody/tr[" \
                           + str(row + 1) + "]/td[" + str(self.__get_column_by_title('付款时间')) + "]"
        row_data['付款时间'] = self.get_element_text(pay_time_locator)
        role_name_locator = 'xpath', \
                            "//div[@style]/div[contains(@class,'achievementReport')]//table/tbody/tr[" \
                            + str(row + 1) + "]/td[" + str(self.__get_column_by_title('角色人')) + "]"
        row_data['角色人'] = self.get_element_text(role_name_locator)
        received_achievement_locator = 'xpath', \
                                       "//div[@style]/div[contains(@class,'achievementReport')]//table/tbody/" \
                                       "tr[" + str(row + 1) + "]/td[" + str(self.__get_column_by_title('实收业绩')) + "]"
        row_data['实收业绩'] = self.get_element_text(received_achievement_locator).replace(',', '')
        role_type_locator = 'xpath', \
                            "//div[@style]/div[contains(@class,'achievementReport')]//table/tbody/tr[" \
                            + str(row + 1) + "]/td[" + str(self.__get_column_by_title('角色类型')) + "]"
        row_data['角色类型'] = self.get_element_text(role_type_locator)
        achievement_proportion_locator = 'xpath', \
                                         "//div[@style]/div[contains(@class,'achievementReport')]//table/tbody/tr[" \
                                         + str(row + 1) + "]/td[" + str(self.__get_column_by_title('业绩比例')) + "]"
        row_data['业绩比例'] = self.get_element_text(achievement_proportion_locator).split('%')[0]
        split_bill_locator = 'xpath', "//div[@style]/div[contains(@class,'achievementReport')]//table/tbody/tr[" \
                             + str(row + 1) + "]/td[" + str(self.__get_column_by_title('分账时间')) + "]"
        row_data['分账时间'] = self.get_element_text(split_bill_locator)
        shop_and_shop_group_locator = 'xpath', \
                                      "//div[@style]/div[contains(@class,'achievementReport')]//table/tbody/tr[" \
                                      + str(row + 1) + "]/td[" + str(self.__get_column_by_title('门店/店组')) + "]"
        row_data['门店/店组'] = self.get_element_text(shop_and_shop_group_locator)
        region_and_district_locator = 'xpath', \
                                      "//div[@style]/div[contains(@class,'achievementReport')]//table/tbody/tr[" \
                                      + str(row + 1) + "]/td[" + str(self.__get_column_by_title('大区/小区')) + "]"
        row_data['大区/小区'] = self.get_element_text(region_and_district_locator)
        om_locator = 'xpath', "//div[@style]/div[contains(@class,'achievementReport')]//table/tbody/tr[" \
                     + str(row + 1) + "]/td[" + str(self.__get_column_by_title('OM')) + "]"
        row_data['OM'] = self.get_element_text(om_locator)
        od_locator = 'xpath', "//div[@style]/div[contains(@class,'achievementReport')]//table/tbody/tr[" \
                     + str(row + 1) + "]/td[" + str(self.__get_column_by_title('OD')) + "]"
        row_data['OD'] = self.get_element_text(od_locator)
        split_bill_status_locator = 'xpath', \
                                    "//div[@style]/div[contains(@class,'achievementReport')]//table/tbody/tr[" \
                                    + str(row + 1) + "]/td[" + str(self.__get_column_by_title('分账状态')) + "]"
        row_data['分账状态'] = self.get_element_text(split_bill_status_locator)
        achievement_examine_time_locator = 'xpath', \
                                           "//div[@style]/div[contains(@class,'achievementReport')]//table/tbody/tr[" \
                                           + str(row + 1) + "]/td[" + str(self.__get_column_by_title('业绩审核时间')) + "]"
        row_data['业绩审核时间'] = self.get_element_text(achievement_examine_time_locator)
        company_locator = 'xpath', "//div[@style]/div[contains(@class,'achievementReport')]//table/tbody/tr[" \
                          + str(row + 1) + "]/td[" + str(self.__get_column_by_title('公司')) + "]"
        row_data['公司'] = self.get_element_text(company_locator)
        return row_data

    def __get_column_by_title(self, title):  # 根据列表头获取index
        title_list = self.find_elements(table['列表头'])
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele) + 1
