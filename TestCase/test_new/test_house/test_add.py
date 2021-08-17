#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_add.py
@date: 2021/7/19 0019
"""

import pytest
import allure
from config.conf import cm
from utils.jsonutil import get_data
from page_object.main.topviewpage import MainTopViewPage
from page_object.main.rightviewpage import MainRightViewPage
from page_object.main.leftviewpage import MainLeftViewPage
from page_object.main.upviewpage import MainUpViewPage
from page_object.house.tablepage import HouseTablePage
from page_object.house.addnewhousepage import HouseAddNewHousePage

person_info = {}


@allure.feature("测试新房源新增楼盘模块")
class TestAdd(object):

    json_file_path = cm.test_data_dir + "/test_new/test_house/test_add.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global person_info

        main_leftview = MainLeftViewPage(web_driver)
        main_rightview = MainRightViewPage(web_driver)

        main_leftview.change_role('超级管理员')
        login_name = main_rightview.get_login_person_name()
        login_phone = main_rightview.get_login_person_phone()
        person_info = {'姓名': login_name, '电话': login_phone}
        main_leftview.click_all_house_label()

    @allure.story("测试新增新房楼盘，查看搜索结果用例")
    @pytest.mark.new
    @pytest.mark.house
    @pytest.mark.run(order=1)
    @pytest.mark.dependency()
    @pytest.mark.flaky(reruns=5, reruns_delay=2)
    def test_001(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_add_new_house = HouseAddNewHousePage(web_driver)

        house_table.click_new_tab()  # 点击新房tab
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter(flag='新房')
        house_table.input_building_name_search(self.test_data['楼盘名称'])
        house_table.click_search_button()
        if house_table.get_house_table_count() != 0:
            house_table.click_delete_button_by_row(1)
            house_table.dialog_click_confirm_button()
            assert main_topview.find_notification_content() == '删除成功'
        house_table.click_off_shelf_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter(flag='新房')
        house_table.input_building_name_search(self.test_data['楼盘名称'])
        house_table.click_search_button()
        if house_table.get_house_table_count() != 0:
            house_table.click_delete_button_by_row(1)
            house_table.dialog_click_confirm_button()
            assert main_topview.find_notification_content() == '删除成功'
        house_table.click_add_new_house_button()
        house_add_new_house.input_building_name(self.test_data['楼盘名称'])
        house_add_new_house.input_building_discount(self.test_data['楼盘优惠'])
        house_add_new_house.choose_building_source_from(self.test_data['房源渠道'])
        house_add_new_house.choose_whether_show_outside(self.test_data['是否外网呈现'])
        house_add_new_house.input_reported_protect_time(self.test_data['报备保护时间'])
        house_add_new_house.input_take_look_protect_time(self.test_data['带看保护时间'])
        house_add_new_house.input_incentive_policy(self.test_data['激励政策'])
        house_add_new_house.add_r_person([person_info])
        house_add_new_house.add_s_person([person_info])
        house_add_new_house.add_d_person([person_info])
        house_add_new_house.click_next_step_button()
        house_add_new_house.input_developer(self.test_data['开发商'])
        house_add_new_house.input_building_sale_price(self.test_data['楼盘价格'])
        house_add_new_house.choose_building_status(self.test_data['楼盘状态'])
        house_add_new_house.input_making_room_time(self.test_data['交房时间'])
        house_add_new_house.input_start_sale_time(self.test_data['开盘时间'])
        house_add_new_house.input_building_address(self.test_data['楼盘地址'])
        house_add_new_house.input_building_project_address(self.test_data['项目地址'])
        house_add_new_house.input_building_sale_address(self.test_data['售楼处地址'])
        house_add_new_house.choose_building_position()
        house_add_new_house.choose_building_type(self.test_data['建筑类型'])
        house_add_new_house.choose_property_year(self.test_data['产权年限'])
        house_add_new_house.input_plot_ratio(self.test_data['容积率'])
        house_add_new_house.input_afforestation_rate(self.test_data['绿化率'])
        house_add_new_house.input_planning_number(self.test_data['规划户数'])
        house_add_new_house.input_planning_parking_space(self.test_data['规划车位'])
        house_add_new_house.input_water_electricity(self.test_data['水电燃气'])
        house_add_new_house.input_house_keeper_company(self.test_data['物业公司'])
        house_add_new_house.input_house_keeper_price(self.test_data['物业费'])
        house_add_new_house.input_heating_type(self.test_data['供暖方式'])
        house_add_new_house.input_house_keeper_type(self.test_data['物业类型'])
        house_add_new_house.click_save_button()
        assert main_topview.find_notification_content() == '添加成功'
        main_upview.clear_all_title()
        main_leftview.click_all_house_label()
        house_table.click_new_tab()
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter(flag='新房')
        house_table.input_building_name_search(self.test_data['楼盘名称'])
        house_table.click_search_button()
        assert house_table.get_house_table_count() == 1
