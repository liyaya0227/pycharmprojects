#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@time: 2021/06/22
"""

from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element

house_table = Element('house/table')


class HouseTablePage(WebPage):

    def click_sale_tab(self):
        self.is_click(house_table['买卖标签'])

    def click_rent_tab(self):
        self.is_click(house_table['租赁标签'])

    def click_new_tab(self):
        self.is_click(house_table['新房标签'])

    def click_all_house_tab(self):
        self.is_click(house_table['全部房源标签'])

    def click_deal_house_tab(self):
        self.is_click(house_table['成交房源标签'])

    def click_add_house_button(self):
        self.is_click(house_table['新增房源按钮'])

    def click_add_new_house_button(self):
        self.is_click(house_table['新增楼盘按钮'])

    def click_off_shelf_house_tab(self):
        self.is_click(house_table['下架房源标签'])

    def choose_estate_name_search(self, community_name):
        self.input_text(house_table['楼盘输入框'], community_name)
        sleep(2)
        community_list = self.find_elements(house_table['楼盘下拉框'])
        for community in community_list:
            if community.text == community_name:
                community.click()
                break

    def choose_building_name_search(self, building_name):
        self.is_click(house_table['楼栋选择框'])
        building_name_list = self.find_elements(house_table['楼栋下拉框'])
        for building_name_ele in building_name_list:
            if building_name_ele.text == building_name:
                building_name_ele.click()
                break

    def choose_doorplate_search(self, doorplate):
        self.is_click(house_table['门牌选择框'])
        doorplate_list = self.find_elements(house_table['门牌下拉框'])
        for doorplate_ele in doorplate_list:
            if doorplate_ele.text == doorplate:
                doorplate_ele.click()
                break

    def input_house_code_search(self, house_code):
        self.input_text(house_table['房源编号搜索项'], house_code)

    def input_building_name_search(self, building_name):
        self.input_text(house_table['楼盘名称搜索项'], building_name)

    def click_search_button(self):
        self.is_click(house_table['搜索按钮'])
        sleep()

    def click_reset_button(self):
        self.is_click(house_table['重置按钮'])
        sleep()

    def clear_filter(self, flag='买卖'):
        if flag == '租赁' or flag == '买卖':
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['关注筛选_不限'], 'class'):
                self.is_click(house_table['关注筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['角色筛选_不限'], 'class'):
                self.is_click(house_table['角色筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['区域筛选_不限'], 'class'):
                self.is_click(house_table['区域筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['价格筛选_不限'], 'class'):
                self.is_click(house_table['价格筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['面积筛选_不限'], 'class'):
                self.is_click(house_table['面积筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['户型筛选_不限'], 'class'):
                self.is_click(house_table['户型筛选_不限'])
            if flag == '买卖':
                if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['标签筛选_不限'], 'class'):
                    self.is_click(house_table['标签筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['装修筛选_不限'], 'class'):
                self.is_click(house_table['装修筛选_不限'])
        elif flag == '新房':
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['区域筛选_不限'], 'class'):
                self.is_click(house_table['区域筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['价格筛选_不限'], 'class'):
                self.is_click(house_table['价格筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['户型筛选_不限'], 'class'):
                self.is_click(house_table['户型筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['物业类型筛选_不限'], 'class'):
                self.is_click(house_table['物业类型筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['类型筛选_不限'], 'class'):
                self.is_click(house_table['类型筛选_不限'])
            if 'ant-radio-button-wrapper-checked' not in self.get_element_attribute(house_table['房源渠道筛选_不限'], 'class'):
                self.is_click(house_table['房源渠道筛选_不限'])
        sleep()

    def go_house_detail_by_row(self, row=1):
        locator = 'xpath', "//div[not(contains(@style,'display'))]//div[@class='ant-row houseManage']//table/tbody/tr["\
                  + str(row) + "]/td[2]"
        ele = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", ele)
        ele.click()
        sleep()
        self.refresh()
        sleep(2)

    def get_house_table_count(self):
        sleep()
        house = self.find_element(house_table['房源列表'])
        houses = house.find_elements_by_xpath(
            "//div[not(contains(@style,'display'))]/div[@class='ant-row houseManage']//table//tbody/tr")
        if houses[0].text == '暂无数据':
            return 0
        return len(houses)

    def click_delete_button_by_row(self, row=1):
        locator = 'xpath', "//div[not(contains(@style,'display'))]//div[@class='ant-row houseManage']//table/tbody/tr["\
                  + str(row) + "]/td[6]/p[contains(text(),'删除')]"
        self.is_click(locator)

    def dialog_click_confirm_button(self):
        self.is_click(house_table['弹窗_删除按钮'])

    def scroll_to_top(self):
        self.execute_js_script("var q=document.documentElement.scrollTop=0")
        sleep(2)
