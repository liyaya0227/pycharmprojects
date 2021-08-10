#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: topviewpage.py
@time: 2021/06/22
"""

from page.webpage import WebPage
from utils.timeutil import sleep
from common.readelement import Element

top_view = Element('main/topview')


class MainTopViewPage(WebPage):

    def click_close_button(self):
        if self.find_element(top_view['关闭按钮'], wait_time=4):
            self.is_click(top_view['关闭按钮'])

    def wait_close_top_view(self):
        while True:
            if self.find_element(top_view['关闭按钮'], wait_time=5):
                self.click_close_button()
                break
            else:
                sleep()

    def find_notification_title(self):
        if self.find_element(top_view['右上角弹窗_标题'], wait_time=4):
            value = self.element_text(top_view['右上角弹窗_标题'])
            self.close_notification()
            return value
        else:
            return ''

    def find_notification_content(self):
        if self.find_element(top_view['右上角弹窗_内容'], wait_time=4):
            value = self.element_text(top_view['右上角弹窗_内容'])
            self.close_notification()
            return value
        else:
            return ''

    def close_notification(self):
        if self.find_element(top_view['右上角弹窗_关闭按钮'], wait_time=4):
            self.is_click(top_view['右上角弹窗_关闭按钮'])
