#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: leftviewpage.py
@date: 2021/10/13 0013
"""
from page.webpage import WebPage
from common.readelement import Element

left_view = Element('jrcw/web/main/leftview')


class MainLeftViewPage(WebPage):

    def click_homepage_overview_label(self):
        self.is_click(left_view['首页概览标签'], sleep_time=0.5)

    def click_user_management_label(self):
        is_expanded = self.get_element_attribute(left_view['系统管理标签'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['系统管理标签'], sleep_time=0.5)
        self.is_click(left_view['用户管理标签'], sleep_time=0.5)

    def click_role_management_label(self):
        is_expanded = self.get_element_attribute(left_view['系统管理标签'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['系统管理标签'], sleep_time=0.5)
        self.is_click(left_view['角色管理标签'], sleep_time=0.5)

    def click_menu_management_label(self):
        is_expanded = self.get_element_attribute(left_view['系统管理标签'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['系统管理标签'], sleep_time=0.5)
        self.is_click(left_view['菜单管理标签'], sleep_time=0.5)
