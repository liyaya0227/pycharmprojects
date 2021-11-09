#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: test_add_house_info.py
@date: 2021/10/26
"""
import random
import allure
import pytest
from case_service.jrxf.house.house_service import HouseService
from common.readconfig import ini
from config.conf import cm
from page_object.jrxf.web.house.detail_page import HouseDetailPage
from page_object.jrxf.web.house.table_page import HouseTablePage
from page_object.jrxf.web.main.leftviewpage import MainLeftViewPage
from page_object.jrxf.web.main.upviewpage import MainUpViewPage
from utils.jsonutil import get_data


@allure.feature("测试房源详情模块")
class TestAdd(object):
    house_name = ''
    main_up_view = None
    main_left_view = None
    add_house_page = None
    house_table_page = None
    audit_house_page = None
    house_detail_page = None

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, xf_web_driver):
        json_file_path = cm.test_data_dir + "/jrxf/house/test_add.json"
        test_add_data = get_data(json_file_path)
        house_service = HouseService(xf_web_driver)
        self.house_name = ini.house_community_name
        self.main_up_view = MainUpViewPage(xf_web_driver)
        self.main_left_view = MainLeftViewPage(xf_web_driver)
        self.house_table_page = HouseTablePage(xf_web_driver)
        self.house_detail_page = HouseDetailPage(xf_web_driver)
        self.main_left_view.change_role('平台管理员')
        house_service.prepare_house(test_add_data, self.house_name)  # 验证房源状态
        yield
        self.main_up_view.clear_all_title()

    @allure.step("进入房源详情")
    def enter_house_detail(self, house_name):
        self.main_left_view.click_house_management_label()
        self.house_table_page.click_coop_house_tab()
        self.house_table_page.serch_unhandle_house(house_name)
        self.house_table_page.enter_house_detail(house_name)

    @allure.step("上传户型介绍")
    def upload_house_model(self):
        json_file_path = cm.test_data_dir + "/jrxf/house/test_add_house_info.json"
        test_add_house_info_data = get_data(json_file_path)
        house_model_info = test_add_house_info_data['tc01_add_house_model'][0]
        add_house_model_info = {
            "house_type_name": house_model_info['newModelName'] + str(random.randint(1, 100)),
            "rooms": house_model_info['rooms'],
            "parlor": house_model_info['parlor'],
            "bathroom": house_model_info['bathroom'],
            "kitchen": house_model_info['kitchen'],
            "area": house_model_info['area'],
            "orientation": house_model_info['orientation'],
            "sale_price_start": house_model_info['salePriceStart'],
            "sale_price_end": house_model_info['salePriceEnd'],
            "pictures_path": [cm.tmp_picture_file]
        }
        self.house_detail_page.switch_tab_by_name('户型介绍')
        self.house_detail_page.click_upload_house_model_btn()
        self.house_detail_page.house_model_content(params=add_house_model_info)

    @allure.story("上传户型介绍")
    @pytest.mark.run(order=2)
    def test_upload_house_model(self):
        self.enter_house_detail(self.house_name)  # 进入房源详情
        initial_house_model_number = self.house_detail_page.get_house_model_number()
        self.house_detail_page.click_see_more()
        self.upload_house_model()  # 上传户型介绍
        self.house_detail_page.switch_tab_by_name('楼盘首页')
        expect_house_model_number = initial_house_model_number + 1
        actual_house_model_number = self.house_detail_page.get_house_model_number()
        assert actual_house_model_number == expect_house_model_number

    @allure.story("维护楼栋信息")
    @pytest.mark.run(order=2)
    def test_add_building_info(self):
        self.enter_house_detail(self.house_name)  # 进入房源详情
        initial_house_model_number = self.house_detail_page.get_house_model_number()
        if initial_house_model_number == 0:  # 上传户型介绍
            self.upload_house_model()
            self.house_detail_page.switch_tab_by_name('楼盘首页')
        else:
            log.info('存在户型介绍，无需新增')
        initial_building_info_number = self.house_detail_page.get_building_info_number()
        self.house_detail_page.click_add_building_info()
        self.house_detail_page.building_info_content(random.randint(1, 100), 1, 1, 100)
        actual_building_info_number = self.house_detail_page.get_building_info_number()
        assert actual_building_info_number == initial_building_info_number + 1

    @allure.story("发布动态")
    @pytest.mark.run(order=2)
    def test_add_house_dynamic(self):
        self.enter_house_detail(self.house_name)  # 进入房源详情
        self.house_detail_page.click_see_more()
        self.house_detail_page.switch_tab_by_name('楼盘动态')
        trend_explain = self.house_detail_page.house_dynamic_content('楼盘动态title', '楼盘动态最新' +
                                                                     str(random.randint(1, 100)))
        self.house_detail_page.switch_tab_by_name('楼盘首页')
        res = self.house_detail_page.verify_dynamic_list_update(trend_explain)
        assert res

    @allure.story("编辑楼盘卖点")
    @pytest.mark.run(order=2)
    def test_edit_house_selling_point(self):
        self.enter_house_detail(self.house_name)  # 进入房源详情
        self.house_detail_page.click_see_more()
        self.house_detail_page.switch_tab_by_name('楼盘卖点')
        push_plate = self.house_detail_page.house_selling_point_content('距离地铁二号线100米' +
                                                                        str(random.randint(1, 100)), '四面通风大平层')
        self.house_detail_page.switch_tab_by_name('楼盘首页')
        actual_result = self.house_detail_page.verify_celling_point_list_update()
        expect_result = '一句话推盘：' + push_plate
        assert actual_result == expect_result


if __name__ == '__main__':
    pytest.main(['-q', 'test_add_house_info.py'])
