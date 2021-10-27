#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: test_house_photo_album.py
@date: 2021/8/24
"""

import random
import pytest
import allure
from config.conf import cm
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from utils.jsonutil import get_data

house_table = None


@allure.feature("楼盘详情页-更多模块")
class TestMore(object):
    json_file_path = cm.test_data_dir + "/jrgj/test_new/test_house/test_add.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="function", autouse=True)
    def prepare(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        main_leftview.change_role('超级管理员')
        main_leftview.click_all_house_label()
        house_table = HouseTablePage(web_driver)
        house_table.click_new_tab()  # 点击新房tab
        house_table.input_building_name_search(self.test_data['楼盘名称'])
        house_table.click_search_button()
        house_table.go_new_house_detail_by_row()
        main_upview = MainUpViewPage(web_driver)
        yield
        main_upview.clear_all_title()

    @allure.story("测试发布楼盘动态")
    @pytest.mark.new
    @pytest.mark.house
    @pytest.mark.run(order=2)
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_release_house_trend(self, web_driver):
        house_detail = HouseDetailPage(web_driver)
        house_detail.click_see_more()
        house_detail.switch_tab_by_name('楼盘动态')
        trend_explain = house_detail.relese_house_trend_content('楼盘动态title', '楼盘动态最新')
        res = house_detail.verify_trend_list_update(trend_explain)
        assert res

    @allure.story("测试编辑楼盘卖点")
    @pytest.mark.new
    @pytest.mark.house
    @pytest.mark.run(order=2)
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_selling_point(self, web_driver):
        house_detail = HouseDetailPage(web_driver)
        house_detail.click_see_more()
        house_detail.switch_tab_by_name('楼盘卖点')
        push_plate = house_detail.edit_house_selling_point('距离地铁二号线100米', '四面通风大平层')
        actual_result = house_detail.verify_celling_point_list_update()
        expect_result = '一句话推盘：' + push_plate
        assert actual_result == expect_result

    @allure.story("测试上传户型介绍")
    @pytest.mark.new
    @pytest.mark.house
    @pytest.mark.run(order=2)
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_upload_house_type(self, web_driver):
        house_detail = HouseDetailPage(web_driver)
        initial_house_introduce_number = house_detail.get_house_type_introduce_number()
        house_detail.click_see_more()
        house_detail.switch_tab_by_name('户型介绍')
        house_detail.click_upload_house_type_btn()
        house_detail.house_type_introduce_content('经济型' + str(random.randint(1, 100)), '100', '南',
                                                  [cm.tmp_picture_file])
        expect_house_introduce_number = initial_house_introduce_number + 1
        house_detail.switch_tab_by_name('楼盘首页')
        actual_house_introduce_number = house_detail.get_house_type_introduce_number()
        assert actual_house_introduce_number == expect_house_introduce_number


if __name__ == '__main__':
    pytest.main(['-q', 'test_more.py'])
