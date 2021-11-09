#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: add_page.py
@time: 2021/10/14
"""
from page.webpage import WebPage
from common.readelement import Element


add_house = Element('jrxf/web/house/add')


class AddHousePage(WebPage):

    def add_house_base_info(self, house_name, developers, house_status, sale_price, start_sale_time, making_room_time,
                            house_keeper_type, city, country, trade, house_address, sale_address):  # 增加房源基础信息
        self.input_text(add_house['楼盘名称输入框'], house_name)
        self.input_text(add_house['开发商输入框'], developers)
        self.select_house_status(house_status)
        self.input_text(add_house['楼盘价格输入框'], sale_price)
        self.select_start_sale_time(start_sale_time)
        self.select_making_room_time(making_room_time)
        self.select_house_keeper_type(house_keeper_type)
        self.select_area(city, country, trade)
        self.input_text(add_house['楼盘地址输入框'], house_address)
        self.input_text(add_house['售楼处地址输入框'], sale_address)
        self.choose_building_position()
        self.click_element(add_house['弹窗_确定按钮'])

    def select_house_status(self, house_status):
        self.click_element(add_house['楼盘状态输入框'])
        self.select_item_option(index=0)

    def select_start_sale_time(self, start_sale_time):
        self.click_element(add_house['开盘时间输入框'])
        self.click_element(add_house['开盘时间_今天选项'])

    def select_making_room_time(self, making_room_time):
        self.click_element(add_house['交房时间输入框'])
        self.click_element(add_house['交房时间_今天选项'])

    def select_area(self, city, country, trade):
        self.click_element(add_house['行政区域_市输入框'])
        self.select_item_option(city)
        self.click_element(add_house['行政区域_区输入框'])
        self.select_item_option(country)
        self.click_element(add_house['行政区域_商圈输入框'])
        self.select_item_option(trade)

    def select_house_keeper_type(self, house_keeper_type):
        self.click_element(add_house['物业类型输入框'])
        self.select_item_option(house_keeper_type)

    def choose_building_position(self):  # 经纬度
        ele_list = [add_house['经度输入框'], add_house['纬度输入框']]
        for ele in ele_list:
            self.set_element_attribute(ele, 'class', 'ant-input')
            self.remove_element_attribute(ele, 'disabled')
        self.input_text(add_house['经度输入框'], '125')
        self.input_text(add_house['纬度输入框'], '125')

    def click_follow_up_tab(self):  # 点击跟进信息tab
        self.click_element(add_house['跟进信息tab'])

    def add_follow_up(self):
        self.click_element(add_house['写跟进按钮'])
        self.input_text(add_house['跟进信息输入框'], '新增跟进信息')
        self.click_element(add_house['跟进弹窗_确定按钮'])

    def click_upload_contract_btn(self):  # 点击上传合同tab
        self.click_element(add_house['上传合同tab'])

    def upload_contract(self, picture_path):  # 上传合同
        self.send_key(add_house['合同图片input'], picture_path)
        self.send_key(add_house['预售许可证图片input'], picture_path)
        self.click_element(add_house['提交审核按钮'])

    def audit_contract(self):
        self.click_element(add_house['审核通过按钮'])
        self.click_element(add_house['上传合同tab'])
        self.click_element(add_house['审核通过按钮'])
        self.click_element(add_house['审核确定按钮'])

    def input_house_preferential(self, preferential='100'):
        self.input_text(add_house['楼盘优惠输入框'], preferential)

    def add_customer_rules(self, advance_reported_time='1', reported_protect_time='1', take_look_time='1'):  # 客户规则
        self.input_text(add_house['提前报备时间输入框'], advance_reported_time)
        self.input_text(add_house['报备保护时间输入框'], reported_protect_time)
        self.input_text(add_house['带看保护时间输入框'], take_look_time)

    def add_planning_info(self):  # 规划信息
        target_ele = self.find_element(add_house['规划信息card_title'])
        self.driver.execute_script("arguments[0].scrollIntoView();", target_ele)  # 拖动到可见的元素去
        self.click_element(add_house['建筑类型输入框'])
        self.select_item_option(index=0)
        self.click_element(add_house['产权年限输入框'])
        self.select_item_option(option='暂无')
        self.input_text(add_house['容积率输入框'], 50)
        self.input_text(add_house['绿化率输入框'], 50)
        self.input_text(add_house['规划户数输入框'], 20000)
        self.input_text(add_house['规划车位输入框'], 20000)

    def add_support_info(self):  # 配套信息
        self.click_element(add_house['水电燃气输入框'])
        self.select_item_option(option='商电 商水')
        self.input_text(add_house['物业公司输入框'], '恒大物业')
        self.input_text(add_house['物业费上线输入框'], '100')
        self.input_text(add_house['物业费下线输入框'], '100')
        self.click_element(add_house['供暖方式输入框'])
        self.select_item_option(option='自采暖')

    def add_contract(self, contract_name, contract_phone):  # 新增联系人
        target_ele = self.find_element(add_house['新增联系人card_title'])
        item_option_value = contract_name + '-' + contract_phone
        self.driver.execute_script("arguments[0].scrollIntoView();", target_ele)  # 拖动到可见的元素去
        self.click_element(add_house['新房案场_新增联系人'])
        self.input_text(add_house['联系人姓名输入框'], contract_name)
        self.select_item_option(option=item_option_value)
        self.click_element(add_house['弹窗_确定按钮'])
        self.click_element(add_house['新房经理_新增联系人'])
        self.input_text(add_house['联系人姓名输入框'], contract_name)
        self.select_item_option(option=item_option_value)
        self.click_element(add_house['弹窗_确定按钮'])
        self.click_element(add_house['新房总监_新增联系人'])
        self.input_text(add_house['联系人姓名输入框'], contract_name)
        self.select_item_option(option=item_option_value)
        self.click_element(add_house['弹窗_确定按钮'])

    def click_save_btn(self):
        self.click_element(add_house['保存按钮'])
        self.click_element(add_house['审核确定按钮'])

    def audit_release(self):
        self.click_element(add_house['上架_审核通过按钮'])
        self.click_element(add_house['审核确定按钮'])

    def select_item_option(self, option=None, index=None):
        if option:
            locator = 'xpath', "//div[@style='' or not(@style)]//div[@class='rc-virtual-list']//div[contains(@class," \
                               "'ant-select-item ant-select-item-option') and @title='" + option + "'] "
            self.click_element(locator)
        else:
            locator = 'xpath', "//div[@style='' or not(@style)]//div[@class='rc-virtual-list']//div[contains(@class," \
                               "'ant-select-item ant-select-item-option')] "
            options = self.find_elements(locator)
            options[index].click()
