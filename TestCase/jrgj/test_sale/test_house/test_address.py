#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_address.py
@date: 2021/8/10 0010
"""
import pytest
import allure
from config.conf import cm
from page_object.common.web.login.loginpage import LoginPage
from common.readconfig import ini
from utils.jsonutil import get_value
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.house.addpage import HouseAddPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage

house_code = ''
gl_driver = None


@allure.feature("测试房源模块")
class TestAddress(object):
    json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_address.json"
    account = get_value(json_file_path, ini.environment)
    main_up_view = None
    main_left_view = None
    main_top_view = None
    house_add_page = None
    house_table_page = None
    house_detail_page = None

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global gl_driver
        gl_driver = web_driver
        self.main_left_view = MainLeftViewPage(gl_driver)
        self.main_up_view = MainUpViewPage(gl_driver)
        self.main_top_view = MainTopViewPage(gl_driver)
        self.house_add_page = HouseAddPage(gl_driver)
        self.house_table_page = HouseTablePage(gl_driver)
        self.house_detail_page = HouseDetailPage(gl_driver)
        yield
        self.main_up_view.clear_all_title()

    @allure.step("验证房源状态")
    def check_house_state(self):
        global house_code
        if self.house_table_page.get_house_code_by_db(flag='买卖') == '':  # 判断房源是否存在，不存在则新增
            self.main_left_view.click_all_house_label()
            self.house_table_page.click_sale_tab()
            self.house_table_page.click_add_house_button()
            self.house_add_page.choose_sale_radio()
            self.house_add_page.choose_estate_name(ini.house_community_name)  # 填写物业地址信息
            self.house_add_page.choose_building_id(ini.house_building_id)
            self.house_add_page.choose_building_cell(ini.house_building_cell)
            self.house_add_page.choose_floor(ini.house_floor)
            self.house_add_page.choose_doorplate(ini.house_doorplate)
            self.house_add_page.click_next_button()
            self.house_add_page.input_owner_info_and_house_info(self.house_data, '买卖')
            self.main_up_view.clear_all_title()
        house_code = self.house_table_page.get_house_code_by_db(flag='买卖')

    @allure.story("测试房源详情右侧地址用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=11)
    def test_view_address(self):
        self.check_house_state()
        self.main_left_view.change_role('经纪人')
        self.main_left_view.click_all_house_label()
        self.house_table_page.click_sale_tab()
        self.house_table_page.click_all_house_tab()
        self.house_table_page.click_reset_button()
        self.house_table_page.clear_filter(flag='买卖')
        self.house_table_page.input_house_code_search(house_code)
        self.house_table_page.click_search_button()
        self.house_table_page.go_house_detail_by_row(1)
        self.house_detail_page.click_address_button()
        assert not self.house_detail_page.dialog_looked_count_exist()
        self.house_detail_page.dialog_click_close_button()

    @allure.story("测试房源详情右侧地址用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=11)
    def test_view_address_maximum(self):
        self.check_house_state()
        login = LoginPage(gl_driver)
        self.main_left_view.log_out()
        login.log_in(self.account[0], self.account[1])
        self.main_left_view.change_role('经纪人')
        self.main_left_view.click_all_house_label()
        self.house_table_page.click_sale_tab()
        self.house_table_page.click_all_house_tab()
        self.house_table_page.click_reset_button()
        self.house_table_page.clear_filter(flag='买卖')
        self.house_table_page.input_house_code_search(house_code)
        self.house_table_page.click_search_button()
        self.house_table_page.go_house_detail_by_row(1)
        self.house_detail_page.click_address_button()
        dialog_content = self.main_top_view.find_notification_content()
        if dialog_content == '':
            looked_count = self.house_detail_page.dialog_get_looked_count()
            self.house_detail_page.dialog_click_close_button()
            if looked_count == 1:
                assert self.house_detail_page.follow_dialog_exist()
            if self.house_detail_page.follow_dialog_exist():
                assert self.house_detail_page.check_dialog_cancel_button_disabled()
                self.house_detail_page.follow_dialog_input_detail_follow('详细跟进信息')
                self.house_detail_page.dialog_click_confirm_button()
                assert self.main_top_view.find_notification_content() == '编辑成功'
            temp = looked_count
            for _ in range(60 - int(looked_count)):
                self.house_detail_page.click_address_button()
                new_looked_count = self.house_detail_page.dialog_get_looked_count()
                self.house_detail_page.dialog_click_close_button()
                assert int(new_looked_count) == int(temp) + 1
                temp = new_looked_count
            self.house_detail_page.click_address_button()
            dialog_content = self.main_top_view.find_notification_content()
        if self.house_detail_page.check_shopowner_recommend() or self.house_detail_page.get_vip_person() != '':
            assert dialog_content == '请联系维护人查看相关房源信息'
        else:
            assert dialog_content == '今日查看次数已经超过60次'
