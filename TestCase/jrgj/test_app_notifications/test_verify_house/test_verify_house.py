#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_verify_house.py
@date: 2021/11/22 0022
"""
import random
import string
import allure
import pytest
from case_service.jrjob.job_service import JobService
from utils.logger import logger
from common.readconfig import ini
from common.globalvar import GlobalVar
from utils.databaseutil import DataBaseUtil
from page_object.jrgj.web.house.verifypage import HouseVerifyPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.common.app.common.commonpage import AppCommonPage
from page_object.jrgj.app.login.loginpage import AppLoginPage
from page_object.jrgj.app.main.mainpage import AppMainPage
from page_object.jrgj.app.message.tablepage import AppMessageTablePage
from page_object.jrgj.app.mine.minepage import AppMinePage
from page_object.common.app.notifications.tablepage import AppNotificationsTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from utils.timeutil import dt_strftime_with_delta


@pytest.mark.app_notifications
@allure.feature("测试APP通知-验真")
class TestVerifyHouse(object):

    @pytest.fixture(scope="function", autouse=True)
    def setup_and_teardown(self, web_driver, android_driver):
        app_login = AppLoginPage(android_driver)
        app_main = AppMainPage(android_driver)
        app_mine = AppMinePage(android_driver)
        app_common = AppCommonPage(android_driver)
        app_notification = AppNotificationsTablePage(android_driver)
        app_message_table = AppMessageTablePage(android_driver)
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)

        main_leftview.change_role('经纪人')
        app_login.log_in(ini.user_account, ini.user_password)
        app_main.close_top_view()
        app_main.click_message_button()
        app_message_table.click_notification_tab()
        app_message_table.click_clear_message_button()
        app_common.open_notifications()
        app_notification.dismiss_all_notification()
        yield
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(self.house_code)
        house_table.click_search_button()
        if house_table.get_house_table_count() == 0:
            main_leftview.click_data_disk_label()
            house_table.click_sale_tab_in_data_disk()
            house_table.input_house_code_search(self.house_code)
            house_table.go_house_detail_by_row(1)
            house_detail.click_transfer_to_sale_btn()
            house_detail.transfer_house(GlobalVar.house_verify_code)
        app_main.click_mine_button()
        app_mine.log_out()

    @allure.story("提交验真审核，验真通过，验真失效，校验推送及消息内容")
    def test_001(self, web_driver, android_driver):
        app_common = AppCommonPage(android_driver)
        app_notification = AppNotificationsTablePage(android_driver)
        app_message_table = AppMessageTablePage(android_driver)

        self.check_house(web_driver)
        self.update_verify_time(web_driver)
        app_common.open_notifications()
        pytest.assume(app_notification.get_notification_title_by_row(1) == '验真房源失效')
        pytest.assume(app_notification.get_notification_content_by_row(1) in
                      "您好，您有一套房源" + ini.house_community_name + self.house_code + "验真举证超期未举证，请及时处理。")
        app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_house_message() ==
                      "您好，您有一套房源" + ini.house_community_name + self.house_code + "验真举证超期未举证，请及时处理。")
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '验真房源失效')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您好，您有一套房源" + ini.house_community_name + self.house_code + "验真举证超期未举证，请及时处理。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '验真房源失效')
        pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您好，您有一套房源" + ini.house_community_name + self.house_code + "验真举证超期未举证，请及时处理。")
        app_common.back_previous_step()
        app_common.back_previous_step()

    @allure.step("经纪人检查房源状态")
    def check_house(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)

        self.house_code = house_table.get_house_code_by_db(flag='买卖')
        assert self.house_code != '', "不存在房源"
        logger.info('房源编号为：' + self.house_code)
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(self.house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        if not house_detail.check_need_house_verify():
            house_detail.view_basic_information()
            house_detail.basic_information_dialog_input_phone("1" + "".join(map(lambda x: random.choice(string.digits),
                                                                                range(10))))
            house_detail.dialog_click_confirm_button()
            main_topview.close_notification()
        main_upview.clear_all_title()

    @allure.step("提交验真审核")
    def submit_verify_examine(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_verify = HouseVerifyPage(web_driver)

        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.click_my_house_button()
        house_verify.verify_again_by_house_code(self.house_code)
        house_verify.choose_verify_code_to_verify()
        house_verify.click_send_verify_code_button()
        house_verify.input_verify_code(GlobalVar.house_verify_code)
        house_verify.click_submit_button()

    @allure.step("更新举证时间超期")
    def update_verify_time(self, web_driver):
        select_trade_house_sql = "select id from trade_house where house_code='" + self.house_code + "'"
        house_id = str(DataBaseUtil('SQL Server', ini.database_name).select_sql(select_trade_house_sql)[0][0])
        update_time_sql = "update house_verify set expiration_time = '" + dt_strftime_with_delta(-2, "%Y-%m-%d") \
                          + "' where house_id = '" + house_id + "' and is_valid = 1"
        DataBaseUtil("SQL Server", ini.database_name).update_sql(update_time_sql)
        JobService().house_verify_out_date_job(web_driver)
