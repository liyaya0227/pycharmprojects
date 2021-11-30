#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/11/29 0029
"""
from page.webpage import WebPage
from common.readelement import Element
from utils.timeutil import sleep

table = Element('jrgj/web/nodicthousefeedback/table')


class NoDictHouseFeedbackTablePage(WebPage):

    def click_sale_tab(self):
        """点击买卖标签"""
        self.click_element(table['买卖标签'])

    def click_rent_tab(self):
        """点击租赁标签"""
        self.click_element(table['租赁标签'])

    def input_estate_name_search(self, estate_name):
        """输入楼盘名称搜索输入框"""
        self.input_text_into_element(table['楼盘名称搜索输入框'], estate_name)

    def click_search_button(self):
        """点击搜索按钮"""
        self.click_element(table['搜索按钮'])
        sleep(2)

    def click_view_detail_button_by_row(self, row: int = 1):
        """根据行， 点击查看按钮"""
        locator = 'xpath', "//div[@class='houses-dispose-management']//div[@class='ant-table']//table/tbody/tr[" \
                  + str(row) + "]/td[8]/a[text()='查看']"
        self.click_element(locator)

    def examine_dialog_click_reject_examine_button(self):
        """审核弹窗，点击审核驳回按钮"""
        self.click_element(table['审批弹窗_审批驳回按钮'])

    def reject_examine_dialog_input_reason(self, reason):
        """驳回理由弹唱，输入理由"""
        self.input_text_into_element(table['驳回弹窗_理由输入框'], reason)

    def examine_dialog_click_match_estate_dict_button(self):
        """审核弹窗，点击匹配楼盘字典按钮"""
        self.click_element(table['审批弹窗_审批驳回按钮'])

    def match_estate_dict_dialog_choose_estate_name(self, estate_name):
        """匹配楼盘字典弹窗，选择楼盘名称"""
        self.input_text_into_element(table['匹配弹窗_楼盘名称输入框'], estate_name)
        self.__drop_down_box_choose_value(estate_name)

    def match_estate_dict_dialog_choose_building_id(self, building_id):
        """匹配楼盘字典弹窗，选择栋座"""
        self.click_element(table['匹配弹窗_栋座输入框'])
        self.__drop_down_box_choose_value(building_id)

    def match_estate_dict_dialog_choose_building_cell(self, building_cell):
        """匹配楼盘字典弹窗，选择单元"""
        self.click_element(table['匹配弹窗_单元输入框'])
        self.__drop_down_box_choose_value(building_cell)

    def match_estate_dict_dialog_choose_floor(self, floor):
        """匹配楼盘字典弹窗，选择楼层"""
        self.click_element(table['匹配弹窗_楼层输入框'])
        self.__drop_down_box_choose_value(floor)

    def match_estate_dict_dialog_choose_doorplate(self, doorplate):
        """匹配楼盘字典弹窗，选择门牌"""
        self.click_element(table['匹配弹窗_门牌输入框'])
        self.__drop_down_box_choose_value(doorplate)

    def __drop_down_box_choose_value(self, value):
        """下拉框选择"""
        locator = 'xpath', "//div[contains(@class, 'ant-select-dropdown') " \
                           "and not(contains(@class, 'ant-select-dropdown-hidden'))]//div[@class='rc-virtual-list']" \
                           "//span[text()='" + value \
                  + "']/ancestor::div[contains(@class,'ant-select-item ant-select-item-option')]"
        self.click_element(locator)
        sleep(2)

    def dialog_click_know_button(self):
        """弹窗，点击知道了按钮"""
        self.click_element(table['弹窗_知道了按钮'])

    def dialog_click_cancel_button(self):
        """弹窗，点击取消按钮"""
        self.click_element(table['弹窗_取消按钮'])

    def dialog_click_confirm_button(self):
        """弹窗，点击确定按钮"""
        self.click_element(table['弹窗_确定按钮'])
