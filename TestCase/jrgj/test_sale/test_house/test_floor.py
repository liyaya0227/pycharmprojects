#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_floor.py
@date: 2021/8/10 0010
"""

import pytest
import allure
from config.conf import cm
from page_object.common.web.login.loginpage import LoginPage
from utils.logger import log
from common.readconfig import ini
from utils.jsonutil import get_value
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage

from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage

house_code = ''


@allure.feature("测试房源模块")
class TestFloor(object):
    json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_floor.json"
    account_list = []
    for key, value in get_value(json_file_path, ini.environment).items():
        account_list.append(value)
    account_list.append([ini.user_account, ini.user_password])

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global house_code

        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)

        main_leftview.change_role('经纪人')
        house_code = house_table.get_house_code_by_db(flag='买卖')
        assert house_code != ''
        log.info('房源编号为：' + house_code)
        yield
        main_upview.clear_all_title()

    @allure.story("测试房源详情右侧楼层用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=11)
    @pytest.mark.parametrize("account", account_list)
    def test_001(self, web_driver, account):
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        login = LoginPage(web_driver)

        main_leftview.log_out()
        login.log_in(account[0], account[1])
        main_leftview.change_role('经纪人')
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter(flag='买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        house_detail.click_floor_button()
        dialog_detail_floor_info = house_detail.get_floor_dialog_detail_floor()
        house_detail.dialog_click_close_button()
        assert dialog_detail_floor_info != ''
