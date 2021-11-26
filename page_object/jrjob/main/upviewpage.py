#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: leftviewpage.py
@date: 2021/10/15 0015
"""
from page.webpage import WebPage
from common.readelement import Element

main_upview = Element('jrjob/main/upview')


class MainUpViewPage(WebPage):

    def log_out(self):
        """退出"""
        self.click_element(main_upview['欢迎标签'])
        self.click_element(main_upview['注销按钮'])
        self.click_element(main_upview['弹窗_确定按钮'])
