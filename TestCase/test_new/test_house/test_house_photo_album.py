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
from utils.logger import log

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
        # house_table.input_building_name_search('露露露楼盘')
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
        count = 0
        house_detail = HouseDetailPage(web_driver)
        house_detail.click_see_more()
        initial_number = house_detail.get_image_list_lenth()
        house_detail.go_upload_album()
        house_detail.upload_image([cm.tmp_picture_file],'效果图')
        count += 1
        house_detail.upload_image([cm.tmp_picture_file], '实景图')
        count += 1
        house_detail.upload_image([cm.tmp_picture_file], '位置图')
        count += 1
        house_detail.click_upload_btn()
        actual_result = house_detail.get_dialog_text()
        actual_number = house_detail.get_image_list_lenth()
        # print('test_upload_photo', count)
        # print('test_upload_photo:actual_number', actual_number)
        if actual_result == '上传成功':
            assert True
        else:
            log.error('图片上传操作失败')
            assert False
        if initial_number == 0:
            if actual_number == count:
                assert True
        else:
            if actual_number == count + initial_number -1:
                assert True

    @allure.story("测试批量删除,默认删除第一张")
    @pytest.mark.new
    @pytest.mark.house
    @pytest.mark.run(order=3)
    # @pytest.mark.flaky(reruns=2, reruns_delay=2)
    def test_batch_delete(self, web_driver):
        house_detail = HouseDetailPage(web_driver)
        house_detail.click_see_more()
        initial_number = house_detail.get_image_list_lenth()
        print('test_batch_delete:initial_number',initial_number)
        house_detail.click_batch_delete_btn()
        house_detail.select_some_image_to_delete()
        deleted_number = house_detail.get_deleted_image_number()
        print('test_batch_delete:deleted_number', deleted_number)
        house_detail.click_delete_btn()
        actual_result = house_detail.get_dialog_text()
        actual_number = house_detail.get_image_list_lenth()
        expect_number = initial_number - deleted_number
        print('test_batch_delete:actual_number',actual_number)
        print('test_batch_delete:expect_number',expect_number)
        if actual_result == '删除成功':
            assert True
        else:
            log.error('批量删除操作执行失败')
            assert False
        if expect_number == actual_number:
            assert True

    @allure.story("测试全部删除")
    @pytest.mark.new
    @pytest.mark.house
    @pytest.mark.run(order=3)
    # @pytest.mark.flaky(reruns=2, reruns_delay=2)
    def test_delete_all(self, web_driver):
        house_detail = HouseDetailPage(web_driver)
        house_detail.click_see_more()
        house_detail.click_batch_delete_btn()
        house_detail.select_all_image_to_delete()
        house_detail.click_delete_btn()
        actual_result = house_detail.get_dialog_text()
        actual_number = house_detail.get_image_list_lenth()
        print('test_batch_delete:actual_number', actual_number)
        if actual_result == '删除成功':
            assert True
        if actual_number == 1:
            assert True
        else:
            log.error('相册列表更新失败')
            assert False


if __name__ == '__main__':
    pytest.main(['-q', 'test_house_photo_album.py'])














