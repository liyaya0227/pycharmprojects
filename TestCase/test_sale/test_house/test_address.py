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
from utils.logger import log
from common.readconfig import ini
from utils.jsonutil import get_value
from page_object.web.main.upviewpage import MainUpViewPage
from page_object.web.house.addpage import HouseAddPage
from page_object.web.main.topviewpage import MainTopViewPage
from page_object.web.main.leftviewpage import MainLeftViewPage
from page_object.web.login.loginpage import LoginPage
from page_object.web.house.tablepage import HouseTablePage
from page_object.web.house.detailpage import HouseDetailPage

house_code = ''


@allure.feature("测试房源模块")
class TestAddress(object):
    json_file_path = cm.test_data_dir + "/test_sale/test_house/test_address.json"
    account = get_value(json_file_path, ini.environment)

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global house_code

        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        house_add = HouseAddPage(web_driver)
        house_table = HouseTablePage(web_driver)

        main_leftview.change_role('经纪人')
        house_code = house_table.get_house_code_by_db(flag='买卖')
        if house_table.get_house_code_by_db(flag='买卖') == '':  # 判断房源是否存在，不存在则新增
            main_leftview.click_all_house_label()
            house_table.click_sale_tab()
            house_table.click_add_house_button()
            house_add.choose_sale_radio()
            house_add.choose_estate_name(ini.house_community_name)  # 填写物业地址信息
            house_add.choose_building_id(ini.house_building_id)
            house_add.choose_building_cell(ini.house_building_cell)
            house_add.choose_floor(ini.house_floor)
            house_add.choose_doorplate(ini.house_doorplate)
            house_add.click_next_button()
            house_add.input_owner_info_and_house_info(self.house_data, '买卖')
            main_upview.clear_all_title()
        main_leftview.click_all_house_label()
        house_code = house_table.get_house_code_by_db(flag='买卖')
        assert house_code != ''
        log.info('房源编号为：' + house_code)
        yield
        main_upview.clear_all_title()

    @allure.story("测试房源详情右侧地址用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=11)
    def test_001(self, web_driver):
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)

        main_leftview.change_role('经纪人')
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter(flag='买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        house_detail.click_address_button()
        assert not house_detail.dialog_looked_count_exist()
        house_detail.dialog_click_close_button()

    @allure.story("测试房源详情右侧地址用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=11)
    def test_002(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        login = LoginPage(web_driver)

        main_leftview.log_out()
        login.log_in(self.account[0], self.account[1])
        main_leftview.change_role('经纪人')
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter(flag='买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        house_detail.click_address_button()
        dialog_content = main_topview.find_notification_content()
        if dialog_content == '':
            looked_count = house_detail.dialog_get_looked_count()
            house_detail.dialog_click_close_button()
            if looked_count == 1:
                assert house_detail.follow_dialog_exist()
            if house_detail.follow_dialog_exist():
                assert house_detail.check_dialog_cancel_button_disabled()
                house_detail.follow_dialog_input_detail_follow('详细跟进信息')
                house_detail.dialog_click_confirm_button()
                assert main_topview.find_notification_content() == '编辑成功'
            temp = looked_count
            for _ in range(60 - int(looked_count)):
                house_detail.click_address_button()
                new_looked_count = house_detail.dialog_get_looked_count()
                house_detail.dialog_click_close_button()
                assert int(new_looked_count) == int(temp) + 1
                temp = new_looked_count
            house_detail.click_address_button()
            dialog_content = main_topview.find_notification_content()
        if house_detail.check_shopowner_recommend() or house_detail.get_vip_person() != '':
            assert dialog_content == '请联系维护人查看相关房源信息'
        else:
            assert dialog_content == '今日查看次数已经超过60次'
