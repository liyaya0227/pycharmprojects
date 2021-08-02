#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@date: 2021/7/8 0008
"""

from page.webpage import WebPage
from common.readelement import Element

detail = Element('achievement/detail')


class AchievementDetailPage(WebPage):

    def click_submit_button(self):
        self.is_click(detail['提交按钮'])

