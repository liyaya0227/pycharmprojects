#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: table_page.py
@time: 2021/10/14
"""
from common.readconfig import ini
from common.readxml import ReadXml
from utils.databaseutil import DataBaseUtil
from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element

house_table = Element('jrxf/web/house/table')
house_sql = ReadXml("jrxf/house/house_sql")


class HouseTablePage(WebPage):

    def click_unhandle_house_tab(self):
        self.click_element(house_table['待办楼盘菜单'])

    def click_audit_house_contract_tab(self):
        self.click_element(house_table['合同审核菜单'])

    def click_unreleased_house_tab(self):
        self.click_element(house_table['待上架楼盘菜单'])

    def click_coop_house_tab(self):
        self.click_element(house_table['合作楼盘菜单'])

    def click_uncoop_house_tab(self):
        self.click_element(house_table['非合作楼盘菜单'])

    def click_add_house_btn(self):
        self.click_element(house_table['新增楼盘按钮'])

    def search_unhandle_house(self, house_name):
        self.input_text(house_table['楼盘名称输入框'], house_name, clear=True)
        self.click_element(house_table['搜索按钮'])
        sleep()

    def click_reset_button(self):
        self.click_element(house_table['重置按钮'])

    def get_search_result(self):
        house_number = self.get_element_text(house_table['搜索结果'])
        return house_number

    def click_edit_btn(self, house_name):
        locator = 'xpath', "//span[text()='" + house_name + "']/parent::td/following-sibling::td/child::span" \
                                                            "[text()=' 编辑 ']"
        self.click_element(locator)

    def click_edit_unreleased_house_btn(self, house_name):
        locator = 'xpath', "//span[text()='" + house_name + "']/parent::td/following-sibling::td/child::a/span" \
                                                            "[text()='编辑']"
        self.click_element(locator)

    def click_delete_unhandle_house_btn(self, house_name):
        locator = 'xpath', "//span[text()='" + house_name + "']/parent::td/following-sibling::td/child::span" \
                                                            "[text()=' 删除 ']"
        self.click_element(locator)

    # 合同审核

    def search_contract_audit_records(self, house_name):
        self.input_text(house_table['合同_楼盘名称输入框'], house_name)
        self.click_element(house_table['合同_搜索按钮'])

    def click_audit_contract_btn(self, house_name):
        locator = 'xpath', "//span[text()='" + house_name + "']/parent::td/following-sibling::td/child::span" \
                                                            "[text()=' 审核 '] "
        self.click_element(locator)

    def audit_contract(self):
        self.click_element(house_table['审核通过按钮'])
        self.click_element(house_table['上传合同tab'])
        self.click_element(house_table['审核通过按钮'])
        self.click_element(house_table['审核确定按钮'])

    # 上架审核

    def search_released_audit_records(self, house_name):
        self.input_text(house_table['上架_楼盘名称输入框'], house_name)
        self.click_element(house_table['上架_搜索按钮'])

    def click_audit_released_house_btn(self, house_name):
        locator = 'xpath', "//span[text()='" + house_name + "']/parent::td/following-sibling::td/child::a/span" \
                                                            "[text()='审核']"
        self.click_element(locator)

    def del_released_house(self, house_name):  # 删除合作楼盘
        locator = 'xpath', "//span[text()='" + house_name + "']/ancestor::td/following-sibling::td/child::span" \
                                                            "[text()='删除']"
        self.click_element(locator)
        self.click_element(house_table['弹窗_删除按钮'])

    def del_unhandle_house(self, house_name):  # 删除待办楼盘
        locator = 'xpath', "//span[text()='" + house_name + "']/parent::td/following-sibling::td/child::span" \
                                                            "[contains(text(),'删除')]"
        self.click_element(locator)
        self.click_element(house_table['弹窗_确定按钮'])

    def check_contract_audit_status(self, house_name):
        locator = 'xpath', "//span[text()='" + house_name + "']/parent::td/following-sibling::td/child::span" \
                                                            "[contains(text(),'待审核')]"
        # return self.is_exists(house_table['合同_审核状态_待审核'])
        return self.is_exists(locator)

    def check_contract_approved_status(self, house_name):
        locator = 'xpath', "//span[text()='" + house_name + "']/parent::td/following-sibling::td/child::span" \
                                                            "[contains(text(),'审核通过')]"
        # return self.is_exists(house_table['合同_审核状态_审核通过'])
        return self.is_exists(locator)

    def check_release_audit_status(self, house_name):
        locator = "xpath", "//span[text()='" + house_name + "']/parent::td/following-sibling::td/child::span" \
                                                            "[contains(text(),'待维护基础信息')]"
        return self.is_exists(locator)

    def check_release_to_audit_status(self, house_name):
        locator = "xpath", "//span[text()='" + house_name + "']/parent::td/following-sibling::td/child::span" \
                                                            "[contains(text(),'待审核')]"
        return self.is_exists(locator)

    def check_release_approved_status(self):
        return self.is_exists(house_table['上架_审核状态_审核通过'])

    def get_house_number_by_name(self, house_name):
        self.input_text(house_table['楼盘名称输入框'], house_name, clear=True)
        self.click_element(house_table['搜索按钮'])
        house_number = self.get_element_text(house_table['搜索结果'])
        return house_number

    def enter_house_detail(self, house_name):
        locator = "xpath", "//div[@style='' or not(@style)]/div[@class='estateManage']//" \
                           "tbody[@class='ant-table-tbody']//span[contains(text(),'" + house_name + "')] "
        self.click_element(locator)

    @staticmethod
    def get_house_info_by_db(house_name):
        database_util = DataBaseUtil('Xf My SQL', ini.xf_database_name)
        get_house_info = house_sql.get_sql('new_house', 'get_house_info').format(new_house_name=house_name)
        house_info = database_util.select_sql(get_house_info)
        if len(house_info) > 0:
            house_status = house_info[0][1]
            show_outside_status = house_info[0][2]
            house_address = house_info[0][3]
            return {"house_status": house_status, "show_outside_status": show_outside_status,
                    "house_address": house_address}
        else:
            return ''
