#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: previewpage.py
@date: 2021/7/7 0007
"""

from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element

preview = Element('web/contract/preview')


class ContractPreviewPage(WebPage):

    def click_pass_button(self):
        self.is_click(preview['通过按钮'], sleep_time=2)

    def click_reject_button(self):
        self.is_click(preview['驳回按钮'])

    def click_update_button(self):
        self.is_click(preview['修改按钮'])

    def click_invalid_button(self):
        self.is_click(preview['无效按钮'])

    def click_print_without_sign_button(self):
        self.is_click(preview['无章打印按钮'], sleep_time=1)

    def click_print_with_sign_button(self):
        self.is_click(preview['有章打印按钮'], sleep_time=4)

    def click_signature_button(self):
        self.is_click(preview['签章按钮'], sleep_time=2)

    def cancel_print(self):
        self.refresh()
