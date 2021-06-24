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

original_purchase_contract_information = Element('house/originalpurchasecontractinformation')


class OriginalPurchaseContractInformationPage(WebPage):

    def input_contract_registration_date(self, date):
        self.is_click(original_purchase_contract_information['原始购房合同登记日期输入框'])
        self.input_text(original_purchase_contract_information['原始购房合同登记日期输入框'], date)
        self.send_enter_key(original_purchase_contract_information['原始购房合同登记日期输入框'])

    def input_building_area(self, building_area):
        self.input_text(original_purchase_contract_information['建筑面积输入框'], building_area)

    def input_room_area(self, room_area):
        self.input_text(original_purchase_contract_information['套内面积输入框'], room_area)

    def choose_is_share(self, is_share):
        self.is_click(original_purchase_contract_information['是否共有输入框'])
        is_share_list = self.find_elements(original_purchase_contract_information['是否共有下拉框'])
        for is_share_ele in is_share_list:
            if is_share_ele.text == is_share:
                is_share_ele.click()
                break

    def input_remark(self, remark):
        self.input_text(original_purchase_contract_information['备注输入框'], remark)

    def upload_picture(self, file_path):
        for file in file_path:
            self.is_click(original_purchase_contract_information['上传图片按钮'])
            sleep()
            upload_file(file)

    def click_close_button(self):
        self.is_click(original_purchase_contract_information['关闭按钮'])

    def click_submit_button(self):
        self.is_click(original_purchase_contract_information['提交按钮'])
