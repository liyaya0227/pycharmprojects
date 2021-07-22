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
from selenium.common.exceptions import TimeoutException

top_view = Element('main/topview')


class MainTopViewPage(WebPage):

    def click_close_button(self):
        try:
            ele = self.find_element_with_wait_time(top_view['关闭按钮'])
            ele.click()
            sleep(1)
        except TimeoutException:
            pass

    def find_notification_title(self):
        try:
            value = self.find_element_with_wait_time(top_view['右上角弹窗_标题']).text
            self.close_notification()
            return value
        except TimeoutException:
            return ''

    def find_notification_content(self):
        try:
            value = self.find_element_with_wait_time(top_view['右上角弹窗_内容']).text
            self.close_notification()
            return value
        except TimeoutException:
            return ''

    def wait_notification_content_exist(self):
        while True:
            try:
                ele = self.find_element(top_view['右上角弹窗_内容'])
                value = ele.text
                self.close_notification()
                return value
            except TimeoutException:
                sleep()

    def close_notification(self):
        try:
            sleep()
            ele = self.find_element(top_view['右上角弹窗_关闭按钮'])
            ele.click()
        except TimeoutException:
            pass
