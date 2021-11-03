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

table = Element('jrgj/web/finance/table')


class FinanceTablePage(WebPage):

    def click_receivable_table_tab(self):  # 点击应收列表tab
        self.click_element(table['应收列表标签'], sleep_time=0.5)

    def click_agent_achievement_table_tab(self):  # 点击应收列表tab
        self.click_element(table['经纪人业绩报表标签'], sleep_time=0.5)

    def click_split_account_data_table_tab(self):  # 点击应收列表tab
        self.click_element(table['分账数据表标签'], sleep_time=0.5)

    def input_contract_code_search(self, contract_code):  # 输入合同编码搜索
        self.input_text(table['合同编号搜索框'], contract_code)

    def clear_split_account_time(self):  # 清除分账时间
        self.click_element(table['分账时间_清除按钮'], sleep_time=0.5)

    def click_search_button(self):  # 点击搜索按钮
        self.click_element(table['查询按钮'], sleep_time=1)

    def click_reset_button(self):  # 点击重置按钮
        self.click_element(table['重置按钮'])

    def get_table_data(self, flag='应收列表'):  # 获取列表所有数据
        last_page_num = self.get_element_text(table['最后页数'])
        data = []
        for _ in range(int(last_page_num)):
            table_rows = self.find_elements(table['列表行数'])
            for m in range(len(table_rows)):
                if flag == '应收列表':
                    row_data = self.get_receivable_table_row_data(m+1)
                elif flag == '经纪人业绩报表':
                    row_data = self.get_agent_achievement_table_row_data(m+1)
                elif flag == '分账数据表':
                    row_data = self.get_split_account_data_table_row_data(m+2)
                else:
                    raise ValueError('传值错误')
                data.append(row_data)
            self.click_element(table['下一页按钮'], sleep_time=1)
        return data

    def get_receivable_table_row_data(self, row=1):  # 获取应收列表行数据
        row_data = {}
        receivable_id_locator = 'xpath', \
                                "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                                + str(row) + "]/td[" + str(self.__get_column_by_title('应收ID')) + "]"
        row_data['应收ID'] = self.get_element_text(receivable_id_locator)
        contract_code_locator = 'xpath', \
                                "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                                + str(row) + "]/td[" + str(self.__get_column_by_title('合同编号')) + "]"
        row_data['合同编号'] = self.get_element_text(contract_code_locator)
        fee_type_locator = 'xpath', \
                           "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                           + str(row) + "]/td[" + str(self.__get_column_by_title('费用类型')) + "]"
        row_data['费用类型'] = self.get_element_text(fee_type_locator)
        trade_type_locator = 'xpath', \
                             "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                             + str(row) + "]/td[" + str(self.__get_column_by_title('业务类型')) + "]"
        row_data['业务类型'] = self.get_element_text(trade_type_locator)
        sign_person_locator = 'xpath', \
                              "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                              + str(row) + "]/td[" + str(self.__get_column_by_title('签约人')) + "]"
        row_data['签约人'] = self.get_element_text(sign_person_locator)
        sign_person_shop_group_locator = 'xpath', \
                                         "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table" \
                                         "/tbody/tr[" + str(row) + "]/td[" \
                                         + str(self.__get_column_by_title('签约店组')) + "]"
        row_data['签约店组'] = self.get_element_text(sign_person_shop_group_locator)
        receivable_money_locator = 'xpath', \
                                   "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                                   + str(row) + "]/td[" + str(self.__get_column_by_title('应收款')) + "]"
        row_data['应收款'] = self.get_element_text(receivable_money_locator)
        received_money_locator = 'xpath', \
                                 "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                                 + str(row) + "]/td[" + str(self.__get_column_by_title('已收款')) + "]"
        row_data['已收款'] = self.get_element_text(received_money_locator)
        not_received_money_locator = 'xpath', \
                                     "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody" \
                                     "/tr[" + str(row) + "]/td[" + str(self.__get_column_by_title('待收款')) + "]"
        row_data['待收款'] = self.get_element_text(not_received_money_locator)
        operate_time_locator = 'xpath', \
                               "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                               + str(row) + "]/td[" + str(self.__get_column_by_title('操作时间')) + "]"
        row_data['操作时间'] = self.get_element_text(operate_time_locator)
        return row_data

    def get_agent_achievement_table_row_data(self, row=1):  # 获取经纪人业绩报表行数据
        row_data = {}
        role_name_locator = 'xpath', \
                            "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                            + str(row) + "]/td[" + str(self.__get_column_by_title('角色人')) + "]"
        row_data['角色人'] = self.get_element_text(role_name_locator)
        contract_code_locator = 'xpath', \
                                "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                                + str(row) + "]/td[" + str(self.__get_column_by_title('合同编号')) + "]"
        row_data['合同编号'] = self.get_element_text(contract_code_locator)
        trade_type_locator = 'xpath', \
                             "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                             + str(row) + "]/td[" + str(self.__get_column_by_title('业务类型')) + "]"
        row_data['业务类型'] = self.get_element_text(trade_type_locator)
        role_type_locator = 'xpath', \
                            "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                            + str(row) + "]/td[" + str(self.__get_column_by_title('角色类型')) + "]"
        row_data['角色类型'] = self.get_element_text(role_type_locator).split('\n')
        role_proportion_locator = 'xpath', \
                                  "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                                  + str(row) + "]/td[" + str(self.__get_column_by_title('角色比例')) + "]"
        row_data['角色比例'] = self.get_element_text(role_proportion_locator).split('\n')
        total_agreement_price_locator = 'xpath', \
                                        "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody" \
                                        "/tr[" + str(row) + "]/td[" + str(self.__get_column_by_title('协议总价')) + "]"
        row_data['协议总价'] = self.get_element_text(total_agreement_price_locator)
        paid_money_locator = 'xpath', \
                             "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                             + str(row) + "]/td[" + str(self.__get_column_by_title('付款金额')) + "]"
        row_data['付款金额'] = self.get_element_text(paid_money_locator)
        not_pay_money_locator = 'xpath', \
                                "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                                + str(row) + "]/td[" + str(self.__get_column_by_title('待付款金额')) + "]"
        row_data['待付款金额'] = self.get_element_text(not_pay_money_locator)
        receivable_commission_locator = 'xpath', "//div[@style='' or not(@style)]/div[contains(@class,'finance')]" \
                                                 "//table/tbody/tr[" + str(row) + "]/td[" \
                                        + str(self.__get_column_by_title('应收业绩')) + "]"
        row_data['应收业绩'] = self.get_element_text(receivable_commission_locator)
        received_commission_locator = 'xpath', \
                                      "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody" \
                                      "/tr[" + str(row) + "]/td[" + str(self.__get_column_by_title('实收业绩')) + "]"
        row_data['实收业绩'] = self.get_element_text(received_commission_locator)
        return row_data

    def get_split_account_data_table_row_data(self, row=1):  # 获取分账数据表行数据
        row_data = {}
        contract_code_locator = 'xpath', \
                                "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                                + str(row) + "]/td[" + str(self.__get_column_by_title('合同编号')) + "]"
        row_data['合同编号'] = self.get_element_text(contract_code_locator)
        contract_code_locator = 'xpath', \
                                "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                                + str(row) + "]/td[" + str(self.__get_column_by_title('实收ID')) + "]"
        row_data['实收ID'] = self.get_element_text(contract_code_locator)
        trade_type_locator = 'xpath', \
                             "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                             + str(row) + "]/td[" + str(self.__get_column_by_title('科目')) + "]"
        row_data['科目'] = self.get_element_text(trade_type_locator)
        role_type_locator = 'xpath', \
                            "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                            + str(row) + "]/td[" + str(self.__get_column_by_title('成交公司-门店')) + "]"
        row_data['成交公司-门店'] = self.get_element_text(role_type_locator)
        role_proportion_locator = 'xpath', \
                                  "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                                  + str(row) + "]/td[" + str(self.__get_column_by_title('分账公司-门店')) + "]"
        row_data['分账公司-门店'] = self.get_element_text(role_proportion_locator)
        total_agreement_price_locator = 'xpath', \
                                        "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody" \
                                        "/tr[" + str(row) + "]/td[" + str(self.__get_column_by_title('付款时间')) + "]"
        row_data['付款时间'] = self.get_element_text(total_agreement_price_locator)
        paid_money_locator = 'xpath', \
                             "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                             + str(row) + "]/td[" + str(self.__get_column_by_title('付款金额')) + "]"
        row_data['付款金额'] = self.get_element_text(paid_money_locator)
        not_pay_money_locator = 'xpath', \
                                "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody/tr[" \
                                + str(row) + "]/td[" + str(self.__get_column_by_title('应收金额')) + "]"
        row_data['应收金额'] = self.get_element_text(not_pay_money_locator)
        receivable_commission_locator = 'xpath', "//div[@style='' or not(@style)]/div[contains(@class,'finance')]" \
                                                 "//table/tbody/tr[" + str(row) + "]/td[" \
                                        + str(self.__get_column_by_title('分账金额')) + "]"
        row_data['分账金额'] = self.get_element_text(receivable_commission_locator)
        received_commission_locator = 'xpath', \
                                      "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody" \
                                      "/tr[" + str(row) + "]/td[" + str(self.__get_column_by_title('入账金额')) + "]"
        row_data['入账金额'] = self.get_element_text(received_commission_locator)
        received_commission_locator = 'xpath', \
                                      "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody" \
                                      "/tr[" + str(row) + "]/td[" + str(self.__get_column_by_title('分账时间')) + "]"
        row_data['分账时间'] = self.get_element_text(received_commission_locator).replace('\n', ' ')
        received_commission_locator = 'xpath', \
                                      "//div[@style='' or not(@style)]/div[contains(@class,'finance')]//table/tbody" \
                                      "/tr[" + str(row) + "]/td[" + str(self.__get_column_by_title('分账状态')) + "]"
        row_data['分账状态'] = self.get_element_text(received_commission_locator)
        return row_data

    def __get_column_by_title(self, title):  # 根据列表头获取index
        title_list = self.find_elements(table['列表头'])
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele) + 1
