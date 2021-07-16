#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@date: 2021/7/8 0008
"""

from utils.timeutil import dt_strftime
from utils.timeutil import sleep
from utils.uploadfile import upload_file
from page.webpage import WebPage
from common.readelement import Element
from selenium.common.exceptions import TimeoutException

detail = Element('achievement/detail')


class AchievementDetailPage(WebPage):

    def click_submit_button(self):
        self.is_click(detail['提交按钮'])
        sleep()

