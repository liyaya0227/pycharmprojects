#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/8/11 0011
"""

from page.webpage import WebPage
from common.readelement import Element

survey_table = Element('survey/table')


class SurveyTablePage(WebPage):

    def click_normal_survey_tab(self):  # 点击普通实勘标签
        self.is_click(survey_table['普通实勘标签'])

    def click_vr_survey_tab(self):  # 点击VR实勘标签
        self.is_click(survey_table['VR实勘标签'])

    def input_house_code_search(self, house_code):
        self.input_text(survey_table['房源编号搜索框'], house_code)

    def click_search_button(self):  # 点击查询按钮
        self.is_click(survey_table['查询按钮'])

    def click_reset_button(self):  # 点击重置按钮
        self.is_click(survey_table['重置按钮'])

    def click_upload_survey_button_by_row(self, row=1):  # 根据行，点击上传实勘
        column = self.__get_column_by_title('操作')
        locator = 'xpath', "//div[@style='' or not(@style)]/div[contains(@class,'surveyManagement')]//tbody" \
                           "/tr[" + str(row) + "]/td[" + str(column + 1) + "]/a[text()='上传实勘']"
        self.is_click(locator)

    def __get_column_by_title(self, title):  # 获取表格title在第几列
        locator = 'xpath', \
                  "//div[@style='' or not(@style)]/div[contains(@class,'surveyManagement')]//table/thead//th"
        title_list = self.find_elements(locator)
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele)
