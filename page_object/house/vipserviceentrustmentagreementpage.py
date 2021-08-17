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
from utils.timeutil import sleep
from utils.uploadfile import upload_file

vip_service_entrustment_agreement = Element('house/vipserviceentrustmentagreement')


class VipServiceEntrustmentAgreementPage(WebPage):

    def upload_picture(self, file_path):
        for file in file_path:
            self.is_click(vip_service_entrustment_agreement['上传图片按钮'])
            upload_file(file)
            sleep(2)

    def input_entrustment_agreement_number(self, entrustment_agreement_number):
        self.input_text(vip_service_entrustment_agreement['委托协议编号输入框'], entrustment_agreement_number)

    def input_entrustment_date(self, entrustment_date):
        self.is_click(vip_service_entrustment_agreement['委托日期输入框'])
        self.input_text(vip_service_entrustment_agreement['委托日期输入框'], entrustment_date)
        self.send_enter_key(vip_service_entrustment_agreement['委托日期输入框'])

    def input_entrustment_end_date(self, entrustment_end_date):
        self.is_click(vip_service_entrustment_agreement['委托截止输入框'])
        self.input_text(vip_service_entrustment_agreement['委托截止输入框'], entrustment_end_date)
        self.send_enter_key(vip_service_entrustment_agreement['委托截止输入框'])

    def choose_entrustment_type(self, entrustment_type):
        self.is_click(vip_service_entrustment_agreement['委托类型选择框'])
        entrustment_type_list = self.find_elements(vip_service_entrustment_agreement['委托类型下拉框'])
        for entrustment_type_ele in entrustment_type_list:
            if entrustment_type_ele.text == entrustment_type:
                entrustment_type_ele.click()
                break

    def input_entrustment_price(self, entrustment_price):
        self.input_text(vip_service_entrustment_agreement['委托价格输入框'], entrustment_price)

    def input_deposit(self, deposit):
        self.input_text(vip_service_entrustment_agreement['保证金输入框'], deposit)

    def choose_payment_object(self, payment_object):
        self.is_click(vip_service_entrustment_agreement['打款对象选择框'])
        payment_object_list = self.find_elements(vip_service_entrustment_agreement['打款对象下拉框'])
        for payment_object_ele in payment_object_list:
            if payment_object_ele.text == payment_object:
                payment_object_ele.click()
                break

    def input_remark(self, remark):
        self.input_text(vip_service_entrustment_agreement['备注输入框'], remark)

    def click_close_button(self):
        self.is_click(vip_service_entrustment_agreement['关闭按钮'])

    def click_submit_button(self):
        self.is_click(vip_service_entrustment_agreement['提交按钮'])
