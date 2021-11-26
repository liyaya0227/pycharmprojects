#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_new_house.py
@date: 2021/11/16 0016
"""
import allure
import pytest

from page_object.common.app.notifications.tablepage import AppNotificationsTablePage
from page_object.jrgj.app.login.loginpage import AppLoginPage
from page_object.jrgj.web.customer.tablepage import CustomerTablePage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.rightviewpage import MainRightViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.newhouseoperation.tablepage import NewHouseOperationTablePage
from utils.timeutil import dt_strftime
from common.readconfig import ini
from page_object.common.app.common.commonpage import AppCommonPage
from page_object.jrgj.app.main.mainpage import AppMainPage
from page_object.jrgj.app.message.tablepage import AppMessageTablePage
from page_object.jrgj.app.mine.minepage import AppMinePage


@allure.feature("测试APP通知-新房")
class TestSurveyTimeChange(object):

    new_house = ini.new_house_name

    @pytest.fixture(scope="class", autouse=True)
    def setup_and_teardown(self, android_driver):
        app_login = AppLoginPage(android_driver)
        app_main = AppMainPage(android_driver)
        app_mine = AppMinePage(android_driver)

        app_login.log_in(ini.user_account, ini.user_password)
        app_main.click_mine_button()
        yield
        app_main.click_mine_button()
        app_mine.log_out()

    @allure.story("测试新房报备-认购-带看流程通知")
    def test_001(self, web_driver, android_driver):
        app_common = AppCommonPage(android_driver)
        app_main = AppMainPage(android_driver)
        app_message_table = AppMessageTablePage(android_driver)
        app_notification = AppNotificationsTablePage(android_driver)

        self.check_new_house(web_driver)
        self.check_customer(web_driver)
        self.check_new_house_operation(web_driver)
        self.new_house_report(web_driver)
        app_common.open_notifications()
        pytest.assume(app_notification.get_notification_title_by_row(1) == '新房报备待审核')
        pytest.assume(app_notification.get_notification_content_by_row(1) in
                      "您收到一条新房报备，经纪人" + self.agent + "，客户" + self.customer_name + ini.custom_telephone
                      + "，楼盘信息" + self.new_house + "楼盘地址，请及时审核。")
        app_notification.dismiss_all_notification()
        app_main.click_message_button()
        app_message_table.click_notification_tab()
        pytest.assume(app_message_table.get_house_message() ==
                      "您收到一条新房报备，经纪人" + self.agent + "，客户" + self.customer_name + ini.custom_telephone
                      + "，楼盘信息" + self.new_house + "楼盘地址，请及时审核。")
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '新房报备待审核')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您收到一条新房报备，经纪人" + self.agent + "，客户" + self.customer_name + ini.custom_telephone
                      + "，楼盘信息" + self.new_house + "楼盘地址，请及时审核。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '新房报备待审核')
        pytest.assume(app_message_table.get_message_detail_message_type() == '客源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您收到一条新房报备，经纪人" + self.agent + "，客户" + self.customer_name + ini.custom_telephone
                      + "，楼盘信息" + self.new_house + "楼盘地址，请及时审核。")
        app_common.back_previous_step()
        app_common.back_previous_step()

    @allure.step("检查新房楼盘存不存在")
    def check_new_house(self, web_driver):
        main_upview = MainUpViewPage(web_driver)
        main_left_view = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)

        main_left_view.click_all_house_label()
        house_table.click_new_tab()  # 点击新房tab
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter(flag='新房')
        house_table.input_building_name_search(self.new_house)
        house_table.click_search_button()
        if house_table.get_house_table_count() == 0:
            raise ValueError("新房楼盘不存在，需手动处理")
        main_upview.clear_all_title()

    @allure.step("检查客源")
    def check_customer(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        customer_table = CustomerTablePage(web_driver)

        main_leftview.click_my_customer_label()
        customer_table.click_all_tab()
        customer_table.choose_customer_wish('不限')
        customer_table.input_search_text(ini.custom_telephone)
        customer_table.click_search_button()
        assert customer_table.get_customer_table_count() == 1
        self.customer_name = customer_table.get_customer_name_by_row(1)
        main_upview.clear_all_title()

    @allure.step("检查新房作业流程是否已存在")
    def check_new_house_operation(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        new_house_operation_table = NewHouseOperationTablePage(web_driver)

        main_leftview.change_role('超级管理员')
        main_leftview.click_new_house_operation_label()
        new_house_operation_table.click_report_tab()  # 点击报备tab
        new_house_operation_table.input_building_name_search(self.new_house)
        new_house_operation_table.input_customer_phone_search(ini.custom_telephone)
        new_house_operation_table.click_search_button()
        if new_house_operation_table.get_table_count() != 0:
            new_house_operation_table.delete_report_by_row(1)
            new_house_operation_table.dialog_click_delete_button()
            main_topview.close_notification()
        new_house_operation_table.click_take_look_tab()
        new_house_operation_table.input_building_name_search(self.new_house)
        new_house_operation_table.input_customer_phone_search(ini.custom_telephone)
        new_house_operation_table.click_search_button()
        if new_house_operation_table.get_table_count() != 0:
            new_house_operation_table.delete_report_by_row(1)
            new_house_operation_table.dialog_click_delete_button()
            main_topview.close_notification()
        new_house_operation_table.click_subscription_tab()
        new_house_operation_table.input_building_name_search(self.new_house)
        new_house_operation_table.input_customer_phone_search(ini.custom_telephone)
        new_house_operation_table.click_search_button()
        if new_house_operation_table.get_table_count() != 0:
            new_house_operation_table.delete_report_by_row(1)
            new_house_operation_table.dialog_click_delete_button()
            main_topview.close_notification()
        main_leftview.change_role('经纪人')

    @allure.step("新房作业-报备")
    def new_house_report(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_rightview = MainRightViewPage(web_driver)
        new_house_operation_table = NewHouseOperationTablePage(web_driver)

        self.agent = main_rightview.get_login_person_name()
        main_leftview.click_new_house_operation_label()
        new_house_operation_table.click_report_tab()
        new_house_operation_table.click_add_button()
        new_house_operation_table.dialog_input_building_info(self.new_house)
        new_house_operation_table.dialog_input_customer_info(
            {'customer_name': self.customer_name, 'customer_phone': ini.custom_telephone})
        new_house_operation_table.dialog_input_expect_arrive_time(dt_strftime("%Y-%m-%d %H:%M"))
        new_house_operation_table.dialog_input_remark("自动化测试需要")
        new_house_operation_table.dialog_click_confirm_button()
        assert main_topview.find_notification_content() == '报备新增成功'

    @allure.step("新房作业-报备, 审核驳回")
    def new_house_report(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        new_house_operation_table = NewHouseOperationTablePage(web_driver)

        main_leftview.change_role('新房案场')
        main_leftview.click_new_house_operation_label()
        new_house_operation_table.click_report_tab()  # 点击报备tab
        new_house_operation_table.input_building_name_search(self.new_house)
        new_house_operation_table.input_customer_phone_search(ini.custom_telephone)
        new_house_operation_table.click_search_button()
        new_house_operation_table.watch_report_by_row(1)
        new_house_operation_table.dialog_click_examine_reject_button()
