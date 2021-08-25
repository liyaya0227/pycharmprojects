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
@allure.feature("测试楼盘相册功能模块")
class TestHousePhotoAlbum(object):

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
        # house_table.input_building_name_search('悦云庭')
        house_table.click_search_button()
        house_table.go_new_house_detail_by_row()
        main_upview = MainUpViewPage(web_driver)
        yield
        main_upview.clear_all_title()

    @allure.story("测试上传楼盘相册")
    @pytest.mark.new
    @pytest.mark.house
    @pytest.mark.run(order=2)
    # @pytest.mark.flaky(reruns=2, reruns_delay=2)
    def test_upload_photo(self, web_driver):
        house_detail = HouseDetailPage(web_driver)
        house_detail.click_see_more()
        house_detail.go_upload_album()
        house_detail.upload_first_image([cm.tmp_picture_file])
        house_detail.upload_real_map_image([cm.tmp_picture_file])
        house_detail.click_upload_btn()
        actual_result = house_detail.get_dialog_text()
        if actual_result == '上传成功':
            assert True

    @allure.story("测试批量删除")
    @pytest.mark.new
    @pytest.mark.house
    @pytest.mark.run(order=3)
    # @pytest.mark.flaky(reruns=2, reruns_delay=2)
    def test_batch_delete(self, web_driver):
        house_detail = HouseDetailPage(web_driver)
        house_detail.click_see_more()
        house_detail.click_batch_delete_btn()
        house_detail.click_select_all_btn()
        house_detail.click_delete_btn()
        actual_result = house_detail.get_dialog_text()
        if actual_result == '删除成功':
            assert True


if __name__ == '__main__':
    pytest.main(['-q', 'test_house_photo_album.py'])














