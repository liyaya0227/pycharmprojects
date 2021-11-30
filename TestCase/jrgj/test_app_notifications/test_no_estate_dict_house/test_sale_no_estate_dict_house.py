#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_sale_no_estate_dict_house.py
@date: 2021/11/29 0029
"""
import string
import allure
import pytest
from config.conf import cm
from utils.logger import logger
from common.readconfig import ini
from page_object.common.app.common.commonpage import AppCommonPage
from page_object.jrgj.app.login.loginpage import AppLoginPage
from page_object.jrgj.app.main.mainpage import AppMainPage
from page_object.jrgj.app.message.tablepage import AppMessageTablePage
from page_object.jrgj.app.mine.minepage import AppMinePage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.common.app.notifications.tablepage import AppNotificationsTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.house.addpage import HouseAddPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.nodicthosuefeedback.tablepage import NoDictHouseFeedbackTablePage


@pytest.mark.app_notifications
@allure.feature("测试APP通知-无楼盘字典反馈")
class TestSaleNoEstateDictHouseFeedback(object):

    @pytest.fixture(scope="class", autouse=True)
    def setup_and_teardown(self, web_driver, android_driver):
        app_login = AppLoginPage(android_driver)
        app_main = AppMainPage(android_driver)
        app_mine = AppMinePage(android_driver)
        app_common = AppCommonPage(android_driver)
        app_notification = AppNotificationsTablePage(android_driver)
        app_message_table = AppMessageTablePage(android_driver)
        main_leftview = MainLeftViewPage(web_driver)

        main_leftview.change_role('经纪人')
        app_login.log_in(ini.user_account, ini.user_password)
        app_main.close_top_view()
        app_main.click_message_button()
        app_message_table.click_notification_tab()
        app_message_table.click_clear_message_button()
        app_common.open_notifications()
        app_notification.dismiss_all_notification()
        yield
        app_main.click_mine_button()
        app_mine.log_out()
        main_leftview.change_role('经纪人')

    @allure.story("买卖房源处理")
    def test_001(self, web_driver, android_driver):
        app_common = AppCommonPage(android_driver)
        app_notification = AppNotificationsTablePage(android_driver)
        app_message_table = AppMessageTablePage(android_driver)

        house_info = {
            'estate_name': '自动化测试楼盘' + "".join(map(lambda x: string.digits, range(2))),
            'building_id': "".join(map(lambda x: string.digits, range(2))),
            'building_cell': "".join(map(lambda x: string.digits, range(2))),
            'floor': "".join(map(lambda x: string.digits, range(2))),
            'doorplate': "".join(map(lambda x: string.digits, range(2))),
            'cert_files': [cm.tmp_picture_file]
        }
        reject_reason = "".join(map(lambda x: string.ascii_letters, range(2)))
        match_estate_info = {
            'estate_name': '自动化测试楼盘',
            'building_id': '1',
            'building_cell': '1',
            'floor': '1',
            'doorplate': '1008'
        }
        self.create_no_dict_house(web_driver, house_info)
        app_common.open_notifications()
        pytest.assume(app_notification.get_notification_title_by_row(1) == '房源反馈创建完成')
        pytest.assume(app_notification.get_notification_content_by_row(1) in
                      "您收到一条无楼盘字典房源反馈，反馈人" + self.feedback_person + "，楼盘信息" + house_info["estate_name"]
                      + "-" + house_info["building_id"] + "-" + house_info["building_cell"] + "-"
                      + house_info["floor"] + "-" + house_info["doorplate"])
        app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_house_message() ==
                      "您收到一条无楼盘字典房源反馈，反馈人" + self.feedback_person + "，楼盘信息" + house_info["estate_name"]
                      + "-" + house_info["building_id"] + "-" + house_info["building_cell"] + "-"
                      + house_info["floor"] + "-" + house_info["doorplate"])
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '房源反馈创建完成')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您收到一条无楼盘字典房源反馈，反馈人" + self.feedback_person + "，楼盘信息" + house_info["estate_name"]
                      + "-" + house_info["building_id"] + "-" + house_info["building_cell"] + "-"
                      + house_info["floor"] + "-" + house_info["doorplate"])
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '房源反馈创建完成')
        pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您收到一条无楼盘字典房源反馈，反馈人" + self.feedback_person + "，楼盘信息" + house_info["estate_name"]
                      + "-" + house_info["building_id"] + "-" + house_info["building_cell"] + "-"
                      + house_info["floor"] + "-" + house_info["doorplate"])
        app_common.back_previous_step()
        app_common.back_previous_step()
        self.reject_no_dict_house_feedback_by_estate_name(web_driver, house_info['estate_name'], reject_reason)
        app_common.open_notifications()
        pytest.assume(app_notification.get_notification_title_by_row(1) == '房源处理被驳回')
        pytest.assume(app_notification.get_notification_content_by_row(1) in
                      "您反馈的无楼盘字典房源已被驳回，驳回理由" + self.reject_reason)
        app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_house_message() ==
                      "您反馈的无楼盘字典房源已被驳回，驳回理由" + self.reject_reason)
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '房源处理被驳回')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您反馈的无楼盘字典房源已被驳回，驳回理由" + self.reject_reason)
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '房源处理被驳回')
        pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您反馈的无楼盘字典房源已被驳回，驳回理由" + self.reject_reason)
        app_common.back_previous_step()
        app_common.back_previous_step()
        self.create_no_dict_house(web_driver, house_info)
        self.match_estate_dict_by_estate_name(web_driver, house_info['estate_name'], match_estate_info)
        app_common.open_notifications()
        pytest.assume(app_notification.get_notification_title_by_row(1) == '房源匹配处理完成')
        pytest.assume(app_notification.get_notification_content_by_row(1) in
                      "您反馈的无楼盘字典房源已处理完成，请尽快创建该房源")
        app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_house_message() ==
                      "您反馈的无楼盘字典房源已处理完成，请尽快创建该房源")
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '房源匹配处理完成')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您反馈的无楼盘字典房源已处理完成，请尽快创建该房源")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '房源匹配处理完成')
        pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您反馈的无楼盘字典房源已处理完成，请尽快创建该房源")
        app_common.back_previous_step()
        app_common.back_previous_step()

    @staticmethod
    def create_no_dict_house(web_driver, house_info: dict):
        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_add = HouseAddPage(web_driver)

        main_leftview.click_all_house_label()
        house_table.click_add_house_button()
        house_add.add_no_estate_dict_house('买卖', house_info['estate_name'], house_info['building_id'],
                                           house_info['building_cell'], house_info['floor'], house_info['doorplate'],
                                           house_info['cert_files'])
        main_upview.clear_all_title()
        logger.info("无楼盘字典房源反馈创建成功")

    @staticmethod
    def reject_no_dict_house_feedback_by_estate_name(web_driver, estate_name: str, reason: str):
        main_leftview = MainLeftViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        no_dict_house_feedback_table = NoDictHouseFeedbackTablePage(web_driver)

        main_leftview.click_no_dict_house_feedback_label()
        no_dict_house_feedback_table.click_sale_tab()
        no_dict_house_feedback_table.input_estate_name_search(estate_name)
        no_dict_house_feedback_table.click_search_button()
        no_dict_house_feedback_table.click_view_detail_button_by_row(1)
        no_dict_house_feedback_table.examine_dialog_click_reject_examine_button()
        no_dict_house_feedback_table.reject_examine_dialog_input_reason(reason)
        no_dict_house_feedback_table.dialog_click_confirm_button()
        main_topview.close_notification()
        main_upview.clear_all_title()
        logger.info("无楼盘字典房源反馈，审核驳回")

    @staticmethod
    def match_estate_dict_by_estate_name(web_driver, estate_name: str, match_estate_info: dict):
        main_leftview = MainLeftViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        no_dict_house_feedback_table = NoDictHouseFeedbackTablePage(web_driver)

        main_leftview.click_no_dict_house_feedback_label()
        no_dict_house_feedback_table.click_sale_tab()
        no_dict_house_feedback_table.input_estate_name_search(estate_name)
        no_dict_house_feedback_table.click_search_button()
        no_dict_house_feedback_table.click_view_detail_button_by_row(1)
        no_dict_house_feedback_table.examine_dialog_click_match_estate_dict_button()
        no_dict_house_feedback_table.match_estate_dict_dialog_choose_estate_name(match_estate_info['estate_name'])
        no_dict_house_feedback_table.match_estate_dict_dialog_choose_building_id(match_estate_info['building_id'])
        no_dict_house_feedback_table.match_estate_dict_dialog_choose_building_cell(match_estate_info['building_cell'])
        no_dict_house_feedback_table.match_estate_dict_dialog_choose_floor(match_estate_info['floor'])
        no_dict_house_feedback_table.match_estate_dict_dialog_choose_doorplate(match_estate_info['doorplate'])
        no_dict_house_feedback_table.dialog_click_confirm_button()
        main_topview.close_notification()
        main_upview.clear_all_title()
        logger.info("匹配楼盘字典成功")
