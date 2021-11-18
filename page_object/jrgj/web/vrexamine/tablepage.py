#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/11/17 0017
"""
from page.webpage import WebPage
from common.readelement import Element

table = Element('jrgj/web/vrexamine/table')


class VrExamineTablePage(WebPage):

    def input_survey_code_search(self, survey_code):
        """输入实勘编号搜索框"""
        self.input_text(table['实勘编号搜索框'], survey_code)

    def click_search_button(self):
        """点击搜索按钮"""
        self.click_element(table['搜索按钮'])

    def click_examine_button_by_row(self, row=1):
        """根据行，点击审核按钮"""
        locator = 'xpath', "//div[not(contains(@style,'display'))]//div[@class='vr-audit-management']//table/tbody" \
                           "/tr[" + str(row) + "]/td[" + str(self.__get_column_by_title('操作') + 1) \
                  + "]/a[contains(text(),'审核')]"
        self.click_element(locator)

    def __get_column_by_title(self, title):
        locator = 'xpath', \
                  "//div[not(contains(@style,'display'))]/div[contains(@class,'vr-audit-management')]//table/thead//th"
        title_list = self.find_elements(locator)
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele)
