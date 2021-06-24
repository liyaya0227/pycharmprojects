#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: vipserviceentrustmentagreementpage.py
@time: 2021/06/22
"""

from page.webpage import WebPage
from common.readelement import Element
from utils.times import sleep

main_upview = Element('main/mainupview')


class MainUpViewPage(WebPage):

    def clear_all_title(self):
        close_button_list = self.find_elements(main_upview['标题列表_关闭按钮'])
        for close_ele in close_button_list:
            close_ele.click()
            sleep()

    def close_title_by_name(self, name):
        locator = 'xpath', "//div[@id='scrollBar']//div[contains(@class,'tag-content') and text()='" + name + \
                  "']/ancestor::span//img[@class='tag-content-close']"
        close_ele = self.find_element(locator)
        close_ele.click()
        sleep()
