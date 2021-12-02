#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: add_page.py
@time: 2021/11/4
"""
from page.webpage import WebPage
from common.readelement import Element
from utils.timeutil import sleep

add_task = Element('jrxf/web/task/add')


class AddHouseTaskPage(WebPage):

    def add_report(self, house_name, house_info):
        self.input_text(add_task['楼盘信息输入框'], house_name)
        self.select_item_option(option=house_info)
        self.click_element(add_task['弹窗title'])
        self.click_element(add_task['客户联系方式输入框'])
        self.select_custom_option()
        self.click_element(add_task['预计到访时间输入框'])
        self.click_element(add_task['时间弹窗_此刻按钮'])
        self.click_element(add_task['弹窗_确定按钮'])

    def select_item_option(self, option=None):
        locator = 'xpath', "//div[@style='' or not(@style)]//div[@class='rc-virtual-list']//div[contains(@class," \
                               "'ant-select-item ant-select-item-option') and @title='" + option + "'] "
        self.click_element(locator)

    def select_custom_option(self):
        locator = 'xpath', "//div[@style='' or not(@style)]//div[@id='customId_list']/following-sibling::div[" \
                          "@class='rc-virtual-list']//div[contains(@class,'ant-select-item ant-select-item-option')] "
        options = self.find_elements(locator)
        options[0].click()

    def click_approved_btn(self):
        self.click_element(add_task['审核弹窗_通过按钮'], 1.5)

    def click_reject_btn(self):
        self.click_element(add_task['审核弹窗_驳回按钮'], 1.5)

    def reject_dialog_input_reason(self, reason):
        self.input_text_into_element(add_task['审核弹窗_驳回理由输入框'], reason)

    def save_take_look(self, picture_path):
        self.click_element(add_task['带看时间输入框'])
        self.click_element(add_task['时间弹窗_此刻按钮'])
        self.send_key(add_task['图片input'], picture_path)
        sleep(2)
        self.click_element(add_task['带看弹窗_确定按钮'], 1.5)

    def save_subscribe(self, block, block_cell, floor, room_number, building_area, money, picture_path):
        self.input_text(add_task['楼栋输入框'], block)
        self.input_text(add_task['单元输入框'], block_cell)
        self.input_text(add_task['楼层输入框'], floor)
        self.input_text(add_task['房间号输入框'], room_number)
        self.input_text(add_task['建筑面积输入框'], building_area)
        self.input_text(add_task['认购金额输入框'], money)
        self.click_element(add_task['认购日期输入框'])
        self.click_element(add_task['时间弹窗_此刻按钮'])
        self.send_key(add_task['认购书图片input'], picture_path)
        self.send_key(add_task['客户证件图片input'], picture_path)
        self.send_key(add_task['交款凭证图片input'], picture_path)
        sleep(1)
        self.click_element(add_task['弹窗_确定按钮'], 1.5)

    def audit_subscribe(self, payment, commission, company_income, deal_prize):
        self.input_text(add_task['供应商打款输入框'], payment)
        self.input_text(add_task['佣金金额输入框'], commission)
        self.input_text(add_task['公司收入输入框'], company_income)
        self.input_text(add_task['成交奖输入框'], deal_prize)
        self.click_element(add_task['审核认购弹窗_通过按钮'], 1)

    def subscribe_dialog_input_payment(self, payment):
        """认购审核弹窗，输入供应商打款"""
        self.input_text_into_element(add_task['供应商打款输入框'], payment)

    def subscribe_dialog_input_commission(self, commission):
        """认购审核弹窗，输入佣金金额"""
        self.input_text_into_element(add_task['佣金金额输入框'], commission)

    def subscribe_dialog_input_company_income(self, company_income):
        """认购审核弹窗，输入公司收入"""
        self.input_text_into_element(add_task['公司收入输入框'], company_income)

    def subscribe_dialog_input_deal_prize(self, deal_prize):
        """认购审核弹窗，输入成交奖"""
        self.input_text_into_element(add_task['成交奖输入框'], deal_prize)

    def audit_rejected_record(self):
        locator = 'xpath', "//td[text()='待审核']/following-sibling::td//a[contains(text(), '查看')] "
        ele_list = self.find_elements(locator)
        for ele in ele_list:
            sleep(1)
            ele.click()
            sleep(1)
            self.click_element(add_task['审核草网签弹窗_驳回按钮'], 1)

    def upload_sign(self, area, sign_amount):
        self.input_text(add_task['sign_建筑面积输入框'], area)
        self.click_element(add_task['草签日期输入框'])
        self.click_element(add_task['草签日期_今天选项'])
        self.input_text(add_task['草签金额输入框'], sign_amount)
        sleep(1)
        self.click_element(add_task['弹窗_确定按钮'], 1)

    def save_sell(self, picture_path):
        self.send_key(add_task['图片input'], picture_path)
        sleep(1)
        self.click_element(add_task['带看弹窗_确定按钮'], 1.5)

    def click_confirm_btn(self):
        self.click_element(add_task['带看弹窗_确定按钮'], 1)





