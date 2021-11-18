#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_rent_contract.py
@date: 2021/11/16 0016
"""
import allure
import pytest
from config.conf import cm
from common.readconfig import ini
from page_object.jrgj.app.login.loginpage import AppLoginPage
from page_object.jrgj.app.mine.minepage import AppMinePage
from utils.jsonutil import get_data
from page_object.common.app.common.commonpage import AppCommonPage
from page_object.common.app.notifications.tablepage import AppNotificationsTablePage
from page_object.jrgj.app.main.mainpage import AppMainPage
from page_object.jrgj.app.message.tablepage import AppMessageTablePage
from page_object.jrgj.web.customer.detailpage import CustomerDetailPage
from page_object.jrgj.web.customer.tablepage import CustomerTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.contract.detailpage import ContractDetailPage
from page_object.jrgj.web.contract.previewpage import ContractPreviewPage
from page_object.jrgj.web.contract.tablepage import ContractTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from case_service.jrgj.web.contract.contract_service import ContractService
from utils.logger import logger


@allure.feature("测试APP通知-合同")
class TestRentContract(object):

    contract_code = ''

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver, oppo_android_driver):
        contract_service = ContractService(web_driver)
        app_login = AppLoginPage(oppo_android_driver)
        app_main = AppMainPage(oppo_android_driver)
        app_mine = AppMinePage(oppo_android_driver)
        app_message_table = AppMessageTablePage(oppo_android_driver)

        app_login.log_in(ini.user_account, ini.user_password)
        app_main.close_top_view()
        app_main.click_message_button()
        app_message_table.click_notification_tab()
        yield
        if self.contract_code:
            contract_service.super_admin_delete_contract(self.contract_code, flag='租赁')
        app_main.click_mine_button()
        app_mine.log_out()

    @allure.story("测试租赁合同审核流程， APP通知内容")
    def test_001(self, web_driver, oppo_android_driver):
        app_common = AppCommonPage(oppo_android_driver)
        app_notification = AppNotificationsTablePage(oppo_android_driver)
        app_message_table = AppMessageTablePage(oppo_android_driver)

        env = ini.environment
        self.prepare_for_add_contract(web_driver)
        self.create_contract_and_submit_examine(web_driver, env)
        app_common.open_notifications()
        pytest.assume(app_notification.get_notification_title_by_row(1) == '店长审核')
        pytest.assume(app_notification.get_notification_content_by_row(1) ==
                      "租赁合同" + self.contract_code + "需要您审核，请尽快处理！")
        app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_contract_message() ==
                      "租赁合同" + self.contract_code + "需要您审核，请尽快处理！")
        app_message_table.go_contract_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '店长审核')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "租赁合同" + self.contract_code + "需要您审核，请尽快处理！")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '店长审核')
        pytest.assume(app_message_table.get_message_detail_message_type() == '签约消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "租赁合同" + self.contract_code + "需要您审核，请尽快处理！")
        app_common.back_previous_step()
        app_common.back_previous_step()
        self.business_manager_reject_examine(web_driver)
        app_common.open_notifications()
        pytest.assume(app_notification.get_notification_title_by_row(1) == '租赁合同审核驳回')
        pytest.assume(app_notification.get_notification_content_by_row(1) ==
                      "您的租赁" + self.contract_code + "被驳回，请去网页端检查合同重新提审。")
        app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_contract_message() ==
                      "您的租赁" + self.contract_code + "被驳回，请去网页端检查合同重新提审。")
        app_message_table.go_contract_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '租赁合同审核驳回')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您的租赁" + self.contract_code + "被驳回，请去网页端检查合同重新提审。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '租赁合同审核驳回')
        pytest.assume(app_message_table.get_message_detail_message_type() == '签约消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您的租赁" + self.contract_code + "被驳回，请去网页端检查合同重新提审。")
        app_common.back_previous_step()
        app_common.back_previous_step()
        self.agent_submit_examine_again_and_pass_examine(web_driver)
        app_common.open_notifications()
        pytest.assume(app_notification.get_notification_title_by_row(1) == '租赁合同审核通过')
        pytest.assume(app_notification.get_notification_content_by_row(1) ==
                      "您的租赁" + self.contract_code + "已审核通过，请去网页端完成后续流程。")
        app_notification.dismiss_all_notification()
        app_common.down_swipe_for_refresh()
        pytest.assume(app_message_table.get_contract_message() ==
                      "您的租赁" + self.contract_code + "已审核通过，请去网页端完成后续流程。")
        app_message_table.go_contract_message_list()
        pytest.assume(app_message_table.get_message_list_message_title_by_row(1) == '租赁合同审核通过')
        pytest.assume(app_message_table.get_message_list_message_content_by_row(1)[5:] ==
                      "您的租赁" + self.contract_code + "已审核通过，请去网页端完成后续流程。")
        app_message_table.go_message_list_message_detail_by_row(1)
        pytest.assume(app_message_table.get_message_detail_message_title() == '租赁合同审核通过')
        pytest.assume(app_message_table.get_message_detail_message_type() == '签约消息')
        pytest.assume(app_message_table.get_message_detail_message_content() ==
                      "您的租赁" + self.contract_code + "已审核通过，请去网页端完成后续流程。")
        app_common.back_previous_step()
        app_common.back_previous_step()

    @allure.step("获取创建合同所需的房源信息")
    def prepare_for_add_contract(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        customer_table = CustomerTablePage(web_driver)
        customer_detail = CustomerDetailPage(web_driver)
        contract_table = ContractTablePage(web_driver)

        main_leftview.change_role('经纪人')
        self.house_code = house_table.get_house_code_by_db(flag='租赁')
        assert self.house_code != '', '租赁房源不存在'
        logger.info('房源编号为：' + self.house_code)
        main_leftview.click_all_house_label()
        house_table.click_rent_tab()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(self.house_code)
        house_table.go_house_detail_by_row(1)
        self.house_info = house_detail.get_address_dialog_house_property_address()
        self.house_info['house_code'] = self.house_code
        self.house_info['house_type'] = house_detail.get_house_type()
        self.house_info['orientations'] = house_detail.get_orientations()
        self.house_info['floor'] = house_detail.get_detail_floor()
        self.house_info['renovation_condition'] = house_detail.get_renovation_condition()
        self.house_info['enable_watch_time'] = house_detail.get_enable_watch_time()
        logger.info('获取房源信息，新建租赁合同校验需要')
        main_upview.clear_all_title()
        main_leftview.click_my_customer_label()
        customer_table.click_all_tab()
        customer_table.choose_customer_wish('不限')
        customer_table.input_search_text(ini.custom_telephone)
        customer_table.click_search_button()
        assert customer_table.get_customer_table_count() == 1, '客源不存在'
        customer_table.go_customer_detail_by_row(1)
        self.customer_code = customer_detail.get_customer_code()
        self.customer_name = customer_detail.get_customer_name()
        logger.info('获取客源信息，新建合同校验需要')
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_rent_contract_tab()
        contract_table.input_house_code_search(self.house_code)
        contract_table.input_customer_code_search(self.customer_code)
        contract_table.click_search_button()
        if contract_table.get_contract_table_count() > 0:
            main_leftview.change_role('超级管理员')
            main_leftview.click_contract_management_label()
            contract_table.click_rent_contract_tab()
            contract_table.input_house_code_search(self.house_code)
            contract_table.input_customer_code_search(self.customer_code)
            contract_table.click_search_button()
            count = contract_table.get_contract_table_count()
            for _ in range(count):
                contract_table.delete_contract_by_row(1)
                contract_table.tooltip_click_confirm_button()
                main_topview.close_notification()
        main_leftview.change_role('经纪人')

    @allure.step("创建合同，提交审核")
    def create_contract_and_submit_examine(self, web_driver, env):
        main_topview = MainTopViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_detail = ContractDetailPage(web_driver)
        contract_service = ContractService(web_driver)
        contract_preview = ContractPreviewPage(web_driver)

        json_file_path = cm.test_data_dir + "/jrgj/test_rent/test_contract/test_create_order.json"
        test_data = get_data(json_file_path)
        self.contract_code = contract_service.agent_add_contract(self.house_code, self.house_info,
                                                                 self.customer_code, env, test_data, flag='租赁')
        main_leftview.click_contract_management_label()  # 经纪人盖章
        contract_table.click_rent_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_preview_button()  # 签章
        contract_preview.click_signature_button()
        main_topview.close_notification()
        contract_preview.click_print_with_sign_button()  # 经纪人有章打印
        contract_preview.cancel_print()
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()  # 经纪人签约时间
        contract_table.click_rent_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_subject_contract()
        contract_detail.upload_two_sign_contract()
        main_topview.close_notification()
        contract_detail.click_subject_contract()  # 经纪人上传主体合同
        contract_detail.upload_pictures([cm.tmp_picture_file])
        contract_detail.click_submit_button()
        contract_detail.click_attachment_info()  # 提交备件审核
        contract_detail.upload_lessor_identification([cm.tmp_picture_file])
        contract_detail.upload_lessor_house_identification([cm.tmp_picture_file])
        contract_detail.upload_tenantry_identification([cm.tmp_picture_file])
        contract_detail.upload_other_attachment([cm.tmp_picture_file])
        contract_detail.upload_other_registration_form([cm.tmp_picture_file])
        contract_detail.upload_other_delivery_note([cm.tmp_picture_file])
        contract_detail.click_submit_examine_button()
        main_topview.close_notification()
        main_upview.clear_all_title()

    @allure.step("商圈经理驳回审核")
    def business_manager_reject_examine(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)

        main_leftview.change_role('商圈经理')  # 商圈经理备件审核
        main_leftview.click_contract_management_label()
        contract_table.click_rent_contract_examine_tab()
        contract_table.click_wait_examine()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.reject_examine_by_row(1, reason="自动化测试需要")
        main_topview.close_notification()
        main_leftview.change_role('初级经纪人')

    @allure.step("经纪人重新提审，商圈经理审核通过")
    def agent_submit_examine_again_and_pass_examine(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_detail = ContractDetailPage(web_driver)

        main_leftview.change_role('初级经纪人')
        main_leftview.click_contract_management_label()  # 经纪人签约时间
        contract_table.click_rent_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_attachment_info()  # 提交备件审核
        # contract_detail.upload_lessor_identification([cm.tmp_picture_file])
        # contract_detail.upload_lessor_house_identification([cm.tmp_picture_file])
        # contract_detail.upload_tenantry_identification([cm.tmp_picture_file])
        # contract_detail.upload_other_attachment([cm.tmp_picture_file])
        # contract_detail.upload_other_registration_form([cm.tmp_picture_file])
        # contract_detail.upload_other_delivery_note([cm.tmp_picture_file])
        contract_detail.click_submit_examine_button()
        main_topview.close_notification()
        main_leftview.change_role('商圈经理')  # 商圈经理备件审核
        main_leftview.click_contract_management_label()
        contract_table.click_rent_contract_examine_tab()
        contract_table.click_wait_examine()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.pass_examine_by_row(1)
        main_topview.close_notification()
        main_leftview.change_role('初级经纪人')
