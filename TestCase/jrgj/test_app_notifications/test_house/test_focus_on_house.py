#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_focus_on_house.py
@date: 2021/11/19 0019
"""
import random
import string
import allure
import pytest
from config.conf import cm
from utils.logger import logger
from common.readconfig import ini
from utils.jsonutil import get_data
from utils.timeutil import dt_strftime_with_delta
from case_service.jrgj.web.contract.contract_service import ContractService
from page_object.jrgj.web.achievement.detailpage import AchievementDetailPage
from page_object.jrgj.web.achievement.tablepage import AchievementTablePage
from page_object.jrgj.web.contract.detailpage import ContractDetailPage
from page_object.jrgj.web.contract.previewpage import ContractPreviewPage
from page_object.jrgj.web.contract.tablepage import ContractTablePage
from page_object.jrgj.web.customer.tablepage import CustomerTablePage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.transaction.detailpage import TransactionDetailPage
from page_object.jrgj.web.transaction.tablepage import TransactionTablePage
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


@pytest.mark.app_notifications
@allure.feature("测试APP通知-关注房源")
class TestFocusOnHouse(object):
    new_house_price = str(random.randint(100, 999)) + "." + "".join(map(lambda x: random.choice(string.digits),
                                                                        range(2)))
    contract_code = ''

    @pytest.fixture(scope="function", autouse=True)
    def setup_and_teardown(self, web_driver, android_driver):
        app_login = AppLoginPage(android_driver)
        app_main = AppMainPage(android_driver)
        app_mine = AppMinePage(android_driver)
        app_common = AppCommonPage(android_driver)
        app_notification = AppNotificationsTablePage(android_driver)
        app_message_table = AppMessageTablePage(android_driver)
        main_leftview = MainLeftViewPage(web_driver)
        contract_service = ContractService(web_driver)

        main_leftview.change_role('经纪人')
        app_login.log_in(ini.user_account, ini.user_password)
        app_main.close_top_view()
        app_main.click_message_button()
        app_message_table.click_notification_tab()
        app_message_table.click_clear_message_button()
        app_common.open_notifications()
        app_notification.dismiss_all_notification()
        yield
        if self.contract_code:
            contract_service.super_admin_delete_contract(self.contract_code, flag='买卖')
        app_main.click_mine_button()
        app_mine.log_out()
        main_leftview.change_role('经纪人')

    @allure.story("调整价格及房源已成交，校验推送和消息内容")
    def test_001(self, web_driver, android_driver):
        app_common = AppCommonPage(android_driver)
        app_notification = AppNotificationsTablePage(android_driver)
        app_message_table = AppMessageTablePage(android_driver)

        env = ini.environment
        self.update_price(web_driver)
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
        self.deal_house(web_driver, env)
        app_common.open_notifications()
        pytest.assume(app_notification.get_notification_title_by_row(1) == '关注房源-房源已成交')
        pytest.assume(app_notification.get_notification_content_by_row(1) in
                      "您关注的房源｛" + ini.house_community_name + "｝｛" + self.house_code
                      + "｝房源状态变更为：｛已成交｝，请知悉。")
        app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_house_message() ==
                      "您关注的房源｛" + ini.house_community_name + "｝｛" + self.house_code
                      + "｝房源状态变更为：｛已成交｝，请知悉。")
        app_message_table.go_house_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '关注房源-房源已成交')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您关注的房源｛" + ini.house_community_name + "｝｛" + self.house_code
                      + "｝房源状态变更为：｛已成交｝，请知悉。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '关注房源-房源已成交')
        pytest.assume(app_message_table.get_message_detail_message_type() == '房源消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您关注的房源｛" + ini.house_community_name + "｝｛" + self.house_code
                      + "｝房源状态变更为：｛已成交｝，请知悉。")
        app_common.back_previous_step()
        app_common.back_previous_step()

    @allure.step("经纪人调整房源价格")
    def update_price(self, web_driver):
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
        house_detail.click_focus_on_house_button()
        self.origin_house_price = house_detail.get_house_price(flag='买卖')
        house_detail.update_house_price(self.new_house_price)
        main_topview.close_notification()

    @allure.step("经纪人成交房源")
    def deal_house(self, web_driver, env):
        self.prepare_for_add_contract(web_driver)
        self.create_contract(web_driver, env)

    def prepare_for_add_contract(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        customer_table = CustomerTablePage(web_driver)
        contract_table = ContractTablePage(web_driver)

        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(self.house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        self.house_info = house_detail.get_address_dialog_house_property_address()
        self.house_info['house_code'] = self.house_code
        self.house_info['house_type'] = house_detail.get_house_type()
        self.house_info['orientations'] = house_detail.get_orientations()
        self.house_info['floor'] = house_detail.get_detail_floor()
        self.house_info['inspect_type'] = house_detail.get_inspect_type()
        self.house_info['house_state'] = house_detail.get_house_state()
        logger.info('获取房源信息，新建合同校验需要')
        main_upview.clear_all_title()
        main_leftview.click_my_customer_label()
        customer_table.click_all_tab()
        customer_table.choose_customer_wish('不限')
        customer_table.input_search_text(ini.custom_telephone)
        customer_table.click_search_button()
        self.customer_code = customer_table.get_customer_code_by_row(1)
        self.customer_name = customer_table.get_customer_name_by_row(1)
        logger.info('获取客源信息，新建合同校验需要')
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_house_code_search(self.house_code)
        contract_table.input_customer_code_search(self.customer_code)
        contract_table.click_search_button()
        if contract_table.get_contract_table_count() > 0:
            main_leftview.change_role('超级管理员')
            main_leftview.click_contract_management_label()
            contract_table.click_sale_contract_tab()
            contract_table.input_house_code_search(self.house_code)
            contract_table.input_customer_code_search(self.customer_code)
            contract_table.click_search_button()
            count = contract_table.get_contract_table_count()
            for _ in range(count):
                contract_table.delete_contract_by_row(1)
                contract_table.tooltip_click_confirm_button()
                main_topview.close_notification()
        main_leftview.change_role('经纪人')

    def create_contract(self, web_driver, env):
        main_topview = MainTopViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_detail = ContractDetailPage(web_driver)
        contract_service = ContractService(web_driver)
        contract_preview = ContractPreviewPage(web_driver)
        achievement_table = AchievementTablePage(web_driver)
        achievement_detail = AchievementDetailPage(web_driver)
        transaction_table = TransactionTablePage(web_driver)
        transaction_detail = TransactionDetailPage(web_driver)

        json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_contract/create_order_" + env + ".json"
        test_data = get_data(json_file_path)
        self.contract_code = contract_service.agent_add_contract(self.house_code, self.house_info,
                                                                 self.customer_code, env, test_data, flag='买卖')
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_go_examine_button()  # 经纪人提交审核
        contract_detail.dialog_click_confirm_button()
        main_leftview.change_role('商圈经理')
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_examine_tab()
        contract_table.click_wait_examine()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.pass_examine_by_row(1)
        main_topview.close_notification()
        main_leftview.change_role('合同法务')
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_examine_tab()
        contract_table.click_wait_examine()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.legal_examine_by_row(1)
        contract_preview.click_pass_button()
        main_topview.close_notification()
        main_leftview.change_role('初级经纪人')
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_preview_button()  # 签章
        contract_preview.click_signature_button()
        main_topview.close_notification()
        contract_preview.click_print_with_sign_button()  # 经纪人有章打印
        contract_preview.cancel_print()
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()   # 经纪人签约时间
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_subject_contract_tab()
        contract_detail.upload_two_sign_contract()
        main_topview.close_notification()
        contract_detail.click_subject_contract_tab()  # 经纪人上传主体合同
        contract_detail.upload_pictures([cm.tmp_picture_file])
        contract_detail.click_submit_button()
        contract_detail.click_report_achievement_button()
        achievement_detail.click_submit_button()
        main_topview.close_notification()
        main_leftview.change_role('商圈经理')  # 商圈经理业绩审核
        main_leftview.click_achievement_label()
        achievement_table.click_achievement_examine_tab()
        achievement_table.click_to_examine_tab()
        achievement_table.input_contract_code_search(self.contract_code)
        achievement_table.click_search_button()
        achievement_table.click_pass_examine_button_by_row(1)
        main_topview.close_notification()
        main_leftview.change_role('超级管理员')  # 线下付款
        payers = ['业主', '客户']
        for n in range(len(payers)):
            main_leftview.click_contract_management_label()
            contract_table.click_sale_contract_tab()
            contract_table.input_contract_code_search(self.contract_code)
            contract_table.click_search_button()
            contract_table.contract_offline_collection_by_row(1)
            if contract_table.offline_collection_dialog_get_pay_money_by_payer(payers[n]) == '0.00':
                contract_table.dialog_click_cancel_button()
                continue
            contract_table.offline_collection_dialog_choose_payer(payers[n])
            contract_table.offline_collection_dialog_input_payer_time(
                dt_strftime_with_delta(-(len(payers)-n), '%Y-%m-%d %H:%M:%S'))
            contract_table.offline_collection_dialog_input_bank_serial(
                "".join(map(lambda x: random.choice(string.digits), range(8))))
            contract_table.offline_collection_dialog_upload_bank_receipt([cm.tmp_picture_file])
            contract_table.dialog_click_confirm_button()
        main_leftview.change_role('权证专员')  # 权证专员过户
        main_leftview.click_on_way_order_label()
        transaction_table.click_contract_code_tab()
        transaction_table.input_search_text(self.contract_code)
        transaction_table.click_search_button()
        transaction_table.go_to_transaction_detail_by_row(1)
        transaction_detail.complete_transfer_house()
        main_topview.close_notification()
        transaction_detail.close_case()  # 权证专员结案
        main_topview.close_notification()
        main_leftview.change_role('经纪人')
