#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_address.py
@date: 2021/8/10 0010
"""

import pytest
import allure
from config.conf import cm
from utils.logger import log
from common.readconfig import ini
from utils.jsonutil import get_value
from page_object.web.main.upviewpage import MainUpViewPage
from page_object.web.main.topviewpage import MainTopViewPage
from page_object.web.main.leftviewpage import MainLeftViewPage
from page_object.web.login.loginpage import LoginPage
from page_object.web.house.tablepage import HouseTablePage
from page_object.web.house.detailpage import HouseDetailPage

house_code = ''


@allure.feature("测试房源模块")
class TestPhone(object):
    json_file_path = cm.test_data_dir + "/test_sale/test_house/test_phone.json"
    account = get_value(json_file_path, ini.environment)

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global house_code

        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        house_table = HouseTablePage(web_driver)

        main_leftview.change_role('经纪人')
        house_code = house_table.get_house_code_by_db(flag='买卖')
        assert house_code != ''
        log.info('房源编号为：' + house_code)
        yield
        main_upview.clear_all_title()

    @allure.story("测试房源详情右侧电话用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=11)
    def test_001(self, web_driver):
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)

        main_leftview.change_role('经纪人')
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter(flag='买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        house_detail.click_phone_button()
        assert house_detail.dialog_get_looked_count() == '0'
        house_detail.dialog_click_close_button()
        house_detail.click_phone_button()
        assert house_detail.dialog_get_looked_count() == '0'
        house_detail.dialog_click_close_button()

    @allure.story("测试房源详情右侧电话用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=11)
    def test_002(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        login = LoginPage(web_driver)

        main_leftview.log_out()
        login.log_in(self.account[0], self.account[1])
        main_leftview.change_role('经纪人')
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter(flag='买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        house_detail.click_phone_button()
        dialog_content = main_topview.find_notification_content()
        if dialog_content == '':
            looked_count = house_detail.dialog_get_looked_count()
            if looked_count == '60':
                house_detail.phone_dialog_click_check_button()
                dialog_content = main_topview.find_notification_content()
                assert dialog_content == '今日查看次数已经超过60次'
                house_detail.dialog_click_close_button()
            else:
                house_detail.phone_dialog_click_check_button()
                house_detail.dialog_click_close_button()
                temp = looked_count
                for _ in range(60 - int(looked_count)):
                    house_detail.click_phone_button()
                    new_looked_count = house_detail.dialog_get_looked_count()
                    house_detail.phone_dialog_click_check_button()
                    if new_looked_count == '60':
                        assert main_topview.find_notification_content() == '今日查看次数已经超过60次'
                    house_detail.dialog_click_close_button()
                    assert int(new_looked_count) == int(temp) + 1
                    temp = new_looked_count
                house_detail.click_phone_button()
                assert main_topview.find_notification_content() == '今日查看次数已经超过60次'
        else:
            if house_detail.check_shopowner_recommend() or house_detail.get_vip_person() != '':
                assert dialog_content == '请联系维护人查看相关房源信息'
