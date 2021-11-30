#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_certificates_process.py
@date: 2021/11/18 0018
"""
import allure
import pytest
from utils.logger import logger
from common.readconfig import ini
from common.globalvar import GlobalVar
from utils.databaseutil import DataBaseUtil
from utils.timeutil import dt_strftime, dt_strftime_with_delta
from page_object.common.app.common.commonpage import AppCommonPage
from page_object.jrgj.app.login.loginpage import AppLoginPage
from page_object.jrgj.app.main.mainpage import AppMainPage
from page_object.jrgj.app.message.tablepage import AppMessageTablePage
from page_object.jrgj.app.mine.minepage import AppMinePage
from page_object.jrgj.web.agreement.listpage import AgreementListPage
from page_object.common.app.notifications.tablepage import AppNotificationsTablePage
from page_object.jrgj.web.main.certificateexaminepage import CertificateExaminePage
from case_service.jrjob.job_service import JobService
from page_object.jrgj.web.main.rightviewpage import MainRightViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage


@pytest.mark.app_notifications
@allure.feature("测试APP通知-买卖证书审核")
class TestSaleSurvey(object):
    agreement_number = ''
    house_code = '100000067536'
    reason = "自动化测试需要，实勘M反馈" + dt_strftime("%Y%m%d%H%M%S")

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

    @allure.story("上传证书，驳回证书审核，证书到期提醒")
    def test_001(self, web_driver, android_driver):
        app_common = AppCommonPage(android_driver)
        app_notification = AppNotificationsTablePage(android_driver)
        app_message_table = AppMessageTablePage(android_driver)

        certificate_type_list = ["书面委托协议", "房产证"] if ini.environment in GlobalVar.city_env['wx'] \
            else ["书面委托协议", "钥匙委托凭证", "VIP服务委托协议", "房产证"]
        for certificate_type in certificate_type_list:
            self.check_certificates(web_driver, certificate_type)
            self.upload_certificates(web_driver, certificate_type)
            app_common.open_notifications()
            pytest.assume(app_notification.get_notification_title_by_row(1) == '上传证书')
            pytest.assume(app_notification.get_notification_content_by_row(1) in
                          "您好，您有" + ini.house_community_name + self.house_code + "的" + certificate_type
                          + "已上传待审核，请及时处理。")
            app_notification.dismiss_all_notification()
            app_common.down_swipe_for_refresh()
            pytest.assume(app_message_table.get_house_message() ==
                          "您好，您有" + ini.house_community_name + self.house_code + "的" + certificate_type
                          + "已上传待审核，请及时处理。")
            app_message_table.go_house_message_list()
            pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '上传证书')
            pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                          "您好，您有" + ini.house_community_name + self.house_code + "的" + certificate_type
                          + "已上传待审核，请及时处理。")
            app_message_table.go_message_list_message_detail_by_row(1)
            pytest.assume(app_message_table.get_message_detail_message_title() == '上传证书')
            pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
            pytest.assume(app_message_table.get_message_detail_message_content() ==
                          "您好，您有" + ini.house_community_name + self.house_code + "的" + certificate_type
                          + "已上传待审核，请及时处理。")
            app_common.back_previous_step()
            app_common.back_previous_step()
            self.om_reject_examine(web_driver, certificate_type)  # om驳回证书审核
            app_common.open_notifications()
            pytest.assume(app_notification.get_notification_title_by_row(1) == '证书审核M＼S驳回')
            pytest.assume(app_notification.get_notification_content_by_row(1) in
                          "您上传房源" + ini.house_community_name + self.house_code + "的" + certificate_type
                          + "，审核驳回，驳回理由：" + self.reason + "，请去系统内重新上传。")
            app_notification.dismiss_all_notification()
            app_common.down_swipe_for_refresh()
            pytest.assume(app_message_table.get_house_message() ==
                          "您上传房源" + ini.house_community_name + self.house_code + "的" + certificate_type
                          + "，审核驳回，驳回理由：" + self.reason + "，请去系统内重新上传。")
            app_message_table.go_house_message_list()
            pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '证书审核M＼S驳回')
            pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                          "您上传房源" + ini.house_community_name + self.house_code + "的" + certificate_type
                          + "，审核驳回，驳回理由：" + self.reason + "，请去系统内重新上传。")
            app_message_table.go_message_list_message_detail_by_row(1)
            pytest.assume(app_message_table.get_message_detail_message_title() == '证书审核M＼S驳回')
            pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
            pytest.assume(app_message_table.get_message_detail_message_content() ==
                          "您上传房源" + ini.house_community_name + self.house_code + "的" + certificate_type
                          + "，审核驳回，驳回理由：" + self.reason + "，请去系统内重新上传。")
            app_common.back_previous_step()
            app_common.back_previous_step()
            if certificate_type in ['书面委托协议', 'VIP服务委托协议']:
                self.upload_certificates(web_driver, certificate_type)  # 重新上传
                self.update_create_time_and_exec_job(web_driver, certificate_type)
                app_common.open_notifications()
                pytest.assume(app_notification.get_notification_title_by_row(1) == '证件到期无效')
                pytest.assume(app_notification.get_notification_content_by_row(1) in
                              "您的房源" + ini.house_community_name + self.house_code
                              + "委托协议7天后即将到期，请尽快重新上传委托协议。")
                app_notification.dismiss_all_notification()
                app_common.down_swipe_for_refresh()
                pytest.assume(app_message_table.get_house_message() ==
                              "您的房源" + ini.house_community_name + self.house_code
                              + "委托协议7天后即将到期，请尽快重新上传委托协议。")
                app_message_table.go_house_message_list()
                pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '证件到期无效')
                pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                              "您的房源" + ini.house_community_name + self.house_code
                              + "委托协议7天后即将到期，请尽快重新上传委托协议。")
                app_message_table.go_message_list_message_detail_by_row(1)
                pytest.assume(app_message_table.get_message_detail_message_title() == '证件到期无效')
                pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
                pytest.assume(app_message_table.get_message_detail_message_content() ==
                              "您的房源" + ini.house_community_name + self.house_code
                              + "委托协议7天后即将到期，请尽快重新上传委托协议。")
                app_common.back_previous_step()
                app_common.back_previous_step()

    @allure.step("检查证书上传情况，确保未上传")
    def check_certificates(self, web_driver, certificate_type):
        main_topview = MainTopViewPage(web_driver)
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
        house_detail.expand_certificates_info()
        if house_detail.check_upload_certificate(certificate_type) != '未上传':
            main_leftview.change_role('超级管理员')
            main_leftview.click_all_house_label()
            house_table.click_sale_tab()
            house_table.clear_filter('买卖')
            house_table.input_house_code_search(self.house_code)
            house_table.go_house_detail_by_row(1)
            house_detail.expand_certificates_info()
            house_detail.delete_certificate(certificate_type)
            main_topview.close_notification()
            main_leftview.change_role('经纪人')

    @allure.step("上传证书")
    def upload_certificates(self, web_driver, certificate_type):
        main_topview = MainTopViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        agreement_list = AgreementListPage(web_driver)

        if certificate_type != '房产证':
            main_leftview.click_agreement_list_label()
            self.agreement_number = agreement_list.get_agreement_number_certificate_name(certificate_type)
            main_upview.clear_all_title()
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(self.house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        house_detail.expand_certificates_info()
        if certificate_type == '书面委托协议':
            house_detail.upload_written_entrustment_agreement_with_random_data(self.agreement_number)
        elif certificate_type == '钥匙委托凭证':
            house_detail.upload_key_entrustment_certificate_with_random_data(self.agreement_number)
        elif certificate_type == 'VIP服务委托协议':
            house_detail.upload_vip_service_entrustment_agreement_with_random_data(self.agreement_number)
        elif certificate_type == '房产证':
            house_detail.upload_property_ownership_certificate_with_random_data()
        main_topview.close_notification()
        main_upview.clear_all_title()

    @allure.step("OM赋能经理审核驳回")
    def om_reject_examine(self, web_driver, certificate_type):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_rightview = MainRightViewPage(web_driver)
        certificate_examine = CertificateExaminePage(web_driver)

        main_leftview.change_role('赋能经理')
        main_rightview.click_certificate_examine()
        certificate_examine.click_reject_examine_button(self.house_code, certificate_type, self.reason)
        main_topview.close_notification()
        main_leftview.change_role('经纪人')

    @allure.step("数据库修改创建时间，执行job")
    def update_create_time_and_exec_job(self, web_driver, certificate_type):
        select_trade_house_sql = "select id from trade_house where house_code='" + self.house_code + "'"
        house_id = str(DataBaseUtil('SQL Server', ini.database_name).select_sql(select_trade_house_sql)[0][0])
        if certificate_type == '书面委托协议':
            update_create_time_sql = "update trade_house_delegate_info set end_time = '" \
                                     + dt_strftime_with_delta(6, "%Y-%m-%d") + "' where house_id = '" \
                                     + house_id + "' and status = 1"
        elif certificate_type == 'VIP服务委托协议':
            update_create_time_sql = "update trade_house_vipdelegate_info set end_time = '" \
                                     + dt_strftime_with_delta(6, "%Y-%m-%d") + "' where house_id = '" \
                                     + house_id + "' and status = 1"
        else:
            raise ValueError('暂不支持')
        DataBaseUtil('SQL Server', ini.database_name).update_sql(update_create_time_sql)
        JobService().certificate_out_date_job(web_driver)
