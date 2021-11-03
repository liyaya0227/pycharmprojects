#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: addpage.py
@date: 2021/7/15 0015
"""

from page.webpage import WebPage
from common.readelement import Element

customer_add_base_info = Element('jrgj/web/customer/addbaseinfo')
customer_add_need_info = Element('jrgj/web/customer/addneedinfo')


class CustomerAddPage(WebPage):

    def input_customer_name(self, customer_name):
        self.input_text(customer_add_base_info['姓名输入框'], customer_name)

    def choose_customer_sex(self, customer_sex):
        if customer_sex == '男':
            self.click_element(customer_add_base_info['性别_男_单选'])
        elif customer_sex == '女':
            self.click_element(customer_add_base_info['性别_女_单选'])
        else:
            raise ValueError('传值错误')

    def choose_phone_area(self, phone_area):
        self.click_element(customer_add_base_info['电话号_区域选择框'], sleep_time=0.5)
        area_list = self.find_elements(customer_add_base_info['电话号_区域下拉框'])
        if phone_area == '':
            area_list[0].click()
            return True
        for area_ele in area_list:
            if area_ele.text == phone_area:
                area_ele.click()
                return True
        raise ValueError('传值错误')

    def input_customer_phone(self, customer_phone):
        self.input_text(customer_add_base_info['电话号_输入框'], customer_phone)

    def choose_customer_wish(self, customer_wish):
        if customer_wish == '一星':
            self.click_element(customer_add_base_info['客户意愿_一星'])
        elif customer_wish == '二星':
            self.click_element(customer_add_base_info['客户意愿_二星'])
        elif customer_wish == '三星':
            self.click_element(customer_add_base_info['客户意愿_三星'])
        else:
            raise ValueError('传值错误')

    def click_add_requirement_button(self):
        self.click_element(customer_add_base_info['需求类型添加按钮'], sleep_time=0.5)

    def choose_requirements(self, requirement):
        if requirement == '买二手住宅':
            self.click_element(customer_add_base_info['买二手住宅勾选'])
        elif requirement == '租赁住宅':
            self.click_element(customer_add_base_info['租赁住宅勾选'])
        elif requirement == '买新房不限':
            self.click_element(customer_add_base_info['买新房不限勾选'])
        else:
            raise ValueError('传值错误')

    def get_all_requirement(self):
        requirements = []
        requirement_list = self.find_elements(customer_add_base_info['需求类型所有标签'])
        for requirement_ele in requirement_list:
            requirements.append(requirement_ele.text)
        return requirements

    def click_dialog_confirm_button(self):
        self.click_element(customer_add_base_info['弹窗_确定按钮'], sleep_time=0.5)

    def click_dialog_cancel_button(self):
        self.click_element(customer_add_base_info['弹窗_取消按钮'])

    def click_cancel_button(self):
        self.click_element(customer_add_base_info['取消按钮'])

    def add_customer_requirements(self, customer_requirements):
        self.click_add_requirement_button()
        for requirement in customer_requirements:
            self.choose_requirements(requirement)
        self.click_dialog_confirm_button()

    def click_next_step_button(self):
        self.click_element(customer_add_base_info['下一步按钮'])

    def get_requirement_tabs(self):
        requirement_tabs = []
        requirement_tab_list = self.find_elements(customer_add_need_info['已选需求类型所有标签'])
        for requirement_tab_ele in requirement_tab_list:
            requirement_tabs.append(requirement_tab_ele.text)
        return requirement_tabs

    def click_sale_need_tab(self):
        self.click_element(customer_add_need_info['买二手住宅标签'])

    def click_rent_need_tab(self):
        self.click_element(customer_add_need_info['租赁住宅标签'])

    def choose_purchase_house_purpose(self, purchase_house_purpose):
        self.click_element(customer_add_need_info['购房目的选择框'], sleep_time=0.5)
        purchase_house_purpose_list = self.find_elements(customer_add_need_info['下拉框'])
        for purchase_house_purpose_ele in purchase_house_purpose_list:
            if purchase_house_purpose_ele.text == purchase_house_purpose:
                purchase_house_purpose_ele.click()
                return True
        raise ValueError('传值错误')

    def choose_rent_type(self, rent_type):
        self.click_element(customer_add_need_info['租赁方式选择框'], sleep_time=0.5)
        rent_type_list = self.find_elements(customer_add_need_info['下拉框'])
        for rent_type_ele in rent_type_list:
            if rent_type_ele.text == rent_type:
                rent_type_ele.click()
                return True
        raise ValueError('传值错误')

    def input_psychology_min_price(self, psychology_min_price):
        self.input_text(customer_add_need_info['心理价位_最低价位'], psychology_min_price)

    def input_psychology_max_price(self, psychology_max_price):
        self.input_text(customer_add_need_info['心理价位_最高价位'], psychology_max_price)

    def input_psychology_price(self, psychology_price):
        if len(psychology_price) != 2 or psychology_price[0] > psychology_price[1]:
            raise ValueError('传值错误')
        self.input_psychology_min_price(psychology_price[0])
        self.input_psychology_max_price(psychology_price[1])

    def input_min_area(self, min_area):
        self.input_text(customer_add_need_info['面积_最小面积'], min_area)

    def input_max_area(self, max_area):
        self.input_text(customer_add_need_info['面积_最大面积'], max_area)

    def input_area(self, area):
        if len(area) != 2 or area[0] > area[1]:
            raise ValueError('传值错误')
        self.input_min_area(area[0])
        self.input_max_area(area[1])

    def input_min_room(self, min_room):
        self.click_element(customer_add_need_info['居室_最小选择框'], sleep_time=0.5)
        room_list = self.find_elements(customer_add_need_info['下拉框'])
        for room_ele in room_list:
            if room_ele.text == min_room:
                room_ele.click()
                return True
        raise ValueError('传值错误')

    def input_max_room(self, max_room):
        self.click_element(customer_add_need_info['居室_最大选择框'], sleep_time=0.5)
        room_list = self.find_elements(customer_add_need_info['下拉框'])
        for room_ele in room_list:
            if room_ele.text == max_room:
                room_ele.click()
                return True
        raise ValueError('传值错误')

    def input_room(self, room):
        if len(room) != 2 or room[0][:1] > room[1][:1]:
            raise ValueError('传值错误')
        self.input_min_room(room[0])
        self.input_max_room(room[1])

    def choose_business_district(self, business_district):
        self.click_element(customer_add_need_info['商圈选择框'], sleep_time=0.5)
        for key, value in business_district.items():
            area_list = self.find_elements(customer_add_need_info['商圈区域列表'])
            for area_ele in area_list:
                if area_ele.text == key:
                    area_ele.click()
                    break
            for town in value:
                town_list = self.find_elements(customer_add_need_info['商圈城镇列表'])
                for town_ele in town_list:
                    if town_ele.text == town:
                        locator = 'xpath',\
                                  "//div[contains(@class, 'kuma-dropdown') and " \
                                  "not(contains(@class, 'kuma-dropdown-hidden'))]" \
                                  "//div[@class='kuma-cascade-multi']/div[2]//li[" +\
                                  str(town_list.index(town_ele) + 1) + "]//s"
                        self.click_element(locator)
                        break
        self.click_element(customer_add_need_info['商圈确定按钮'], sleep_time=0.5)

    def choose_use(self, use):
        self.click_element(customer_add_need_info['用途选择框'], sleep_time=0.5)
        use_list = self.find_elements(customer_add_need_info['下拉框'])
        for use_ele in use_list:
            if use_ele.text == use:
                use_ele.click()
                return True
        raise ValueError('传值错误')

    def input_check_in_date(self, check_in_date):
        self.click_element(customer_add_need_info['入住日期输入框'])
        self.input_text_with_enter(customer_add_need_info['入住日期输入框'], check_in_date)

    def choose_pay_type(self, pay_type):
        self.click_element(customer_add_need_info['付款方式选择框'], sleep_time=0.5)
        pay_type_list = self.find_elements(customer_add_need_info['下拉框'])
        for pay_type_ele in pay_type_list:
            if pay_type_ele.text == pay_type:
                pay_type_ele.click()
                return True
        raise ValueError('传值错误')

    def choose_rent_range(self, rent_range):
        self.click_element(customer_add_need_info['租期选择框'], sleep_time=0.5)
        rent_range_list = self.find_elements(customer_add_need_info['下拉框'])
        for rent_range_ele in rent_range_list:
            if rent_range_ele.text == rent_range:
                rent_range_ele.click()
                return True
        raise ValueError('传值错误')

    def input_first_min_pay(self, first_min_pay):
        self.input_text(customer_add_need_info['首付最低输入框'], first_min_pay)

    def input_first_max_pay(self, first_max_pay):
        self.input_text(customer_add_need_info['首付最高输入框'], first_max_pay)

    def input_first_pay(self, first_pay):
        if len(first_pay) != 2 or first_pay[0] > first_pay[1]:
            raise ValueError('传值错误')
        self.input_first_min_pay(first_pay[0])
        self.input_first_max_pay(first_pay[1])

    def input_month_min_pay(self, month_min_pay):
        self.input_text(customer_add_need_info['月供最低输入框'], month_min_pay)

    def input_month_max_pay(self, month_max_pay):
        self.input_text(customer_add_need_info['月供最高输入框'], month_max_pay)

    def input_month_pay(self, month_pay):
        if len(month_pay) != 2 or month_pay[0] > month_pay[1]:
            raise ValueError('传值错误')
        self.input_month_min_pay(month_pay[0])
        self.input_month_max_pay(month_pay[1])

    def choose_decoration(self, decoration):
        if '不限' in decoration:
            self.click_element(customer_add_need_info['装修_不限勾选'])
        if '豪华' in decoration:
            self.click_element(customer_add_need_info['装修_豪华勾选'])
        if '毛坯' in decoration:
            self.click_element(customer_add_need_info['装修_毛坯勾选'])
        if '简装' in decoration:
            self.click_element(customer_add_need_info['装修_简装勾选'])
        if '精装' in decoration:
            self.click_element(customer_add_need_info['装修_精装勾选'])

    def choose_orientation(self, orientation):
        if '不限' in orientation:
            self.click_element(customer_add_need_info['朝向_不限勾选'])
        if '东' in orientation:
            self.click_element(customer_add_need_info['朝向_东勾选'])
        if '东南' in orientation:
            self.click_element(customer_add_need_info['朝向_东南勾选'])
        if '南' in orientation:
            self.click_element(customer_add_need_info['朝向_南勾选'])
        if '西南' in orientation:
            self.click_element(customer_add_need_info['朝向_西南勾选'])
        if '西' in orientation:
            self.click_element(customer_add_need_info['朝向_西勾选'])
        if '西北' in orientation:
            self.click_element(customer_add_need_info['朝向_西北勾选'])
        if '北' in orientation:
            self.click_element(customer_add_need_info['朝向_北勾选'])
        if '东北' in orientation:
            self.click_element(customer_add_need_info['朝向_东北勾选'])

    def choose_floor(self, floor):
        if '不限' in floor:
            self.click_element(customer_add_need_info['楼层_不限勾选'])
        if '低楼层' in floor:
            self.click_element(customer_add_need_info['楼层_低楼层勾选'])
        if '中楼层' in floor:
            self.click_element(customer_add_need_info['楼层_中楼层勾选'])
        if '高楼层' in floor:
            self.click_element(customer_add_need_info['楼层_高楼层勾选'])
        if '不要一层' in floor:
            self.click_element(customer_add_need_info['楼层_不要一层勾选'])
        if '不要顶层' in floor:
            self.click_element(customer_add_need_info['楼层_不要顶层勾选'])

    def choose_floor_year(self, floor_year):
        if '不限' in floor_year:
            self.click_element(customer_add_need_info['楼龄_不限勾选'])
        if '5年内' in floor_year:
            self.click_element(customer_add_need_info['楼龄_5年内勾选'])
        if '5-10年' in floor_year:
            self.click_element(customer_add_need_info['楼龄_5-10年勾选'])
        if '10-15年' in floor_year:
            self.click_element(customer_add_need_info['楼龄_10-15年勾选'])
        if '15-20年' in floor_year:
            self.click_element(customer_add_need_info['楼龄_15-20年勾选'])
        if '20年以上' in floor_year:
            self.click_element(customer_add_need_info['楼龄_20年以上勾选'])

    def click_back_step_button(self):
        self.click_element(customer_add_need_info['上一步按钮'])

    def click_complete_button(self):
        self.click_element(customer_add_need_info['完成按钮'], sleep_time=1)
