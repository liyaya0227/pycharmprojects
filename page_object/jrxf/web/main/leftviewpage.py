#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: leftviewpage.py
@time: 2021/10/14
"""

from page.webpage import WebPage
from utils.timeutil import sleep
from common.readelement import Element

left_view = Element('jrxf/web/main/leftview')


class MainLeftViewPage(WebPage):

    def change_role(self, role_name):
        self.click_element(left_view['功能按钮'], sleep_time=0.5)
        self.click_element(left_view['切换角色按钮'], sleep_time=0.5)
        role_list = self.find_elements(left_view['角色选项'])
        for role in role_list:
            if role_name in role.text:
                if not ('ant-radio-wrapper-checked' in role.get_attribute('class')):
                    role.click()
                    sleep(0.5)
                self.click_element(left_view['切换角色弹窗_确定按钮'], sleep_time=1)
                break

    def log_out(self):
        self.browser_refresh()
        self.click_element(left_view['功能按钮'])
        self.click_element(left_view['退出登录按钮'], sleep_time=2)

    def click_homepage_overview_label(self):
        self.click_element(left_view['首页概览标签'], sleep_time=0.5)

    def click_house_management_label(self):
        is_expanded = self.get_element_attribute(left_view['新房管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.click_element(left_view['新房管理菜单'], sleep_time=0.5)
        self.click_element(left_view['楼盘管理标签'], sleep_time=0.5)

    def click_house_contract_audit_label(self):
        is_expanded = self.get_element_attribute(left_view['新房管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.click_element(left_view['新房管理菜单'], sleep_time=0.5)
        self.click_element(left_view['楼盘合同审核标签'], sleep_time=0.5)

    def click_house_released_audit_label(self):
        is_expanded = self.get_element_attribute(left_view['新房管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.click_element(left_view['新房管理菜单'], sleep_time=0.5)
        self.click_element(left_view['上架楼盘审核标签'], sleep_time=0.5)
