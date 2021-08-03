#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: createorderpage.py
@date: 2021/7/2 0002
"""

from common.readconfig import ini
from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element
from page_object.contract.createsaleorder_szpage import ContractCreateSaleOrderDetailSZPage
from page_object.contract.createsaleorder_kspage import ContractCreateSaleOrderDetailKSPage
from page_object.contract.createsaleorder_wxpage import ContractCreateSaleOrderDetailWXPage
from page_object.contract.createrentorderpage import ContractCreateRentOrderPage

create_order = Element('contract/createorder')


class ContractCreateOrderPage(WebPage):

    def choose_business_type(self, business_type):
        self.is_click(create_order['业务类型选择框'])
        business_type_list = self.find_elements(create_order['业务类型下拉框'])
        for business_type_ele in business_type_list:
            if business_type in business_type_ele.text:
                business_type_ele.click()
                sleep()
                break

    def input_house_code(self, house_code):
        self.input_text(create_order['房源编号输入框'], house_code)

    def click_get_house_info_button(self):
        self.is_click(create_order['获取房源信息按钮'])

    def verify_house_info(self, house_info):
        verify_first_label = self.element_text(create_order['校验一标签'])
        verify_second_label = self.element_text(create_order['校验二标签'])
        verify_third_label = self.element_text(create_order['校验三标签'])
        verify_four_label = self.element_text(create_order['校验四标签'])
        labels = [verify_first_label, verify_second_label, verify_third_label, verify_four_label]
        flag = ['一', '二', '三', '四']
        for label in labels:
            self.is_click(create_order['校验' + flag[labels.index(label)] + '输入框'])
            ele_list = self.find_elements(create_order['校验下拉框'])
            for ele in ele_list:
                if ele.text == self.get_value(label, house_info):
                    ele.click()
                    sleep(2)
                    break

    @staticmethod
    def get_value(label_name, house_info):
        if label_name == '楼盘':
            return house_info['estate_name']
        if label_name == '楼层':
            return house_info['floor'] + '层'
        if label_name == '门牌号':
            return house_info['door_name']
        if label_name == '居室':
            return house_info['house_type'].get('room') + '室'
        if label_name == '楼号':
            return house_info['building_name']
        if label_name == '可看时间':
            return house_info['enable_watch_time']
        if label_name == '装修情况':
            return house_info['renovation_condition']
        if label_name == '房屋现状':
            return house_info['house_state']
        if label_name == '抵押状态':
            return house_info['has_pledge']

    def click_verify_house_button(self):
        self.is_click(create_order['校验房源信息按钮'])

    def input_customer_code(self, customer_code):
        self.input_text(create_order['客源编号输入框'], customer_code)

    def click_get_customer_info_button(self):
        self.is_click(create_order['获取客源信息按钮'])

    def get_customer_name(self):
        return self.element_text(create_order['客源信息标签'])

    def click_next_step_button(self):
        self.is_click(create_order['下一步按钮'])

    def choose_district_contract(self):
        if ini.environment == 'sz':
            self.is_click(create_order['苏州合同单选按钮'])
        elif ini.environment == 'ks':
            self.is_click(create_order['昆山合同单选按钮'])

    def click_confirm_button_in_dialog(self):  # 选择合同弹窗，点击确定按钮
        self.is_click(create_order['确定按钮'])

    def click_save_button(self):
        self.is_click(create_order['保存按钮'])

    def click_submit_button(self):
        self.is_click(create_order['提交按钮'])
        sleep(4)

    def input_contract_content(self, test_data, flag='买卖'):
        if flag == '买卖':
            if ini.environment == 'sz':
                ContractCreateSaleOrderDetailSZPage(self.driver).input_contract_content(test_data)
            elif ini.environment == 'ks':
                ContractCreateSaleOrderDetailKSPage(self.driver).input_contract_content(test_data)
            elif ini.environment == 'wx':
                ContractCreateSaleOrderDetailWXPage(self.driver).input_contract_content(test_data)
            elif ini.environment == 'cz':
                ContractCreateSaleOrderDetailWXPage(self.driver).input_contract_content(test_data)
            else:
                raise ValueError('传值错误')
        elif flag == '租赁':
            ContractCreateRentOrderPage(self.driver).input_contract_content(test_data)
        else:
            raise ValueError('传值错误')
