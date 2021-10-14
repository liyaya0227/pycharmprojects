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
from utils.logger import log
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

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global house_code
        global login_person_name
        global login_person_phone

        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_rightview = MainRightViewPage(web_driver)
        house_table = HouseTablePage(web_driver)

        main_leftview.change_role('经纪人')
        main_leftview.click_homepage_overview_label()
        login_person_name = main_rightview.get_login_person_name()
        login_person_phone = main_rightview.get_login_person_phone()
        house_code = house_table.get_house_code_by_db(flag='买卖')
        assert house_code != ''
        log.info('房源编号为：' + house_code)
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter(flag='买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        yield
        main_upview.clear_all_title()

    @allure.story("测试房源详情右侧分享用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=11)
    def test_001(self, web_driver):
        house_detail = HouseDetailPage(web_driver)

        house_type = house_detail.get_house_type()
        size = house_detail.get_size()
        orientations = house_detail.get_orientations()
        house_detail.click_share_button()
        dialog_community_name = house_detail.share_dialog_get_community_name()
        dialog_house_type = house_detail.share_dialog_get_house_type()
        dialog_size = house_detail.share_dialog_get_size()
        dialog_orientations = house_detail.share_dialog_get_orientations()
        dialog_name = house_detail.share_dialog_get_name()
        dialog_phone = house_detail.share_dialog_get_phone()
        house_detail.dialog_click_cancel_button()
        pytest.assume(ini.house_community_name == dialog_community_name)
        pytest.assume(house_type == dialog_house_type)
        pytest.assume(size == dialog_size)
        pytest.assume(orientations == dialog_orientations)
        pytest.assume(login_person_name == dialog_name)
        pytest.assume(login_person_phone == dialog_phone)
