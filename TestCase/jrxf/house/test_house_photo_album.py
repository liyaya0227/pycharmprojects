#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: test_house_photo_album.py
@date: 2021/10/25
"""
import allure
import pytest
from case_service.jrxf.house.house_service import HouseService
from common.readconfig import ini
from config.conf import cm
from page_object.jrxf.web.house.detail_page import HouseDetailPage
from page_object.jrxf.web.house.table_page import HouseTablePage
from page_object.jrxf.web.main.leftviewpage import MainLeftViewPage
from page_object.jrxf.web.main.upviewpage import MainUpViewPage
from utils.logger import logger

gl_web_driver = None


@allure.feature("京日新房房源详情模块-楼盘相册")
class TestAdd(object):
    house_name = ''

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, xf_web_driver):
        global gl_web_driver
        gl_web_driver = xf_web_driver
        self.house_name = ini.house_community_name
        house_service = HouseService(gl_web_driver)
        self.main_up_view = MainUpViewPage(gl_web_driver)
        self.main_left_view = MainLeftViewPage(gl_web_driver)
        self.house_table_page = HouseTablePage(gl_web_driver)
        self.house_detail_page = HouseDetailPage(gl_web_driver)
        self.main_left_view.change_role('平台管理员')
        house_service.check_house_state(gl_web_driver, self.house_name)  # 验证房源状态
        yield
        self.main_up_view.clear_all_title()

    @allure.step("进入房源详情")
    def enter_house_detail(self, house_name):
        self.main_left_view.click_house_management_label()
        self.house_table_page.click_coop_house_tab()
        self.house_table_page.serch_unhandle_house(house_name)
        self.house_table_page.enter_house_detail(house_name)

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
        self.house_detail_page.click_confirm_upload_btn()
        return count

    @allure.story("批量上传")
    @pytest.mark.run(order=2)
    def test_batch_upload_house_img(self):
        self.enter_house_detail(self.house_name)  # 进入房源详情
        self.house_detail_page.click_see_more()  # 批量上传图片
        initial_number = self.house_detail_page.get_image_list_lenth()
        count = self.add_new_house_img()
        actual_result = self.house_detail_page.get_dialog_text()
        actual_number = self.house_detail_page.get_image_list_lenth()
        assert actual_result == '上传成功'
        if initial_number == 0:
            assert actual_number == count
        else:
            assert actual_number == count + initial_number - 1

    @allure.step("批量删除图片")
    @pytest.mark.run(order=2)
    def test_batch_delete_house_img(self):
        self.enter_house_detail(self.house_name)  # 进入房源详情
        self.house_detail_page.click_see_more()
        initial_number = self.house_detail_page.get_image_list_lenth()
        if initial_number <= 1:  # 上传图片
            self.add_new_house_img()
            initial_number = self.house_detail_page.get_image_list_lenth()
        else:
            logger.info('无需上传，直接执行删除')
        self.house_detail_page.click_batch_delete_btn()  # 批量删除
        self.house_detail_page.select_some_image_to_delete()
        deleted_number = self.house_detail_page.get_deleted_image_number()
        self.house_detail_page.click_delete_btn()
        actual_result = self.house_detail_page.get_dialog_text()
        actual_number = self.house_detail_page.get_image_list_lenth()
        expect_number = initial_number - deleted_number
        assert actual_result == '删除成功'
        assert expect_number == actual_number

    @allure.step("全选删除图片")
    @pytest.mark.run(order=2)
    def test_select_all_to_delete_house_img(self):
        self.enter_house_detail(self.house_name)  # 进入房源详情
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
        assert actual_result == '删除成功'
        assert actual_number == 1


if __name__ == '__main__':
    pytest.main(['-q', 'test_house_photo_album.py'])
