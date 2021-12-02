#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: test_share.py
@date: 2021/10/26
"""
import random
import pytest
import allure
from case_service.jrxf.house.house_service import HouseService
from common.readconfig import ini
from config.conf import cm
from page_object.jrxf.web.house.detail_page import HouseDetailPage
from page_object.jrxf.web.house.table_page import HouseTablePage
from page_object.jrxf.web.main.leftviewpage import MainLeftViewPage
from page_object.jrxf.web.main.upviewpage import MainUpViewPage
from utils.jsonutil import get_data
from utils.logger import logger

person_info = {}
gl_xf_web_driver = None
add_house_model_info = {}


@allure.feature("房源分享功能")
class TestShare(object):
    json_file_path = cm.test_data_dir + "/jrxf/house/test_add.json"
    test_add_data = get_data(json_file_path)
    new_house_name = ini.new_house_name

    @pytest.fixture(scope="class", autouse=True)
    def check_house(self, xf_web_driver):
        global gl_xf_web_driver
        gl_xf_web_driver = xf_web_driver
        house_service = HouseService(gl_xf_web_driver)
        house_service.check_current_role('平台管理员')
        house_service.prepare_house(self.test_add_data, self.new_house_name)  # 验证房源状态

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self):
        self.main_up_view = MainUpViewPage(gl_xf_web_driver)
        self.main_left_view = MainLeftViewPage(gl_xf_web_driver)
        self.house_table_page = HouseTablePage(gl_xf_web_driver)
        self.house_detail_page = HouseDetailPage(gl_xf_web_driver)
        yield
        self.main_up_view.clear_all_title()

    @allure.step("进入房源详情")
    def enter_house_detail(self, house_name):
        self.main_left_view.click_house_management_label()
        self.house_table_page.click_coop_house_tab()
        self.house_table_page.search_unhandle_house(house_name)
        self.house_table_page.enter_house_detail(house_name)

    @allure.step("上传户型介绍")
    def upload_house_model(self):
        global add_house_model_info
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
        house_type_name = self.house_detail_page.house_model_content(add_house_model_info)
        return house_type_name

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

    @allure.story("测试分享页面个人及房源信息")
    @pytest.mark.new
    @pytest.mark.house
    @pytest.mark.run(order=3)
    # @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_info_in_share_page(self):
        user_info = self.house_detail_page.get_user_info_from_db(ini.user_account)  # 获取用户信息
        user_name = user_info[0]
        cell_phone = user_info[1]
        self.enter_house_detail(self.new_house_name)  # 进入房源详情
        self.house_detail_page.click_see_more()
        self.upload_house_model()  # 上传户型介绍
        self.house_detail_page.switch_tab_by_name('楼盘首页')  # 进入分享页面
        self.house_detail_page.click_share()
        account_name, account_phone = self.house_detail_page.get_user_info_in_share_page()  # 获取分享页面的用户和房源信息
        model_info, area, orientation, sale_price = self.house_detail_page.get_model_info_in_share_page()
        self.house_detail_page.close_dialog()  # 关闭弹窗
        rooms = add_house_model_info['rooms']  # 获取测试数据中的房源信息
        parlor = add_house_model_info['parlor']
        bathroom = add_house_model_info['bathroom']
        kitchen = add_house_model_info['kitchen']
        sale_price_start = add_house_model_info['sale_price_start']
        sale_price_end = add_house_model_info['sale_price_end']
        expect_area = add_house_model_info['area']
        expect_orientation = add_house_model_info['orientation']
        expect_model_info = str(rooms) + '室' + str(parlor) + '厅' + str(bathroom) + '卫' + str(kitchen) + '厨'
        expect_sale_price = sale_price_start + '-' + sale_price_end
        pytest.assume(account_name == user_name)
        pytest.assume(account_phone == cell_phone)
        pytest.assume(area == expect_area)
        pytest.assume(orientation == expect_orientation)
        pytest.assume(model_info == expect_model_info)
        pytest.assume(sale_price == expect_sale_price)

    @allure.story("测试生成二维码")
    @pytest.mark.run(order=3)
    def test_generate_qr_code(self):
        self.enter_house_detail(self.new_house_name)
        house_model_number = self.house_detail_page.get_house_model_number()
        house_img_number = self.house_detail_page.get_house_img_number()
        if house_model_number == 0:  # 上传户型介绍
            self.upload_house_model()
            self.house_detail_page.switch_tab_by_name('楼盘首页')
        else:
            logger.info('存在户型介绍，无需新增')
        if house_img_number == 0:  # 上传图片
            self.house_detail_page.click_see_more()
            self.add_new_house_img()
            self.house_detail_page.switch_tab_by_name('楼盘首页')
        else:
            logger.info('存在房源图片，无需上传')
        self.house_detail_page.click_share()  # 生成二维码
        self.house_detail_page.generate_code()
        res = self.house_detail_page.verify_generate_code_success()
        self.house_detail_page.close_code_dialog()
        self.house_detail_page.close_dialog()
        assert res



