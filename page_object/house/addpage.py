#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: addpage.py
@time: 2021/06/22
"""

from page.webpage import WebPage
from common.readelement import Element
from utils.timeutil import sleep
from common.readconfig import ini

house_add = Element('house/add')


class HouseAddPage(WebPage):

    def choose_sale_radio(self):
        self.is_click(house_add['委托类型_出售单选'])

    def choose_rent_radio(self):
        self.is_click(house_add['委托类型_出租单选'])

    def check_sale_radio(self):
        value = self.get_element_attribute(house_add['委托类型_出售单选'], 'class')
        if 'checked' in value:
            return True
        else:
            return False

    def check_rent_radio(self):
        value = self.get_element_attribute(house_add['委托类型_出租单选'], 'class')
        if 'checked' in value:
            return True
        else:
            return False

    def choose_estate_name(self, community_name):
        self.input_text(house_add['楼盘名称输入框'], community_name)
        sleep()
        community_list = self.find_elements(house_add['楼盘名称下拉框'])
        for community in community_list:
            if community.text == community_name:
                community.click()
                break

    def choose_building_id(self, building_id):
        self.is_click(house_add['栋座选择框'])
        building_id_list = self.find_elements(house_add['栋座下拉框'])
        for building_id_element in building_id_list:
            if building_id_element.text == building_id:
                building_id_element.click()
                break

    def choose_building_cell(self, building_cell):
        self.is_click(house_add['单元选择框'])
        building_cell_list = self.find_elements(house_add['单元下拉框'])
        for building_cell_element in building_cell_list:
            if building_cell_element.text == building_cell:
                building_cell_element.click()
                break

    def choose_floor(self, floor):
        self.is_click(house_add['楼层选择框'])
        floor_list = self.find_elements(house_add['楼层下拉框'])
        for floor_element in floor_list:
            if floor_element.text == floor:
                floor_element.click()
                break

    def choose_doorplate(self, doorplate):
        self.is_click(house_add['门牌选择框'])
        doorplate_list = self.find_elements(house_add['门牌下拉框'])
        for doorplate_element in doorplate_list:
            if doorplate_element.text == doorplate:
                doorplate_element.click()
                break

    def find_dialog(self):
        if self.find_element_with_wait_time(house_add['资料盘认领弹窗_前往按钮']):
            return True
        else:
            return False

    def click_dialog_cancel_button(self):
        self.is_click(house_add['资料盘认领弹窗_取消按钮'])

    def click_dialog_go_button(self):
        self.is_click(house_add['资料盘认领弹窗_前往按钮'])

    def click_submit_button(self):  # 资料盘提交按钮
        self.is_click(house_add['提交按钮'])

    def click_next_button(self):
        self.is_click(house_add['下一步按钮'])

    def input_house_owner_name(self, house_owner_name):
        self.input_text(house_add['业主姓名输入框'], house_owner_name)

    def input_house_owner_phone(self, house_owner_phone):
        self.input_text(house_add['手机号码输入框'], house_owner_phone)

    def choose_house_type(self, house_types):
        house_types_list = ['室', '厅', '卫', '厨']
        for i in range(len(house_types_list)):
            self.is_click(house_add['户型_' + house_types_list[i] + '选择框'])
            type_list = self.find_elements(house_add['户型_' + house_types_list[i] + '下拉框'])
            for type_element in type_list:
                if type_element.text == house_types[i]:
                    type_element.click()
                    break

    def input_area(self, area):
        self.input_text(house_add['面积输入框'], area)

    def choose_orientations(self, orientations):
        for orientation in orientations:
            self.is_click(house_add['朝向_' + orientation + '勾选'])

    def input_sale_price(self, sale_price):
        self.input_text(house_add['售价输入框'], sale_price)

    def input_rent_price(self, rent_price):
        self.input_text(house_add['租价输入框'], rent_price)

    def input_rent_time(self, rent_time):
        self.is_click(house_add['可入住时间输入框'])
        self.input_text(house_add['可入住时间输入框'], rent_time)
        self.send_enter_key(house_add['可入住时间输入框'])

    def choose_inspect_type(self, inspect_type):
        self.is_click(house_add['看房选择框'])
        inspect_type_list = self.find_elements(house_add['看房下拉框'])
        for inspect_type_element in inspect_type_list:
            if inspect_type_element.get_attribute('label') == inspect_type:
                inspect_type_element.click()
                break

    def choose_decoration_state(self, decoration_state):
        self.is_click(house_add['装修情况选择框'])
        decoration_state_list = self.find_elements(house_add['装修情况下拉框'])
        for decoration_state_element in decoration_state_list:
            if decoration_state_element.get_attribute('label') == decoration_state:
                decoration_state_element.click()
                break

    def click_add_button(self):
        self.is_click(house_add['添加按钮'])

    def input_property_address(self, flag):
        if flag == '买卖':
            self.choose_sale_radio()
        elif flag == '租赁':
            self.choose_rent_radio()
        else:
            raise ValueError('传值错误，只能是买卖或者租赁')
        self.choose_estate_name(ini.house_community_name)  # 填写物业地址信息
        self.choose_building_id(ini.house_building_id)
        self.choose_building_cell(ini.house_building_cell)
        self.choose_floor(ini.house_floor)
        self.choose_doorplate(ini.house_doorplate)
        self.click_next_button()  # 点击下一步按钮

    def input_owner_info_and_house_info(self, test_data, flag):
        self.input_house_owner_name(test_data['house_owner_name'])
        self.input_house_owner_phone(test_data['house_owner_phone'])
        self.choose_house_type(test_data['house_types'])
        self.input_area(test_data['area'])
        self.choose_orientations(test_data['orientations'])
        if flag == '买卖':
            self.input_sale_price(test_data['sale_price'])
        elif flag == '租赁':
            self.input_rent_price(test_data['rent_price'])
            self.input_rent_time(test_data['rent_time'])
        else:
            raise ValueError('传值错误，只能是买卖或者租赁')
        self.choose_inspect_type(test_data['inspect_type'])
        if flag == '租赁':
            self.choose_decoration_state(test_data['decoration_state'])
        self.click_add_button()
