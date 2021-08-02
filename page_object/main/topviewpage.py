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
        if self.find_element_with_wait_time(top_view['关闭按钮']):
            self.is_click(top_view['关闭按钮'])

    def find_notification_title(self):
        if self.find_element_with_wait_time(top_view['右上角弹窗_标题']):
            value = self.element_text(top_view['右上角弹窗_标题'])
            self.close_notification()
            return value
        else:
            return ''

    def find_notification_content(self):
        if self.find_element_with_wait_time(top_view['右上角弹窗_内容']):
            value = self.element_text(top_view['右上角弹窗_内容'])
            self.close_notification()
            return value
        else:
            return ''

    def wait_notification_content_exist(self):
        while True:
            if self.find_element_with_wait_time(top_view['右上角弹窗_内容']):
                value = self.element_text(top_view['右上角弹窗_内容'])
                self.close_notification()
                return value
            else:
                sleep()

    def close_notification(self):
        sleep()
        if self.find_element_with_wait_time(top_view['右上角弹窗_关闭按钮']):
            self.is_click(top_view['右上角弹窗_关闭按钮'])
