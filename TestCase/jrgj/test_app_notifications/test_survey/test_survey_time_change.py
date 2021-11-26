#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_survey_time_change.py
@date: 2021/11/15 0015
"""
import allure
import pytest
from page_object.jrgj.app.login.loginpage import AppLoginPage
from utils.logger import logger
from utils.timeutil import dt_strftime, dt_strftime_with_delta
from common.readconfig import ini
from page_object.common.web.login.loginpage import LoginPage
from page_object.common.app.common.commonpage import AppCommonPage
from page_object.jrgj.app.main.mainpage import AppMainPage
from page_object.jrgj.app.message.tablepage import AppMessageTablePage
from page_object.jrgj.app.mine.minepage import AppMinePage
from page_object.common.app.notifications.tablepage import AppNotificationsTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.survey.tablepage import SurveyTablePage


@allure.feature("测试APP通知-实勘")
class TestSurveyTimeChange(object):

    change_time = ["明天", "14:00-15:00"]

    @pytest.fixture(scope="class", autouse=True)
    def setup_and_teardown(self, web_driver, android_driver):
        main_leftview = MainLeftViewPage(web_driver)
        app_login = AppLoginPage(android_driver)
        app_main = AppMainPage(android_driver)
        app_mine = AppMinePage(android_driver)

        main_leftview.change_role('经纪人')
        app_login.log_in(ini.user_account, ini.user_password)
        app_main.close_top_view()
        app_main.click_mine_button()
        yield
        app_main.click_mine_button()
        app_mine.log_out()
        main_leftview.change_role('经纪人')

    @allure.story("预约实勘时间更改")
    def test_001(self, web_driver, android_driver):
        app_common = AppCommonPage(android_driver)
        app_main = AppMainPage(android_driver)
        app_notification = AppNotificationsTablePage(android_driver)
        app_message_table = AppMessageTablePage(android_driver)

        self.appointment_survey(web_driver)
        self.change_survey_time(web_driver)
        if self.change_time[0] == '今天':
            survey_change_date = dt_strftime("%Y-%m-%d")
        elif self.change_time[0] == '明天':
            survey_change_date = dt_strftime_with_delta(1, "%Y-%m-%d")
        else:
            raise ValueError("预约时间不对")
        app_common.open_notifications()
        pytest.assume(app_notification.get_notification_title_by_row(1) == '预约实勘时间更改')
        pytest.assume(app_notification.get_notification_content_by_row(1) in
                      "房源编号" + self.house_code + ini.house_community_name + "预约实勘时间已被摄影师更改，最新实勘时间"
                      + survey_change_date + " " + self.change_time[1])
        app_notification.dismiss_all_notification()
        app_main.click_message_button()
        app_message_table.click_notification_tab()
        pytest.assume(app_message_table.get_house_message() ==
                      "房源编号" + self.house_code + ini.house_community_name + "预约实勘时间已被摄影师更改，最新实勘时间"
                      + survey_change_date + " " + self.change_time[1])
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '预约实勘时间更改')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "房源编号" + self.house_code + ini.house_community_name + "预约实勘时间已被摄影师更改，最新实勘时间"
                      + survey_change_date + " " + self.change_time[1])
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '预约实勘时间更改')
        pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "房源编号" + self.house_code + ini.house_community_name + "预约实勘时间已被摄影师更改，最新实勘时间"
                      + survey_change_date + " " + self.change_time[1])
        app_common.back_previous_step()
        app_common.back_previous_step()

    @allure.step("预约实勘")
    def appointment_survey(self, web_driver):
        login = LoginPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        survey_table = SurveyTablePage(web_driver)

        self.house_code = house_table.get_house_code_by_db(flag='买卖')
        assert self.house_code != '', "不存在房源"
        logger.info('房源编号为：' + self.house_code)
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(self.house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        if house_detail.check_survey_status() == '已预约':
            logger.info('已预约实勘，取消实勘预约')  # 须优化实勘已上传的情况
            main_leftview.change_role('超级管理员')
            main_leftview.click_survey_management_label()
            survey_table.input_house_code_search(self.house_code)
            survey_table.click_search_button()
            if survey_table.get_order_status_by_row(1) == '待拍摄':
                survey_person_phone = survey_table.get_survey_person_phone_by_row(1)
                if survey_person_phone != ini.survey_user_account:
                    raise ValueError("摄影师账号不知道密码，需手动处理")
                main_leftview.log_out()
                login.log_in(survey_person_phone, 'Autotest1')  # 切换其他门店经纪人账号预约实勘
                main_leftview.change_role('实勘人员')
                main_leftview.click_survey_management_label()
                survey_table.input_house_code_search(self.house_code)
                survey_table.click_search_button()
                survey_table.click_back_order_button_by_row(1)
                survey_table.back_order_dialog_choose_reason('其他')
                survey_table.back_order_dialog_click_back_order_button()
            elif survey_table.get_order_status_by_row(1) == '拍摄完成':
                survey_table.click_cancel_order_button_by_row(1)
                survey_table.dialog_click_confirm_button()
            else:
                survey_table.click_vr_survey_tab()
                survey_table.input_house_code_search(self.house_code)
                survey_table.click_search_button()
                if survey_table.get_order_status_by_row(1) == '待拍摄':
                    survey_person_phone = survey_table.get_survey_person_phone_by_row(1)
                    main_leftview.log_out()
                    if survey_person_phone != ini.survey_user_account:
                        raise ValueError("摄影师账号不知道密码，需手动处理")
                    login.log_in(survey_person_phone, 'Autotest1')  # 切换其他门店经纪人账号预约实勘
                    main_leftview.change_role('实勘人员')
                    main_leftview.click_survey_management_label()
                    survey_table.click_vr_survey_tab()
                    survey_table.input_house_code_search(self.house_code)
                    survey_table.click_search_button()
                    survey_table.click_back_order_button_by_row(1)
                    survey_table.back_order_dialog_choose_reason('其他')
                    survey_table.back_order_dialog_click_back_order_button()
                elif survey_table.get_order_status_by_row(1) == '拍摄完成':
                    survey_table.click_cancel_order_button_by_row(1)
                    survey_table.dialog_click_confirm_button()
                else:
                    raise ValueError("实勘该状态需手动处理")
            main_leftview.log_out()
            login.log_in(ini.user_account, ini.user_password)
            main_leftview.change_role('经纪人')
            main_leftview.click_all_house_label()
            house_table.clear_filter(flag='买卖')
            house_table.input_house_code_search(self.house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row(1)
        elif house_detail.check_survey_status() == '已上传':
            main_leftview.change_role('超级管理员')
            main_leftview.click_all_house_label()
            house_table.click_sale_tab()
            house_table.click_all_house_tab()
            house_table.clear_filter(flag='买卖')
            house_table.input_house_code_search(self.house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row(1)
            house_detail.click_delete_survey_button()
            house_detail.dialog_click_confirm_button()
            main_topview.close_notification()
            main_leftview.log_out()
            login.log_in(ini.user_account, ini.user_password)
            main_leftview.change_role('经纪人')
            main_leftview.click_all_house_label()
            house_table.clear_filter(flag='买卖')
            house_table.input_house_code_search(self.house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row(1)
        else:
            pass
        house_detail.click_survey_appointment_button()
        house_detail.dialog_choose_normal_survey()
        house_detail.dialog_choose_photographer(ini.survey_user_account)
        house_detail.dialog_choose_exploration_time(["明天", "16:00-17:00"])
        house_detail.dialog_input_appointment_instructions('自动化测试')
        house_detail.dialog_click_confirm_button()
        main_topview.close_notification()
        main_leftview.change_role("初级经纪人")

    @allure.step("更改实勘时间")
    def change_survey_time(self, web_driver):
        login = LoginPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        survey_table = SurveyTablePage(web_driver)

        main_leftview.log_out()
        login.log_in(ini.survey_user_account, ini.survey_user_password)
        main_leftview.click_survey_management_label()
        survey_table.input_house_code_search(self.house_code)
        survey_table.click_search_button()
        survey_table.click_change_time_by_row(1)
        survey_table.dialog_click_confirm_button()
        survey_table.change_time_dialog_choose_time(self.change_time)
        survey_table.dialog_click_confirm_button()
        survey_table.dialog_click_known_button()
        main_leftview.log_out()
        login.log_in(ini.user_account, ini.user_password)
        main_leftview.change_role("初级经纪人")
