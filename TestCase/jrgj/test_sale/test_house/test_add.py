#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_add.py
@time: 2021/06/22
"""
import pytest
import allure
from case_service.jrgj.web.house.house_service import HouseService
from config.conf import cm
from common.readconfig import ini
from utils.jsonutil import get_data
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.house.addpage import HouseAddPage

HOUSE_TYPE = 'sale'
gl_web_driver = None


@allure.feature("新增买卖房源模块")
class TestAddSaleHouse(object):
    json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_add.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global gl_web_driver
        gl_web_driver = web_driver
        self.main_up_view = MainUpViewPage(gl_web_driver)
        self.house_add_page = HouseAddPage(gl_web_driver)
        self.main_top_view = MainTopViewPage(gl_web_driver)
        self.main_left_view = MainLeftViewPage(gl_web_driver)
        self.house_table_page = HouseTablePage(gl_web_driver)
        yield
        self.main_up_view.clear_all_title()

    @allure.story("测试新增买卖房源，查看搜索结果用例")
    @pytest.mark.rent
    @pytest.mark.house
    @pytest.mark.run(order=1)
    # @pytest.mark.dependency()
    # @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_add(self):
        house_service = HouseService(gl_web_driver)  # 获取房源信息
        flag_dist = {'sale': "买卖", 'rent': "租赁"}
        get_house_info_flg = flag_dist[HOUSE_TYPE]
        house_info = house_service.get_house_info_by_db(get_house_info_flg)
        if len(house_info) != 0:  # 如房源已存在，不执行新增房源的操作
            house_service.check_house_state(house_info, HOUSE_TYPE)
            house_code = house_info[0]
            assert True
        else:
            self.main_left_view.click_all_house_label()
            self.house_table_page.click_add_house_button()  # 点击新增房源按钮
            assert self.house_add_page.check_sale_radio()  # 判断新增界面委托类型的默认勾选
            self.house_add_page.input_property_address('sale')  # 填写物业地址
            self.house_add_page.input_owner_info_and_house_info(self.test_data, 'sale')
            assert '新增成功' in self.main_top_view.find_notification_content()
            house_code = self.house_table_page.get_house_code_by_db(flag='买卖')
            assert house_code != ''
        self.main_left_view.click_all_house_label()
        self.house_table_page.choose_estate_name_search(ini.house_community_name)  # 验证搜索
        self.house_table_page.choose_building_name_search(ini.house_building_id)
        self.house_table_page.click_search_button()
        res = self.house_table_page.house_code_in_house_list(house_code)
        assert res
