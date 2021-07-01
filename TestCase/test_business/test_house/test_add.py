#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_add.py
@time: 2021/06/22
"""

import re
import pytest
import allure
from utils.logger import log
from common.readconfig import ini
from config.conf import cm
from utils.jsonutil import get_data
from page_object.main.maintopviewpage import MainTopViewPage
from page_object.main.mianleftviewpage import MainLeftViewPage
from page_object.main.mainrightviewpage import MainRightViewPage
from page_object.main.invalidhousepage import InvalidHousePage
from page_object.house.housetablepage import HouseTablePage
from page_object.house.houseaddpage import HouseAddPage
from page_object.house.housedatailpage import HouseDetailPage


@allure.feature("测试房源模块")
class TestAdd(object):

    json_file_path = cm.test_data_dir + "/test_business/test_house/test_add.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="class", autouse=True)
    def close_topview(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_topview.click_close_button()
        main_leftview.change_role('经纪人')
        main_topview.click_close_button()
        main_leftview.click_all_house_label()

    @allure.story("测试新增房源，查看搜索结果用例")
    # @pytest.mark.business_house_add
    @pytest.mark.run(order=1)
    @pytest.mark.dependency()
    @pytest.mark.flaky(reruns=5, reruns_delay=2)
    def test_001(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_rightview = MainRightViewPage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        house_table = HouseTablePage(web_driver)
        invalid_house_page = InvalidHousePage(web_driver)
        house_add = HouseAddPage(web_driver)

        house_table.click_add_house_button()
        house_add.choose_sale_radio()
        house_add.choose_estate_name(ini.house_community_name)
        house_add.choose_building_id(ini.house_building_id)
        house_add.choose_building_cell(ini.house_building_cell)
        house_add.choose_floor(ini.house_floor)
        house_add.choose_doorplate(ini.house_doorplate)
        house_add.choose_sale_radio()
        house_add.click_next_button()
        content = main_topview.find_notification_title()
        if content != '':
            log.info('房源已存在')
            house_code = re.search(r"房源编号(\d+?)，", content).group(1)
            main_leftview.click_all_house_label()
            house_table.clear_filter()
            house_table.input_house_code_search(house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row()
            house_detail.click_invalid_house_button()
            house_detail.input_invalid_reason("测试需要")
            house_detail.click_invalid_reason_confirm_button()
            content = main_topview.find_notification_title()
            if content == '错误':
                log.info('无效申请已提交')
                house_detail.click_invalid_reason_cancel_button()
            main_leftview.change_role('超级管理员')
            main_rightview.click_invalid_house()
            invalid_house_page.click_pass_by_housecode(house_code)
            invalid_house_page.click_invalid_house_confirm_button()
            content = main_topview.find_notification_title()
            if content != '成功':
                invalid_house_page.click_pass_by_housecode(house_code)
                invalid_house_page.click_invalid_house_confirm_button()
            main_leftview.change_role('经纪人')
            main_leftview.click_all_house_label()
            house_table.click_add_house_button()
            house_add.choose_rent_radio()
            house_add.choose_estate_name(ini.house_community_name)
            house_add.choose_building_id(ini.house_building_id)
            house_add.choose_building_cell(ini.house_building_cell)
            house_add.choose_floor(ini.house_floor)
            house_add.choose_doorplate(ini.house_doorplate)
            house_add.choose_sale_radio()
            house_add.click_next_button()
        log.info('填写物业地址成功')
        house_add.input_house_owner_name(self.test_data['house_owner_name'])
        house_add.input_house_owner_phone(self.test_data['house_owner_phone'])
        log.info('填写业主信息成功')
        house_add.choose_house_type(self.test_data['house_types'])
        house_add.input_area(self.test_data['area'])
        house_add.choose_orientations(self.test_data['orientations'])
        house_add.input_sale_price(self.test_data['sale_price'])
        house_add.choose_inspect_type(self.test_data['inspect_type'])
        house_add.click_add_button()
        log.info('填写房源信息成功')
        main_leftview.click_all_house_label()
        house_table.choose_estate_name_search(ini.house_community_name)
        house_table.choose_building_name_search(ini.house_building_id)
        house_table.click_search_button()
        assert house_table.get_house_table_count() == 1
        log.info('搜索结果正确')


if __name__ == '__main__':
    pytest.main(["-v", "-s", "D:/PythonProject/UIAutomation/ui/TestCase/test_business/test_house/test_add.py"])
    # pytest.main(["-v", "-k", "house and not upload"])
