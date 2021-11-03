#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@date: 2021/9/1 0001
"""

from page.webpage import WebPage
from common.readelement import Element

detail = Element('jrgj/web/finance/detail')


class FinanceDetailPage(WebPage):

    def get_collection_list_table_data(self):  # 获取收款列表所有数据
        last_page_num = self.get_element_text(detail['最后页数'])
        data = []
        for _ in range(int(last_page_num)):
            table_rows = self.find_elements(detail['列表行数'], timeout=1)
            for m in range(len(table_rows)):
                row_data = self.get_table_row_data(m + 1)
                data.append(row_data)
            self.click_element(detail['下一页按钮'], sleep_time=1)
        return data

    def get_table_row_data(self, row=1):
        row_data = {}
        collection_id_locator = 'xpath', \
                                "(//div[@style='' or not(@style)]/div[contains(@class,'storeDetail')]" \
                                "//div[text()='收款列表']/parent::div//table/tbody/tr[@data-row-key])[" \
                                + str(row) + "]/td[" + str(self.__get_column_by_title('收款ID')) + "]"
        row_data['收款ID'] = self.get_element_text(collection_id_locator)
        payer_locator = 'xpath', \
                        "(//div[@style='' or not(@style)]/div[contains(@class,'storeDetail')]//div[text()='收款列表']" \
                        "/parent::div//table/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                        + str(self.__get_column_by_title('付款方')) + "]"
        row_data['付款方'] = self.get_element_text(payer_locator)
        pay_money_locator = 'xpath', \
                            "(//div[@style='' or not(@style)]/div[contains(@class,'storeDetail')]//div[text()='收款列表']" \
                            "/parent::div//table/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                            + str(self.__get_column_by_title('付款金额')) + "]"
        row_data['付款金额'] = self.get_element_text(pay_money_locator)
        submit_time_locator = 'xpath', \
                              "(//div[@style='' or not(@style)]/div[contains(@class,'storeDetail')]" \
                              "//div[text()='收款列表']/parent::div//table/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                              + str(self.__get_column_by_title('提交时间')) + "]"
        row_data['提交时间'] = self.get_element_text(submit_time_locator)
        pay_time_locator = 'xpath', \
                           "(//div[@style='' or not(@style)]/div[contains(@class,'storeDetail')]//div[text()='收款列表']" \
                           "/parent::div//table/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                           + str(self.__get_column_by_title('付款时间')) + "]"
        row_data['付款时间'] = self.get_element_text(pay_time_locator)
        split_account_money_locator = 'xpath', \
                                      "(//div[@style='' or not(@style)]/div[contains(@class,'storeDetail')]" \
                                      "//div[text()='收款列表']/parent::div//table/tbody/tr[@data-row-key])[" \
                                      + str(row) + "]/td[" + str(self.__get_column_by_title('分账金额')) + "]"
        row_data['分账金额'] = self.get_element_text(split_account_money_locator)
        split_account_detail_locator = 'xpath', \
                                       "(//div[@style='' or not(@style)]/div[contains(@class,'storeDetail')]" \
                                       "//div[text()='收款列表']/parent::div" \
                                       "//table/tbody/tr[@data-row-key])[" + str(row) + "]/td[" \
                                       + str(self.__get_column_by_title('分账明细')) + "]"
        row_data['分账明细'] = self.get_element_text(split_account_detail_locator).split('\n')
        return row_data

    def get_collection_id_in_table(self):
        last_page_num = self.get_element_text(detail['最后页数'])
        data = []
        for _ in range(int(last_page_num)):
            table_rows = self.find_elements(detail['列表行数'], timeout=1)
            for m in range(len(table_rows)):
                collection_id_locator = 'xpath', \
                                        "(//div[@style='' or not(@style)]/div[contains(@class,'storeDetail')]" \
                                        "//div[text()='收款列表']/parent::div//table/tbody/tr[@data-row-key])[" \
                                        + str(m+1) + "]/td[" + str(self.__get_column_by_title('收款ID')) + "]"
                data.append(self.get_element_text(collection_id_locator))
            self.click_element(detail['下一页按钮'], sleep_time=1)
        return data

    def __get_column_by_title(self, title):  # 根据列表头获取index
        title_list = self.find_elements(detail['列表头'])
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele) + 1
