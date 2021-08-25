#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: test_house_photo_album.py
@date: 2021/8/24
"""

import pytest
import allure
from config.conf import cm
from page_object.web.house.detailpage import HouseDetailPage
from page_object.web.house.tablepage import HouseTablePage
from page_object.web.main.leftviewpage import MainLeftViewPage
from page_object.web.main.upviewpage import MainUpViewPage
from utils.jsonutil import get_data

house_table = None
@allure.feature("测试楼盘动态功能模块")
class TestReleaseHouseTrend(object):

    json_file_path = cm.test_data_dir + "/test_new/test_house/test_add.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="function", autouse=True)
    def prepare(self, web_driver):
        global house_table
        main_leftview = MainLeftViewPage(web_driver)
        main_leftview.change_role('超级管理员')
        main_leftview.click_all_house_label()
        house_table = HouseTablePage(web_driver)
        house_table.click_new_tab()  # 点击新房tab
        house_table.input_building_name_search(self.test_data['楼盘名称'])
        house_table.click_search_button()
        house_table.go_new_house_detail_by_row()
        # main_upview = MainUpViewPage(web_driver)
        # yield
        # main_upview.clear_all_title()

    @allure.story("测试上传楼盘相册")
    @pytest.mark.new
    @pytest.mark.house
    @pytest.mark.run(order=2)
    # @pytest.mark.flaky(reruns=2, reruns_delay=2)
    def test_release_house_trend(self, web_driver):
        house_detail = HouseDetailPage(web_driver)
        house_detail.click_see_more()
        house_detail.switch_tab_by_name('楼盘动态')
        trend_explain = house_detail.relese_house_trend_content('楼盘动态title','楼盘动态最新')
        res = house_detail.verify_trend_list_update(trend_explain)
        assert res



    # @allure.story("测试批量删除")
    # @pytest.mark.new
    # @pytest.mark.house
    # @pytest.mark.run(order=3)
    # # @pytest.mark.flaky(reruns=2, reruns_delay=2)
    # def test_batch_delete(self, web_driver):
    #     house_detail = HouseDetailPage(web_driver)
    #     house_detail.click_see_more()
    #     house_detail.click_batch_delete_btn()
    #     house_detail.click_select_all_btn()
    #     house_detail.click_delete_btn()
    #     actual_result = house_detail.get_dialog_text()
    #     if actual_result == '删除成功':
    #         assert True


if __name__ == '__main__':
    pytest.main(['-q', 'test_house_photo_album.py'])














