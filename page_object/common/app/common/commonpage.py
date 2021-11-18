#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: commonpage.py
@date: 2021/11/15 0015
"""
from utils.timeutil import sleep
from page.androidpage import AndroidPage


class AppCommonPage(AndroidPage):

    def click_previous_step_button(self):
        """返回"""
        self.back_previous_step()
        sleep(1)

    def down_swipe_for_refresh(self):
        """下拉刷新"""
        self.down_swipe()
        sleep(2)

    def open_notifications(self):
        """打开通知"""
        self.open_notification()
        sleep(4)
