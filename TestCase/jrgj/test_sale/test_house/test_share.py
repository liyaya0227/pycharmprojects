#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_share.py
@date: 2021/8/9 0009
"""

import pytest
import allure
from utils.logger import logger
from common.readconfig import ini
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.rightviewpage import MainRightViewPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage

house_code = ''
login_person_name = ''
login_person_phone = ''


@allure.feature("测试房源模块")
class TestShare(object):
    main_up_view = None
    main_left_view = None
    main_right_view = None
    house_table_page = None
    house_detail_page = None

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global house_code, login_person_name, login_person_phone
        self.main_up_view = MainUpViewPage(web_driver)
        self.main_left_view = MainLeftViewPage(web_driver)
        self.main_right_view = MainRightViewPage(web_driver)
        self.house_table_page = HouseTablePage(web_driver)
        self.house_detail_page = HouseDetailPage(web_driver)
        self.main_left_view.click_homepage_overview_label()
        login_person_name = self.main_right_view.get_login_person_name()
        login_person_phone = self.main_right_view.get_login_person_phone()
        house_code = self.house_table_page.get_house_code_by_db(flag='买卖')
        # assert house_code != ''
        logger.info('房源编号为：' + house_code)
        yield
        self.main_up_view.clear_all_title()

    @allure.story("测试房源详情右侧分享用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=11)
    def test_share(self, web_driver):
        self.main_left_view.click_all_house_label()
        self.house_table_page.click_sale_tab()
        self.house_table_page.click_all_house_tab()
        self.house_table_page.click_reset_button()
        self.house_table_page.clear_filter(flag='买卖')
        self.house_table_page.input_house_code_search(house_code)
        self.house_table_page.click_search_button()
        self.house_table_page.go_house_detail_by_row(1)
        house_type = self.house_detail_page.get_house_type()
        size = self.house_detail_page.get_size()
        orientations = self.house_detail_page.get_orientations()
        self.house_detail_page.click_share_button()
        dialog_community_name = self.house_detail_page.share_dialog_get_community_name()
        dialog_house_type = self.house_detail_page.share_dialog_get_house_type()
        dialog_size = self.house_detail_page.share_dialog_get_size()
        dialog_orientations = self.house_detail_page.share_dialog_get_orientations()
        dialog_name = self.house_detail_page.share_dialog_get_name()
        dialog_phone = self.house_detail_page.share_dialog_get_phone()
        self.house_detail_page.dialog_click_cancel_button()
        pytest.assume(ini.house_community_name == dialog_community_name)
        pytest.assume(house_type == dialog_house_type)
        pytest.assume(size == dialog_size)
        pytest.assume(orientations == dialog_orientations)
        pytest.assume(login_person_name == dialog_name)
        pytest.assume(login_person_phone == dialog_phone)
