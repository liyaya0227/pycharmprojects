#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: topviewpage.py
@time: 2021/06/22
"""
from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element

top_view = Element('jrgj/web/main/topview')


class MainTopViewPage(WebPage):

    def click_close_button(self):
        if self.element_is_exist(top_view['关闭按钮'], timeout=4):
            sleep()
            self.click_element(top_view['关闭按钮'])

    def find_notification_title(self):
        if self.element_is_exist(top_view['右上角弹窗_标题'], timeout=2):
            sleep()
            value = self.get_element_text(top_view['右上角弹窗_标题'])
            self.click_element(top_view['右上角弹窗_关闭按钮'])
            return value
        else:
            return ''

    def find_notification_content(self):
        if self.element_is_exist(top_view['右上角弹窗_内容'], timeout=15):
            sleep()
            value = self.get_element_text(top_view['右上角弹窗_内容'])
            self.click_element(top_view['右上角弹窗_关闭按钮'], 10)
            return value
        else:
            return ''

    def close_notification(self):
        if self.element_is_exist(top_view['右上角弹窗_关闭按钮'], timeout=5):
            sleep()
            self.click_element(top_view['右上角弹窗_关闭按钮'])
