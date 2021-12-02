#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_new_house_process.py
@date: 2021/11/16 0016
"""
import string
import random
import allure
import pytest
from common.readconfig import ini
from config.conf import cm
from utils.logger import logger
from utils.timeutil import dt_strftime, sleep
from page_object.common.web.login.loginpage import LoginPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrxf.web.main.leftviewpage import MainLeftViewPage as XfMainLeftViewPage
from page_object.jrxf.web.main.topviewpage import MainTopViewPage as XfMainTopViewPage
from page_object.jrgj.web.main.rightviewpage import MainRightViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrxf.web.task.add_page import AddHouseTaskPage
from page_object.jrxf.web.task.table_page import HouseTaskTablePage
from page_object.jrgj.web.customer.tablepage import CustomerTablePage
from page_object.jrgj.web.newhouseoperation.tablepage import NewHouseOperationTablePage
from page_object.jrgj.app.login.loginpage import AppLoginPage
from page_object.common.app.common.commonpage import AppCommonPage
from page_object.jrgj.app.main.mainpage import AppMainPage
from page_object.jrgj.app.message.tablepage import AppMessageTablePage
from page_object.jrgj.app.mine.minepage import AppMinePage
from page_object.common.app.notifications.tablepage import AppNotificationsTablePage


@allure.feature("测试APP通知-新房")
@pytest.mark.app_notifications
class TestNewHouseProcess(object):

    new_house = ini.new_house_name

    @pytest.fixture(scope="function", autouse=True)
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
        app_main.click_message_button()
        app_message_table.click_notification_tab()
        app_message_table.click_clear_message_button()
        app_common.open_notifications()
        app_notification.dismiss_all_notification()
        yield
        app_main.click_mine_button()
        app_mine.log_out()

    @allure.story("测试新房报备-认购-带看流程通知")
    def test_001(self, web_driver, android_driver):
        app_common = AppCommonPage(android_driver)
        app_message_table = AppMessageTablePage(android_driver)
        app_notification = AppNotificationsTablePage(android_driver)

        report_reject_reason = "自动化测试需要" + "".join(map(lambda x: random.choice(string.digits), range(5)))
        take_look_reject_reason = "自动化测试需要" + "".join(map(lambda x: random.choice(string.digits), range(5)))
        subscription_reject_reason = "自动化测试需要" + "".join(map(lambda x: random.choice(string.digits), range(5)))
        subscription_amount = str(int("".join(map(lambda x: random.choice(string.digits), range(5))))) + '.' + "".join(
            map(lambda x: random.choice(string.digits), range(2)))
        self.check_new_house(web_driver)
        self.check_customer(web_driver)
        self.check_new_house_operation(web_driver)
        self.new_house_report(web_driver)
        # app_common.open_notifications()
        # pytest.assume(app_notification.get_notification_title_by_row(1) == '新房报备待审核')
        # pytest.assume(app_notification.get_notification_content_by_row(1) in
        #               "您收到一条新房报备，经纪人" + self.agent + ini.user_account + "，客户" + self.customer_name
        #               + ini.custom_telephone + "，楼盘信息" + self.new_house + self.address + "，请及时审核。")
        # app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_customer_message() ==
                      "您收到一条新房报备，经纪人" + self.agent + ini.user_account + "，客户" + self.customer_name
                      + ini.custom_telephone + "，楼盘信息" + self.new_house + self.address + "，请及时审核。")
        app_message_table.go_customer_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '新房报备待审核')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您收到一条新房报备，经纪人" + self.agent + ini.user_account + "，客户" + self.customer_name
                      + ini.custom_telephone + "，楼盘信息" + self.new_house + self.address + "，请及时审核。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '新房报备待审核')
        pytest.assume(app_message_table.get_message_detail_message_type() == '客源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您收到一条新房报备，经纪人" + self.agent + ini.user_account + "，客户" + self.customer_name
                      + ini.custom_telephone + "，楼盘信息" + self.new_house + self.address + "，请及时审核。")
        app_common.back_previous_step()
        app_common.back_previous_step()
        self.new_house_report_reject(web_driver, report_reject_reason)
        # app_common.open_notifications()
        # pytest.assume(app_notification.get_notification_title_by_row(1) == '新房报备审核驳回')
        # pytest.assume(app_notification.get_notification_content_by_row(1) in
        #               "您报备的客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
        #               + self.address + "已驳回。")
        # app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_customer_message() ==
                      "您报备的客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "已驳回。")
        app_message_table.go_customer_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '新房报备审核驳回')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您报备的客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "已驳回。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '新房报备审核驳回')
        pytest.assume(app_message_table.get_message_detail_message_type() == '客源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您报备的客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "已驳回。")
        app_common.back_previous_step()
        app_common.back_previous_step()
        self.new_house_report(web_driver)
        self.new_house_report_pass(web_driver)
        # app_common.open_notifications()
        # pytest.assume(app_notification.get_notification_title_by_row(1) == '新房报备审核通过')
        # pytest.assume(app_notification.get_notification_content_by_row(1) in
        #               "您报备的客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
        #               + self.address + "已审核通过。")
        # app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_customer_message() ==
                      "您报备的客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "已审核通过。")
        app_message_table.go_customer_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '新房报备审核通过')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您报备的客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "已审核通过。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '新房报备审核通过')
        pytest.assume(app_message_table.get_message_detail_message_type() == '客源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您报备的客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "已审核通过。")
        app_common.back_previous_step()
        app_common.back_previous_step()
        self.new_house_take_look(web_driver)
        # app_common.open_notifications()
        # pytest.assume(app_notification.get_notification_title_by_row(1) == '带看待审核')
        # pytest.assume(app_notification.get_notification_content_by_row(1) in
        #               "您收到一条新房带看单，经纪人" + self.agent + ini.user_account + "，客户" + self.customer_name
        #               + ini.custom_telephone + "，楼盘信息" + self.new_house + self.address + "请及时审核。")
        # app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_house_message() ==
                      "您收到一条新房带看单，经纪人" + self.agent + ini.user_account + "，客户" + self.customer_name
                      + ini.custom_telephone + "，楼盘信息" + self.new_house + self.address + "请及时审核。")
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '带看待审核')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您收到一条新房带看单，经纪人" + self.agent + ini.user_account + "，客户" + self.customer_name
                      + ini.custom_telephone + "，楼盘信息" + self.new_house + self.address + "请及时审核。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '带看待审核')
        pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您收到一条新房带看单，经纪人" + self.agent + ini.user_account + "，客户" + self.customer_name
                      + ini.custom_telephone + "，楼盘信息" + self.new_house + self.address + "请及时审核。")
        app_common.back_previous_step()
        app_common.back_previous_step()
        self.new_house_take_look_reject(web_driver, take_look_reject_reason)
        # app_common.open_notifications()
        # pytest.assume(app_notification.get_notification_title_by_row(1) == '带看审核驳回')
        # pytest.assume(app_notification.get_notification_content_by_row(1) in
        #               "您申请的带看单，客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
        #               + self.address + "已驳回。")
        # app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_house_message() ==
                      "您申请的带看单，客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "已驳回。")
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '带看审核驳回')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您申请的带看单，客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "已驳回。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '带看审核驳回')
        pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您申请的带看单，客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "已驳回。")
        app_common.back_previous_step()
        app_common.back_previous_step()
        self.new_house_take_look(web_driver)
        self.new_house_take_look_pass(web_driver)
        # app_common.open_notifications()
        # pytest.assume(app_notification.get_notification_title_by_row(1) == '带看审核通过')
        # pytest.assume(app_notification.get_notification_content_by_row(1) in
        #               "您申请的带看单，客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
        #               + self.address + "已审核通过")
        # app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_house_message() ==
                      "您申请的带看单，客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "已审核通过")
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '带看审核通过')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您申请的带看单，客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "已审核通过")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '带看审核通过')
        pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您申请的带看单，客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "已审核通过")
        app_common.back_previous_step()
        app_common.back_previous_step()
        self.new_house_subscription(web_driver, subscription_amount)
        # app_common.open_notifications()
        # pytest.assume(app_notification.get_notification_title_by_row(1) == '新房认购待审核')
        # pytest.assume(app_notification.get_notification_content_by_row(1) in
        #               "您收到一条新房报单，经纪人" + self.agent + ini.user_account + "，客户" + self.customer_name
        #               + ini.custom_telephone + "，楼盘信息" + self.new_house + self.address + "，认购金额"
        #               + subscription_amount + "元，请及时审核。")
        # app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_customer_message() ==
                      "您收到一条新房报单，经纪人" + self.agent + ini.user_account + "，客户" + self.customer_name
                      + ini.custom_telephone + "，楼盘信息" + self.new_house + self.address + "，认购金额"
                      + subscription_amount + "元，请及时审核。")
        app_message_table.go_customer_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '新房认购待审核')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您收到一条新房报单，经纪人" + self.agent + ini.user_account + "，客户" + self.customer_name
                      + ini.custom_telephone + "，楼盘信息" + self.new_house + self.address + "，认购金额"
                      + subscription_amount + "元，请及时审核。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '新房认购待审核')
        pytest.assume(app_message_table.get_message_detail_message_type() == '客源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您收到一条新房报单，经纪人" + self.agent + ini.user_account + "，客户" + self.customer_name
                      + ini.custom_telephone + "，楼盘信息" + self.new_house + self.address + "，认购金额"
                      + subscription_amount + "元，请及时审核。")
        app_common.back_previous_step()
        app_common.back_previous_step()
        self.new_house_subscription_reject(web_driver, subscription_reject_reason)
        # app_common.open_notifications()
        # pytest.assume(app_notification.get_notification_title_by_row(1) == '新房认购审核驳回')
        # pytest.assume(app_notification.get_notification_content_by_row(1) in
        #               "您申请的新房认购客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
        #               + self.address + "，认购金额" + subscription_amount + "元，已驳回。")
        # app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_customer_message() ==
                      "您申请的新房认购客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "，认购金额" + subscription_amount + "元，已驳回。")
        app_message_table.go_customer_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '新房认购审核驳回')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您申请的新房认购客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "，认购金额" + subscription_amount + "元，已驳回。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '新房认购审核驳回')
        pytest.assume(app_message_table.get_message_detail_message_type() == '客源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您申请的新房认购客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "，认购金额" + subscription_amount + "元，已驳回。")
        app_common.back_previous_step()
        app_common.back_previous_step()
        self.new_house_subscription_again(web_driver)
        self.new_house_subscription_pass(web_driver)
        # app_common.open_notifications()
        # pytest.assume(app_notification.get_notification_title_by_row(1) == '新房认购审核通过')
        # pytest.assume(app_notification.get_notification_content_by_row(1) in
        #               "您申请的新房认购客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
        #               + self.address + "，认购金额" + subscription_amount + "元，已审核通过。")
        # app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_customer_message() ==
                      "您申请的新房认购客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "，认购金额" + subscription_amount + "元，已审核通过。")
        app_message_table.go_customer_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '新房认购审核通过')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您申请的新房认购客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "，认购金额" + subscription_amount + "元，已审核通过。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '新房认购审核通过')
        pytest.assume(app_message_table.get_message_detail_message_type() == '客源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您申请的新房认购客户" + self.customer_name + ini.custom_telephone + "，楼盘信息" + self.new_house
                      + self.address + "，认购金额" + subscription_amount + "元，已审核通过。")
        app_common.back_previous_step()
        app_common.back_previous_step()

    @allure.step("检查新房楼盘存不存在")
    def check_new_house(self, web_driver):
        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)

        main_leftview.change_role('经纪人')
        main_leftview.click_all_house_label()
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

        main_leftview.change_role('经纪人')
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
        for _ in range(new_house_operation_table.get_table_count()):
            new_house_operation_table.delete_report_by_row(1)
            new_house_operation_table.dialog_click_delete_button()
            main_topview.close_notification()
        new_house_operation_table.click_take_look_tab()
        new_house_operation_table.input_building_name_search(self.new_house)
        new_house_operation_table.input_customer_phone_search(ini.custom_telephone)
        new_house_operation_table.click_search_button()
        for _ in range(new_house_operation_table.get_table_count()):
            new_house_operation_table.delete_report_by_row(1)
            new_house_operation_table.dialog_click_delete_button()
            main_topview.close_notification()
        new_house_operation_table.click_subscription_tab()
        new_house_operation_table.input_building_name_search(self.new_house)
        new_house_operation_table.input_customer_phone_search(ini.custom_telephone)
        new_house_operation_table.click_search_button()
        for _ in range(new_house_operation_table.get_table_count()):
            new_house_operation_table.delete_report_by_row(1)
            new_house_operation_table.dialog_click_delete_button()
            main_topview.close_notification()
        main_leftview.change_role('经纪人')

    @allure.step("新房作业-报备")
    def new_house_report(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_rightview = MainRightViewPage(web_driver)
        new_house_operation_table = NewHouseOperationTablePage(web_driver)

        main_leftview.change_role('经纪人')
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
        main_topview.close_notification()
        new_house_operation_table.click_report_tab()  # 点击报备tab
        new_house_operation_table.input_building_name_search(self.new_house)
        new_house_operation_table.input_customer_phone_search(ini.custom_telephone)
        new_house_operation_table.click_search_button()
        self.report_code = new_house_operation_table.get_report_code_by_row(1)
        self.address = new_house_operation_table.get_estate_address_by_row(1)
        main_upview.clear_all_title()
        logger.info('报告新增成功')

    @allure.step("新房系统，报备, 审核驳回")
    def new_house_report_reject(self, web_driver, reject_reason):
        xf_login = LoginPage(web_driver)
        xf_main_leftview = XfMainLeftViewPage(web_driver)
        xf_main_topview = XfMainTopViewPage(web_driver)
        xf_house_task_table = HouseTaskTablePage(web_driver)
        xf_add_house_task = AddHouseTaskPage(web_driver)

        current_handle = web_driver.current_window_handle
        js = "window.open('" + ini.xf_url + "');"  # 通过执行js，开启一个新的窗口
        web_driver.execute_script(js)
        sleep(4)
        all_handles = web_driver.window_handles  # 获取当前窗口句柄
        for handle in all_handles:
            if handle != current_handle:
                web_driver.switch_to_window(handle)  # 切换窗口
                break
        xf_login.log_in(ini.user_account, ini.user_password)
        xf_main_leftview.change_role('新房案场')
        xf_main_leftview.click_house_task_label()
        xf_house_task_table.switch_tab_by_tab_name('报备')  # 点击报备tab
        xf_house_task_table.search_records_by_report_no(self.report_code)
        xf_house_task_table.click_view_report_btn(self.report_code)
        xf_add_house_task.click_reject_btn()
        xf_add_house_task.reject_dialog_input_reason(reject_reason)
        xf_add_house_task.click_confirm_btn()
        xf_main_topview.close_notification()
        web_driver.close()
        web_driver.switch_to_window(current_handle)  # 切换窗口
        sleep(2)

    @allure.step("新房系统，报备, 审核通过")
    def new_house_report_pass(self, web_driver):
        xf_login = LoginPage(web_driver)
        xf_main_leftview = XfMainLeftViewPage(web_driver)
        xf_main_topview = XfMainTopViewPage(web_driver)
        xf_house_task_table = HouseTaskTablePage(web_driver)
        xf_add_house_task = AddHouseTaskPage(web_driver)

        current_handle = web_driver.current_window_handle
        js = "window.open('" + ini.xf_url + "');"  # 通过执行js，开启一个新的窗口
        web_driver.execute_script(js)
        sleep(4)
        all_handles = web_driver.window_handles  # 获取当前窗口句柄
        for handle in all_handles:
            if handle != current_handle:
                web_driver.switch_to_window(handle)  # 切换窗口
                break
        xf_login.log_in(ini.user_account, ini.user_password)
        xf_main_leftview.change_role('新房案场')
        xf_main_leftview.click_house_task_label()
        xf_house_task_table.switch_tab_by_tab_name('报备')  # 点击报备tab
        xf_house_task_table.search_records_by_report_no(self.report_code)
        xf_house_task_table.click_view_report_btn(self.report_code)
        xf_add_house_task.click_approved_btn()
        xf_main_topview.close_notification()
        web_driver.close()
        web_driver.switch_to_window(current_handle)  # 切换窗口
        sleep(2)

    @allure.step("新房作业-带看")
    def new_house_take_look(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        new_house_operation_table = NewHouseOperationTablePage(web_driver)

        main_leftview.change_role('经纪人')
        main_leftview.click_new_house_operation_label()
        new_house_operation_table.click_report_tab()  # 点击报备tab
        new_house_operation_table.input_report_code_search(self.report_code)
        new_house_operation_table.click_search_button()
        new_house_operation_table.enter_take_look_by_row(1)
        new_house_operation_table.dialog_input_take_look_time(dt_strftime("%Y-%m-%d %H:%M"))
        new_house_operation_table.dialog_upload_picture([cm.tmp_picture_file])
        new_house_operation_table.dialog_click_confirm_button()
        main_topview.close_notification()
        main_upview.clear_all_title()
        logger.info('带看新增成功')

    @allure.step("新房系统-带看, 审核驳回")
    def new_house_take_look_reject(self, web_driver, reject_reason):
        xf_login = LoginPage(web_driver)
        xf_main_leftview = XfMainLeftViewPage(web_driver)
        xf_main_topview = XfMainTopViewPage(web_driver)
        xf_house_task_table = HouseTaskTablePage(web_driver)
        xf_add_house_task = AddHouseTaskPage(web_driver)

        current_handle = web_driver.current_window_handle
        js = "window.open('" + ini.xf_url + "');"  # 通过执行js，开启一个新的窗口
        web_driver.execute_script(js)
        sleep(4)
        all_handles = web_driver.window_handles  # 获取当前窗口句柄
        for handle in all_handles:
            if handle != current_handle:
                web_driver.switch_to_window(handle)  # 切换窗口
                break
        xf_login.log_in(ini.user_account, ini.user_password)
        xf_main_leftview.change_role('新房案场')
        xf_main_leftview.click_house_task_label()
        xf_house_task_table.switch_tab_by_tab_name('带看')  # 点击报备tab
        xf_house_task_table.search_records_by_report_no(self.report_code)
        xf_house_task_table.click_view_report_btn(self.report_code)
        xf_add_house_task.click_reject_btn()
        xf_add_house_task.reject_dialog_input_reason(reject_reason)
        xf_add_house_task.click_confirm_btn()
        xf_main_topview.close_notification()
        web_driver.close()
        web_driver.switch_to_window(current_handle)  # 切换窗口
        sleep(2)

    @allure.step("新房系统-带看, 审核通过")
    def new_house_take_look_pass(self, web_driver):
        xf_login = LoginPage(web_driver)
        xf_main_leftview = XfMainLeftViewPage(web_driver)
        xf_main_topview = XfMainTopViewPage(web_driver)
        xf_house_task_table = HouseTaskTablePage(web_driver)
        xf_add_house_task = AddHouseTaskPage(web_driver)

        current_handle = web_driver.current_window_handle
        js = "window.open('" + ini.xf_url + "');"  # 通过执行js，开启一个新的窗口
        web_driver.execute_script(js)
        sleep(4)
        all_handles = web_driver.window_handles  # 获取当前窗口句柄
        for handle in all_handles:
            if handle != current_handle:
                web_driver.switch_to_window(handle)  # 切换窗口
                break
        xf_login.log_in(ini.user_account, ini.user_password)
        xf_main_leftview.change_role('新房案场')
        xf_main_leftview.click_house_task_label()
        xf_house_task_table.switch_tab_by_tab_name('带看')  # 点击报备tab
        xf_house_task_table.search_records_by_report_no(self.report_code)
        xf_house_task_table.click_view_report_btn(self.report_code)
        xf_add_house_task.click_approved_btn()
        xf_main_topview.close_notification()
        web_driver.close()
        web_driver.switch_to_window(current_handle)  # 切换窗口
        sleep(2)

    @allure.step("新房作业-认购")
    def new_house_subscription(self, web_driver, subscription_amount):
        main_topview = MainTopViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        new_house_operation_table = NewHouseOperationTablePage(web_driver)

        main_leftview.change_role('经纪人')
        main_leftview.click_new_house_operation_label()
        new_house_operation_table.click_take_look_tab()  # 点击带看tab
        new_house_operation_table.input_report_code_search(self.report_code)
        new_house_operation_table.click_search_button()
        new_house_operation_table.enter_subscribe_by_row(1)
        new_house_operation_table.dialog_input_block(str(random.randint(1, 9)))
        new_house_operation_table.dialog_input_block_cell(str(random.randint(1, 4)))
        new_house_operation_table.dialog_input_floor(str(random.randint(1, 33)))
        new_house_operation_table.dialog_input_room_number(str(random.randint(1, 9)))
        new_house_operation_table.dialog_input_building_area(str(random.randint(80, 200)))
        new_house_operation_table.dialog_input_subscribe_price(subscription_amount)
        new_house_operation_table.dialog_input_subscribe_time(dt_strftime("%Y-%m-%d %H:%M"))
        new_house_operation_table.dialog_upload_subscribe_form([cm.tmp_picture_file])
        new_house_operation_table.dialog_upload_customer_certificate([cm.tmp_picture_file])
        new_house_operation_table.dialog_upload_payment_voucher([cm.tmp_picture_file])
        new_house_operation_table.dialog_click_confirm_button()
        main_topview.close_notification()
        main_upview.clear_all_title()
        logger.info('认购新增成功')

    @allure.step("新房作业-重新认购")
    def new_house_subscription_again(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        new_house_operation_table = NewHouseOperationTablePage(web_driver)

        main_leftview.change_role('经纪人')
        main_leftview.click_new_house_operation_label()
        new_house_operation_table.click_subscription_tab()  # 点击带看tab
        new_house_operation_table.input_report_code_search(self.report_code)
        new_house_operation_table.click_search_button()
        new_house_operation_table.click_edit_button_by_row(1)
        new_house_operation_table.dialog_click_confirm_button()
        main_topview.close_notification()
        main_upview.clear_all_title()
        logger.info('认购新增成功')

    @allure.step("新房系统-认购, 审核驳回")
    def new_house_subscription_reject(self, web_driver, reject_reason):
        xf_login = LoginPage(web_driver)
        xf_main_leftview = XfMainLeftViewPage(web_driver)
        xf_main_topview = XfMainTopViewPage(web_driver)
        xf_house_task_table = HouseTaskTablePage(web_driver)
        xf_add_house_task = AddHouseTaskPage(web_driver)

        current_handle = web_driver.current_window_handle
        js = "window.open('" + ini.xf_url + "');"  # 通过执行js，开启一个新的窗口
        web_driver.execute_script(js)
        sleep(4)
        all_handles = web_driver.window_handles  # 获取当前窗口句柄
        for handle in all_handles:
            if handle != current_handle:
                web_driver.switch_to_window(handle)  # 切换窗口
                break
        xf_login.log_in(ini.user_account, ini.user_password)
        xf_main_leftview.change_role('新房案场')
        xf_main_leftview.click_house_task_label()
        xf_house_task_table.switch_tab_by_tab_name('认购')  # 点击报备tab
        xf_house_task_table.search_records_by_report_no(self.report_code)
        xf_house_task_table.click_view_report_btn(self.report_code)
        xf_add_house_task.click_reject_btn()
        xf_add_house_task.reject_dialog_input_reason(reject_reason)
        xf_add_house_task.click_confirm_btn()
        xf_main_topview.close_notification()
        web_driver.close()
        web_driver.switch_to_window(current_handle)  # 切换窗口
        sleep(2)

    @allure.step("新房系统-认购, 审核通过")
    def new_house_subscription_pass(self, web_driver):
        xf_login = LoginPage(web_driver)
        xf_main_leftview = XfMainLeftViewPage(web_driver)
        xf_main_topview = XfMainTopViewPage(web_driver)
        xf_house_task_table = HouseTaskTablePage(web_driver)
        xf_add_house_task = AddHouseTaskPage(web_driver)

        current_handle = web_driver.current_window_handle
        js = "window.open('" + ini.xf_url + "');"  # 通过执行js，开启一个新的窗口
        web_driver.execute_script(js)
        sleep(4)
        all_handles = web_driver.window_handles  # 获取当前窗口句柄
        for handle in all_handles:
            if handle != current_handle:
                web_driver.switch_to_window(handle)  # 切换窗口
                break
        xf_login.log_in(ini.user_account, ini.user_password)
        xf_main_leftview.change_role('新房案场')
        xf_main_leftview.click_house_task_label()
        xf_house_task_table.switch_tab_by_tab_name('认购')  # 点击报备tab
        xf_house_task_table.search_records_by_report_no(self.report_code)
        xf_house_task_table.click_view_report_btn(self.report_code)
        xf_add_house_task.subscribe_dialog_input_payment(str(random.randint(100, 9999)))
        xf_add_house_task.subscribe_dialog_input_commission(str(random.randint(100, 9999)))
        xf_add_house_task.subscribe_dialog_input_company_income(str(random.randint(100, 9999)))
        xf_add_house_task.subscribe_dialog_input_deal_prize(str(random.randint(100, 9999)))
        xf_add_house_task.click_approved_btn()
        xf_main_topview.close_notification()
        web_driver.close()
        web_driver.switch_to_window(current_handle)  # 切换窗口
        sleep(2)
