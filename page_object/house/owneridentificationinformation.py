#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: vipserviceentrustmentagreementpage.py
@time: 2021/06/22
"""

from page.webpage import WebPage
from common.readelement import Element
from utils.times import sleep
from utils.uploadfile import upload_file

owner_identification_information = Element('house/owneridentificationinformation')


class OwnerIdentificationInformationPage(WebPage):

    def choose_seller_type(self, seller_type):
        self.is_click(owner_identification_information['卖方类型输入框'])
        seller_type_list = self.find_elements(owner_identification_information['卖方类型下拉框'])
        for seller_type_ele in seller_type_list:
            if seller_type_ele.text == seller_type:
                seller_type_ele.click()
                break

    def choose_identity_type(self, identity_type):
        self.is_click(owner_identification_information['证件类型输入框'])
        identity_type_list = self.find_elements(owner_identification_information['证件类型下拉框'])
        for identity_type_ele in identity_type_list:
            if identity_type_ele.text == identity_type:
                identity_type_ele.click()
                break

    def upload_picture(self, file_path):
        for file in file_path:
            self.is_click(owner_identification_information['上传图片按钮'])
            sleep()
            upload_file(file)

    def choose_nationality(self, nationality):
        self.is_click(owner_identification_information['选择国籍输入框'])
        nationality_list = self.find_elements(owner_identification_information['选择国籍下拉框'])
        for nationality_ele in nationality_list:
            if nationality_ele.text == nationality:
                nationality_ele.click()
                break

    def input_owner_name(self, owner_name):
        self.input_text(owner_identification_information['业主姓名输入框'], owner_name)

    def input_valid_period_start(self, start_date):
        self.is_click(owner_identification_information['有效期限_开始日期输入框'])
        self.input_text(owner_identification_information['有效期限_开始日期输入框'], start_date)
        self.send_enter_key(owner_identification_information['有效期限_开始日期输入框'])

    def input_valid_period_end(self, end_date):
        self.is_click(owner_identification_information['有效期限_结束日期输入框'])
        self.input_text(owner_identification_information['有效期限_结束日期输入框'], end_date)
        self.send_enter_key(owner_identification_information['有效期限_结束日期输入框'])

    def input_remark(self, remark):
        self.input_text(owner_identification_information['备注输入框'], remark)

    def click_close_button(self):
        self.is_click(owner_identification_information['关闭按钮'])

    def click_submit_button(self):
        self.is_click(owner_identification_information['提交按钮'])
