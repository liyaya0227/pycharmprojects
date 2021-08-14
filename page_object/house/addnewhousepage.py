#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: addnewhousepage.py
@date: 2021/7/19 0019
"""

from page.webpage import WebPage
from common.readelement import Element
from utils.timeutil import sleep

house_add_new_house = Element('house/addnewhouse')


class HouseAddNewHousePage(WebPage):

    def input_building_name(self, building_name):
        self.input_text(house_add_new_house['楼盘名称输入框'], building_name)

    def input_building_discount(self, building_discount):
        if building_discount == '':
            self.is_click(house_add_new_house['楼盘优惠_暂无勾选框'])
        else:
            self.input_text(house_add_new_house['楼盘名称输入框'], building_discount)

    def choose_building_source_from(self, building_source_from):
        if building_source_from == '58爱房':
            self.is_click(house_add_new_house['房源渠道_58爱房按钮'])
        elif building_source_from == '京日新房':
            self.is_click(house_add_new_house['房源渠道_京日新房按钮'])
        else:
            raise ValueError('传值错误')

    def choose_whether_show_outside(self, whether_show):
        if whether_show == '是':
            self.choose_show_outside()
        elif whether_show == '否':
            self.choose_not_show_outside()
        else:
            raise ValueError('传值错误')

    def choose_show_outside(self):
        if self.get_element_attribute(house_add_new_house['是否外网呈现按钮'], 'aria-checked') == 'true':
            return True
        else:
            self.is_click(house_add_new_house['是否外网呈现按钮'])

    def choose_not_show_outside(self):
        if self.get_element_attribute(house_add_new_house['是否外网呈现按钮'], 'aria-checked') == 'false':
            return True
        else:
            self.is_click(house_add_new_house['是否外网呈现按钮'])

    def input_can_take_look_time(self, can_take_look_time):
        if len(can_take_look_time) != 2:
            raise ValueError('传值错误')
        self.is_click(house_add_new_house['可带看时间_开始时间输入框'])
        self.input_text_with_enter(house_add_new_house['可带看时间_开始时间输入框'], can_take_look_time[0])
        self.is_click(house_add_new_house['可带看时间_结束时间输入框'])
        self.input_text_with_enter(house_add_new_house['可带看时间_结束时间输入框'], can_take_look_time[1])

    def input_team_take_look_protect_time(self, team_take_look_protect_time):
        self.input_text(house_add_new_house['团购保护时间输入框'], team_take_look_protect_time)

    def input_advance_reported_time(self, advance_reported_time):
        self.input_text(house_add_new_house['提前报备时间输入框'], advance_reported_time)

    def input_confirm_role(self, confirm_role):
        self.input_text(house_add_new_house['客户确认规则输入框'], confirm_role)

    def input_reported_number(self, reported_number):
        self.input_text(house_add_new_house['报备完整号码输入框'], reported_number)

    def choose_developers_rechecking(self, developers_rechecking):
        self.is_click(house_add_new_house['开发商查重选择框'])
        developers_rechecking_list = self.find_elements(house_add_new_house['下拉框'])
        for developers_rechecking_ele in developers_rechecking_list:
            if developers_rechecking_ele.text == developers_rechecking:
                developers_rechecking_ele.click()
                return True
        raise ValueError('传值错误')

    def input_reported_protect_time(self, reported_protect_time):
        self.input_text(house_add_new_house['报备保护时间输入框'], reported_protect_time)

    def input_take_look_protect_time(self, take_look_protect_time):
        self.input_text(house_add_new_house['带看保护时间输入框'], take_look_protect_time)

    def input_incentive_policy(self, incentive_policy):
        self.input_text(house_add_new_house['激励政策输入框'], incentive_policy)

    def add_r_person(self, r_person):
        for person in r_person:
            self.is_click(house_add_new_house['R新房案场端_新增联系人按钮'])
            self.__dialog_choose_person(person)

    def add_s_person(self, s_person):
        for person in s_person:
            self.is_click(house_add_new_house['S新房经理_新增联系人按钮'])
            self.__dialog_choose_person(person)

    def add_d_person(self, d_person):
        for person in d_person:
            self.is_click(house_add_new_house['D新房总监_新增联系人按钮'])
            self.__dialog_choose_person(person)

    def __dialog_choose_person(self, person):
        self.is_click(house_add_new_house['弹窗_姓名输入框'])
        self.input_text(house_add_new_house['弹窗_姓名输入框'], person['姓名'])
        person_list = self.find_elements(house_add_new_house['下拉框'])
        for person_ele in person_list:
            if person_ele.text == person['姓名'] + '-' + person['电话']:
                person_ele.click()
                break
        self.is_click(house_add_new_house['弹窗_确定按钮'])

    def click_cancel_button(self):
        self.is_click(house_add_new_house['取消按钮'])

    def click_next_step_button(self):
        self.is_click(house_add_new_house['下一步按钮'])

    def input_developer(self, developer):
        self.input_text(house_add_new_house['开发商输入框'], developer)

    def input_building_sale_price(self, building_sale_price):
        if building_sale_price == '':
            self.is_click(house_add_new_house['楼盘价格_价格待定勾选框'])
        else:
            self.input_text(house_add_new_house['楼盘价格输入框'], building_sale_price)

    def check_building_sale_price_pending(self):
        self.is_click(house_add_new_house['楼盘价格_价格待定勾选框'])

    def choose_building_status(self, building_status):
        self.is_click(house_add_new_house['楼盘状态选择框'])
        building_status_list = self.find_elements(house_add_new_house['下拉框'])
        for building_status_ele in building_status_list:
            if building_status_ele.text == building_status:
                building_status_ele.click()
                return True
        raise ValueError('传值错误')

    def input_making_room_time(self, making_room_time):
        if making_room_time == '':
            self.is_click(house_add_new_house['交房时间_暂无勾选框'])
        else:
            self.is_click(house_add_new_house['交房时间输入框'])
            self.input_text_with_enter(house_add_new_house['交房时间输入框'], making_room_time)

    def check_making_room_time_none(self):
        self.is_click(house_add_new_house['交房时间_暂无勾选框'])

    def input_start_sale_time(self, start_sale_time):
        if start_sale_time == '':
            self.is_click(house_add_new_house['开盘时间_暂无勾选框'])
        else:
            self.is_click(house_add_new_house['开盘时间输入框'])
            self.input_text_with_enter(house_add_new_house['开盘时间输入框'], start_sale_time)

    def check_start_sale_time_none(self):
        self.is_click(house_add_new_house['开盘时间_暂无勾选框'])

    def input_building_address(self, building_address):
        self.input_text(house_add_new_house['楼盘地址输入框'], building_address)

    def input_building_project_address(self, building_project_address):
        if len(building_project_address) != 2:
            raise ValueError('传值错误')
        self.is_click(house_add_new_house['项目地址_区选择框'])
        country_list = self.find_elements(house_add_new_house['下拉框'])
        if building_project_address[0] == '':
            country_list[0].click()
        else:
            for country_ele in country_list:
                if country_ele.text == building_project_address[0]:
                    country_ele.click()
                    break
        self.is_click(house_add_new_house['项目地址_镇选择框'])
        town_list = self.find_elements(house_add_new_house['下拉框'])
        if building_project_address[1] == '':
            town_list[0].click()
        else:
            for town_ele in town_list:
                if town_ele.text == building_project_address[1]:
                    town_ele.click()
                    break

    def input_building_sale_address(self, building_sale_address):
        self.input_text(house_add_new_house['售楼处地址选择框'], building_sale_address)

    def choose_building_position(self):
        self.is_click(house_add_new_house['楼盘经纬度_地图选点按钮'])
        sleep()
        self.is_click(house_add_new_house['弹窗_确定按钮'])

    def choose_building_type(self, building_type):
        self.is_click(house_add_new_house['建筑类型选择框'])
        building_type_list = self.find_elements(house_add_new_house['下拉框'])
        for building_type_ele in building_type_list:
            if building_type_ele.text == building_type:
                building_type_ele.click()
                return True
        raise ValueError('传值错误')

    def choose_property_year(self, property_year):
        self.is_click(house_add_new_house['产权年限选择框'])
        property_year_list = self.find_elements(house_add_new_house['下拉框'])
        for property_year_ele in property_year_list:
            if property_year_ele.text == property_year:
                property_year_ele.click()
                return True
        raise ValueError('传值错误')

    def input_plot_ratio(self, plot_ratio):
        if plot_ratio == '':
            self.is_click(house_add_new_house['容积率_暂无勾选框'])
        else:
            self.input_text(house_add_new_house['容积率输入框'], plot_ratio)

    def check_plot_ratio_none(self):
        self.is_click(house_add_new_house['容积率_暂无勾选框'])

    def input_afforestation_rate(self, afforestation_rate):
        if afforestation_rate == '':
            self.is_click(house_add_new_house['绿化率_暂无勾选框'])
        else:
            self.input_text(house_add_new_house['绿化率输入框'], afforestation_rate)

    def check_afforestation_rate_none(self):
        self.is_click(house_add_new_house['绿化率_暂无勾选框'])

    def input_planning_number(self, planning_number):
        if planning_number == '':
            self.is_click(house_add_new_house['规划户数_暂无勾选框'])
        else:
            self.input_text(house_add_new_house['规划户数输入框'], planning_number)

    def check_planning_number_none(self):
        self.is_click(house_add_new_house['规划户数_暂无勾选框'])

    def input_planning_parking_space(self, plot_ratio):
        if plot_ratio == '':
            self.is_click(house_add_new_house['规划车位_暂无勾选框'])
        else:
            self.input_text(house_add_new_house['规划车位输入框'], plot_ratio)

    def check_planning_parking_space_none(self):
        self.is_click(house_add_new_house['规划车位_暂无勾选框'])

    def input_water_electricity(self, water_electricity):
        self.is_click(house_add_new_house['水电燃气选择框'])
        water_electricity_list = self.find_elements(house_add_new_house['下拉框'])
        for water_electricity_ele in water_electricity_list:
            if water_electricity_ele.text == water_electricity:
                water_electricity_ele.click()
                return True
        raise ValueError('传值错误')

    def input_house_keeper_company(self, house_keeper_company):
        if house_keeper_company == '':
            self.is_click(house_add_new_house['物业公司_暂无勾选框'])
        else:
            self.input_text(house_add_new_house['物业公司输入框'], house_keeper_company)

    def check_house_keeper_company_none(self):
        self.is_click(house_add_new_house['物业公司_暂无勾选框'])

    def input_house_keeper_price(self, house_keeper_price):
        if len(house_keeper_price) != 2:
            raise ValueError('传值错误')
        if house_keeper_price[0] == '' or house_keeper_price[1] == '':
            self.is_click(house_add_new_house['物业费_暂无勾选框'])
        else:
            self.input_text(house_add_new_house['物业费最小输入框'], house_keeper_price[0])
            self.input_text(house_add_new_house['物业费最大输入框'], house_keeper_price[1])

    def check_house_keeper_price_none(self):
        self.is_click(house_add_new_house['物业费_暂无勾选框'])

    def input_heating_type(self, heating_type):
        self.is_click(house_add_new_house['供暖方式选择框'])
        heating_type_list = self.find_elements(house_add_new_house['下拉框'])
        for heating_type_ele in heating_type_list:
            if heating_type_ele.text == heating_type:
                heating_type_ele.click()
                return True
        raise ValueError('传值错误')

    def input_house_keeper_type(self, house_keeper_type):
        self.is_click(house_add_new_house['物业类型选择框'])
        house_keeper_type_list = self.find_elements(house_add_new_house['下拉框'])
        for house_keeper_type_ele in house_keeper_type_list:
            if house_keeper_type_ele.text == house_keeper_type:
                house_keeper_type_ele.click()
                return True
        raise ValueError('传值错误')

    def click_up_step_button(self):
        self.is_click(house_add_new_house['上一步按钮'])

    def click_save_button(self):
        self.is_click(house_add_new_house['保存按钮'])
