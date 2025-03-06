"""
@author: lijiahui
@version: V1.0
@file: test11.py
@time: 2022/1/11
"""
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


from common.readconfig import ini
from common.readelement import Element
from page.webpage import WebPage
from utils.timeutil import sleep

# 指定页面元素路径
create_house = Element('house/create_house')


class CreateHouse(WebPage):

    def click_house_manager(self):
        self.is_click(create_house['新房管理按钮'])

    def click_new_house_manager(self):
        self.is_click(create_house['楼盘管理按钮'])

    def click_house_create(self):
        self.is_click(create_house['新增楼盘按钮'])

    def input_house_name(self, house_name):
        self.input_text(create_house['楼盘名称'], house_name)

    def input_house_developers(self, developers):
        self.input_text(create_house['开发商'], developers)

    def choose_house_state(self, house_state):
        self.is_click(create_house['楼盘状态输入'], house_state)
        sleep(0.5)
        house_state_list = self.find_elements(create_house['楼盘状态选择'])
        for item in house_state_list:
            if item.get_attribute('label') == house_state:
                item.click()
                break

    def input_house_price(self, house_price):
        self.input_text(create_house['楼盘价格'], house_price)

    def input_house_open_time(self, open_time):
        self.is_click(create_house['开盘时间'], open_time)

    def input_house_sell_time(self, sell_time):
        self.is_click(create_house['交房时间'], sell_time)

    def choose_house_property(self, house_property):
        self.input_text(create_house['物业类型输入'], house_property)
        sleep(0.5)
        house_property_list = self.find_elements(create_house['物业类型选择'])
        for item in house_property_list:
            if item.text == house_property:
                item.click()
                break

    def choose_house_city(self, house_city):
        self.input_text(create_house['项目行政区域城市输入'], house_city)
        sleep(0.5)
        house_city_list = self.find_elements(create_house['项目行政区域城市选择'])
        for item in house_city_list:
            if item.text == house_city:
                item.click

                break

    def choose_house_area(self, house_area):
        self.input_text(create_house['项目行政区域区输入'], house_area)
        sleep(0.5)
        house_area_list = self.find_elements(create_house['项目行政区域区选择'])
        for item in house_area_list:
            if item.text == house_area:
                item.click()
                break

    def choose_house_county(self, house_county):
        self.input_text(create_house['项目行政区域商圈输入'], house_county)
        sleep(0.5)
        house_county_list = self.find_elements(create_house['项目行政区域商圈选择框'])
        for item in house_county_list:
            if item.text == house_county:
                item.click()
                break

    def input_house_address(self, house_address):
        self.input_text(create_house['楼盘地址'], house_address)

    def input_sell_house_address(self, sell_house_address):
        self.input_text(create_house['售楼处地址'], sell_house_address)

    def choose_longitude_and_latitude(self):
        self.is_click(create_house['楼盘经纬度选择'])

    def determine_longitude_and_latitude(self):
        self.is_click(create_house['楼盘经纬度确定'])

    def determine_all_information(self):
        self.is_click(create_house['楼盘基础信息确定按钮'])

    def input_new_house(self, test_data):
        self.click_house_manager()
        self.click_new_house_manager()
        self.click_house_create()
        self.input_house_name(test_data['house_name'])
        self.input_house_developers(test_data['house_developers'])
        self.choose_house_state(test_data['house_state'])
        self.input_house_price(test_data['house_price'])
        self.input_house_open_time(test_data['house_open_time'])
        self.input_house_sell_time(test_data['house_sell_time'])
        self.choose_house_property(test_data['house_property'])
        self.choose_house_city(test_data['house_city'])
        self.choose_house_area(test_data['house_area'])
        self.choose_house_county(test_data['house_county'])
        self.input_house_address(test_data['house_address'])
        self.input_sell_house_address(test_data['sell_house_address'])
        self.choose_longitude_and_latitude()
        self.determine_longitude_and_latitude()
        # self.determine_all_informatio