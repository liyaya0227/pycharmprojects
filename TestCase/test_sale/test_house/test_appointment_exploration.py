#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_appointment_exploration.py
@time: 2021/06/22
"""

import pytest
import allure
from utils.logger import log
from common.readconfig import ini
from config.conf import cm
from utils.jsonutil import get_data
from page_object.main.topviewpage import MainTopViewPage
from page_object.main.leftviewpage import MainLeftViewPage
from page_object.main.upviewpage import MainUpViewPage
from page_object.house.tablepage import HouseTablePage
from page_object.house.detailpage import HouseDetailPage

house_code = ''


@allure.feature("测试房源模块")
class TestAppointmentExploration(object):

    json_file_path = cm.test_data_dir + "/test_sale/test_house/test_appointment_exploration.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="class", autouse=True)
    def test_prepare(self, web_driver):
        global house_code

        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)

        main_leftview.change_role('经纪人')
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter(flag='买卖')
        house_table.choose_estate_name_search(ini.house_community_name)
        house_table.choose_building_name_search(ini.house_building_id)
        house_table.click_search_button()
        table_count = house_table.get_house_table_count()
        assert table_count > 0
        for row in range(table_count):
            house_table.go_house_detail_by_row(row + 1)
            house_property_address = house_detail.get_house_property_address()
            if house_property_address['estate_name'] == ini.house_community_name \
                    and house_property_address['building_name'] == ini.house_building_id \
                    and house_property_address['door_name'] == ini.house_doorplate:
                house_code = house_detail.get_house_code()
                main_upview.close_title_by_name(house_property_address['estate_name'])
                break
            main_upview.close_title_by_name(house_property_address['estate_name'])
            house_table.click_reset_button()
            house_table.clear_filter('买卖')
            house_table.choose_estate_name_search(ini.house_community_name)
            house_table.choose_building_name_search(ini.house_building_id)
            house_table.click_search_button()
        assert house_code != ''
        log.info('房源编号: ' + house_code)
        main_upview.clear_all_title()
        main_leftview.click_all_house_label()

    @allure.story("测试房源预约实勘用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=2)
    def test_001(self, web_driver):
        main_upview = MainUpViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)

        house_table.click_sale_tab()
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter(flag='买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        if house_detail.check_exploration():
            log.info('实勘已预约,实勘退单')
            house_detail.click_back_exploration_button()
            house_detail.choose_back_exploration_reason('其他')
            house_detail.click_back_exploration_return_button()
            assert main_topview.wait_notification_content_exist() == '退单成功'
        house_detail.click_exploration_button()
        house_detail.choose_normal_exploration()
        house_detail.choose_photographer(self.test_data['photographer'])
        house_detail.choose_exploration_time(self.test_data['exploration_time'])
        house_detail.input_appointment_instructions(self.test_data['appointment_instructions'])
        house_detail.click_exploration_confirm_button()
        log.info('预约实勘申请已提交')
        main_upview.clear_all_title()
