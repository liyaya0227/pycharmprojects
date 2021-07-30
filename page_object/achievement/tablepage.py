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

table = Element('achievement/table')


class AchievementTablePage(WebPage):

    def click_achievement_examine_tab(self):
        self.is_click(table['业绩审核标签'])

    def click_to_submit_tab(self):
        self.is_click(table['待提交标签'])

    def click_to_examine_tab(self):
        self.is_click(table['待审核标签'])
        sleep()

    def click_pass_examine_tab(self):
        self.is_click(table['审核通过标签'])
        sleep()

    def click_reject_examine_tab(self):
        self.is_click(table['驳回标签'])

    def input_contract_code_search(self, contract_code):
        self.input_text(table['合同编号搜索框'], contract_code)

    def input_sign_start_date_search(self, sign_start_date):
        self.is_click(table['签约日期开始日期搜索框'])
        self.input_text_with_enter(table['签约日期开始日期搜索框'], sign_start_date)

    def input_sign_end_date_search(self, sign_end_date):
        self.is_click(table['签约日期结束日期搜索框'])
        self.input_text_with_enter(table['签约日期结束日期搜索框'], sign_end_date)

    def choose_business_type_search(self, business_type):
        self.is_click(table['业务类型搜索框'])
        business_type_list = self.find_elements(table['搜索下拉框'])
        for business_type_ele in business_type_list:
            if business_type_ele.text == business_type:
                business_type_ele.click()
                sleep()
                break

    def input_submit_person_search(self, submit_person):
        self.input_text(table['提交人搜索框'], submit_person)

    def click_search_button(self):
        self.is_click(table['查询按钮'])

    def click_pass_examine_button_by_row(self, row=1):
        examine_table = self.find_element(table['业绩列表'])
        contract = examine_table.find_element_by_xpath(
            "//div[@style='' or not(@style)]/div[@class='ant-row achievement']"
            "//div[@role='tabpanel' and @aria-hidden='false']//table//tbody/tr[" + str(row) + "]/td[9]/a[text()='通过']")
        contract.click()
        sleep()

    def get_achievement_table_count(self):
        examine_table = self.find_element(table['业绩列表'])
        contracts = examine_table.find_elements_by_xpath(
            "//div[@style='' or not(@style)]/div[@class='ant-row achievement']"
            "//div[@role='tabpanel' and @aria-hidden='false']//table//tbody/tr")
        if contracts[0].text == '暂无数据':
            return 0
        return len(contracts)
