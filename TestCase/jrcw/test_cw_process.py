#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_cw_process.py
@date: 2021/10/12 0012
"""
import pytest
import allure
from config.conf import cm
from utils.logger import log
from common.readconfig import ini
from utils.jsonutil import get_data
from common.globalvar import GlobalVar
from page_object.common.web.login.loginpage import LoginPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.customer.tablepage import CustomerTablePage
from page_object.jrgj.web.customer.detailpage import CustomerDetailPage
from page_object.jrgj.web.contract.tablepage import ContractTablePage
from page_object.jrgj.web.contract.detailpage import ContractDetailPage
from page_object.jrgj.web.contract.previewpage import ContractPreviewPage
from page_object.jrgj.web.contract.createorderpage import ContractCreateOrderPage
from case_service.jrgj.web.contract.contract_service import ContractService


@pytest.mark.sale
@pytest.mark.contract
@pytest.mark.run(order=21)
@allure.feature("测试买卖合同，财务流程模块")
class TestCWProcess(object):
    contract_code = ''

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        login = LoginPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_detail = ContractDetailPage(web_driver)
        contract_preview = ContractPreviewPage(web_driver)
        contract_service = ContractService()

        self.check_house_and_customer(web_driver)
        json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_contract/create_order_" + ini.environment + ".json"
        test_data = get_data(json_file_path)
        self.contract_code = contract_service.agent_add_contract(web_driver, GlobalVar.house_code, GlobalVar.house_info,
                                                                 GlobalVar.customer_code, ini.environment, test_data)
        contract_service.agent_submit_examine(web_driver, self.contract_code)
        # self.add_contract(web_driver, ini.environment, test_data)
        # main_leftview.click_contract_management_label()
        # contract_table.click_sale_contract_tab()
        # contract_table.input_house_code_search(GlobalVar.house_code)
        # contract_table.input_customer_code_search(GlobalVar.customer_code)
        # contract_table.click_search_button()
        # self.contract_code = contract_table.get_contract_code_by_row(1)
        # contract_table.go_contract_detail_by_row(1)
        # contract_detail.click_go_examine_button()  # 经纪人提交审核
        # contract_detail.dialog_click_confirm_button()
        main_leftview.change_role('商圈经理')  # 商圈经理审核
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_examine_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.pass_examine_by_row(1)
        main_topview.close_notification()
        main_leftview.change_role('合同法务')  # 法务审核
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_examine_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.legal_examine_by_row(1)
        contract_preview.click_pass_button()
        main_topview.close_notification()
        main_leftview.change_role('经纪人')  # 签章
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_preview_button()
        contract_preview.click_signature_button()
        main_topview.close_notification()
        main_leftview.log_out()
        login.log_in(ini.cw_user_account, ini.cw_user_password, app='财务系统web端')
        yield
        if self.contract_code:
            main_leftview.change_role('超级管理员')
            main_leftview.click_contract_management_label()
            contract_table.click_sale_contract_tab()
            contract_table.input_contract_code_search(self.contract_code)
            contract_table.click_search_button()
            contract_table.delete_contract_by_row(1)
            contract_table.tooltip_click_confirm_button()
            main_topview.close_notification()
        main_leftview.change_role('经纪人')

    @staticmethod
    def check_house_and_customer(web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        customer_table = CustomerTablePage(web_driver)
        customer_detail = CustomerDetailPage(web_driver)
        contract_table = ContractTablePage(web_driver)

        main_leftview.change_role('经纪人')
        GlobalVar.house_code = house_table.get_house_code_by_db(flag='买卖')
        assert GlobalVar.house_code != ''
        log.info('房源编号为：' + GlobalVar.house_code)
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.clear_filter('买卖')
        house_table.input_house_code_search(GlobalVar.house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        GlobalVar.house_info = house_detail.get_address_dialog_house_property_address()
        GlobalVar.house_info['house_code'] = GlobalVar.house_code
        GlobalVar.house_info['house_type'] = house_detail.get_house_type()
        GlobalVar.house_info['orientations'] = house_detail.get_orientations()
        GlobalVar.house_info['floor'] = house_detail.get_detail_floor()
        GlobalVar.house_info['inspect_type'] = house_detail.get_inspect_type()
        GlobalVar.house_info['house_state'] = house_detail.get_house_state()
        log.info('获取房源信息，新建合同校验需要')
        main_upview.clear_all_title()
        main_leftview.click_my_customer_label()
        customer_table.click_all_tab()
        customer_table.choose_customer_wish('不限')
        customer_table.input_search_text(ini.custom_telephone)
        customer_table.click_search_button()
        customer_table.go_customer_detail_by_row(1)
        GlobalVar.customer_code = customer_detail.get_customer_code()
        GlobalVar.customer_name = customer_detail.get_customer_name()
        log.info('获取客源信息，新建合同校验需要')
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_house_code_search(GlobalVar.house_code)
        contract_table.input_customer_code_search(GlobalVar.customer_code)
        contract_table.click_search_button()
        if contract_table.get_contract_table_count() > 0:
            main_leftview.change_role('超级管理员')
            main_leftview.click_contract_management_label()
            contract_table.click_sale_contract_tab()
            contract_table.input_house_code_search(GlobalVar.house_code)
            contract_table.input_customer_code_search(GlobalVar.customer_code)
            contract_table.click_search_button()
            count = contract_table.get_contract_table_count()
            for _ in range(count):
                contract_table.delete_contract_by_row(1)
                contract_table.tooltip_click_confirm_button()
                main_topview.close_notification()
        main_leftview.change_role('经纪人')

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
        contract_create_order.input_house_code(GlobalVar.house_code)
        contract_create_order.click_get_house_info_button()
        contract_create_order.verify_house_info(GlobalVar.house_info)
        contract_create_order.click_verify_house_button()
        assert main_topview.find_notification_content() == '房源信息校验通过！'
        log.info('房源信息校验通过')
        contract_create_order.input_customer_code(GlobalVar.customer_code)
        contract_create_order.click_get_customer_info_button()
        contract_create_order.click_next_step_button()
        if ini.environment == 'sz':
            contract_create_order.choose_district_contract(env)
            contract_create_order.click_confirm_button_in_dialog()
        contract_create_order.input_sale_contract_content(env, test_data)
        contract_create_order.click_submit_button()
        assert main_topview.find_notification_content() == '提交成功'
        log.info('合同创建成功')
        main_upview.clear_all_title()

    @allure.story("测试买卖合同，财务流程模块")
    def test_001(self, web_driver):
        pass
