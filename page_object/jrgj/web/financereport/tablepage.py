#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/9/1 0001
"""

from page.webpage import WebPage
from common.readelement import Element

table = Element('jrgj/web/financereport/table')


class FinanceReportTablePage(WebPage):

    def click_paid_label(self):  # 点击已支付标签
        self.click_element(table['已支付标签'], sleep_time=0.5)

    def click_not_pay_label(self):  # 点击未支付标签
        self.click_element(table['未支付标签'], sleep_time=0.5)

    def input_contract_code_search(self, contract_code):  # 输入合同编码搜索
        self.input_text(table['合同编号搜索框'], contract_code)

    def click_search_button(self):  # 点击搜索按钮
        self.click_element(table['搜索按钮'], sleep_time=1)

    def click_reset_button(self):  # 点击重置按钮
        self.click_element(table['重置按钮'])

    def get_table_data(self, flag='已支付'):  # 获取列表所有数据
        last_page_num = self.get_element_text(table['最后页数'])
        data = []
        for _ in range(int(last_page_num)):
            table_rows = self.find_elements(table['列表行数'], timeout=1)
            for m in range(len(table_rows)):
                row_data = self.get_table_row_data(m+1, flag)
                data.append(row_data)
            self.click_element(table['下一页按钮'], sleep_time=1)
        return data

    def get_table_row_data(self, row=1, flag='已支付'):  # 获取列表行数据
        row_data = {}
        contract_code_locator = 'xpath', \
                                "(//div[@class='financial-statements']/div[contains(@class,'table')]//table/tbody" \
                                "/tr[@data-row-key])[" + str(row) + "]/td[" \
                                + str(self.__get_column_by_title('合同信息')) + "]"
        row_data['合同信息'] = self.get_element_text(contract_code_locator).split('\n')
        trade_type_locator = 'xpath', \
                             "(//div[@class='financial-statements']/div[contains(@class,'table')]//table/tbody" \
                             "/tr[@data-row-key])[" + str(row) + "]/td[" \
                             + str(self.__get_column_by_title('交易类型')) + "]"
        row_data['交易类型'] = self.get_element_text(trade_type_locator)
        receivable_commission_locator = 'xpath', \
                                        "(//div[@class='financial-statements']/div[contains(@class,'table')]//table" \
                                        "/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                                        + str(self.__get_column_by_title('应收佣金')) + "]"
        row_data['应收佣金'] = self.get_element_text(receivable_commission_locator).replace(',', '')
        warrant_fee_locator = 'xpath', \
                              "(//div[@class='financial-statements']/div[contains(@class,'table')]//table/tbody" \
                              "/tr[@data-row-key])[" + str(row) + "]/td[" \
                              + str(self.__get_column_by_title('权证费')) + "]"
        row_data['权证费'] = self.get_element_text(warrant_fee_locator).replace(',', '')
        if flag == '已支付':
            paid_money_locator = 'xpath', \
                                 "(//div[@class='financial-statements']/div[contains(@class,'table')]//table/tbody" \
                                 "/tr[@data-row-key])[" + str(row) + "]/td[" \
                                 + str(self.__get_column_by_title('付款金额')) + "]"
            row_data['付款金额'] = self.get_element_text(paid_money_locator).replace(',', '')
            pay_time_locator = 'xpath', \
                               "(//div[@class='financial-statements']/div[contains(@class,'table')]//table/tbody" \
                               "/tr[@data-row-key])[" + str(row) + "]/td[" + str(self.__get_column_by_title('付款时间')) + "]"
            row_data['付款时间'] = self.get_element_text(pay_time_locator)
        settlement_month_locator = 'xpath', \
                                   "(//div[@class='financial-statements']/div[contains(@class,'table')]//table/tbody" \
                                   "/tr[@data-row-key])[" + str(row) + "]/td[" \
                                   + str(self.__get_column_by_title('结算月')) + "]"
        row_data['结算月'] = self.get_element_text(settlement_month_locator)
        role_type_locator = 'xpath', \
                            "(//div[@class='financial-statements']/div[contains(@class,'table')]//table/tbody" \
                            "/tr[@data-row-key])[" + str(row) + "]/td[" + str(self.__get_column_by_title('角色类型')) + "]"
        row_data['角色类型'] = self.get_element_text(role_type_locator).split('\n')
        proportion_locator = 'xpath', \
                             "(//div[@class='financial-statements']/div[contains(@class,'table')]//table/tbody" \
                             "/tr[@data-row-key])[" + str(row) + "]/td[" \
                             + str(self.__get_column_by_title('分配比例')) + "]"
        row_data['分配比例'] = self.get_element_text(proportion_locator).split('\n')
        if flag == '未支付':
            receivable_achievement_locator = 'xpath', \
                                             "(//div[@class='financial-statements']/div[contains(@class,'table')]" \
                                             "//table/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                                             + str(self.__get_column_by_title('应分业绩额')) + "]"
            row_data['应分业绩额'] = self.get_element_text(receivable_achievement_locator).replace(',', '').split('\n')
        elif flag == '已支付':
            achievement_locator = 'xpath', \
                                  "(//div[@class='financial-statements']/div[contains(@class,'table')]//table/tbody" \
                                  "/tr[@data-row-key])[" + str(row) + "]/td[" \
                                  + str(self.__get_column_by_title('业绩额')) + "]"
            row_data['业绩额'] = self.get_element_text(achievement_locator).replace(',', '').split('\n')
        role_name_locator = 'xpath', \
                            "(//div[@class='financial-statements']/div[contains(@class,'table')]//table/tbody" \
                            "/tr[@data-row-key])[" + str(row) + "]/td[" + str(self.__get_column_by_title('角色人')) + "]"
        row_data['角色人'] = self.get_element_text(role_name_locator).split('\n')
        role_shop_locator = 'xpath', \
                            "(//div[@class='financial-statements']/div[contains(@class,'table')]//table/tbody" \
                            "/tr[@data-row-key])[" + str(row) + "]/td[" \
                            + str(self.__get_column_by_title('角色人门店')) + "]"
        row_data['角色人门店'] = self.get_element_text(role_shop_locator).split('\n')
        role_shop_group_locator = 'xpath', \
                                  "(//div[@class='financial-statements']/div[contains(@class,'table')]//table/tbody" \
                                  "/tr[@data-row-key])[" + str(row) + "]/td[" \
                                  + str(self.__get_column_by_title('角色人店组')) + "]"
        row_data['角色人店组'] = self.get_element_text(role_shop_group_locator).split('\n')
        manager_locator = 'xpath', \
                          "(//div[@class='financial-statements']/div[contains(@class,'table')]//table/tbody" \
                          "/tr[@data-row-key])[" + str(row) + "]/td[" + str(self.__get_column_by_title('商圈经理')) + "]"
        row_data['商圈经理'] = self.get_element_text(manager_locator).split('\n')
        company_locator = 'xpath', \
                          "(//div[@class='financial-statements']/div[contains(@class,'table')]//table/tbody" \
                          "/tr[@data-row-key])[" + str(row) + "]/td[" + str(self.__get_column_by_title('加盟商')) + "]"
        row_data['加盟商'] = self.get_element_text(company_locator).split('\n')
        if flag == '已支付':
            split_account_money_locator = 'xpath', \
                                          "(//div[@class='financial-statements']/div[contains(@class,'table')]//table" \
                                          "/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                                          + str(self.__get_column_by_title('实分账')) + "]"
            row_data['实分账'] = self.get_element_text(split_account_money_locator).replace(',', '').split('\n')
        service_fee_locator = 'xpath', \
                              "(//div[@class='financial-statements']/div[contains(@class,'table')]//table/tbody" \
                              "/tr[@data-row-key])[" + str(row) + "]/td[" \
                              + str(self.__get_column_by_title('手续费')) + "]"
        row_data['手续费'] = self.get_element_text(service_fee_locator).replace(',', '').split('\n')
        if flag == '已支付':
            split_account_time_locator = 'xpath', \
                                         "(//div[@class='financial-statements']/div[contains(@class,'table')]//table" \
                                         "/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                                         + str(self.__get_column_by_title('分账时间')) + "]"
            row_data['分账时间'] = self.get_element_text(split_account_time_locator).split('\n')
            settlement_status_locator = 'xpath', \
                                        "(//div[@class='financial-statements']/div[contains(@class,'table')]//table" \
                                        "/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                                        + str(self.__get_column_by_title('结算情况')) + "]"
            row_data['结算情况'] = self.get_element_text(settlement_status_locator).split('\n')
        return row_data

    def __get_column_by_title(self, title):  # 根据列表头获取index
        title_list = self.find_elements(table['列表头'])
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele) + 1
