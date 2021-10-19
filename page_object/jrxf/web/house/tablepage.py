#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: tablepage.py
@time: 2021/10/14
"""
from page_object.jrxf.web.main.leftviewpage import MainLeftViewPage
from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element

house_table = Element('jrxf/web/house/table')


class HouseTablePage(WebPage):

    def click_unhandle_house_tab(self):
        self.is_click(house_table['待办楼盘菜单'])

    def click_audit_house_contract_tab(self):
        self.is_click(house_table['合同审核菜单'])

    def click_unreleased_house_tab(self):
        self.is_click(house_table['待上架楼盘菜单'])

    def click_coop_house_tab(self):
        self.is_click(house_table['合作楼盘菜单'])

    def click_uncoop_house_tab(self):
        self.is_click(house_table['非合作楼盘菜单'])

    def click_add_house_btn(self):
        self.is_click(house_table['新增楼盘按钮'])

    def serch_unhandle_house(self, house_name):
        self.input_text(house_table['楼盘名称输入框'], house_name, clear=True)
        self.is_click(house_table['搜索按钮'])
        sleep()

    def click_reset_button(self):
        self.is_click(house_table['重置按钮'])

    def get_serch_result(self):
        house_number = self.element_text(house_table['搜索结果'])
        return house_number

    def click_edit_btn(self, house_name):
        locator = 'xpath', "//span[text()='" + house_name + "']/parent::td/following-sibling::td/child::span[text()=' " \
                                                            "编辑 ']"
        self.is_click(locator)

    def click_edit_unreleased_house_btn(self, house_name):
        locator = 'xpath', "//span[text()='" + house_name + "']/parent::td/following-sibling::td/child::a/span[text()='编辑']"
        self.is_click(locator)

    def click_delete_unhandle_house_btn(self, house_name):
        locator = 'xpath', "//span[text()='" + house_name + "']/parent::td/following-sibling::td/child::span[text()=' " \
                                                            "删除 ']"
        self.is_click(locator)

    # 合同审核

    def serch_contract_audit_records(self, house_name):
        self.input_text(house_table['合同_楼盘名称输入框'], house_name)
        self.is_click(house_table['合同_搜索按钮'])

    def click_audit_contract_btn(self, house_name):
        locator = 'xpath', "//span[text()='" + house_name + "']/parent::td/following-sibling::td/child::span[text()=' " \
                                                            "审核 '] "
        self.is_click(locator)

    def audit_contract(self):
        self.is_click(house_table['审核通过按钮'])
        self.is_click(house_table['上传合同tab'])
        self.is_click(house_table['审核通过按钮'])
        self.is_click(house_table['审核确定按钮'])

    # 上架审核

    def serch_released_audit_records(self, house_name):
        self.input_text(house_table['上架_楼盘名称输入框'], house_name)
        self.is_click(house_table['上架_搜索按钮'])

    def click_audit_released_house_btn(self, house_name):
        locator = 'xpath', "//span[text()='" + house_name + "']/parent::td/following-sibling::td/child::a/span[text()='审核']"
        self.is_click(locator)

    def del_released_house(self, house_name):  # 删除合作楼盘
        locator = 'xpath', "//span[text()='" + house_name + "']/ancestor::td/following-sibling::td/child::span[text()='删除']"
        self.is_click(locator)
        self.is_click(house_table['弹窗_删除按钮'])

    def del_unhandle_house(self, house_name):  # 删除待办楼盘
        locator = 'xpath', "//span[text()='" + house_name + "']/parent::td/following-sibling::td/child::span[contains(text(),'删除')]"
        self.is_click(locator)
        self.is_click(house_table['弹窗_确定按钮'])

    def check_contract_audit_status(self):
        return self.is_exists(house_table['合同_审核状态_待审核'])

    def check_contract_approved_status(self):
        return self.is_exists(house_table['合同_审核状态_审核通过'])

    def check_release_audit_status(self):
        return self.is_exists(house_table['上架_审核状态_待维护基础信息'])

    def check_release_to_audit_status(self):
        return self.is_exists(house_table['上架_审核状态_待审核'])

    def check_release_approved_status(self):
        return self.is_exists(house_table['上架_审核状态_审核通过'])

    def get_house_number_by_name(self, house_name):
        self.input_text(house_table['楼盘名称输入框'], house_name, clear=True)
        self.is_click(house_table['搜索按钮'])
        house_number = self.element_text(house_table['搜索结果'])
        return house_number



    # def check_house_status(self, house_name):  # 验证房源是否存在,如存在删除
    #     main_left_view = MainLeftViewPage(self.driver)
    #     tab_list = [house_table['待办楼盘菜单'], house_table['合同审核菜单'], house_table['待上架楼盘菜单'], house_table['合作楼盘菜单'],
    #                 house_table['非合作楼盘菜单']]
    #     for tab in tab_list:
    #         self.is_click(tab)
    #         self.serch_unhandle_house(house_name)
    #         house_number = int(self.get_serch_result())
    #         if house_number >= 1:
    #             if tab == house_table['待办楼盘菜单']:
    #                 self.del_unhandle_house(house_name)
    #             elif tab == house_table['合作楼盘菜单']:
    #                 self.del_released_house(house_name)
    #             elif tab == house_table['合同审核菜单']:
    #                 if self.is_exists(house_table['合同_审核状态_待审核']):
    #                     main_left_view.click_house_contract_audit_label()
    #                     self.serch_contract_audit_records(house_name)
    #                     self.click_audit_contract_btn(house_name)
    #                     self.audit_contract()
    #             else:
    #                 # 上架审核
    #                 pass
    #             break


