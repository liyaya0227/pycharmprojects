#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@date: 2021/7/16 0016
"""

from page.webpage import WebPage
from common.readelement import Element
from utils.timeutil import sleep

customer_detail = Element('customer/detail')


class CustomerDetailPage(WebPage):

    def get_customer_name(self):
        return self.element_text(customer_detail['客户姓名标签'])

    def get_customer_code(self):
        code = self.element_text(customer_detail['客户编码标签'])
        return code.split('：')[1]

    def click_invalid_customer_button(self):
        self.is_click(customer_detail['无效客源按钮'])

    def choose_invalid_customer_type(self, invalid_customer_type):
        self.is_click(customer_detail['无效客源申请弹窗_无效类型选择框'])
        invalid_customer_type_list = self.find_elements(customer_detail['无效客源申请弹窗_无效类型下拉框'])
        for invalid_customer_type_ele in invalid_customer_type_list:
            if invalid_customer_type_ele.text == invalid_customer_type:
                invalid_customer_type_ele.click()
                return True
        raise ValueError('传值错误')

    def input_invalid_customer_reason(self, invalid_customer_reason):
        self.input_text(customer_detail['无效客源申请弹窗_无效原因输入框'], invalid_customer_reason)

    def click_dialog_confirm_button(self):
        self.is_click(customer_detail['无效客源申请弹窗_确定按钮'])
        sleep(2)
