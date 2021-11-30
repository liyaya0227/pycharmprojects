#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_vr_survey.py
@date: 2021/11/17 0017
"""
import allure
import pytest
import requests
from page_object.jrgj.web.survey.detailpage import SurveyDetailPage
from utils.timeutil import sleep
from page_object.common.app.notifications.tablepage import AppNotificationsTablePage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from utils.logger import logger
from utils.timeutil import dt_strftime, dt_strftime_with_delta
from common.readconfig import ini
from page_object.common.web.login.loginpage import LoginPage
from page_object.common.app.common.commonpage import AppCommonPage
from page_object.jrgj.app.login.loginpage import AppLoginPage
from page_object.jrgj.app.main.mainpage import AppMainPage
from page_object.jrgj.app.message.tablepage import AppMessageTablePage
from page_object.jrgj.app.mine.minepage import AppMinePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.survey.tablepage import SurveyTablePage
from page_object.jrgj.web.vrexamine.tablepage import VrExamineTablePage
from page_object.jrgj.web.vrexamine.detailpage import VrExamineDetailPage


@pytest.mark.app_notifications
@allure.feature("测试APP通知-实勘")
class TestVRSurvey(object):

    exploration_time = ["明天", "16:00-17:00"]
    feedback = "自动化测试需要，实勘M反馈" + dt_strftime("%Y%m%d%H%M%S")

    @pytest.fixture(scope="class", autouse=True)
    def setup_and_teardown(self, web_driver, android_driver, android_driver2):
        main_leftview = MainLeftViewPage(web_driver)
        app_login = AppLoginPage(android_driver)
        app_main = AppMainPage(android_driver)
        app_mine = AppMinePage(android_driver)
        app_message_table = AppMessageTablePage(android_driver)
        app_common = AppCommonPage(android_driver)
        app_notification = AppNotificationsTablePage(android_driver)
        second_app_login = AppLoginPage(android_driver2)
        second_app_main = AppMainPage(android_driver2)
        second_app_mine = AppMinePage(android_driver2)
        second_app_message_table = AppMessageTablePage(android_driver2)
        second_app_common = AppCommonPage(android_driver2)
        second_app_notification = AppNotificationsTablePage(android_driver2)

        main_leftview.change_role('经纪人')
        app_login.log_in(ini.user_account, ini.user_password)
        app_main.close_top_view()
        app_main.click_message_button()
        app_message_table.click_notification_tab()
        app_message_table.click_clear_message_button()
        app_common.open_notifications()
        app_notification.dismiss_all_notification()
        second_app_login.log_in(ini.survey_user_account, ini.survey_user_password)
        second_app_main.close_top_view()
        second_app_main.click_message_button()
        second_app_message_table.click_notification_tab()
        second_app_message_table.click_clear_message_button()
        second_app_common.open_notifications()
        second_app_notification.dismiss_all_notification()
        yield
        app_main.click_mine_button()
        app_mine.log_out()
        second_app_main.click_mine_button()
        second_app_mine.log_out()
        main_leftview.change_role('经纪人')

    @allure.story("预约VR实勘")
    def test_001(self, web_driver, android_driver, android_driver2):
        app_common = AppCommonPage(android_driver)
        app_notification = AppNotificationsTablePage(android_driver)
        app_message_table = AppMessageTablePage(android_driver)
        second_app_common = AppCommonPage(android_driver2)
        second_app_notification = AppNotificationsTablePage(android_driver2)
        second_app_message_table = AppMessageTablePage(android_driver2)

        self.appointment_survey(web_driver)
        if self.exploration_time[0] == '今天':
            survey_date = dt_strftime("%Y-%m-%d")
        elif self.exploration_time[0] == '明天':
            survey_date = dt_strftime_with_delta(1, "%Y-%m-%d")
        else:
            raise ValueError("预约时间不对")
        app_common.open_notifications()
        pytest.assume(app_notification.get_notification_title_by_row(1) == '预约实勘-预约人')
        pytest.assume(app_notification.get_notification_content_by_row(1) in
                      "实勘预约成功，您已经预约" + self.survey_person_name + "在" + survey_date + " "
                      + self.exploration_time[1] + "到" + ini.house_community_name + " " + ini.house_building_id
                      + "-" + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "进行实勘拍摄，订单编号为" + self.survey_code + "。")
        app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_house_message() ==
                      "实勘预约成功，您已经预约" + self.survey_person_name + "在" + survey_date + " "
                      + self.exploration_time[1] + "到" + ini.house_community_name + " " + ini.house_building_id
                      + "-" + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "进行实勘拍摄，订单编号为" + self.survey_code + "。")
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '预约实勘-预约人')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "实勘预约成功，您已经预约" + self.survey_person_name + "在" + survey_date + " "
                      + self.exploration_time[1] + "到" + ini.house_community_name + " " + ini.house_building_id
                      + "-" + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "进行实勘拍摄，订单编号为" + self.survey_code + "。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '预约实勘-预约人')
        pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "实勘预约成功，您已经预约" + self.survey_person_name + "在" + survey_date + " "
                      + self.exploration_time[1] + "到" + ini.house_community_name + " " + ini.house_building_id
                      + "-" + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "进行实勘拍摄，订单编号为" + self.survey_code + "。")
        app_common.back_previous_step()
        app_common.back_previous_step()
        second_app_common.open_notifications()
        pytest.assume(second_app_notification.get_notification_title_by_row(1) == '预约实勘-实勘人摄影师')
        pytest.assume(second_app_notification.get_notification_content_by_row(1) ==
                      "您已经被预约在" + survey_date + " "
                      + self.exploration_time[1] + "到" + ini.house_community_name + " " + ini.house_building_id
                      + "-" + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "进行实勘拍摄，订单编号为" + self.survey_code + "。")
        second_app_notification.dismiss_all_notification()
        second_app_common.down_swipe_for_refresh()
        pytest.assume(second_app_message_table.get_house_message() in "您已经被预约在" + survey_date + " "
                      + self.exploration_time[1] + "到" + ini.house_community_name + " " + ini.house_building_id
                      + "-" + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "进行实勘拍摄，订单编号为" + self.survey_code + "。")
        second_app_message_table.go_house_message_list()
        pytest.assume(second_app_message_table.get_message_list_message_title_by_row(1) == '预约实勘-实勘人摄影师')
        pytest.assume(second_app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您已经被预约在" + survey_date + " "
                      + self.exploration_time[1] + "到" + ini.house_community_name + " " + ini.house_building_id
                      + "-" + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "进行实勘拍摄，订单编号为" + self.survey_code + "。")
        second_app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(second_app_message_table.get_message_detail_message_title() == '预约实勘-实勘人摄影师')
        pytest.assume(second_app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(second_app_message_table.get_message_detail_message_content() ==
                      "您已经被预约在" + survey_date + " "
                      + self.exploration_time[1] + "到" + ini.house_community_name + " " + ini.house_building_id
                      + "-" + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "进行实勘拍摄，订单编号为" + self.survey_code + "。")
        second_app_common.back_previous_step()
        second_app_common.back_previous_step()
        self.upload_vr(self.survey_code)
        app_common.open_notifications()
        pytest.assume(app_notification.get_notification_title_by_row(1) == 'VR实勘待审核')
        pytest.assume(app_notification.get_notification_content_by_row(1) in "您预约的房源" + ini.house_community_name
                      + self.house_code + "实勘，VR 实勘已生成，请在VR审核页面审核。")
        app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_house_message() == "您预约的房源" + ini.house_community_name
                      + self.house_code + "实勘，VR 实勘已生成，请在VR审核页面审核。")
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == 'VR实勘待审核')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] == "您预约的房源"
                      + ini.house_community_name + self.house_code + "实勘，VR 实勘已生成，请在VR审核页面审核。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == 'VR实勘待审核')
        pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() == "您预约的房源" + ini.house_community_name
                      + self.house_code + "实勘，VR 实勘已生成，请在VR审核页面审核。")
        app_common.back_previous_step()
        app_common.back_previous_step()
        self.agent_reject_vr_examine(web_driver)
        second_app_common.open_notifications()
        pytest.assume(second_app_notification.get_notification_title_by_row(1) == 'VR审核实勘驳回')
        pytest.assume(second_app_notification.get_notification_content_by_row(1) in "您拍摄的房源"
                      + ini.house_community_name + self.house_code + "，VR实勘已被预约实勘人审核驳回")
        second_app_notification.dismiss_all_notification()
        second_app_common.down_swipe_for_refresh()
        pytest.assume(second_app_message_table.get_house_message() == "您拍摄的房源" + ini.house_community_name
                      + self.house_code + "，VR实勘已被预约实勘人审核驳回")
        second_app_message_table.go_house_message_list()
        pytest.assume(second_app_message_table.get_message_list_message_title_by_row(1) == 'VR审核实勘驳回')
        pytest.assume(second_app_message_table.get_message_list_message_content_by_row(1)[5:] == "您拍摄的房源"
                      + ini.house_community_name + self.house_code + "，VR实勘已被预约实勘人审核驳回")
        second_app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(second_app_message_table.get_message_detail_message_title() == 'VR审核实勘驳回')
        pytest.assume(second_app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(second_app_message_table.get_message_detail_message_content() == "您拍摄的房源"
                      + ini.house_community_name + self.house_code + "，VR实勘已被预约实勘人审核驳回")
        second_app_common.back_previous_step()
        second_app_common.back_previous_step()
        self.upload_vr(self.survey_code)
        self.agent_pass_vr_examine(web_driver)
        app_common.open_notifications()
        pytest.assume(app_notification.get_notification_title_by_row(1) == '实勘上传完成图片')
        pytest.assume(app_notification.get_notification_content_by_row(1) in
                      "您好！您预约的房源" + ini.house_community_name + self.house_code
                      + "实勘，摄影师已上传完成，实勘详情请去系统内查看。")
        app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_house_message() ==
                      "您好！您预约的房源" + ini.house_community_name + self.house_code
                      + "实勘，摄影师已上传完成，实勘详情请去系统内查看。")
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '实勘上传完成图片')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您好！您预约的房源" + ini.house_community_name + self.house_code
                      + "实勘，摄影师已上传完成，实勘详情请去系统内查看。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '实勘上传完成图片')
        pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您好！您预约的房源" + ini.house_community_name + self.house_code
                      + "实勘，摄影师已上传完成，实勘详情请去系统内查看。")
        app_common.back_previous_step()
        app_common.back_previous_step()
        second_app_common.open_notifications()
        pytest.assume(second_app_notification.get_notification_title_by_row(1) == 'VR审核实勘完成')
        pytest.assume(second_app_notification.get_notification_content_by_row(1) in "您拍摄的房源"
                      + ini.house_community_name + self.house_code + "，VR实勘已被预约实勘人审核通过")
        second_app_notification.dismiss_all_notification()
        second_app_common.down_swipe_for_refresh()
        pytest.assume(second_app_message_table.get_house_message() == "您拍摄的房源" + ini.house_community_name
                      + self.house_code + "，VR实勘已被预约实勘人审核通过")
        second_app_message_table.go_house_message_list()
        pytest.assume(second_app_message_table.get_message_list_message_title_by_row(1) == 'VR审核实勘完成')
        pytest.assume(second_app_message_table.get_message_list_message_content_by_row(1)[5:] == "您拍摄的房源"
                      + ini.house_community_name + self.house_code + "，VR实勘已被预约实勘人审核通过")
        second_app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(second_app_message_table.get_message_detail_message_title() == 'VR审核实勘完成')
        pytest.assume(second_app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(second_app_message_table.get_message_detail_message_content() == "您拍摄的房源"
                      + ini.house_community_name + self.house_code + "，VR实勘已被预约实勘人审核通过")
        second_app_common.back_previous_step()
        second_app_common.back_previous_step()
        self.survey_m_feedback(web_driver)
        second_app_common.open_notifications()
        pytest.assume(second_app_notification.get_notification_title_by_row(1) == '实勘人M反馈')
        pytest.assume(second_app_notification.get_notification_content_by_row(1) in "您好！您拍摄的房源 "
                      + ini.house_community_name + ini.house_building_id + ini.house_building_cell
                      + ini.house_doorplate + "实勘订单编号" + self.survey_code + "收到反馈，反馈内容：" + self.feedback
                      + "，请及时处理。")
        second_app_notification.dismiss_all_notification()
        second_app_common.down_swipe_for_refresh()
        pytest.assume(second_app_message_table.get_house_message() == "您好！您拍摄的房源 "
                      + ini.house_community_name + ini.house_building_id + ini.house_building_cell
                      + ini.house_doorplate + "实勘订单编号" + self.survey_code + "收到反馈，反馈内容：" + self.feedback
                      + "，请及时处理。")
        second_app_message_table.go_house_message_list()
        pytest.assume(second_app_message_table.get_message_list_message_title_by_row(1) == '实勘人M反馈')
        pytest.assume(second_app_message_table.get_message_list_message_content_by_row(1)[5:] == "您好！您拍摄的房源 "
                      + ini.house_community_name + ini.house_building_id + ini.house_building_cell
                      + ini.house_doorplate + "实勘订单编号" + self.survey_code + "收到反馈，反馈内容：" + self.feedback
                      + "，请及时处理。")
        second_app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(second_app_message_table.get_message_detail_message_title() == '实勘人M反馈')
        pytest.assume(second_app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(second_app_message_table.get_message_detail_message_content() == "您好！您拍摄的房源 "
                      + ini.house_community_name + ini.house_building_id + ini.house_building_cell
                      + ini.house_doorplate + "实勘订单编号" + self.survey_code + "收到反馈，反馈内容：" + self.feedback
                      + "，请及时处理。")
        second_app_common.back_previous_step()
        second_app_common.back_previous_step()

    @allure.step("预约VR实勘")
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
                main_leftview.log_out()
                if survey_person_phone != ini.survey_user_account:
                    raise ValueError("摄影师账号不知道密码，需手动处理")
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
            main_leftview.change_role('经纪人')
            main_leftview.click_all_house_label()
            house_table.clear_filter(flag='买卖')
            house_table.input_house_code_search(self.house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row(1)
        else:
            pass
        house_detail.click_survey_appointment_button()
        house_detail.dialog_choose_vr_survey()
        house_detail.dialog_choose_photographer(ini.survey_user_account)
        house_detail.dialog_choose_exploration_time(self.exploration_time)
        house_detail.dialog_input_appointment_instructions('自动化测试')
        house_detail.dialog_click_confirm_button()
        main_topview.close_notification()
        main_leftview.change_role("超级管理员")
        main_leftview.click_survey_management_label()
        survey_table.click_vr_survey_tab()
        survey_table.input_house_code_search(self.house_code)
        survey_table.click_search_button()
        self.survey_code = survey_table.get_survey_code_by_row(1)
        self.survey_person_name = survey_table.get_survey_person_name_by_row(1)
        main_leftview.change_role("初级经纪人")

    @allure.step("实勘人上传VR")
    def upload_vr(self, survey_code):
        header = {'Content-Type': 'application/json', 'Connection': 'close'}
        json = {
            "city": "",
            "project_name": 122,
            "creator": 110,
            "url": "?m=897a5cae_Ow0f_b6f9",
            "timestamp": 1616641475,
            "mid": "1bcfba3e_6PbZ_b6f9_cs",
            "vr_cover": "https://static.jingrizf.com/sz/img/1624500355510752.jpg",
            "creator_account": "shzyvrcs01",
            "hid": survey_code,
            "key": "8613add538260d7a7026b021c379105e",
            "survey": [{
                "path": "https://static.jingrizf.com/img/1616655312438.jpg",
                "name": "餐厅"
            }, {
                "path": "https://static.jingrizf.com/img/1616655312398.jpg",
                "name": "阳台"
            }, {
                "path": "https://static.jingrizf.com/img/1616655312544.jpg",
                "name": "花园"
            }, {
                "path": "https://static.jingrizf.com/img/1614771706813.jpg",
                "name": "厨房"
            }, {
                "path": "https://static.jingrizf.com/img/160673226627938.jpg",
                "name": "卧室"
            }, {
                "path": "https://static.jingrizf.com/img/1614771725575.jpg",
                "name": "卫生间"
            }, {
                "path": "https://static.jingrizf.com/img/1614771719314.jpg",
                "name": "客厅"
            }, {
                "path": "https://static.jingrizf.com/img/1616637954581.png",
                "name": "衣帽间"
            }, {
                "path": "https://static.jingrizf.com/img/1616637953715.png",
                "name": "储藏室"
            }],
            "floorplan_info": {
                "floors": [{
                    "color_pic": "https://static.jingrizf.com/file/1617686019315.jpg",
                    "bw_pic": "https://static.jingrizf.com/file/1617686019315.jpg",
                    "name": "负一层"
                }, {
                    "color_pic": "https://static.jingrizf.com/img/1618292801541.jpg",
                    "bw_pic": "https://static.jingrizf.com/img/1618292801541.jpg",
                    "name": "一层"
                }],
                "merge_bw_pic": "",
                "is_multi_floor": 1
            }
        }
        url = "https://uat-piblicgateway.jingrizf.com/system/vr/house/notify"
        response = requests.get(url=url, headers=header, json=json)
        if response.json()['errorMsg'] != '房源信息更新成功！':
            raise ValueError("VR 上传失败")
        sleep(8)

    @allure.step("经纪人驳回VR审核")
    def agent_reject_vr_examine(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        vr_examine_table = VrExamineTablePage(web_driver)
        vr_examine_detail = VrExamineDetailPage(web_driver)

        main_leftview.click_vr_examine_label()
        vr_examine_table.input_survey_code_search(self.survey_code)
        vr_examine_table.click_search_button()
        vr_examine_table.click_examine_button_by_row(1)
        vr_examine_detail.reject_vr_examine("自动化测试需要" + dt_strftime("%Y%m%d%H%M%S"))
        main_upview.clear_all_title()

    @allure.step("经纪人通过VR审核")
    def agent_pass_vr_examine(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        vr_examine_table = VrExamineTablePage(web_driver)
        vr_examine_detail = VrExamineDetailPage(web_driver)

        main_leftview.click_vr_examine_label()
        vr_examine_table.input_survey_code_search(self.survey_code)
        vr_examine_table.click_search_button()
        vr_examine_table.click_examine_button_by_row(1)
        vr_examine_detail.pass_vr_examine()
        main_topview.close_notification()
        main_upview.clear_all_title()

    @allure.step("实勘M反馈")
    def survey_m_feedback(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        survey_table = SurveyTablePage(web_driver)
        survey_detail = SurveyDetailPage(web_driver)

        main_leftview.change_role("实勘M")
        main_leftview.click_survey_management_label()
        survey_table.click_vr_survey_tab()
        survey_table.input_survey_code_search(self.survey_code)
        survey_table.click_search_button()
        survey_table.click_order_detail_button_by_row(1)
        survey_detail.input_feedback(self.feedback)
        survey_detail.click_submit_button()
        main_leftview.change_role("初级经纪人")
