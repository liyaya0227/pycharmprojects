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
from case_service.jrgj.web.house.house_service import HouseService
from common.readxml import ReadXml
from config.conf import cm
from page_object.common.web.login.loginpage import LoginPage
from page_object.jrgj.web.main.rightviewpage import MainRightViewPage
from utils.databaseutil import DataBaseUtil
from utils.logger import logger
from common.readconfig import ini
from utils.jsonutil import get_value
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from utils.timeutil import sleep

house_code = ''
gl_driver = None
house_service = HouseService()
house_sql = ReadXml("jrgj/house_sql")


@allure.feature("房源详情模块")
class TestPhone(object):
    json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_phone.json"
    account = get_value(json_file_path, ini.environment)
    main_up_view = None
    main_top_view = None
    main_left_view = None
    main_right_view = None
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
        self.main_right_view = MainRightViewPage(web_driver)
        house_code = self.house_table_page.get_house_code_by_db(flag='买卖')
        logger.info('房源编号为：' + house_code)
        yield
        sleep(2)
        self.main_up_view.clear_all_title()

    # @allure.step("验证房源状态")
    # def check_house_state(self):
    #     global house_code
    #     if self.house_table_page.get_house_code_by_db(flag='买卖') == '':  # 判断房源是否存在，不存在则新增
    #         house_service.add_house(gl_driver, 'sale')
    #         self.main_up_view.clear_all_title()
    #     house_code = self.house_table_page.get_house_code_by_db(flag='买卖')
    @allure.step("验证房源状态")
    def check_house_state(self):
        global house_code
        if self.house_table_page.get_house_status_by_db(flag='sale') == '':  # 判断房源是否存在，不存在则新增
            house_service.add_house(gl_driver, 'sale')
            self.main_up_view.clear_all_title()
        house_code = self.house_table_page.get_house_status_by_db(flag='sale')[0][2]

    @allure.step("进入房源详情")
    def enter_house_detail(self):
        login_person_name = self.main_right_view.get_login_person_name()
        # login_person_phone = self.main_right_view.get_login_person_phone()
        database_util = DataBaseUtil('SQL Server', ini.database_name)
        get_house_info = house_sql.get_sql('trade_house', 'get_house_info').format(account_name=login_person_name)
        house_info_list = database_util.select_sql(get_house_info)
        self.main_left_view.click_all_house_label()
        self.house_table_page.clear_filter(flag='买卖')
        for house_info in house_info_list:
            self.house_table_page.input_house_code_search(house_info[1])
            self.house_table_page.click_search_button()
            number = self.house_table_page.get_house_number()
            if int(number) > 0:
                self.house_table_page.go_house_detail_by_row(1)
                break

    @allure.story("测试手机号正确")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=3)
    def test_view_phone(self):
        self.check_house_state()
        self.enter_house_detail()  # 进入房源详情
        self.house_detail_page.click_phone_button()  # 查看业主联系方式
        self.house_detail_page.phone_dialog_click_check_button()
        dialog_content = self.main_top_view.find_notification_content()
        if dialog_content == '':
            phone_number = self.house_detail_page.phone_dialog_get_phone()
            assert len(phone_number) == 11
            self.house_detail_page.dialog_click_close_button()
        else:
            self.house_detail_page.dialog_click_close_button()
            assert True

    @allure.story("测试查看号码最大次数")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=11)
    def test_view_phone_maximum(self):
        self.check_house_state()
        self.enter_house_detail()  # 进入房源详情
        self.house_detail_page.click_phone_button()  # 查看业主联系方式
        looked_count = self.house_detail_page.dialog_get_looked_count()
        if looked_count == '60':
            self.house_detail_page.phone_dialog_click_check_button()
            dialog_content = self.main_top_view.find_notification_content()
            assert dialog_content == '今日查看次数已经超过60次'
            self.house_detail_page.dialog_click_close_button()
        else:
            self.house_detail_page.dialog_click_close_button()
            for _ in range(60 - int(looked_count)):
                self.house_detail_page.click_phone_button()
                self.house_detail_page.phone_dialog_click_check_button()
                self.house_detail_page.dialog_click_close_button()
            self.house_detail_page.click_phone_button()
            self.house_detail_page.phone_dialog_click_check_button()
            assert self.main_top_view.find_notification_content() == '今日查看次数已经超过60次'
            self.house_detail_page.dialog_click_close_button()

    # looked_count = self.house_detail_page.dialog_get_looked_count()
    #     if looked_count == '60':
    #         self.house_detail_page.phone_dialog_click_check_button()
    #         dialog_content = self.main_top_view.find_notification_content()
    #         assert dialog_content == '今日查看次数已经超过60次'
    #         self.house_detail_page.dialog_click_close_button()
    #     else:
    #         self.house_detail_page.phone_dialog_click_check_button()
    #         self.house_detail_page.dialog_click_close_button()
    #         temp = looked_count
    #         for _ in range(60 - int(looked_count)):
    #             self.house_detail_page.click_phone_button()
    #             new_looked_count = self.house_detail_page.dialog_get_looked_count()
    #             self.house_detail_page.phone_dialog_click_check_button()
    #             if new_looked_count == '60':
    #                 assert self.main_top_view.find_notification_content() == '今日查看次数已经超过60次'
    #             self.house_detail_page.dialog_click_close_button()
    #             assert int(new_looked_count) == int(temp) + 1
    #             temp = new_looked_count
    #         self.house_detail_page.click_phone_button()
    #         self.house_detail_page.phone_dialog_click_check_button()
    #         assert self.main_top_view.find_notification_content() == '今日查看次数已经超过60次'
    # else:
    #     if self.house_detail_page.check_shopowner_recommend() or self.house_detail_page.get_vip_person() != '':
    #         assert dialog_content == '请联系维护人查看相关房源信息'
