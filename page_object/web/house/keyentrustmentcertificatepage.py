#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: keyentrustmentcertificatepage.py
@time: 2021/06/22
"""

from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element
from utils.uploadfile import upload_file

key_entrustment_certificate = Element('web/house/keyentrustmentcertificate')


class KeyEntrustmentCertificatePage(WebPage):

    def input_agreement_number(self, agreement_number):
        self.input_text(key_entrustment_certificate['协议编号输入框'], agreement_number)

    def choose_key_type(self, key):
        self.is_click(key_entrustment_certificate['钥匙类型选择框'], sleep_time=0.5)
        key_type_list = self.find_elements(key_entrustment_certificate['钥匙类型下拉框'])
        for key_type in key_type_list:
            if key_type.text == key[0]:
                key_type.click()
                break
        self.input_text(key_entrustment_certificate['钥匙类型输入框'], key[1])

    def input_shop_space(self, shop_space):
        self.input_text(key_entrustment_certificate['存放店面输入框'], shop_space)

    def input_remark(self, remark):
        self.input_text(key_entrustment_certificate['备注说明输入框'], remark)

    def upload_picture(self, file_path):
        for file in file_path:
            self.is_click(key_entrustment_certificate['上传照片按钮'])
            upload_file(file)
            sleep(2)

    def click_close_button(self):
        self.is_click(key_entrustment_certificate['关闭按钮'])

    def click_save_button(self):
        self.is_click(key_entrustment_certificate['保存按钮'], sleep_time=1)
