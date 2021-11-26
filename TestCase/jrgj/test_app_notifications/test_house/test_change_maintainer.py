#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_change_maintainer.py
@date: 2021/11/19 0019
"""
import allure
import pytest
from page_object.common.web.login.loginpage import LoginPage
from utils.logger import logger
from common.readconfig import ini
from page_object.common.app.common.commonpage import AppCommonPage
from page_object.jrgj.app.login.loginpage import AppLoginPage
from page_object.jrgj.app.main.mainpage import AppMainPage
from page_object.jrgj.app.message.tablepage import AppMessageTablePage
from page_object.jrgj.app.mine.minepage import AppMinePage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.common.app.notifications.tablepage import AppNotificationsTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.main.rightviewpage import MainRightViewPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage


@allure.feature("测试APP通知-维护人变更")
class TestChangeMaintainer(object):
    new_maintainer_name = '自动化测试AAAAA'
    new_maintainer_account = '15800000001'
    new_maintainer_password = 'Autotest1'

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
        app_login.log_in(self.new_maintainer_account, self.new_maintainer_password)
        app_main.close_top_view()
        app_main.click_message_button()
        app_message_table.click_notification_tab()
        app_common.open_notifications()
        app_notification.dismiss_all_notification()
        yield
        app_main.click_mine_button()
        app_mine.log_out()
        main_leftview.change_role('经纪人')

    @allure.story("维护人变更")
    def test_001(self, web_driver, android_driver):
        app_common = AppCommonPage(android_driver)
        app_notification = AppNotificationsTablePage(android_driver)
        app_message_table = AppMessageTablePage(android_driver)

        self.change_maintainer(web_driver)
        # app_common.open_notifications()
        # pytest.assume(app_notification.get_notification_title_by_row(1) == '维护人变更')
        # pytest.assume(app_notification.get_notification_content_by_row(1) in
        #               "您已成为楼盘地址" + ini.house_community_name + "-" + ini.house_building_id + "-"
        #               + ini.house_building_cell + "-" + ini.house_doorplate + "房源编号" + self.house_code
        #               + "的维护人，请及时维护房源相关信息 。")
        # app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_house_message() ==
                      "您已成为楼盘地址" + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_doorplate + "房源编号" + self.house_code
                      + "的维护人，请及时维护房源相关信息 。")
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '维护人变更')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您已成为楼盘地址" + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_doorplate + "房源编号" + self.house_code
                      + "的维护人，请及时维护房源相关信息 。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '维护人变更')
        pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您已成为楼盘地址" + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_doorplate + "房源编号" + self.house_code
                      + "的维护人，请及时维护房源相关信息 。")
        app_common.back_previous_step()
        app_common.back_previous_step()
        self.change_maintainer_back(web_driver)

    @allure.step("经纪人调整房源价格")
    def change_maintainer(self, web_driver):
        main_upview = MainUpViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_rightview = MainRightViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)

        self.house_code = house_table.get_house_code_by_db(flag='买卖')
        assert self.house_code != '', "不存在房源"
        logger.info('房源编号为：' + self.house_code)
        self.origin_maintainer_name = main_rightview.get_login_person_name()
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(self.house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        house_detail.replace_maintainer(self.new_maintainer_name)
        main_topview.close_notification()
        main_upview.clear_all_title()

    @allure.step("经纪人调整房源价格")
    def change_maintainer_back(self, web_driver):
        login = LoginPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)

        main_leftview.log_out()
        login.log_in(self.new_maintainer_account, self.new_maintainer_password)
        main_leftview.change_role("经纪人")
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(self.house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        house_detail.replace_maintainer(self.origin_maintainer_name)
        main_topview.close_notification()
        main_leftview.log_out()
        login.log_in(ini.user_account, ini.user_password)
        main_leftview.change_role("经纪人")
