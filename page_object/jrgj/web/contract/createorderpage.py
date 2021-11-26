#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: createorderpage.py
@date: 2021/7/2 0002
"""
from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element
from page_object.jrgj.web.contract.createsaleorder_szpage import ContractCreateSaleOrderDetailSZPage
from page_object.jrgj.web.contract.createsaleorder_kspage import ContractCreateSaleOrderDetailKSPage
from page_object.jrgj.web.contract.createsaleorder_zjgpage import ContractCreateSaleOrderDetailZJGPage
from page_object.jrgj.web.contract.createsaleorder_wxpage import ContractCreateSaleOrderDetailWXPage
from page_object.jrgj.web.contract.createsaleorder_hzpage import ContractCreateSaleOrderDetailHZPage
from page_object.jrgj.web.contract.createrentorderpage import ContractCreateRentOrderPage

create_order = Element('jrgj/web/contract/createorder')


class ContractCreateOrderPage(WebPage):

    def choose_business_type(self, business_type):
        self.click_element(create_order['业务类型选择框'], sleep_time=0.5)
        business_type_list = self.find_elements(create_order['业务类型下拉框'])
        for business_type_ele in business_type_list:
            if business_type in business_type_ele.text:
                business_type_ele.click()
                break

    def input_house_code(self, house_code):
        self.input_text(create_order['房源编号输入框'], house_code)

    def click_get_house_info_button(self):
        self.click_element(create_order['获取房源信息按钮'])

    def verify_house_info(self, house_info):
        verify_first_label = self.get_element_text(create_order['校验一标签'])
        verify_second_label = self.get_element_text(create_order['校验二标签'])
        verify_third_label = self.get_element_text(create_order['校验三标签'])
        verify_four_label = self.get_element_text(create_order['校验四标签'])
        labels = [verify_first_label, verify_second_label, verify_third_label, verify_four_label]
        flag = ['一', '二', '三', '四']
        for label in labels:
            self.click_element(create_order['校验' + flag[labels.index(label)] + '输入框'], sleep_time=0.5)
            ele_list = self.find_elements(create_order['校验下拉框'])
            for ele in ele_list:
                if ele.text == self.get_value(label, house_info):
                    ele.click()
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
        self.click_element(create_order['校验房源信息按钮'], sleep_time=1)

    def input_customer_code(self, customer_code):
        self.input_text(create_order['客源编号输入框'], customer_code)

    def click_get_customer_info_button(self):
        self.click_element(create_order['获取客源信息按钮'], sleep_time=1)

    def get_customer_name(self):
        return self.get_element_text(create_order['客源信息标签'])

    def click_next_step_button(self):
        self.click_element(create_order['下一步按钮'], sleep_time=1)

    def choose_district_contract(self, env):
        if env == 'sz':
            self.click_element(create_order['苏州合同单选按钮'])
        elif env == 'ks':
            self.click_element(create_order['昆山合同单选按钮'])
        elif env == 'zjg':
            self.click_element(create_order['张家港合同单选按钮'])
        else:
            raise ValueError('暂不支持')

    def click_confirm_button_in_dialog(self):  # 选择合同弹窗，点击确定按钮
        self.click_element(create_order['确定按钮'])

    def click_save_button(self):
        self.click_element(create_order['保存按钮'])

    def click_submit_button(self):
        self.click_element(create_order['提交按钮'], sleep_time=4)

    def click_submit_change_button(self):
        sleep(2)
        self.click_element(create_order['提交变更按钮'], sleep_time=4)

    def input_sale_contract_content(self, env, test_data):
        if env == 'sz':
            ContractCreateSaleOrderDetailSZPage(self.driver).input_contract_content(test_data)
        elif env == 'ks':
            ContractCreateSaleOrderDetailKSPage(self.driver).input_contract_content(test_data)
        elif env == 'zjg':
            ContractCreateSaleOrderDetailZJGPage(self.driver).input_contract_content(test_data)
        elif env == 'wx':
            ContractCreateSaleOrderDetailWXPage(self.driver).input_contract_content(test_data)
        elif env == 'hz':
            ContractCreateSaleOrderDetailHZPage(self.driver).input_contract_content(test_data)
        elif env == 'tl':
            ContractCreateSaleOrderDetailHZPage(self.driver).input_contract_content(test_data)
        elif env == 'cz':
            ContractCreateSaleOrderDetailWXPage(self.driver).input_contract_content(test_data)
        else:
            raise ValueError('传值错误')

    def input_rent_contract_content(self, test_data):
        ContractCreateRentOrderPage(self.driver).input_contract_content(test_data)
