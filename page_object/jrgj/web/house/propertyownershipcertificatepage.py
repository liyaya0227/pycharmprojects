#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: propertyownershipcertificatepage.py
@time: 2021/06/23
"""

from page.webpage import WebPage
from common.readelement import Element
from utils.timeutil import sleep
from utils.uploadfile import upload_file

property_ownership_certificate = Element('jrgj/web/house/propertyownershipcertificate')


class PropertyOwnershipCertificatePage(WebPage):

    def upload_picture(self, file_path):
        for file in file_path:
            self.click_element(property_ownership_certificate['上传图片按钮'])
            upload_file(file)
            sleep(2)

    def input_contract_registration_date(self, date):
        self.click_element(property_ownership_certificate['登记日期输入框'])
        self.input_text(property_ownership_certificate['登记日期输入框'], date)
        self.send_enter_key(property_ownership_certificate['登记日期输入框'])

    def choose_is_share(self, is_share):
        self.click_element(property_ownership_certificate['是否共有输入框'], sleep_time=0.5)
        is_share_list = self.find_elements(property_ownership_certificate['是否共有下拉框'])
        for is_share_ele in is_share_list:
            if is_share_ele.text == is_share:
                is_share_ele.click()
                break

    def input_building_area(self, building_area):
        self.input_text(property_ownership_certificate['建筑面积输入框'], building_area)

    def input_room_area(self, room_area):
        self.input_text(property_ownership_certificate['套内面积输入框'], room_area)

    def input_remark(self, remark):
        self.input_text(property_ownership_certificate['备注输入框'], remark)

    def click_close_button(self):
        self.click_element(property_ownership_certificate['关闭按钮'])

    def click_submit_button(self):
        self.click_element(property_ownership_certificate['提交按钮'], sleep_time=1)
