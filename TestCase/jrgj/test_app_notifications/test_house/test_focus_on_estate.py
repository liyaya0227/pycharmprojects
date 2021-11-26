#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_focus_on_estate.py
@date: 2021/11/22 0019
"""
import allure
import pytest
from config.conf import cm
from utils.logger import logger
from common.readconfig import ini
from utils.jsonutil import get_data
from utils.databaseutil import DataBaseUtil
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.common.app.common.commonpage import AppCommonPage
from page_object.jrgj.app.login.loginpage import AppLoginPage
from page_object.jrgj.app.main.mainpage import AppMainPage
from page_object.jrgj.app.message.tablepage import AppMessageTablePage
from page_object.jrgj.app.mine.minepage import AppMinePage
from page_object.common.app.notifications.tablepage import AppNotificationsTablePage
from page_object.jrgj.web.house.addpage import HouseAddPage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage


@allure.feature("测试APP通知-关注小区")
class TestFocusOnEstate(object):

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
        app_main.close_top_view()
        app_main.click_message_button()
        app_message_table.click_notification_tab()
        app_common.open_notifications()
        app_notification.dismiss_all_notification()
        yield
        app_main.click_mine_button()
        app_mine.log_out()
        main_leftview.change_role('经纪人')

    @allure.story("新增房源，校验推送和消息内容")
    def test_001(self, web_driver, android_driver):
        app_common = AppCommonPage(android_driver)
        app_notification = AppNotificationsTablePage(android_driver)
        app_message_table = AppMessageTablePage(android_driver)

        self.focus_on_estate(web_driver)
        self.update_house_to_invalid(web_driver)
        self.add_new_house(web_driver)
        app_common.open_notifications()
        pytest.assume(app_notification.get_notification_title_by_row(1) == '关注房源-价格调整')
        pytest.assume(app_notification.get_notification_content_by_row(1) in
                      "您关注的房源 {" + ini.house_community_name + "} {" + self.house_code + "} 原价格"
                      + self.origin_house_price + "万元变更为" + self.new_house_price + "万元，请知悉。")
        app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_house_message() ==
                      "您关注的房源 {" + ini.house_community_name + "} {" + self.house_code + "} 原价格"
                      + self.origin_house_price + "万元变更为" + self.new_house_price + "万元，请知悉。")
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '关注房源-调整价格')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您关注的房源 {" + ini.house_community_name + "} {" + self.house_code + "} 原价格"
                      + self.origin_house_price + "万元变更为" + self.new_house_price + "万元，请知悉。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '关注房源-调整价格')
        pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您关注的房源 {" + ini.house_community_name + "} {" + self.house_code + "} 原价格"
                      + self.origin_house_price + "万元变更为" + self.new_house_price + "万元，请知悉。")
        app_common.back_previous_step()
        app_common.back_previous_step()

    @allure.step("经纪人关注小区")
    def focus_on_estate(self, web_driver):
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
        house_detail.click_focus_on_estate_button()
        main_upview.clear_all_title()

    @allure.step("将房源改为无效状态")
    def update_house_to_invalid(self):
        update_invalid_sql = "update trade_house set is_valid=0 where house_code='" + self.house_code + "'"
        DataBaseUtil("SQL Server", ini.database_name).update_sql(update_invalid_sql)

    @allure.step("经纪人新增房源")
    def add_new_house(self, web_driver):
        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_add = HouseAddPage(web_driver)

        json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_add.json"
        test_data = get_data(json_file_path)

        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.click_add_house_button()  # 点击新增房源按钮
        house_add.input_property_address('sale')  # 填写物业地址
        house_add.input_owner_info_and_house_info(test_data, 'sale')
        self.house_code = house_table.get_house_code_by_db(flag='买卖')
        main_upview.clear_all_title()
