#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_order_change.py
@date: 2021/9/28 0028
"""
import pytest
import allure
from common.globalvar import GlobalVar
from config.conf import cm
from utils.jsonutil import get_data
from utils.logger import logger
from common.readconfig import ini
from page_object.common.web.login.loginpage import LoginPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.contract.createorderpage import ContractCreateOrderPage
from page_object.jrgj.web.contract.tablepage import ContractTablePage
from page_object.jrgj.web.contract.detailpage import ContractDetailPage
from page_object.jrgj.web.contract.previewpage import ContractPreviewPage


@pytest.mark.rent
@pytest.mark.contract
@pytest.mark.run(order=-22)
@pytest.mark.skipif(ini.environment != 'sz', reason='只支持苏州')
@allure.feature("测试租赁合同变更模块")
class TestOrderChange(object):

    contract_code = ''

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)

        yield
        if self.contract_code:
            main_leftview.change_role('超级管理员')
            main_leftview.click_contract_management_label()
            contract_table.click_rent_contract_tab()
            contract_table.input_contract_code_search(self.contract_code)
            contract_table.click_search_button()
            contract_table.delete_contract_by_row(1)
            contract_table.tooltip_click_confirm_button()
            main_topview.close_notification()
        main_leftview.change_role('经纪人')

    @allure.story("测试租赁合同变更流程")
    @pytest.mark.parametrize('env', GlobalVar.city_env[ini.environment])
    def test_001(self, web_driver, env):
        login = LoginPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_create_order = ContractCreateOrderPage(web_driver)
        contract_detail = ContractDetailPage(web_driver)
        contract_preview = ContractPreviewPage(web_driver)

        if env == 'zjg':
            logger.info('暂不支持张家港')
            pytest.skip('暂不支持张家港')
        json_file_path = cm.test_data_dir + "/jrgj/test_rent/test_contract/test_create_order.json"
        test_data = get_data(json_file_path)
        self.add_contract(web_driver, env, test_data)
        main_leftview.click_contract_management_label()
        contract_table.click_rent_contract_tab()
        contract_table.input_house_code_search(GlobalVar.house_code)
        contract_table.input_customer_code_search(GlobalVar.customer_code)
        contract_table.click_search_button()
        self.contract_code = contract_table.get_contract_code_by_row(1)
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_preview_button()
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
        contract_detail.click_change_button()  # 经纪人变更
        contract_create_order.click_submit_change_button()
        if contract_detail.check_dialog_exist():
            contract_detail.dialog_click_confirm_button()
        contract_detail.cancel_change_dialog_input_reason('自动化测试')
        contract_detail.cancel_change_dialog_upload_picture([cm.tmp_picture_file])
        contract_detail.dialog_click_confirm_button()
        main_leftview.log_out()  # 商圈经理审核通过
        login.log_in(ini.s_user_account, ini.s_user_password)
        main_topview.click_close_button()
        main_leftview.click_contract_management_label()
        contract_table.click_change_contract_examine_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.change_contract_examine_pass_by_row(1)
        main_topview.close_notification()
        main_leftview.log_out()  # 经纪人查看状态
        login.log_in(ini.user_account, ini.user_password)
        main_topview.click_close_button()
        main_leftview.click_contract_management_label()
        contract_table.click_rent_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()

    @staticmethod
    def add_contract(web_driver, env, test_data):
        main_upview = MainUpViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_create_order = ContractCreateOrderPage(web_driver)

        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.click_create_order_button()
        contract_create_order.choose_business_type('租赁')
        contract_create_order.input_house_code(GlobalVar.house_code)
        contract_create_order.click_get_house_info_button()
        contract_create_order.verify_house_info(GlobalVar.house_info)
        contract_create_order.click_verify_house_button()
        assert main_topview.find_notification_content() == '房源信息校验通过！'
        logger.info('房源信息校验通过')
        contract_create_order.input_customer_code(GlobalVar.customer_code)
        contract_create_order.click_get_customer_info_button()
        contract_create_order.click_next_step_button()
        if ini.environment == 'sz':
            contract_create_order.choose_district_contract(env)
            contract_create_order.click_confirm_button_in_dialog()
        contract_create_order.input_rent_contract_content(test_data)
        contract_create_order.click_submit_button()
        assert main_topview.find_notification_content() == '提交成功'
        logger.info('合同创建成功')
        main_upview.clear_all_title()
