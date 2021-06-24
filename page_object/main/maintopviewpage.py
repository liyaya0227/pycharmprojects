#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: vipserviceentrustmentagreementpage.py
@time: 2021/06/22
"""

from selenium.common.exceptions import TimeoutException

from page.webpage import WebPage
from common.readelement import Element
from utils.times import sleep

main_topview = Element('main/maintopview')


class MainTopViewPage(WebPage):

    def click_close_button(self):
        sleep()
        try:
            ele = self.find_element_with_wait_time(main_topview['关闭按钮'])
            ele.click()
            # self.is_click(main_topview['关闭按钮'])
        except TimeoutException:
            pass

    def find_notification_title(self):
        try:
            ele = self.find_element_with_wait_time(main_topview['右上角弹窗_标题'])
            return ele.text  # self.element_text(main_topview['右上角弹窗_标题'])
        except TimeoutException:
            return ''

    def find_notification_content(self):
        try:
            ele = self.find_element_with_wait_time(main_topview['右上角弹窗_内容'])
            return ele.text  # self.element_text(main_topview['右上角弹窗_内容'])
        except TimeoutException:
            return ''

    def close_notification(self):
        try:
            ele = self.find_element_with_wait_time(main_topview['右上角弹窗_关闭按钮'])
            ele.click()
            # self.is_click(main_topview['右上角弹窗_关闭按钮'])
        except TimeoutException:
            pass
