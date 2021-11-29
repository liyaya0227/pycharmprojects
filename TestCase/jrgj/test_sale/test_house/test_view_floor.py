#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_view_floor.py
@date: 2021/8/10 0010
"""
import pytest
import allure
from case_service.jrgj.web.house.house_service import HouseService
from common.readxml import ReadXml
from config.conf import cm
from page_object.jrgj.web.main.rightviewpage import MainRightViewPage
from utils.databaseutil import DataBaseUtil
from common.readconfig import ini
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from utils.jsonutil import get_data

HOUSE_TYPE = 'sale'
gl_driver = None
house_info = ''
house_sql = ReadXml("jrgj/house_sql")


@allure.feature("买卖房源详情模块-查看楼层")
class TestViewFloor(object):
    json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_add.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="class", autouse=True)
    def prepare_house(self, web_driver):
        global gl_driver, house_info
        gl_driver = web_driver
        house_service = HouseService(gl_driver)
        house_info = house_service.prepare_house(self.test_data, HOUSE_TYPE)

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self):
        self.house_table_page = HouseTablePage(gl_driver)
        self.house_detail_page = HouseDetailPage(gl_driver)
        self.main_up_view = MainUpViewPage(gl_driver)
        self.main_left_view = MainLeftViewPage(gl_driver)
        self.main_right_view = MainRightViewPage(gl_driver)
        yield
        self.main_up_view.clear_all_title()

    @allure.step("进入房源详情")
    def enter_house_detail(self):
        login_person_name = self.main_right_view.get_login_person_name()
        database_util = DataBaseUtil('SQL Server', ini.database_name)
        get_house_info = house_sql.get_sql('trade_house', 'get_house_info').format(account_name=login_person_name)
        house_info_list = database_util.select_sql(get_house_info)
        self.main_left_view.click_all_house_label()
        self.house_table_page.clear_filter(flag='买卖')
        for house in house_info_list:
            self.house_table_page.input_house_code_search(house[1])
            self.house_table_page.click_search_button()
            number = self.house_table_page.get_house_number()
            if int(number) > 0:
                self.house_table_page.go_house_detail_by_row(1)
                break

    @allure.story("测试房源详情右侧楼层用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=5)
    def test_view_floor(self):
        self.enter_house_detail()
        self.house_detail_page.click_floor_button()
        dialog_detail_floor_info = self.house_detail_page.get_floor_dialog_detail_floor()
        self.house_detail_page.dialog_click_close_button()
        assert dialog_detail_floor_info != ''
