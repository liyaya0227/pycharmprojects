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
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.rightviewpage import MainRightViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.house.addnewhousepage import HouseAddNewHousePage

person_info = {}
driver = None


@allure.feature("测试新房源新增楼盘模块")
class TestAdd(object):
    json_file_path = cm.test_data_dir + "/jrgj/test_new/test_house/test_add.json"
    test_data = get_data(json_file_path)
    main_left_view = None

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global person_info, driver
        driver = web_driver
        self.house_table = HouseTablePage(driver)
        self.main_up_view = MainUpViewPage(driver)
        self.main_top_view = MainTopViewPage(driver)
        self.main_left_view = MainLeftViewPage(driver)
        self.main_right_view = MainRightViewPage(driver)
        self.add_house_page = HouseAddNewHousePage(driver)
        self.main_left_view.change_role('超级管理员')
        login_name = self.main_right_view.get_login_person_name()
        login_phone = self.main_right_view.get_login_person_phone()
        person_info = {'姓名': login_name, '电话': login_phone}
        self.main_left_view.click_all_house_label()
        yield
        self.main_up_view.clear_all_title()

    @allure.step("验证房源状态")
    def check_house_state(self, house_name):
        self.house_table.click_new_tab()  # 点击新房tab
        self.house_table.click_all_house_tab()
        self.house_table.click_reset_button()
        self.house_table.clear_filter(flag='新房')
        self.house_table.input_building_name_search(self.test_data['楼盘名称'])
        self.house_table.click_search_button()
        if self.house_table.get_house_table_count() != 0:  # 删除已存在的新房
            self.house_table.click_delete_button_by_row(1)
            self.house_table.dialog_click_confirm_button()
            assert self.main_top_view.find_notification_content() == '删除成功'
        self.house_table.click_off_shelf_house_tab()
        self.house_table.click_reset_button()
        self.house_table.clear_filter(flag='新房')
        self.house_table.input_building_name_search(self.test_data['楼盘名称'])
        self.house_table.click_search_button()
        if self.house_table.get_house_table_count() != 0:
            self.house_table.click_delete_button_by_row(1)
            self.house_table.dialog_click_confirm_button()
            assert self.main_top_view.find_notification_content() == '删除成功'

    @allure.story("测试新增新房楼盘，查看搜索结果用例")
    @pytest.mark.new
    @pytest.mark.house
    @pytest.mark.run(order=1)
    @pytest.mark.dependency()
    # @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_add(self):
        self.check_house_state(self.test_data['楼盘名称'])
        self.house_table.click_add_new_house_button()
        self.add_house_page.input_building_name(self.test_data['楼盘名称'])
        self.add_house_page.input_building_discount(self.test_data['楼盘优惠'])
        self.add_house_page.choose_building_source_from(self.test_data['房源渠道'])
        self.add_house_page.choose_whether_show_outside(self.test_data['是否外网呈现'])
        self.add_house_page.input_reported_protect_time(self.test_data['报备保护时间'])
        self.add_house_page.input_take_look_protect_time(self.test_data['带看保护时间'])
        self.add_house_page.input_incentive_policy(self.test_data['激励政策'])
        self.add_house_page.add_r_person([person_info])
        self.add_house_page.add_s_person([person_info])
        self.add_house_page.add_d_person([person_info])
        self.add_house_page.click_next_step_button()
        self.add_house_page.input_developer(self.test_data['开发商'])
        self.add_house_page.input_building_sale_price(self.test_data['楼盘价格'])
        self.add_house_page.choose_building_status(self.test_data['楼盘状态'])
        self.add_house_page.input_making_room_time(self.test_data['交房时间'])
        self.add_house_page.input_start_sale_time(self.test_data['开盘时间'])
        self.add_house_page.input_building_address(self.test_data['楼盘地址'])
        self.add_house_page.input_building_project_address(self.test_data['项目地址'])
        self.add_house_page.input_building_sale_address(self.test_data['售楼处地址'])
        self.add_house_page.choose_building_position()
        self.add_house_page.choose_building_type(self.test_data['建筑类型'])
        self.add_house_page.choose_property_year(self.test_data['产权年限'])
        self.add_house_page.input_plot_ratio(self.test_data['容积率'])
        self.add_house_page.input_afforestation_rate(self.test_data['绿化率'])
        self.add_house_page.input_planning_number(self.test_data['规划户数'])
        self.add_house_page.input_planning_parking_space(self.test_data['规划车位'])
        self.add_house_page.input_water_electricity(self.test_data['水电燃气'])
        self.add_house_page.input_house_keeper_company(self.test_data['物业公司'])
        self.add_house_page.input_house_keeper_price(self.test_data['物业费'])
        self.add_house_page.input_heating_type(self.test_data['供暖方式'])
        self.add_house_page.input_house_keeper_type(self.test_data['物业类型'])
        self.add_house_page.click_save_button()
        assert self.main_top_view.find_notification_content() == '添加成功'
        self.main_up_view.clear_all_title()
        self.main_left_view.click_all_house_label()
        self.house_table.click_new_tab()
        self.house_table.click_all_house_tab()
        self.house_table.click_reset_button()
        self.house_table.clear_filter(flag='新房')
        self.house_table.input_building_name_search(self.test_data['楼盘名称'])
        self.house_table.click_search_button()
        assert self.house_table.get_house_table_count() == 1
        self.main_up_view.clear_all_title()
