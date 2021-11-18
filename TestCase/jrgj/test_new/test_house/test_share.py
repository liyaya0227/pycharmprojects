#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: test_share.py
@date: 2021/8/24
"""

import pytest
import allure
from config.conf import cm
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.rightviewpage import MainRightViewPage
from utils.jsonutil import get_data

person_info = {}
gl_web_driver = None


@allure.feature("测试分享新房源功能模块")
class TestShare(object):

    json_file_path = cm.test_data_dir + "/jrgj/test_new/test_house/test_add.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global gl_web_driver
        gl_web_driver = web_driver
        self.main_left_view = MainLeftViewPage(gl_web_driver)
        self.main_right_view = MainRightViewPage(web_driver)
        self.house_table_page = HouseTablePage(gl_web_driver)
        self.house_detail_page = HouseDetailPage(gl_web_driver)
        yield
        self.main_up_view.clear_all_title()

    @allure.step("进入房源详情")
    def enter_house_detail(self):
        global person_info
        self.main_left_view.change_role('超级管理员')
        login_name = self.main_right_view.get_login_person_name()
        login_phone = self.main_right_view.get_login_person_phone()
        person_info = {'姓名': login_name, '电话': login_phone}
        self.main_left_view.click_all_house_label()
        self.house_table_page.click_new_tab()
        self.house_table_page.click_off_shelf_house_tab()
        self.house_table_page.input_building_name_search(self.test_data['楼盘名称'])
        self.house_table_page.click_search_button()
        self.house_table_page.go_new_house_detail_by_row()

    @allure.story("测试分享功能")
    @pytest.mark.new
    @pytest.mark.house
    @pytest.mark.run(order=3)
    # @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_share_house(self):
        house_type_in_detail_page = self.house_detail_page.get_house_type_in_detail_page()
        self.house_detail_page.click_share_btn()
        login_name = person_info['姓名']
        login_phone = person_info['电话']
        house_type, account_name, account_phone = self.house_detail_page.get_information_in_share_page()
        self.house_detail_page.choose_image_in_share_page()
        self.house_detail_page.click_generate_code_btn()
        res = self.house_detail_page.verify_generate_code_success()
        pytest.assume(house_type_in_detail_page == house_type)
        pytest.assume(login_phone == account_phone)
        pytest.assume(login_name == account_name)
        pytest.assume(res is True)










