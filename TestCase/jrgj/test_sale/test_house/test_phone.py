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
from page_object.common.web.login.loginpage import LoginPage
from utils.logger import log
from common.readconfig import ini
from utils.jsonutil import get_value
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage

house_code = ''
gl_driver = None


@allure.feature("测试房源模块")
class TestPhone(object):
    json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_phone.json"
    account = get_value(json_file_path, ini.environment)
    main_up_view = None
    main_top_view = None
    main_left_view = None
    house_table_page = None
    house_detail_page = None

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global house_code, gl_driver
        gl_driver = web_driver
        self.login_page = LoginPage(gl_driver)
        self.main_up_view = MainUpViewPage(gl_driver)
        self.main_up_view = MainUpViewPage(gl_driver)
        self.main_top_view = MainTopViewPage(web_driver)
        self.main_left_view = MainLeftViewPage(gl_driver)
        self.house_table_page = HouseTablePage(gl_driver)
        self.house_detail_page = HouseDetailPage(gl_driver)
        house_code = self.house_table_page.get_house_code_by_db(flag='买卖')
        log.info('房源编号为：' + house_code)
        yield
        self.main_up_view.clear_all_title()

    @allure.story("测试房源详情右侧电话用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=11)
    def test_view_phone(self):
        self.main_left_view.change_role('经纪人')
        self.main_left_view.click_all_house_label()
        self.house_table_page.click_sale_tab()
        self.house_table_page.click_all_house_tab()
        self.house_table_page.click_reset_button()
        self.house_table_page.clear_filter(flag='买卖')
        self.house_table_page.input_house_code_search(house_code)
        self.house_table_page.click_search_button()
        self.house_table_page.go_house_detail_by_row(1)
        self.house_detail_page.click_phone_button()
        assert self.house_detail_page.dialog_get_looked_count() == '0'
        self.house_detail_page.dialog_click_close_button()
        self.house_detail_page.click_phone_button()
        assert self.house_detail_page.dialog_get_looked_count() == '0'
        self.house_detail_page.dialog_click_close_button()

    @allure.story("测试房源详情右侧电话用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=11)
    def test_view_phone_maximum(self):
        self.main_left_view.log_out()
        self.login_page.log_in(self.account[0], self.account[1])
        self.main_left_view.change_role('经纪人')
        self.main_left_view.click_all_house_label()
        self.house_table_page.click_sale_tab()
        self.house_table_page.click_all_house_tab()
        self.house_table_page.click_reset_button()
        self.house_table_page.clear_filter(flag='买卖')
        self.house_table_page.input_house_code_search(house_code)
        self.house_table_page.click_search_button()
        self.house_table_page.go_house_detail_by_row()
        self.house_detail_page.click_phone_button()
        dialog_content = self.main_top_view.find_notification_content()
        if dialog_content == '':
            looked_count = self.house_detail_page.dialog_get_looked_count()
            if looked_count == '60':
                self.house_detail_page.phone_dialog_click_check_button()
                dialog_content = self.main_top_view.find_notification_content()
                assert dialog_content == '今日查看次数已经超过60次'
                self.house_detail_page.dialog_click_close_button()
            else:
                self.house_detail_page.phone_dialog_click_check_button()
                self.house_detail_page.dialog_click_close_button()
                temp = looked_count
                for _ in range(60 - int(looked_count)):
                    self.house_detail_page.click_phone_button()
                    new_looked_count = self.house_detail_page.dialog_get_looked_count()
                    self.house_detail_page.phone_dialog_click_check_button()
                    if new_looked_count == '60':
                        assert self.main_top_view.find_notification_content() == '今日查看次数已经超过60次'
                    self.house_detail_page.dialog_click_close_button()
                    assert int(new_looked_count) == int(temp) + 1
                    temp = new_looked_count
                self.house_detail_page.click_phone_button()
                self.house_detail_page.phone_dialog_click_check_button()
                assert self.main_top_view.find_notification_content() == '今日查看次数已经超过60次'
        else:
            if self.house_detail_page.check_shopowner_recommend() or self.house_detail_page.get_vip_person() != '':
                assert dialog_content == '请联系维护人查看相关房源信息'
