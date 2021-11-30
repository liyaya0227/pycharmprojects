#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_sale_share_house.py
@date: 2021/11/26 0026
"""
import allure
import pytest
from utils.logger import logger
from common.readconfig import ini
from utils.databaseutil import DataBaseUtil
from utils.timeutil import dt_strftime_with_delta
from case_service.jrjob.job_service import JobService
from page_object.common.app.common.commonpage import AppCommonPage
from page_object.jrgj.app.login.loginpage import AppLoginPage
from page_object.jrgj.app.main.mainpage import AppMainPage
from page_object.jrgj.app.message.tablepage import AppMessageTablePage
from page_object.jrgj.app.mine.minepage import AppMinePage
from page_object.common.app.notifications.tablepage import AppNotificationsTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.sharepool.tablepage import SharePoolTablePage


@pytest.mark.app_notifications
@allure.feature("测试APP通知-共享池")
class TestSaleSharePool(object):

    @pytest.fixture(scope="class", autouse=True)
    def setup_and_teardown(self, web_driver, android_driver, android_driver2):
        app_login = AppLoginPage(android_driver)
        app_main = AppMainPage(android_driver)
        app_mine = AppMinePage(android_driver)
        app_common = AppCommonPage(android_driver)
        app_notification = AppNotificationsTablePage(android_driver)
        app_message_table = AppMessageTablePage(android_driver)
        main_leftview = MainLeftViewPage(web_driver)
        second_app_login = AppLoginPage(android_driver2)
        second_app_main = AppMainPage(android_driver2)
        second_app_mine = AppMinePage(android_driver2)
        second_app_common = AppCommonPage(android_driver2)
        second_app_notification = AppNotificationsTablePage(android_driver2)
        second_app_message_table = AppMessageTablePage(android_driver2)
        house_table = HouseTablePage(web_driver)

        main_leftview.change_role('经纪人')
        self.house_code = house_table.get_house_code_by_db(flag='买卖')
        assert self.house_code != '', "不存在房源"
        app_login.log_in(ini.user_account, ini.user_password)
        app_main.close_top_view()
        app_main.click_message_button()
        app_message_table.click_notification_tab()
        app_message_table.click_clear_message_button()
        app_common.open_notifications()
        app_notification.dismiss_all_notification()
        second_app_login.log_in(ini.om_user_account, ini.om_user_password)
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

    @allure.story("二手房源未跟进，校验推送和消息内容")
    def test_001(self, web_driver, android_driver, android_driver2):
        app_common = AppCommonPage(android_driver)
        app_notification = AppNotificationsTablePage(android_driver)
        app_message_table = AppMessageTablePage(android_driver)
        second_app_common = AppCommonPage(android_driver2)
        second_app_notification = AppNotificationsTablePage(android_driver2)
        second_app_message_table = AppMessageTablePage(android_driver2)

        self.check_house(web_driver, self.house_code)
        self.update_house_not_follow_info(self.house_code, -20)
        self.exec_follow_up_remind_job(web_driver)
        app_common.open_notifications()
        pytest.assume(app_notification.get_notification_title_by_row(1) == '二手房源14天未跟进')
        pytest.assume(app_notification.get_notification_content_by_row(1) in
                      "房源编号" + self.house_code + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "已有14天没有跟进动作，请及时跟进")
        app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_house_message() ==
                      "房源编号" + self.house_code + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "已有14天没有跟进动作，请及时跟进")
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '二手房源14天未跟进')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "房源编号" + self.house_code + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "已有14天没有跟进动作，请及时跟进")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '二手房源14天未跟进')
        pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "房源编号" + self.house_code + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "已有14天没有跟进动作，请及时跟进")
        app_common.back_previous_step()
        app_common.back_previous_step()
        self.exec_into_share_pool_remind_job(web_driver)
        app_common.open_notifications()
        pytest.assume(app_notification.get_notification_title_by_row(1) == '二手房源15天未跟进')
        pytest.assume(app_notification.get_notification_content_by_row(1) in
                      "房源编号" + self.house_code + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "已有15天没有跟进动作，即将进入门店共享池，请及时跟进")
        app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_house_message() ==
                      "房源编号" + self.house_code + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "已有15天没有跟进动作，即将进入门店共享池，请及时跟进")
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '二手房源15天未跟进')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "房源编号" + self.house_code + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "已有15天没有跟进动作，即将进入门店共享池，请及时跟进")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '二手房源15天未跟进')
        pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "房源编号" + self.house_code + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "已有15天没有跟进动作，即将进入门店共享池，请及时跟进")
        app_common.back_previous_step()
        app_common.back_previous_step()
        self.exec_into_store_share_pool_job(web_driver)
        app_common.open_notifications()
        pytest.assume(app_notification.get_notification_title_by_row(1) == '二手房源进入门店共享池')
        pytest.assume(app_notification.get_notification_content_by_row(1) in
                      "房源编号" + self.house_code + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "由于15天内没有跟进动作，房源进入门店共享池")
        app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_house_message() ==
                      "房源编号" + self.house_code + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "由于15天内没有跟进动作，房源进入门店共享池")
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '二手房源进入门店共享池')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "房源编号" + self.house_code + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "由于15天内没有跟进动作，房源进入门店共享池")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '二手房源进入门店共享池')
        pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "房源编号" + self.house_code + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "由于15天内没有跟进动作，房源进入门店共享池")
        app_common.back_previous_step()
        app_common.back_previous_step()
        self.update_entry_time(self.house_code, -20)
        self.exec_into_region_share_pool_job(web_driver)
        second_app_common.open_notifications()
        pytest.assume(second_app_notification.get_notification_title_by_row(1) == '房源进入区域共享池')
        pytest.assume(second_app_notification.get_notification_content_by_row(1) in
                      "房源编号" + self.house_code + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "由于在门店共享池没有认领，房源进入区域共享池")
        second_app_notification.dismiss_all_notification()
        second_app_common.down_swipe_for_refresh()
        pytest.assume(second_app_message_table.get_house_message() ==
                      "房源编号" + self.house_code + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "由于在门店共享池没有认领，房源进入区域共享池")
        second_app_message_table.go_house_message_list()
        pytest.assume(second_app_message_table.get_message_list_message_title_by_row(1) == '房源进入区域共享池')
        pytest.assume(second_app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "房源编号" + self.house_code + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "由于在门店共享池没有认领，房源进入区域共享池")
        second_app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(second_app_message_table.get_message_detail_message_title() == '房源进入区域共享池')
        pytest.assume(second_app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(second_app_message_table.get_message_detail_message_content() ==
                      "房源编号" + self.house_code + ini.house_community_name + "-" + ini.house_building_id + "-"
                      + ini.house_building_cell + "-" + ini.house_floor + "-" + ini.house_doorplate
                      + "由于在门店共享池没有认领，房源进入区域共享池")
        second_app_common.back_previous_step()
        second_app_common.back_previous_step()
        self.claim_house(web_driver, self.house_code)

    @allure.step("处理房源状态")
    def check_house(self, web_driver, house_code):
        main_upview = MainUpViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        share_pool_table = SharePoolTablePage(web_driver)

        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        if house_detail.check_house_in_share_pool():
            main_upview.clear_all_title()
            main_leftview.click_share_pool_label()
            share_pool_table.click_store_share_pool_tab()
            share_pool_table.click_sale_tab()
            share_pool_table.input_house_code_search(house_code)
            share_pool_table.click_search_button()
            if share_pool_table.get_table_count() != 0:
                share_pool_table.claim_house_by_row(1)
                main_topview.close_notification()
            else:
                share_pool_table.click_region_share_pool_tab()
                share_pool_table.click_sale_tab()
                share_pool_table.click_reset_button()
                share_pool_table.input_house_code_search(house_code)
                share_pool_table.click_search_button()
                share_pool_table.claim_house_by_row(1)
                main_topview.close_notification()
        main_upview.clear_all_title()

    @allure.step("更新房源未跟进时间")
    def update_house_not_follow_info(self, house_code, not_follow_day):
        delete_sys_private_phone_record_sql = "delete from sys_private_phone_record where house_no='" \
                                              + house_code + "'"
        DataBaseUtil('SQL Server', ini.database_name).update_sql(delete_sys_private_phone_record_sql)
        house_id = str(DataBaseUtil('SQL Server', ini.database_name).select_sql(
            "select id from trade_house where house_code='" + house_code + "'")[0][0])
        delete_house_followup_sql = "delete from trade_house_followup where trade_id='" + house_id + "'"
        DataBaseUtil('SQL Server', ini.database_name).update_sql(delete_house_followup_sql)
        delete_take_look_info_sql = "delete from take_look_info where house_resource like '%" + house_id + "%'"
        DataBaseUtil('SQL Server', ini.database_name).update_sql(delete_take_look_info_sql)
        delete_important_update_record_sql = "delete from trade_Important_update_recond where house_id='" \
                                             + house_id + "'"
        DataBaseUtil('SQL Server', ini.database_name).update_sql(delete_important_update_record_sql)
        update_house_role_log_sql = "update trade_house_role_log set create_time='" \
                                    + dt_strftime_with_delta(not_follow_day, "%Y-%m-%d %H:%M:%S") \
                                    + "' where house_id='" + house_id + "'"
        DataBaseUtil('SQL Server', ini.database_name).update_sql(update_house_role_log_sql)
        logger.info("数据库修改跟进时间成功")

    @allure.step("执行14天未跟进的job")
    def exec_follow_up_remind_job(self, web_driver):
        JobService().house_follow_up_remind_job(web_driver, flag='买卖')
        logger.info("执行执行14天未跟进的job成功")

    @allure.step("执行房源即将进入共享池的job")
    def exec_into_share_pool_remind_job(self, web_driver):
        JobService().house_into_share_pool_remind_job(web_driver, flag='买卖')
        logger.info("执行即将进入共享池的job成功")

    @allure.step("执行进入门店共享池的job")
    def exec_into_store_share_pool_job(self, web_driver):
        JobService().house_into_store_share_pool_job(web_driver)
        logger.info("执行进入门店共享池的job成功")

    @allure.step("更新房源未跟进时间")
    def update_entry_time(self, house_code, entry_time):
        house_id = str(DataBaseUtil('SQL Server', ini.database_name).select_sql(
            "select id from trade_house where house_code='" + house_code + "'")[0][0])
        update_house_role_log_sql = "update trade_house_share_pool set store_entry_time='" \
                                    + dt_strftime_with_delta(entry_time, "%Y-%m-%d %H:%M:%S") \
                                    + "' where house_id='" + house_id + "'"
        DataBaseUtil('SQL Server', ini.database_name).update_sql(update_house_role_log_sql)
        logger.info("数据库修改跟进时间成功")

    @allure.step("执行进入区域共享池的job")
    def exec_into_region_share_pool_job(self, web_driver):
        JobService().house_into_region_share_pool_job(web_driver)
        logger.info("执行进入区域共享池的job成功")

    @allure.step("认领房源")
    def claim_house(self, web_driver, house_code):
        main_topview = MainTopViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        share_pool_table = SharePoolTablePage(web_driver)

        main_leftview.click_share_pool_label()
        share_pool_table.click_region_share_pool_tab()
        share_pool_table.click_sale_tab()
        share_pool_table.input_house_code_search(house_code)
        share_pool_table.click_search_button()
        share_pool_table.claim_house_by_row(1)
        main_topview.close_notification()
        main_upview.clear_all_title()
