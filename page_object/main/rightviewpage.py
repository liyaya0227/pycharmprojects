#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: rightviewpage.py
@time: 2021/06/22
"""

from page.webpage import WebPage
from common.readelement import Element

right_view = Element('main/rightview')


class MainRightViewPage(WebPage):

    def click_invalid_house(self):
        self.is_click(right_view['房源待办_无效房源'])

    def click_certificate_examine(self):
        self.is_click(right_view['房源待办_证件审批'])
