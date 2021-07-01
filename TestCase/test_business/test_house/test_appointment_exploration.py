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
from page_object.main.maintopviewpage import MainTopViewPage
from page_object.main.mianleftviewpage import MainLeftViewPage
from page_object.house.housetablepage import HouseTablePage
from page_object.house.housedatailpage import HouseDetailPage


@allure.feature("测试房源模块")
class TestAppointmentExploration(object):

    json_file_path = cm.test_data_dir + "/test_business/test_house/test_appointment_exploration.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="class", autouse=True)
    def close_topview(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_topview.click_close_button()
        main_leftview.change_role('经纪人')
        main_topview.click_close_button()
        main_leftview.click_all_house_label()

    @allure.story("测试房源预约实勘用例")
    # @pytest.mark.business_house_update
    @pytest.mark.run(order=2)
    @pytest.mark.dependency(depends=['ui/TestCase/test_business/test_house/test_add.py::TestAdd::test_001'],
                            scope='session')
    def test_001(self, web_driver):

        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)

        main_leftview.click_all_house_label()
        house_table.click_reset_button()
        house_table.clear_filter()
        house_table.choose_estate_name_search(ini.house_community_name)
        house_table.choose_building_name_search(ini.house_building_id)
        house_table.click_search_button()
        house_table.go_house_detail_by_row()
        house_detail.click_exploration_button()
        house_detail.choose_normal_exploration()
        house_detail.choose_photographer(self.test_data['photographer'])
        house_detail.choose_exploration_time(self.test_data['exploration_time'])
        house_detail.input_appointment_instructions(self.test_data['appointment_instructions'])
        house_detail.click_exploration_confirm_button()
        log.info('预约实勘申请已提交')


if __name__ == '__main__':
    # pytest.main(["-v", "-s", "D:/PythonProject/UIAutomation/ui/TestCase/house/"])
    pytest.main(["-v", "-k", "house and not upload"])
