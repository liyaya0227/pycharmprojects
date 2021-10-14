#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: leftviewpage.py
@time: 2021/06/22
"""

from page.webpage import WebPage
from utils.timeutil import sleep
from common.readelement import Element
from page_object.jrgj.web.main.topviewpage import MainTopViewPage

left_view = Element('jrgj/web/main/leftview')


class MainLeftViewPage(WebPage):

    def change_role(self, role_name):
        # label_name = self.element_text(left_view['角色标签'])
        # if role_name in label_name:
        #     return
        self.is_click(left_view['功能按钮'], sleep_time=0.5)
        self.is_click(left_view['切换角色按钮'], sleep_time=0.5)
        role_list = self.find_elements(left_view['角色选项'])
        for role in role_list:
            if role_name in role.text:
                # if 'ant-radio-wrapper-checked' in role.get_attribute('class'):
                #     self.is_click(left_view['切换角色弹窗_取消按钮'], sleep_time=1)
                #     return
                if not ('ant-radio-wrapper-checked' in role.get_attribute('class')):
                    role.click()
                    sleep(0.5)
                self.is_click(left_view['切换角色弹窗_确定按钮'], sleep_time=1)
                break
        main_topview = MainTopViewPage(self.driver)
        main_topview.click_close_button()

    def log_out(self):
        self.refresh()
        self.is_click(left_view['功能按钮'])
        self.is_click(left_view['退出登录按钮'], sleep_time=2)

    def click_homepage_overview_label(self):
        self.is_click(left_view['首页概览标签'], sleep_time=0.5)

    def click_shop_management_label(self):
        is_expanded = self.get_element_attribute(left_view['系统管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['系统管理菜单'], sleep_time=0.5)
        self.is_click(left_view['门店管理标签'], sleep_time=0.5)

    def click_user_management_label(self):
        is_expanded = self.get_element_attribute(left_view['系统管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['系统管理菜单'], sleep_time=0.5)
        self.is_click(left_view['用户管理标签'], sleep_time=0.5)

    def click_contract_report_label(self):
        is_expanded = self.get_element_attribute(left_view['数据报表菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['数据报表菜单'], sleep_time=0.5)
        self.is_click(left_view['合同报表标签'], sleep_time=0.5)

    def click_received_achievement_report_label(self):
        is_expanded = self.get_element_attribute(left_view['数据报表菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['数据报表菜单'], sleep_time=0.5)
        self.is_click(left_view['实收业绩报表标签'], sleep_time=0.5)

    def click_payment_flow_label(self):
        is_expanded = self.get_element_attribute(left_view['数据报表菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['数据报表菜单'], sleep_time=0.5)
        self.is_click(left_view['流水标签'], sleep_time=0.5)

    def click_all_house_label(self):
        is_expanded = self.get_element_attribute(left_view['房源管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['房源管理菜单'], sleep_time=0.5)
        self.is_click(left_view['全部房源标签'], sleep_time=0.5)

    def click_survey_management_label(self):
        is_expanded = self.get_element_attribute(left_view['房源管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['房源管理菜单'], sleep_time=0.5)
        self.is_click(left_view['实勘管理标签'], sleep_time=0.5)

    def click_data_disk_label(self):
        is_expanded = self.get_element_attribute(left_view['房源管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['房源管理菜单'], sleep_time=0.5)
        self.is_click(left_view['资料盘标签'], sleep_time=0.5)

    def click_my_customer_label(self):
        is_expanded = self.get_element_attribute(left_view['客源管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['客源管理菜单'], sleep_time=0.5)
        self.is_click(left_view['我的客户标签'], sleep_time=0.5)

    def click_new_house_operation_label(self):
        is_expanded = self.get_element_attribute(left_view['客源管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['客源管理菜单'], sleep_time=0.5)
        self.is_click(left_view['新房作业标签'], sleep_time=0.5)

    def click_contract_management_label(self):
        is_expanded = self.get_element_attribute(left_view['签约管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['签约管理菜单'], sleep_time=0.5)
        self.is_click(left_view['签约管理标签'], sleep_time=0.5)

    def click_achievement_label(self):
        is_expanded = self.get_element_attribute(left_view['签约管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['签约管理菜单'], sleep_time=0.5)
        self.is_click(left_view['业绩标签'], sleep_time=0.5)

    def click_finance_label(self):
        is_expanded = self.get_element_attribute(left_view['签约管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['签约管理菜单'], sleep_time=0.5)
        self.is_click(left_view['财务标签'], sleep_time=0.5)

    def click_shop_split_account_data_table_label(self):
        is_expanded = self.get_element_attribute(left_view['签约管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['签约管理菜单'], sleep_time=0.5)
        self.is_click(left_view['门店分账数据表标签'], sleep_time=0.5)

    def click_brand_rebate_data_table_label(self):
        is_expanded = self.get_element_attribute(left_view['签约管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['签约管理菜单'], sleep_time=0.5)
        self.is_click(left_view['品牌返佣数据表标签'], sleep_time=0.5)

    def click_brand_rebate_split_account_data_table_label(self):
        is_expanded = self.get_element_attribute(left_view['签约管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['签约管理菜单'], sleep_time=0.5)
        self.is_click(left_view['品牌返佣分账数据表标签'], sleep_time=0.5)

    def click_finance_report_label(self):
        is_expanded = self.get_element_attribute(left_view['签约管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['签约管理菜单'], sleep_time=0.5)
        self.is_click(left_view['财务报表标签'], sleep_time=0.5)

    def click_survey_department_split_account_label(self):
        is_expanded = self.get_element_attribute(left_view['签约管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['签约管理菜单'], sleep_time=0.5)
        self.is_click(left_view['实勘部业绩分账标签'], sleep_time=0.5)

    def click_on_way_order_label(self):
        is_expanded = self.get_element_attribute(left_view['交易管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['交易管理菜单'], sleep_time=0.5)
        self.is_click(left_view['在途单标签'], sleep_time=0.5)

    def click_completed_order_label(self):
        is_expanded = self.get_element_attribute(left_view['交易管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['交易管理菜单'], sleep_time=0.5)
        self.is_click(left_view['终结单标签'], sleep_time=0.5)

    def click_agreement_list_label(self):
        is_expanded = self.get_element_attribute(left_view['协议应用菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(left_view['协议应用菜单'], sleep_time=0.5)
        self.is_click(left_view['协议列表标签'], sleep_time=0.5)
