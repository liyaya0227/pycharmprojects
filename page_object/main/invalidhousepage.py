#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: invalidhousepage.py
@time: 2021/06/22
"""

from utils.times import sleep

from page.webpage import WebPage
from common.readelement import Element

invalid_house_table = Element('main/invalidhouse')


class InvalidHousePage(WebPage):

    def click_pass_by_housecode(self, housecode):
        invalid_house_tab = self.find_element(invalid_house_table['无效房源列表'])
        invalid_housecode_list = invalid_house_tab.find_elements_by_xpath("//table/tbody/tr/td[2]/a/span")
        for invalid_housecode in invalid_housecode_list:
            if invalid_housecode.text == housecode:
                ele = invalid_house_tab.find_element_by_xpath("//table/tbody/tr[" +
                                                              str(invalid_housecode_list.index(invalid_housecode) + 1) +
                                                              "]/td[10]//a[text()='通过']")
                ele.click()
                sleep()
                break

    def click_invalid_house_confirm_button(self):
        self.is_click(invalid_house_table['弹窗_确定按钮'])
        sleep()
