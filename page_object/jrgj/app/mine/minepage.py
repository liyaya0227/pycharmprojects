#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: minepage.py
@date: 2021/8/10 0010
"""

from page.androidpage import AndroidPage
from common.readelement import Element

mine = Element('jrgj/app/mine/mine')


class AppMinePage(AndroidPage):

    def click_change_role_button(self):  # 点击切换角色按钮
        self.click_element(mine['切换角色按钮'])

    def change_role_choose_role(self, role):
        locator = 'xpath', "//*[@class='android.widget.TextView' and contains(@text,'" + role + "')]"
        self.click_element(locator)

    def change_role_click_confirm_button(self):
        self.click_element(mine['确定按钮'])

    def click_setting_center_button(self):  # 点击设置中心按钮
        self.click_element(mine['设置中心按钮'])

    def setting_center_click_log_out_button(self):  # 点击退出登录按钮
        self.click_element(mine['退出登录按钮'])

    def setting_center_click_confirm_button(self):  # 点击退出登录确认按钮
        self.click_element(mine['退出登录_确认按钮'])

    def log_out(self):  # 退出登录流程
        self.click_setting_center_button()
        self.setting_center_click_log_out_button()
        self.setting_center_click_confirm_button()

    def get_user_role(self):  # 角色标签
        return self.get_element_text(mine['角色标签'])
