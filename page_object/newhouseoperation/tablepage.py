#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/7/20 0020
"""

from page.webpage import WebPage
from common.readelement import Element
from utils.timeutil import sleep
from utils.timeutil import dt_strftime
from utils.uploadfile import upload_file

new_house_operation_table = Element('newhouseoperation/table')


class NewHouseOperationTablePage(WebPage):

    def click_report_tab(self):
        self.is_click(new_house_operation_table['报备标签'])

    def click_take_look_tab(self):
        self.is_click(new_house_operation_table['带看标签'])

    def click_subscription_tab(self):
        self.is_click(new_house_operation_table['认购标签'])

    def input_building_name_search(self, building_name):
        self.input_text(new_house_operation_table['楼盘名称搜索框'], building_name)
        sleep()
        building_name_list = self.find_elements(new_house_operation_table['下拉框'])
        for building_name_ele in building_name_list:
            if building_name_ele.text == building_name:
                building_name_ele.click()
                sleep()
                return True
        raise ValueError('传值错误')

    def input_company_name_search(self, company_name):
        self.input_text(new_house_operation_table['公司名称搜索框'], company_name)

    def input_customer_phone_search(self, customer_phone):
        self.input_text(new_house_operation_table['客户手机号搜索框'], customer_phone)

    def input_store_info_search(self, store_info):
        self.input_text(new_house_operation_table['门店信息搜索框'], store_info)

    def input_group_search(self, group):
        self.input_text(new_house_operation_table['店组搜索框'], group)

    def input_user_info_search(self, user_info):
        self.input_text(new_house_operation_table['经纪人信息搜索框'], user_info)

    def input_report_time_start_search(self, report_time_start):
        self.input_text(new_house_operation_table['报备单创建时间_开始搜索框'], report_time_start)

    def input_report_time_end_search(self, report_time_end):
        self.input_text(new_house_operation_table['报备单创建时间_结束搜索框'], report_time_end)

    def input_report_code_search(self, report_code):
        self.input_text(new_house_operation_table['报备编号搜索框'], report_code)

    def choose_report_status_search(self, report_status):
        self.is_click(new_house_operation_table['报备状态搜索框'])
        report_status_list = self.find_elements(new_house_operation_table['下拉框'])
        for report_status_ele in report_status_list:
            if report_status_ele.text == report_status:
                report_status_ele.click()
                sleep()
                return True
        raise ValueError('传值错误')

    def click_search_button(self):
        self.is_click(new_house_operation_table['搜索按钮'])

    def click_add_button(self):
        self.is_click(new_house_operation_table['新增按钮'])

    def dialog_input_building_info(self, build_info):
        self.input_text_without_clear(new_house_operation_table['弹窗_楼盘信息输入框'], build_info)
        sleep()
        building_info_list = self.find_elements(new_house_operation_table['下拉框'])
        for building_info_ele in building_info_list:
            value = building_info_ele.text
            if value.split(' - ')[0] == build_info:
                building_info_ele.click()
                sleep()
                return True
        raise ValueError('传值错误')

    def dialog_input_customer_info(self, customer_info):
        self.input_text(new_house_operation_table['弹窗_客户联系方式选择框'], customer_info['customer_name'])
        sleep()
        customer_info_list = self.find_elements(new_house_operation_table['下拉框'])
        for customer_info_ele in customer_info_list:
            value = customer_info_ele.text
            if value == customer_info['customer_name'] + '-' + customer_info['customer_phone']:
                customer_info_ele.click()
                sleep()
                return True
        raise ValueError('传值错误')

    def dialog_input_expect_arrive_time(self, expect_arrive_time):
        self.is_click(new_house_operation_table['弹窗_预计到访时间输入框'])
        if expect_arrive_time == '':
            time_srf = dt_strftime('%Y-%m-%d %H:%M')
            self.input_text_with_enter(new_house_operation_table['弹窗_预计到访时间输入框'], time_srf)
        else:
            self.input_text_with_enter(new_house_operation_table['弹窗_预计到访时间输入框'], expect_arrive_time)

    def dialog_input_remark(self, remark):
        self.input_text(new_house_operation_table['弹窗_备注输入框'], remark)

    def dialog_input_take_look_time(self, take_look_time):
        self.is_click(new_house_operation_table['弹窗_带看日期输入框'])
        if take_look_time == '':
            time_srf = dt_strftime('%Y-%m-%d %H:%M')
            self.input_text_with_enter(new_house_operation_table['弹窗_带看日期输入框'], time_srf)
        else:
            self.input_text_with_enter(new_house_operation_table['弹窗_带看日期输入框'], take_look_time)

    def dialog_upload_picture(self, pictures):
        for picture in pictures:
            self.is_click(new_house_operation_table['弹窗_上传图片按钮'])
            upload_file(picture)
            sleep()

    def dialog_input_block(self, block):
        self.input_text(new_house_operation_table['弹窗_楼栋输入框'], block)

    def dialog_input_block_cell(self, block_cell):
        self.input_text(new_house_operation_table['弹窗_单元输入框'], block_cell)

    def dialog_input_floor(self, floor):
        self.input_text(new_house_operation_table['弹窗_楼层输入框'], floor)

    def dialog_input_room_number(self, room_number):
        self.input_text(new_house_operation_table['弹窗_房间号输入框'], room_number)

    def dialog_input_building_area(self, building_area):
        self.input_text(new_house_operation_table['弹窗_建筑面积输入框'], building_area)

    def dialog_input_subscribe_price(self, subscribe_price):
        self.input_text(new_house_operation_table['弹窗_认购金额输入框'], subscribe_price)

    def dialog_input_subscribe_time(self, subscribe_time):
        self.is_click(new_house_operation_table['弹窗_认购日期输入框'])
        if subscribe_time == '':
            time_srf = dt_strftime('%Y-%m-%d %H:%M')
            self.input_text_with_enter(new_house_operation_table['弹窗_认购日期输入框'], time_srf)
        else:
            self.input_text_with_enter(new_house_operation_table['弹窗_认购日期输入框'], subscribe_time)

    def dialog_upload_subscribe_form(self, subscribe_forms):
        for subscribe_form in subscribe_forms:
            self.is_click(new_house_operation_table['弹窗_认购书_上传图片按钮'])
            upload_file(subscribe_form)
            sleep()

    def dialog_upload_customer_certificate(self, customer_certificates):
        for customer_certificate in customer_certificates:
            self.is_click(new_house_operation_table['弹窗_客户证件_上传图片按钮'])
            upload_file(customer_certificate)
            sleep()

    def dialog_upload_payment_voucher(self, payment_vouchers):
        for payment_voucher in payment_vouchers:
            self.is_click(new_house_operation_table['弹窗_交款凭证_上传图片按钮'])
            upload_file(payment_voucher)
            sleep()

    def input_commission_price(self, commission_price):
        self.input_text(new_house_operation_table['弹窗_佣金金额输入框'], commission_price)

    def input_company_income(self, company_income):
        self.input_text(new_house_operation_table['弹窗_公司收入输入框'], company_income)

    def dialog_click_cancel_button(self):
        self.is_click(new_house_operation_table['弹窗_取消按钮'])

    def dialog_click_confirm_button(self):
        self.is_click(new_house_operation_table['弹窗_确定按钮'])

    def dialog_click_delete_button(self):
        self.is_click(new_house_operation_table['弹窗_删除按钮'])

    def dialog_click_examine_reject_button(self):
        self.is_click(new_house_operation_table['弹窗_审核驳回按钮'])

    def dialog_click_examine_pass_button(self):
        self.is_click(new_house_operation_table['弹窗_审核通过按钮'])

    def get_table_count(self):
        locator = 'xpath', "//div[@style='']/div[@class='new-house-management']//table/tbody/tr[not(@aria-hidden)]"
        table_list = self.find_elements(locator)
        if table_list[0].text == '暂无数据':
            return 0
        else:
            return len(table_list)

    def delete_report_by_row(self, row=1):
        locator = 'xpath', "(//div[@style='']/div[@class='new-house-management']//table/tbody/tr[not(@aria-hidden)])["\
                  + str(row) + "]/td[11]//a[text()='删除']"
        self.is_click(locator)

    def watch_report_by_row(self, row=1):
        locator = 'xpath', "(//div[@style='']/div[@class='new-house-management']//table/tbody/tr[not(@aria-hidden)])["\
                  + str(row) + "]/td[11]//a[text()='查看']"
        self.is_click(locator)

    def enter_take_look_by_row(self, row=1):
        locator = 'xpath', "(//div[@style='']/div[@class='new-house-management']//table/tbody/tr[not(@aria-hidden)])[" \
                  + str(row) + "]/td[11]//a[text()='录入带看']"
        self.is_click(locator)

    def enter_subscribe_by_row(self, row=1):
        locator = 'xpath', "(//div[@style='']/div[@class='new-house-management']//table/tbody/tr[not(@aria-hidden)])[" \
                  + str(row) + "]/td[11]//a[text()='录认购']"
        self.is_click(locator)
