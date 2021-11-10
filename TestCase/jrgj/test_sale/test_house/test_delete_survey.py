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
from utils.logger import logger
from page_object.jrgj.web.main.rightviewpage import MainRightViewPage
from common.readconfig import ini
from utils.jsonutil import get_value
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.app.login.loginpage import AppLoginPage
from page_object.jrgj.app.main.mainpage import AppMainPage
from page_object.jrgj.app.mine.minepage import AppMinePage


house_code = ''
gl_web_driver = None
gl_app_driver = None
house_service = HouseService()
survey_service = SurveyService()


@allure.feature("房源详情模块-更多")
class TestDeleteSurvey(object):
    json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_out_show.json"
    login_page = None
    main_up_view = None
    main_top_view = None
    main_left_view = None
    main_right_view = None
    house_table_page = None
    house_detail_page = None
    agreement_list_page = None
    certificate_examine_page = None
    app_main_page = None
    app_mine_page = None
    app_login_page = None

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver, android_driver):
        global gl_web_driver, gl_app_driver
        gl_web_driver = web_driver
        gl_app_driver = android_driver
        self.login_page = LoginPage(gl_web_driver)
        self.main_up_view = MainUpViewPage(gl_web_driver)
        self.main_top_view = MainTopViewPage(gl_web_driver)
        self.main_left_view = MainLeftViewPage(gl_web_driver)
        self.main_right_view = MainRightViewPage(gl_web_driver)
        self.house_table_page = HouseTablePage(gl_web_driver)
        self.house_detail_page = HouseDetailPage(gl_web_driver)
        self.app_main_page = AppMainPage(gl_app_driver)
        self.app_mine_page = AppMinePage(gl_app_driver)
        self.app_login_page = AppLoginPage(gl_app_driver)
        yield
        self.main_up_view.clear_all_title()

    # @allure.step("验证房源状态")
    # def check_house_state(self):
    #     global house_code
    #     house_code = self.house_table_page.get_house_code_by_db(flag='买卖')
    #     if house_code == '':  # 判断房源是否存在，不存在则新增
    #         house_service.add_house(gl_web_driver, 'sale')
    #         self.main_up_view.clear_all_title()
    #     house_code = self.house_table_page.get_house_code_by_db(flag='买卖')

    @allure.step("验证房源状态")
    def check_house_state(self):
        global house_code
        if self.house_table_page.get_house_status_by_db(flag='sale') == '':  # 判断房源是否存在，不存在则新增
            house_service.add_house(gl_web_driver, 'sale')
            self.main_up_view.clear_all_title()
        house_code = self.house_table_page.get_house_status_by_db(flag='sale')[0][2]

    @allure.step("进入房源详情")
    def enter_house_detail(self):
        self.main_left_view.click_all_house_label()
        self.house_table_page.input_house_code_search(house_code)
        self.house_table_page.click_search_button()
        self.house_table_page.go_house_detail_by_row(1)

    @allure.story("测试删除实勘用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=3)
    def test_delete_survey(self):
        survey_person_info = get_value(self.json_file_path, ini.environment)
        exploration_info = get_value(self.json_file_path, 'exploration_info')
        self.check_house_state()
        self.main_left_view.change_role('超级管理员')
        self.enter_house_detail()
        if self.house_detail_page.check_survey_status() != '已上传':
            logger.info('未上传实勘，进行实勘预约')
            if self.house_detail_page.check_survey_status() == '已预约':  # 实勘退单
                self.house_detail_page.click_back_survey_button()
                self.house_detail_page.dialog_choose_back_exploration_reason('其他')
                self.house_detail_page.dialog_click_back_exploration_return_button()
            survey_service.order_survey(gl_web_driver, survey_person_info['photographer'],
                                        exploration_info['exploration_time'],  # 预约实勘
                                        exploration_info['appointment_instructions'])
            # if not self.app_login_page.check_login_page():  # 拍摄实勘
            #     self.app_main_page.close_top_view()
            #     self.app_main_page.click_mine_button()
            #     self.app_mine_page.log_out()
            # self.app_login_page.log_in(survey_person_info['photographer_phone'],
            #                            survey_person_info['photographer_password'])
            # self.app_main_page.click_mine_button()
            # if '实勘人员' not in self.app_mine_page.get_user_role():
            #     self.app_mine_page.click_setting_center_button()
            #     self.app_mine_page.change_role_choose_role('实勘人员')
            #     self.app_mine_page.change_role_click_confirm_button()
            self.app_main_page.click_order_button()  # 拍摄实勘
            exploration_time = exploration_info['exploration_time'][0].split(',')[0]
            survey_service.shoot_survey(gl_app_driver, house_code, exploration_time)
            self.main_left_view.log_out()  # 上传实勘
            self.login_page.log_in(survey_person_info['photographer_phone'],
                                   survey_person_info['photographer_password'])
            self.main_left_view.change_role('实勘人员')
            survey_service.upload_survey(gl_web_driver, house_code)
            self.main_left_view.log_out()
            self.login_page.log_in(ini.user_account, ini.user_password)
            self.main_left_view.change_role('超级管理员')
            self.enter_house_detail()
        self.house_detail_page.click_delete_survey_button()
        self.house_detail_page.dialog_click_confirm_button()
        assert self.main_top_view.find_notification_content() == '删除实勘成功'

# @pytest.fixture(scope="function", autouse=True)
# def test_prepare(self, web_driver):
#     login = LoginPage(web_driver)
#     main_upview = MainUpViewPage(web_driver)
#     main_leftview = MainLeftViewPage(web_driver)
#     yield
#     main_leftview.log_out()
#     login.log_in(ini.user_account, ini.user_password)
#     main_upview.clear_all_title()
#
# @allure.story("测试房源删除实勘")
# @pytest.mark.sale
# @pytest.mark.house
# @pytest.mark.run(order=13)
# @pytest.mark.parametrize("account", account_list)
# def test_001(self, web_driver, android_driver, account):
#     login = LoginPage(web_driver)
#     main_leftview = MainLeftViewPage(web_driver)
#     main_upview = MainUpViewPage(web_driver)
#     main_topview = MainTopViewPage(web_driver)
#     house_table = HouseTablePage(web_driver)
#     house_detail = HouseDetailPage(web_driver)
#     survey_table = SurveyTablePage(web_driver)
#     survey_detail = SurveyDetailPage(web_driver)
#     app_main = AppMainPage(android_driver)
#     app_mine = AppMinePage(android_driver)
#     app_login = AppLoginPage(android_driver)
#     app_order_table = AppOrderTablePage(android_driver)
#     app_order_detail = AppOrderDetailPage(android_driver)
#
#     main_leftview.change_role('经纪人')
#     house_code = house_table.get_house_code_by_db(flag='买卖')
#     assert house_code != ''
#     log.info('房源编号为：' + house_code)
#     main_leftview.click_all_house_label()
#     house_table.click_sale_tab()
#     house_table.click_all_house_tab()
#     house_table.click_reset_button()
#     house_table.clear_filter(flag='买卖')
#     house_table.input_house_code_search(house_code)
#     house_table.click_search_button()
#     house_table.go_house_detail_by_row(1)
#     if house_detail.check_survey_status() == '已预约':
#         log.info('未预约实勘，进行实勘预约')  # 须优化实勘已上传的情况
#         house_detail.click_back_survey_button()
#         house_detail.dialog_choose_back_exploration_reason('其他')
#         house_detail.dialog_click_back_exploration_return_button()
#     elif house_detail.check_survey_status() == '已上传':
#         main_leftview.change_role('超级管理员')
#         main_leftview.click_all_house_label()
#         house_table.click_sale_tab()
#         house_table.click_all_house_tab()
#         house_table.click_reset_button()
#         house_table.clear_filter(flag='买卖')
#         house_table.input_house_code_search(house_code)
#         house_table.click_search_button()
#         house_table.go_house_detail_by_row(1)
#         house_detail.click_delete_survey_button()
#         house_detail.dialog_click_confirm_button()
#         main_leftview.change_role('经纪人')
#         main_leftview.click_all_house_label()
#         house_table.click_sale_tab()
#         house_table.click_all_house_tab()
#         house_table.click_reset_button()
#         house_table.clear_filter(flag='买卖')
#         house_table.input_house_code_search(house_code)
#         house_table.click_search_button()
#         house_table.go_house_detail_by_row(1)
#     else:
#         pass
#     house_detail.click_survey_appointment_button()
#     house_detail.dialog_choose_normal_survey()
#     house_detail.dialog_choose_photographer(self.person_info['实勘人员']['姓名'])
#     house_detail.dialog_choose_exploration_time(self.exploration_info['exploration_time'])
#     house_detail.dialog_input_appointment_instructions(self.exploration_info['appointment_instructions'])
#     house_detail.dialog_click_confirm_button()
#     main_upview.clear_all_title()
#     if not app_login.check_login_page():
#         app_main.close_top_view()
#         app_main.click_mine_button()
#         app_mine.log_out()
#     app_login.log_in(self.person_info['实勘人员']['电话'], self.person_info['实勘人员']['密码'])
#     app_main.click_mine_button()
#     if '实勘人员' not in app_mine.get_user_role():
#         app_mine.click_setting_center_button()
#         app_mine.change_role_choose_role('实勘人员')
#         app_mine.change_role_click_confirm_button()
#     app_main.click_order_button()
#     app_order_table.click_search_button()
#     app_order_table.input_search_content(house_code)
#     if self.exploration_info['exploration_time'][0] == '今天':
#         date = dt_strftime("%d %m %Y")
#     elif self.exploration_info['exploration_time'][0] == '明天':
#         date = dt_strftime_with_delta(1, "%d %m %Y")
#     else:
#         raise '传值错误'
#     app_order_table.choose_date(date)
#     app_order_table.go_order_detail_by_index(1)
#     app_order_detail.click_start_shot_button()
#     app_order_detail.click_end_shot_button()
#     main_leftview.log_out()
#     login.log_in(self.person_info['实勘人员']['电话'], self.person_info['实勘人员']['密码'])
#     main_leftview.change_role('实勘人员')
#     main_leftview.click_survey_management_label()
#     survey_table.click_reset_button()
#     survey_table.input_house_code_search(house_code)
#     survey_table.click_search_button()
#     survey_table.click_upload_survey_button_by_row(1)
#     upload_pictures = [cm.tmp_picture_file, cm.tmp_picture_file]
#     survey_detail.upload_picture(upload_pictures)
#     survey_detail.set_title_picture_by_index(randint(1, len(upload_pictures)))
#     survey_detail.click_save_button()
#     main_leftview.log_out()
#     login.log_in(account[0], account[1])
#     main_leftview.change_role('超级管理员')
#     main_leftview.click_all_house_label()
#     house_table.click_sale_tab()
#     house_table.click_all_house_tab()
#     house_table.click_reset_button()
#     house_table.clear_filter(flag='买卖')
#     house_table.input_house_code_search(house_code)
#     house_table.click_search_button()
#     house_table.go_house_detail_by_row(1)
#     house_detail.click_delete_survey_button()
#     if account[0] == ini.user_account:
#         house_detail.dialog_click_confirm_button()
#         assert main_topview.find_notification_content() == '删除实勘成功'
#     else:
#         assert house_detail.get_tooltip_content() == '该房源状态不允许操作'
