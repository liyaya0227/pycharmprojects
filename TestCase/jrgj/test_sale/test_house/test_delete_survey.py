#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_delete_survey.py
@date: 2021/8/11 0011
"""
import pytest
import allure
from case_service.jrgj.web.house.house_service import HouseService
from case_service.jrgj.web.survey.survey_service import SurveyService
from config.conf import cm
from page_object.common.web.login.loginpage import LoginPage
from page_object.jrgj.web.survey.tablepage import SurveyTablePage
from utils.logger import logger
from page_object.jrgj.web.main.rightviewpage import MainRightViewPage
from common.readconfig import ini
from utils.jsonutil import get_value, get_data
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.app.login.loginpage import AppLoginPage
from page_object.jrgj.app.main.mainpage import AppMainPage
from page_object.jrgj.app.mine.minepage import AppMinePage

HOUSE_TYPE = 'sale'
house_info = ''
gl_web_driver = None
gl_app_driver = None
survey_service = SurveyService()


@allure.feature("房源详情模块-删除实勘")
class TestDeleteSurvey(object):
    add_house_json_file_path = cm.test_data_dir + "/jrgj/test_rent/test_house/test_add.json"
    json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_out_show.json"
    test_add_data = get_data(add_house_json_file_path)

    @pytest.fixture(scope="class", autouse=True)
    def prepare_house(self, web_driver):
        global gl_web_driver, house_info
        gl_web_driver = web_driver
        house_service = HouseService(gl_web_driver)
        house_info = house_service.prepare_house(self.test_add_data, HOUSE_TYPE)

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, android_driver):
        global gl_app_driver
        gl_app_driver = android_driver
        self.login_page = LoginPage(gl_web_driver)
        self.main_up_view = MainUpViewPage(gl_web_driver)
        self.main_top_view = MainTopViewPage(gl_web_driver)
        self.main_left_view = MainLeftViewPage(gl_web_driver)
        self.main_right_view = MainRightViewPage(gl_web_driver)
        self.house_table_page = HouseTablePage(gl_web_driver)
        self.house_detail_page = HouseDetailPage(gl_web_driver)
        self.survey_table_page = SurveyTablePage(gl_web_driver)
        self.app_main_page = AppMainPage(gl_app_driver)
        self.app_mine_page = AppMinePage(gl_app_driver)
        self.app_login_page = AppLoginPage(gl_app_driver)
        yield
        self.main_up_view.clear_all_title()

    # @allure.step("进入房源详情")
    # def enter_house_detail(self, house_code):
    #     self.main_left_view.click_all_house_label()
    #     self.house_table_page.input_house_code_search(house_code)
    #     self.house_detail_page.enter_house_detail()

    @allure.step("进入房源详情")
    def enter_house_detail(self, house_code):
        self.main_left_view.click_all_house_label()
        self.house_table_page.input_house_code_search(house_code)
        for i in range(4):
            number = self.house_table_page.get_house_number()
            if int(number) > 0:
                self.house_detail_page.enter_house_detail()
                break
            else:
                self.house_table_page.click_search_button()

    @allure.story("测试删除实勘用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=3)
    def test_delete_survey(self):
        house_code = house_info[0]
        survey_person_info = get_value(self.json_file_path, ini.environment)
        exploration_info = get_value(self.json_file_path, 'exploration_info')
        # self.main_left_view.change_role('超级管理员')
        self.enter_house_detail(house_code)
        if self.house_detail_page.check_survey_status() != '已上传':
            logger.info('未上传实勘，进行实勘预约')
            if self.house_detail_page.check_survey_status() == '已预约':
                if self.house_detail_page.check_back_survey():  # 实勘退单
                    self.house_detail_page.click_back_survey_button()
                    self.house_detail_page.dialog_choose_back_exploration_reason('其他')
                    self.house_detail_page.dialog_click_back_exploration_return_button()
                else:
                    self.main_up_view.clear_all_title()
                    self.main_left_view.change_role('超级管理员')
                    self.main_left_view.click_survey_management_label()  # 取消实勘订单
                    self.survey_table_page.input_house_code_search(house_code)
                    self.survey_table_page.click_search_button()
                    self.survey_table_page.click_cancel_the_order()
                    self.survey_table_page.dialog_click_confirm_button()
                    self.enter_house_detail(house_code)
            self.main_up_view.clear_all_title()
            self.main_left_view.change_role('经纪人')
            self.enter_house_detail(house_code)
            survey_service.order_survey(gl_web_driver, survey_person_info['photographer'],
                                        exploration_info['exploration_time'],  # 预约实勘
                                        exploration_info['appointment_instructions'])
            if not self.app_login_page.check_is_logged_in():  # 拍摄实勘
                self.app_main_page.close_top_view()
                self.app_main_page.click_mine_button()
                self.app_mine_page.log_out()
            self.app_login_page.log_in(survey_person_info['photographer_phone'],
                                       survey_person_info['photographer_password'])
            self.app_main_page.click_mine_button()
            if '实勘人员' not in self.app_mine_page.get_user_role():
                self.app_mine_page.click_setting_center_button()
                self.app_mine_page.change_role_choose_role('实勘人员')
                self.app_mine_page.change_role_click_confirm_button()
            self.app_main_page.click_order_button()  # 拍摄实勘
            exploration_time = exploration_info['exploration_time'][0].split(',')[0]
            survey_service.shoot_survey(gl_app_driver, house_code, exploration_time)
            self.main_left_view.log_out()  # 上传实勘
            self.login_page.log_in(survey_person_info['photographer_phone'],
                                   survey_person_info['photographer_password'])
            self.main_left_view.change_role('实勘人员')
            survey_service.upload_survey(gl_web_driver, house_code)
            self.main_top_view.close_notification()
            self.main_left_view.log_out()
            self.login_page.log_in(ini.user_account, ini.user_password)
            self.main_left_view.change_role('超级管理员')
            self.enter_house_detail(house_code)
        self.house_detail_page.click_delete_survey_button()
        self.house_detail_page.dialog_click_confirm_button()
        assert self.main_top_view.find_notification_content() == '删除实勘成功'

