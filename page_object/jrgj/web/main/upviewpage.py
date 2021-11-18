#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: upviewpage.py
@time: 2021/06/22
"""

from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element
from selenium.common.exceptions import TimeoutException

up_view = Element('jrgj/web/main/upview')


class MainUpViewPage(WebPage):

    def clear_all_title(self):
        try:
            self.browser_refresh()
            close_button_list = self.find_elements(up_view['标题列表_关闭按钮'], timeout=4)
            for close_ele in close_button_list:
                close_ele.click()
                sleep(0.5)
        except TimeoutException:
            pass

    def close_title_by_name(self, name):
        locator = 'xpath', "//div[@id='scrollBar']//div[contains(@class,'tag-content') and contains(text(),'" + \
                  name[:5] + "')]/ancestor::span//img[@class='tag-content-close']"
        self.click_element(locator)
