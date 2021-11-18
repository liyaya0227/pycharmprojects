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
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from utils.jsonutil import get_data
from utils.logger import logger

gl_web_driver = None


@allure.feature("京日管家新房房源详情模块-楼盘相册")
class TestHousePhotoAlbum(object):
    json_file_path = cm.test_data_dir + "/jrgj/test_new/test_house/test_add.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global gl_web_driver
        gl_web_driver = web_driver
        self.main_up_view = MainUpViewPage(gl_web_driver)
        self.main_left_view = MainLeftViewPage(gl_web_driver)
        self.house_table_page = HouseTablePage(gl_web_driver)
        self.house_detail_page = HouseDetailPage(gl_web_driver)
        yield
        self.main_up_view.clear_all_title()

    @allure.step("进入房源详情")
    def enter_house_detail(self):
        self.main_left_view.change_role('超级管理员')
        self.main_left_view.click_all_house_label()
        self.house_table_page.click_new_tab()
        self.house_table_page.click_off_shelf_house_tab()
        self.house_table_page.input_building_name_search(self.test_data['楼盘名称'])
        self.house_table_page.click_search_button()
        self.house_table_page.go_new_house_detail_by_row()

    @allure.step("批量上传图片")
    def add_new_house_img(self):
        count = 0
        self.house_detail_page.click_upload_btn()
        self.house_detail_page.upload_image([cm.tmp_picture_file], '效果图')
        count += 1
        self.house_detail_page.upload_image([cm.tmp_picture_file], '实景图')
        count += 1
        self.house_detail_page.upload_image([cm.tmp_picture_file], '位置图')
        count += 1
        self.house_detail_page.click_upload_btn()
        return count

    @allure.story("测试上传楼盘相册")
    @pytest.mark.new
    @pytest.mark.house
    @pytest.mark.run(order=2)
    # @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_upload_photo(self, web_driver):
        self.enter_house_detail()
        self.house_detail_page.click_see_more()
        initial_number = self.house_detail_page.get_image_list_lenth()
        self.house_detail_page.go_upload_album()
        count = self.add_new_house_img()
        actual_result = self.house_detail_page.get_dialog_text()
        actual_number = self.house_detail_page.get_image_list_lenth()
        pytest.assume(actual_result == '上传成功')
        if initial_number == 0:
            assert actual_number == count
        else:
            assert actual_number == count + initial_number - 1

    @allure.step("测试批量删除图片")
    @pytest.mark.run(order=2)
    def test_batch_delete_house_img(self):
        self.enter_house_detail()  # 进入房源详情
        self.house_detail_page.click_see_more()
        initial_number = self.house_detail_page.get_image_list_lenth()
        if initial_number <= 1:  # 上传图片
            self.add_new_house_img()
            initial_number = self.house_detail_page.get_image_list_lenth()
        else:
            logger.info('无需上传，直接执行删除')
        self.house_detail_page.click_batch_delete_btn()
        self.house_detail_page.select_some_image_to_delete()
        deleted_number = self.house_detail_page.get_deleted_image_number()
        self.house_detail_page.click_delete_btn()
        actual_result = self.house_detail_page.get_dialog_text()
        actual_number = self.house_detail_page.get_image_list_lenth()
        expect_number = initial_number - deleted_number
        pytest.assume(actual_result == '删除成功')
        assert expect_number == actual_number

    @allure.story("测试全部删除")
    @pytest.mark.new
    @pytest.mark.house
    @pytest.mark.run(order=4)
    # @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_delete_all(self, web_driver):
        self.enter_house_detail()  # 进入房源详情
        self.house_detail_page.click_see_more()
        initial_number = self.house_detail_page.get_image_list_lenth()
        if initial_number <= 1:  # 上传图片
            self.add_new_house_img()
        else:
            logger.info('无需上传，直接执行删除')
        self.house_detail_page.click_batch_delete_btn()
        self.house_detail_page.select_all_image_to_delete()
        self.house_detail_page.click_delete_btn()
        actual_result = self.house_detail_page.get_dialog_text()
        actual_number = self.house_detail_page.get_image_list_lenth()
        pytest.assume(actual_result == '删除成功')
        assert actual_number == 1


if __name__ == '__main__':
    pytest.main(['-q', 'test_house_photo_album.py'])
