#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: mainleftviewpage.py
@time: 2021/06/22
"""

from page.webpage import WebPage
from common.readelement import Element
from page_object.main.topviewpage import MainTopViewPage
from utils.timeutil import sleep

left_view = Element('main/leftview')


class MainLeftViewPage(WebPage):

    def change_role(self, role_name):
        label_name = self.element_text(left_view['角色标签'])
        if role_name in label_name:
            return
        self.is_click(left_view['功能按钮'])
        self.is_click(left_view['切换角色按钮'])
        role_list = self.find_elements(left_view['角色选项'])
        for role in role_list:
            if role_name in role.text:
                if 'ant-radio-wrapper-checked' in role.get_attribute('class'):
                    self.is_click(left_view['切换角色弹窗_取消按钮'])
                    break
                role.click()
                self.is_click(left_view['切换角色弹窗_确定按钮'])
                sleep(2)
                break
        if role_name in '经纪人':
            main_topview = MainTopViewPage(self.driver)
            main_topview.click_close_button()

    def click_homepage_overview_label(self):
        self.is_click(left_view['首页概览标签'])

    def click_all_house_label(self):
        is_expanded = self.get_element_attribute(left_view['房源管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['房源管理菜单'])
        self.is_click(left_view['全部房源标签'])

    def click_my_customer_label(self):
        is_expanded = self.get_element_attribute(left_view['客源管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['客源管理菜单'])
        self.is_click(left_view['我的客户标签'])

    def click_new_house_operation_label(self):
        is_expanded = self.get_element_attribute(left_view['客源管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['客源管理菜单'])
        self.is_click(left_view['新房作业标签'])

    def click_contract_management_label(self):
        is_expanded = self.get_element_attribute(left_view['签约管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['签约管理菜单'])
        self.is_click(left_view['签约管理标签'])
        sleep()

    def click_achievement_label(self):
        is_expanded = self.get_element_attribute(left_view['签约管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['签约管理菜单'])
        self.is_click(left_view['业绩标签'])

    def click_on_way_order_label(self):
        is_expanded = self.get_element_attribute(left_view['交易管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['交易管理菜单'])
        self.is_click(left_view['在途单标签'])

    def click_agreement_list(self):
        is_expanded = self.get_element_attribute(left_view['协议应用菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['协议应用菜单'])
        self.is_click(left_view['协议列表标签'])
