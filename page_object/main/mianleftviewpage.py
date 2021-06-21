# -*- coding:utf-8 -*-
from page.webpage import WebPage
from common.readelement import Element
from utils.times import sleep

main_leftview = Element('main/mainleftview')


class MainLeftViewPage(WebPage):

    def change_role(self, role_name):
        self.is_click(main_leftview['功能按钮'])
        self.is_click(main_leftview['切换角色按钮'])
        role_list = self.find_elements(main_leftview['角色选项'])
        for role in role_list:
            if role_name in role.text:
                role.click()
                break
        self.is_click(main_leftview['切换角色弹窗_确定按钮'])
        sleep()

    def click_homepage_overview_label(self):
        self.is_click(main_leftview['首页概览标签'])

    def click_all_house_label(self):
        is_expanded = self.get_element_attribute(main_leftview['房源管理菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(main_leftview['房源管理菜单'])
        self.is_click(main_leftview['全部房源标签'])

    def click_agreement_list(self):
        is_expanded = self.get_element_attribute(main_leftview['协议应用菜单'], 'aria-expanded')
        if is_expanded == 'false':
            self.is_click(main_leftview['协议应用菜单'])
        self.is_click(main_leftview['协议列表标签'])
