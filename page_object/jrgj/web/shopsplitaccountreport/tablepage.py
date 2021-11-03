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

table = Element('jrgj/web/shopbranddatareport/table')


class ShopBrandDataReportTablePage(WebPage):

    def click_wait_split_account_tab(self):  # 点击待分账tab
        self.click_element(table['待分账标签'], sleep_time=0.5)

    def click_complete_split_account_tab(self):  # 点击完成分账tab
        self.click_element(table['分账完成标签'], sleep_time=0.5)

    def click_wait_rebate_commission_tab(self):  # 点击待返佣tab
        self.click_element(table['待返佣标签'], sleep_time=0.5)

    def click_complete_rebate_commission_tab(self):  # 点击完成返佣tab
        self.click_element(table['返佣完成标签'], sleep_time=0.5)

    def input_contract_code_search(self, contract_code):  # 输入合同编码搜索
        self.input_text(table['合同编号搜索框'], contract_code)

    def clear_split_account_time_search(self):  # 清空分账时间
        self.click_element(table['清空分账时间按钮'], sleep_time=0.5)

    def clear_rebate_time_search(self):  # 清空分账时间
        self.click_element(table['清空返佣时间按钮'], sleep_time=0.5)

    def clear_pay_time_search(self):  # 清空付款时间
        self.click_element(table['清空付款时间按钮'], sleep_time=0.5)

    def click_search_button(self):  # 点击搜索按钮
        self.click_element(table['查询按钮'], sleep_time=1)

    def click_reset_button(self):  # 点击重置按钮
        self.click_element(table['重置按钮'])

    def pay_money_all_table(self):  # 待分账列表所有数据打款
        locator = 'xpath', "//div[@style]/div[contains(@class,'platformStore')]//table/tbody/tr[2]/td[" \
                  + str(self.__get_column_by_title('操作')) + "]//span[text()='打款']/parent::button"
        while self.get_current_table_count() != 0:
            self.click_element(locator, sleep_time=0.5)
            self.dialog_click_confirm_split_account_button()

    def get_current_table_count(self):
        table_rows = self.find_elements(table['列表行数'], timeout=1)
        return len(table_rows)

    def dialog_click_confirm_split_account_button(self):
        self.click_element(table['弹窗_确认分账按钮'], sleep_time=1)

    def get_table_data(self, flag='分账完成'):  # 获取列表所有数据
        last_page_num = self.get_element_text(table['最后页数'])
        data = []
        for _ in range(int(last_page_num)):
            table_rows = self.find_elements(table['列表行数'], timeout=1)
            for m in range(len(table_rows)):
                if '分账' in flag:
                    row_data = self.get_split_account_table_row_data(m+1, flag)
                elif '返佣' in flag:
                    row_data = self.get_rebate_commission_table_row_data(m+1, flag)
                else:
                    raise ValueError('传值错误')
                data.append(row_data)
            self.click_element(table['下一页按钮'], sleep_time=1)
        return data

    def get_split_account_table_row_data(self, row=1, flag='分账完成'):
        row_data = {}
        contract_code_locator = 'xpath', \
                                "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table/tbody" \
                                "/tr[@data-row-key])[" + str(row) + "]/td[" \
                                + str(self.__get_column_by_title('合同编号')) + "]"
        row_data['合同编号'] = self.get_element_text(contract_code_locator)
        received_id_locator = 'xpath', \
                              "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table/tbody" \
                              "/tr[@data-row-key])[" + str(row) + "]/td[" + str(self.__get_column_by_title('实收ID')) + "]"
        row_data['实收ID'] = self.get_element_text(received_id_locator)
        fee_status_locator = 'xpath', \
                             "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table/tbody" \
                             "/tr[@data-row-key])[" + str(row) + "]/td[" + str(self.__get_column_by_title('科目')) + "]"
        row_data['科目'] = self.get_element_text(fee_status_locator)
        deal_company_shop_locator = 'xpath', \
                                    "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table/tbody" \
                                    "/tr[@data-row-key])[" + str(row) + "]/td[" \
                                    + str(self.__get_column_by_title('成交公司-门店')) + "]"
        row_data['成交公司-门店'] = self.get_element_text(deal_company_shop_locator).replace('\n', '-')
        split_account_company_shop_locator = 'xpath', \
                                             "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]" \
                                             "//table/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                                             + str(self.__get_column_by_title('分账公司-门店')) + "]"
        row_data['分账公司-门店'] = self.get_element_text(split_account_company_shop_locator).replace('\n', '-')
        pay_time_locator = 'xpath', \
                           "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table/tbody" \
                           "/tr[@data-row-key])[" + str(row) + "]/td[" + str(self.__get_column_by_title('付款时间')) + "]"
        row_data['付款时间'] = self.get_element_text(pay_time_locator).replace('\n', ' ')
        pay_money_locator = 'xpath', \
                            "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table/tbody" \
                            "/tr[@data-row-key])[" + str(row) + "]/td[" + str(self.__get_column_by_title('付款金额')) + "]"
        row_data['付款金额'] = self.get_element_text(pay_money_locator).replace(',', '')
        receivable_money_locator = 'xpath', \
                                   "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table/tbody" \
                                   "/tr[@data-row-key])[" + str(row) + "]/td[" \
                                   + str(self.__get_column_by_title('应收金额')) + "]"
        row_data['应收金额'] = self.get_element_text(receivable_money_locator).replace(',', '')
        receivable_split_money_locator = 'xpath', \
                                         "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table" \
                                         "/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                                         + str(self.__get_column_by_title('应分账金额')) + "]"
        row_data['应分账金额'] = self.get_element_text(receivable_split_money_locator).replace(',', '')
        received_split_money_locator = 'xpath', \
                                       "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table" \
                                       "/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                                       + str(self.__get_column_by_title('实分账金额')) + "]"
        row_data['实分账金额'] = self.get_element_text(received_split_money_locator).replace(',', '')
        if flag == '分账完成':
            in_account_money_locator = 'xpath', \
                                       "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table" \
                                       "/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                                       + str(self.__get_column_by_title('入账金额')) + "]"
            row_data['入账金额'] = self.get_element_text(in_account_money_locator).replace(',', '')
            split_account_time_locator = 'xpath', \
                                         "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table" \
                                         "/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                                         + str(self.__get_column_by_title('分账时间')) + "]"
            row_data['分账时间'] = self.get_element_text(split_account_time_locator)
        split_account_status_locator = 'xpath', \
                                       "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table" \
                                       "/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                                       + str(self.__get_column_by_title('分账状态')) + "]"
        row_data['分账状态'] = self.get_element_text(split_account_status_locator)
        return row_data

    def get_rebate_commission_table_row_data(self, row=1, flag='返佣完成'):
        row_data = {}
        contract_code_locator = 'xpath', \
                                "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table/tbody" \
                                "/tr[@data-row-key])[" + str(row) + "]/td[" \
                                + str(self.__get_column_by_title('合同编号')) + "]"
        row_data['合同编号'] = self.get_element_text(contract_code_locator)
        received_id_locator = 'xpath', \
                              "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table/tbody" \
                              "/tr[@data-row-key])[" + str(row) + "]/td[" \
                              + str(self.__get_column_by_title('实收ID')) + "]"
        row_data['实收ID'] = self.get_element_text(received_id_locator)
        fee_type_locator = 'xpath', \
                           "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table" \
                           "/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                           + str(self.__get_column_by_title('科目')) + "]"
        row_data['科目'] = self.get_element_text(fee_type_locator)
        deal_company_shop_locator = 'xpath', \
                                    "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table/tbody" \
                                    "/tr[@data-row-key])[" + str(row) + "]/td[" \
                                    + str(self.__get_column_by_title('成交公司-门店')) + "]"
        row_data['成交公司-门店'] = self.get_element_text(deal_company_shop_locator)
        if flag == '返佣完成':
            split_account_company_locator = 'xpath', \
                                            "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]" \
                                            "//table/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                                            + str(self.__get_column_by_title('分账公司')) + "]"
            row_data['分账公司'] = self.get_element_text(split_account_company_locator)
        elif flag == '待返佣':
            split_account_company_shop_locator = 'xpath', \
                                                 "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]" \
                                                 "//table/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                                                 + str(self.__get_column_by_title('分账公司-门店')) + "]"
            row_data['分账公司-门店'] = self.get_element_text(split_account_company_shop_locator)
        pay_time_locator = 'xpath', \
                           "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table/tbody" \
                           "/tr[@data-row-key])[" + str(row) + "]/td[" + str(self.__get_column_by_title('付款时间')) + "]"
        row_data['付款时间'] = self.get_element_text(pay_time_locator).replace('\n', ' ')
        pay_money_locator = 'xpath', \
                            "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table/tbody" \
                            "/tr[@data-row-key])[" + str(row) + "]/td[" + str(self.__get_column_by_title('付款金额')) + "]"
        row_data['付款金额'] = self.get_element_text(pay_money_locator)
        rebate_money_locator = 'xpath', \
                               "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]//table/tbody" \
                               "/tr[@data-row-key])[" + str(row) + "]/td[" \
                               + str(self.__get_column_by_title('返佣金额')) + "]"
        row_data['返佣金额'] = self.get_element_text(rebate_money_locator)
        rebate_commission_status_locator = 'xpath', \
                                           "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]" \
                                           "//table/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                                           + str(self.__get_column_by_title('返佣状态')) + "]"
        row_data['返佣状态'] = self.get_element_text(rebate_commission_status_locator)
        if flag == '返佣完成':
            rebate_in_account_money_locator = 'xpath', \
                                              "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]" \
                                              "//table/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                                              + str(self.__get_column_by_title('返佣入账金额')) + "]"
            row_data['返佣入账金额'] = self.get_element_text(rebate_in_account_money_locator)
            rebate_commission_time_locator = 'xpath', \
                                             "(//div[@style or not(@style)]/div[contains(@class,'platformStore')]" \
                                             "//table/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                                             + str(self.__get_column_by_title('返佣时间')) + "]"
            row_data['返佣时间'] = self.get_element_text(rebate_commission_time_locator)
        return row_data

    def __get_column_by_title(self, title):  # 根据列表头获取index
        title_list = self.find_elements(table['列表头'])
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele) + 1
