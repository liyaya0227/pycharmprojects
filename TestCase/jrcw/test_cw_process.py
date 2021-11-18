#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_cw_process.py
@date: 2021/10/12 0012
"""
import random
import string
import pytest
import allure
from config.conf import cm
from utils.databaseutil import DataBaseUtil
from utils.logger import logger
from common.readconfig import ini
from utils.jsonutil import get_data
from common.globalvar import GlobalVar
from common_enum.city_name import CityNameEnum
from utils.timeutil import dt_strftime_with_delta, dt_strftime
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
from page_object.jrgj.web.achievement.detailpage import AchievementDetailPage
from page_object.jrgj.web.achievement.tablepage import AchievementTablePage
from case_service.jrjob.job_service import JobService
from page_object.jrcw.web.main.mainpage import MainPage as CwMainPage
from page_object.jrcw.web.sale.tablepage import SaleTablePage as CwSaleTablePage
from page_object.jrcw.web.receipt.tablepage import ReceiptTablePage as CwReceiptTablePage
from page_object.jrcw.web.settlement.tablepage import SettlementTablePage as CwSettlementTablePage
from page_object.jrcw.web.reconciliation.tablepage import ReconciliationTablePage as CwSReconciliationTablePage
from page_object.jrgj.web.shopsplitaccountreport.tablepage import ShopBrandDataReportTablePage
from page_object.jrgj.web.surveysplitaccountreport.tablepage import SurveySplitAccountReportTablePage
from page_object.jrcw.web.pay.tablepage import PayTablePage as CwPayTablePage


@pytest.mark.sale
@pytest.mark.finance
@pytest.mark.run(order=21)
@allure.feature("测试买卖合同，财务流程模块")
class TestCWProcess(object):

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)

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

    @allure.story("测试买卖合同，财务流程模块")
    def test_001(self, web_driver):
        json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_contract/create_order_" + ini.environment + ".json"
        test_data = get_data(json_file_path)
        self.contract_prepare(web_driver, test_data)
        self.check_sale(web_driver)
        self.pay_contract(web_driver)
        self.check_receipt(web_driver)
        self.pay_commission(web_driver)
        self.check_settlement(web_driver)
        JobService().generate_account_statement_job(web_driver)
        self.check_reconciliation(web_driver)
        self.check_pay(web_driver)
        self.check_jrgj_store_company(web_driver)

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
        logger.info('房源编号为：' + GlobalVar.house_code)
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
        logger.info('获取房源信息，新建合同校验需要')
        main_upview.clear_all_title()
        main_leftview.click_my_customer_label()
        customer_table.click_all_tab()
        customer_table.choose_customer_wish('不限')
        customer_table.input_search_text(ini.custom_telephone)
        customer_table.click_search_button()
        customer_table.go_customer_detail_by_row(1)
        GlobalVar.customer_code = customer_detail.get_customer_code()
        GlobalVar.customer_name = customer_detail.get_customer_name()
        logger.info('获取客源信息，新建合同校验需要')
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
        logger.info('房源信息校验通过')
        contract_create_order.input_customer_code(GlobalVar.customer_code)
        contract_create_order.click_get_customer_info_button()
        contract_create_order.click_next_step_button()
        if ini.environment == 'sz':
            contract_create_order.choose_district_contract(env)
            contract_create_order.click_confirm_button_in_dialog()
        contract_create_order.input_sale_contract_content(env, test_data)
        contract_create_order.click_submit_button()
        assert main_topview.find_notification_content() == '提交成功'
        logger.info('合同创建成功')
        main_upview.clear_all_title()

    @allure.step("B端创建合同及盖章")
    def contract_prepare(self, web_driver, test_data):
        main_leftview = MainLeftViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_detail = ContractDetailPage(web_driver)
        contract_preview = ContractPreviewPage(web_driver)
        contract_service = ContractService(web_driver)

        self.check_house_and_customer(web_driver)
        self.contract_code = contract_service.agent_add_contract(GlobalVar.house_code, GlobalVar.house_info,
                                                                 GlobalVar.customer_code, ini.environment, test_data)
        contract_service.agent_submit_examine(self.contract_code)
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

    @allure.step("财务系统查看销售单")
    def check_sale(self, web_driver):
        login = LoginPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        cw_main = CwMainPage(web_driver)
        cw_sale_table = CwSaleTablePage(web_driver)

        main_leftview.log_out()
        login.log_in(ini.cw_user_account, ini.cw_user_password, app='财务系统web端')
        cw_main.click_sale_label()
        cw_sale_table.input_order_code_search(self.contract_code)
        cw_sale_table.choose_city_search(CityNameEnum[ini.environment].value)
        cw_sale_table.click_search_button()
        pytest.assume(cw_sale_table.get_table_total_count() != '0')
        cw_main.log_out()
        login.log_in(ini.user_account, ini.user_password)
        main_leftview.change_role('经纪人')

    @allure.step("B端支付合同佣金")
    def pay_contract(self, web_driver):
        main_upview = MainUpViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_detail = ContractDetailPage(web_driver)
        contract_preview = ContractPreviewPage(web_driver)

        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_preview_button()
        contract_preview.click_print_with_sign_button()  # 打印
        contract_preview.cancel_print()
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_subject_contract()
        contract_detail.upload_two_sign_contract()  # 经纪人签约时间
        main_topview.close_notification()
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_subject_contract()
        contract_detail.upload_pictures([cm.tmp_picture_file])  # 经纪人上传主体合同
        contract_detail.click_submit_button()
        contract_detail.dialog_click_close_button()
        main_leftview.change_role('超级管理员')  # 线下付款
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        payers = ['业主', '客户']
        for n, payer in enumerate(payers):
            contract_table.contract_offline_collection_by_row(1)
            if contract_table.offline_collection_dialog_get_pay_money_by_payer(payer) == '0.00':
                contract_table.dialog_click_cancel_button()
                continue
            contract_table.offline_collection_dialog_choose_payer(payer)
            contract_table.offline_collection_dialog_input_payer_time(dt_strftime_with_delta(-4, '%Y-%m-%d %H:%M:%S'))
            contract_table.offline_collection_dialog_input_bank_serial(
                "".join(map(lambda x: random.choice(string.digits), range(8))))
            contract_table.offline_collection_dialog_upload_bank_receipt([cm.tmp_picture_file])
            contract_table.dialog_click_confirm_button()

    @allure.step("财务系统查看收款单")
    def check_receipt(self, web_driver):
        login = LoginPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        cw_main = CwMainPage(web_driver)
        cw_receipt_table = CwReceiptTablePage(web_driver)

        main_leftview.log_out()
        login.log_in(ini.cw_user_account, ini.cw_user_password, app='财务系统web端')
        cw_main.click_receipt_label()
        cw_receipt_table.input_order_code_search(self.contract_code)
        cw_receipt_table.choose_city_search(CityNameEnum[ini.environment].value)
        cw_receipt_table.click_search_button()
        pytest.assume(cw_receipt_table.get_table_total_count() != '0')
        cw_main.log_out()
        login.log_in(ini.user_account, ini.user_password)
        main_leftview.change_role('经纪人')

    @allure.step("B端审核合同业绩")
    def pay_commission(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_detail = ContractDetailPage(web_driver)
        achievement_table = AchievementTablePage(web_driver)
        achievement_detail = AchievementDetailPage(web_driver)

        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_achievement_detail_tab()
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

    @allure.step("财务系统查看结算单并在数据库修改结算时间")
    def check_settlement(self, web_driver):
        login = LoginPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        cw_main = CwMainPage(web_driver)
        cw_settlement_table = CwSettlementTablePage(web_driver)

        main_leftview.log_out()
        login.log_in(ini.cw_user_account, ini.cw_user_password, app='财务系统web端')
        cw_main.click_settlement_label()
        cw_settlement_table.input_order_code_search(self.contract_code)
        cw_settlement_table.choose_city_search(CityNameEnum[ini.environment].value)
        cw_settlement_table.click_search_button()
        pytest.assume(cw_settlement_table.get_table_total_count() != '0')
        for settlement_code in cw_settlement_table.get_table_settlement_code():
            update_settle_date_sql = "update doc_settlement set settle_date='" + dt_strftime("%Y-%m-%d") \
                                     + "' where settlement_identifier_no='" + settlement_code + "'"
            DataBaseUtil('Cw My SQL', ini.cw_database_name).update_sql(update_settle_date_sql)

    @allure.step("财务系统查看对账单")
    def check_reconciliation(self, web_driver):
        cw_main = CwMainPage(web_driver)
        cw_reconciliation_table = CwSReconciliationTablePage(web_driver)

        cw_main.click_reconciliation_label()
        cw_reconciliation_table.input_order_code_search(self.contract_code)
        cw_reconciliation_table.choose_city_search(CityNameEnum[ini.environment].value)
        cw_reconciliation_table.click_search_button()
        row_count = cw_reconciliation_table.get_table_total_count()
        pytest.assume(row_count != '0')
        for row in range(int(row_count)):
            cw_reconciliation_table.click_examine_button_by_row(row+1)
            cw_main.close_notice()

    @allure.step("财务系统查看付款单")
    def check_pay(self, web_driver):
        login = LoginPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        cw_main = CwMainPage(web_driver)
        cw_pay_table = CwPayTablePage(web_driver)

        cw_main.click_pay_label()
        cw_pay_table.input_order_code_search(self.contract_code)
        cw_pay_table.choose_city_search(CityNameEnum[ini.environment].value)
        cw_pay_table.click_search_button()
        row_count = cw_pay_table.get_table_total_count()
        pytest.assume(row_count != '0')
        for row in range(int(row_count)):
            cw_pay_table.click_pay_button_by_row(row+1)
            cw_pay_table.tip_pop_click_confirm_button()
            cw_main.close_notice()
        cw_main.log_out()
        login.log_in(ini.user_account, ini.user_password)
        main_leftview.change_role('经纪人')

    @allure.step("京日管家端查看门店及公司是否已分账")
    def check_jrgj_store_company(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        shop_brand_data_report = ShopBrandDataReportTablePage(web_driver)
        survey_split_account_report = SurveySplitAccountReportTablePage(web_driver)

        main_leftview.change_role('超级管理员')
        main_leftview.click_shop_split_account_data_table_label()
        shop_brand_data_report.click_wait_split_account_tab()
        shop_brand_data_report.input_contract_code_search(self.contract_code)
        shop_brand_data_report.clear_pay_time_search()
        shop_brand_data_report.click_search_button()
        pytest.assume(shop_brand_data_report.get_current_table_count() == 0)
        main_leftview.click_brand_rebate_data_table_label()
        shop_brand_data_report.click_wait_rebate_commission_tab()
        shop_brand_data_report.input_contract_code_search(self.contract_code)
        shop_brand_data_report.clear_pay_time_search()
        shop_brand_data_report.click_search_button()
        pytest.assume(shop_brand_data_report.get_current_table_count() == 0)
        main_leftview.click_survey_department_split_account_label()
        survey_split_account_report.click_wait_split_account_tab()
        survey_split_account_report.input_contract_code_search(self.contract_code)
        survey_split_account_report.clear_pay_time_search()
        survey_split_account_report.click_search_button()
        pytest.assume(survey_split_account_report.get_current_table_count() == 0)
