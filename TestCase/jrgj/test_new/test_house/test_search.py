#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: test_search.py
@date: 2021/8/24
"""
import pytest
import allure
from common.readconfig import ini
from config.conf import cm
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from utils.jsonutil import get_data


gl_web_driver = None


@allure.feature("京日管家新房房源-搜索")
class TestSearch(object):
    json_file_path = cm.test_data_dir + "/jrgj/test_new/test_house/test_add.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global gl_web_driver
        gl_web_driver = web_driver
        self.main_left_view = MainLeftViewPage(web_driver)
        self.house_table_page = HouseTablePage(web_driver)

    @allure.story("测试根据新房类型、区域等字段搜索新房功能")
    @pytest.mark.new
    @pytest.mark.house
    @pytest.mark.run(order=2)
    # @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_search_house(self, web_driver):
        self.main_left_view.change_role('超级管理员')
        self.main_left_view.click_all_house_label()
        self.house_table_page.click_new_tab()  # 点击新房tab
        if self.test_data['是否外网呈现'] == '是':  # 根据创建时是否外网呈现，确定所属种类
            self.house_table_page.click_all_house_tab()
        else:
            self.house_table_page.click_off_shelf_house_tab()
        area = ini.environment
        if area == 'sz':
            option = '工业园区'
        elif area == 'wx':
            option = '江阴市'
        else:
            option = '桐庐'
        self.house_table_page.choose_option('区域', option)
        self.house_table_page.choose_option('类型', self.test_data['楼盘状态'])
        self.house_table_page.choose_option('房源渠道', self.test_data['房源渠道'])
        self.house_table_page.click_search_button()
        assert self.house_table_page.verify_house_exist(self.test_data['楼盘名称'])


if __name__ == '__main__':
    pytest.main(['-q', 'test_serch.py'])
