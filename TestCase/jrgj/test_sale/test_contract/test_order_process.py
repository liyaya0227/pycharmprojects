#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_order_process.py
@date: 2021/7/6 0006
"""
import pytest
import allure
from common.globalvar import GlobalVar
from config.conf import cm
from utils.jsonutil import get_data
from utils.logger import logger
from common.readconfig import ini
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.contract.createorderpage import ContractCreateOrderPage
from page_object.jrgj.web.contract.tablepage import ContractTablePage
from page_object.jrgj.web.contract.detailpage import ContractDetailPage
from page_object.jrgj.web.contract.previewpage import ContractPreviewPage
from page_object.jrgj.web.achievement.detailpage import AchievementDetailPage
from page_object.jrgj.web.achievement.tablepage import AchievementTablePage
from page_object.jrgj.web.transaction.tablepage import TransactionTablePage
from page_object.jrgj.web.transaction.detailpage import TransactionDetailPage


@pytest.mark.sale
@pytest.mark.contract
@pytest.mark.run(order=21)
@allure.feature("测试买卖合同流程模块")
class TestOrderProcess(object):

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
            contract_table.click_sale_contract_tab()
            contract_table.input_contract_code_search(self.contract_code)
            contract_table.click_search_button()
            contract_table.delete_contract_by_row(1)
            contract_table.tooltip_click_confirm_button()
            main_topview.close_notification()
        main_leftview.change_role('经纪人')

    @allure.story("测试买卖合同流程")
    @pytest.mark.parametrize('env', GlobalVar.city_env[ini.environment])
    def test_001(self, web_driver, env):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_detail = ContractDetailPage(web_driver)
        contract_preview = ContractPreviewPage(web_driver)
        achievement_table = AchievementTablePage(web_driver)
        achievement_detail = AchievementDetailPage(web_driver)
        transaction_table = TransactionTablePage(web_driver)
        transaction_detail = TransactionDetailPage(web_driver)

        json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_contract/create_order_" + env + ".json"
        test_data = get_data(json_file_path)
        self.add_contract(web_driver, env, test_data)
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_house_code_search(GlobalVar.house_code)
        contract_table.input_customer_code_search(GlobalVar.customer_code)
        contract_table.click_search_button()
        self.contract_code = contract_table.get_contract_code_by_row(1)
        assert contract_table.get_contract_table_count() == 1
        contract_details = contract_table.get_contract_detail_by_row(1)
        assert contract_details['contract_status'] == '起草中'
        assert contract_details['pre_examine'] == '未知'
        # assert contract_details['change_rescind'] == '未知'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '未知'
        contract_table.go_contract_detail_by_row(1)
        assert contract_detail.create_contract_icon_is_light()
        logger.info('初始状态显示正确')
        contract_detail.click_go_examine_button()  # 经纪人提交审核
        contract_detail.dialog_click_confirm_button()
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1)
        assert contract_details['contract_status'] == '审核中'
        assert contract_details['pre_examine'] == '待审核'
        # assert contract_details['change_rescind'] == '未知'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '未知'
        contract_table.go_contract_detail_by_row(1)
        assert contract_detail.submit_examine_icon_is_light()
        logger.info('经纪人提交审核后，状态显示正确')
        main_leftview.change_role('商圈经理')  # 商圈经理审核
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_examine_tab()
        contract_table.click_wait_examine()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        assert contract_table.get_contract_table_count() == 1
        contract_table.pass_examine_by_row(1)
        assert main_topview.find_notification_content() == '操作成功'
        contract_table.click_had_examine()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        assert contract_table.get_contract_table_count() == 1
        main_leftview.change_role('经纪人')
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1)
        assert contract_details['contract_status'] == '审核中'
        assert contract_details['pre_examine'] == '审核中'
        # assert contract_details['change_rescind'] == '未知'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '未知'
        contract_table.go_contract_detail_by_row(1)
        assert contract_detail.submit_examine_icon_is_light()
        assert not contract_detail.pass_examine_icon_is_light()
        logger.info('商圈经理审核后，状态显示正确')
        main_leftview.change_role('合同法务')  # 法务审核
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_examine_tab()
        contract_table.click_wait_examine()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        assert contract_table.get_contract_table_count() == 1
        contract_table.legal_examine_by_row(1)
        contract_preview.click_pass_button()
        assert main_topview.find_notification_content() == '操作成功'
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_examine_tab()
        contract_table.click_had_examine()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        assert contract_table.get_contract_table_count() == 1
        main_leftview.change_role('经纪人')
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1)
        assert contract_details['contract_status'] == '审核通过'
        assert contract_details['pre_examine'] == '通过'
        # assert contract_details['change_rescind'] == '未知'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '未知'
        contract_table.go_contract_detail_by_row(1)
        assert contract_detail.pass_examine_icon_is_light()
        logger.info('法务审核通过后，状态显示正确')
        contract_detail.click_preview_button()  # 签章
        contract_preview.click_signature_button()
        assert main_topview.find_notification_content() == '操作成功'
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1)
        assert contract_details['contract_status'] == '已盖章'
        assert contract_details['pre_examine'] == '通过'
        # assert contract_details['change_rescind'] == '未知'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '未知'
        contract_table.go_contract_detail_by_row(1)
        assert contract_detail.last_sign_icon_is_light()
        logger.info('经纪人盖章后，状态显示正确')
        contract_detail.click_preview_button()  # 经纪人有章打印
        contract_preview.click_print_with_sign_button()
        contract_preview.cancel_print()
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1)
        assert contract_details['contract_status'] == '已盖章'
        assert contract_details['pre_examine'] == '通过'
        # assert contract_details['change_rescind'] == '未知'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '未知'
        contract_table.go_contract_detail_by_row(1)
        assert contract_detail.last_sign_print_icon_is_light()
        logger.info('经纪人有章打印后，状态显示正确')
        main_upview.clear_all_title()  # 经纪人签约时间
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_subject_contract()
        contract_detail.upload_two_sign_contract()
        assert main_topview.find_notification_content() == '操作成功'
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1)
        assert contract_details['contract_status'] == '已签约'
        assert contract_details['pre_examine'] == '通过'
        # assert contract_details['change_rescind'] == '未知'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '未知'
        contract_table.go_contract_detail_by_row(1)
        assert contract_detail.sign_time_icon_is_light()
        logger.info('经纪人填写签约时间后，状态显示正确')
        contract_detail.click_subject_contract()  # 经纪人上传主体合同
        contract_detail.upload_pictures([cm.tmp_picture_file])
        contract_detail.click_submit_button()
        assert contract_detail.check_dialog_exist()
        contract_detail.dialog_click_close_button()
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1)
        assert contract_details['contract_status'] == '已签约'
        assert contract_details['pre_examine'] == '通过'
        # assert contract_details['change_rescind'] == '未知'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '未知'
        contract_table.go_contract_detail_by_row(1)
        assert contract_detail.upload_contract_icon_is_light()
        logger.info('经纪人上传合同后，状态显示正确')
        contract_detail.click_subject_contract()  # 经纪人提交业绩审核
        contract_detail.click_submit_button()
        contract_detail.click_report_achievement_button()
        achievement_detail.click_submit_button()
        assert main_topview.find_notification_content() == '操作成功'
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1)
        assert contract_details['contract_status'] == '已签约'
        assert contract_details['pre_examine'] == '通过'
        # assert contract_details['change_rescind'] == '未知'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '初始'
        logger.info('经纪人提交业绩审核后，状态显示正确')
        main_leftview.change_role('商圈经理')  # 商圈经理业绩审核
        main_leftview.click_achievement_label()
        achievement_table.click_achievement_examine_tab()
        achievement_table.click_to_examine_tab()
        achievement_table.input_contract_code_search(self.contract_code)
        achievement_table.click_search_button()
        assert achievement_table.get_achievement_table_count() == 1
        achievement_table.click_pass_examine_button_by_row(1)
        assert main_topview.find_notification_content() == '操作成功'
        main_upview.clear_all_title()
        main_leftview.click_achievement_label()
        achievement_table.click_achievement_examine_tab()
        achievement_table.click_pass_examine_tab()
        achievement_table.input_contract_code_search(self.contract_code)
        achievement_table.click_search_button()
        assert achievement_table.get_achievement_table_count() == 1
        main_leftview.change_role('经纪人')
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1)
        assert contract_details['contract_status'] == '已签约'
        assert contract_details['pre_examine'] == '通过'
        # assert contract_details['change_rescind'] == '未知'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '审核通过'
        logger.info('商圈经理审核业绩后，状态显示正确')
        contract_table.update_agency_fee(self.contract_code)  # 数据库修改代理费
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1)
        assert contract_details['contract_status'] == '已签约'
        assert contract_details['pre_examine'] == '通过'
        # assert contract_details['change_rescind'] == '未知'
        assert contract_details['agency_fee_status'] == '已收齐'
        assert contract_details['achievement_status'] == '审核通过'
        logger.info('代理费收取后，状态显示正确')
        main_leftview.change_role('权证专员')  # 权证专员过户
        main_leftview.click_on_way_order_label()
        transaction_table.click_contract_code_tab()
        transaction_table.input_search_text(self.contract_code)
        transaction_table.click_search_button()
        assert transaction_table.get_table_count() == 1
        transaction_table.go_to_transaction_detail_by_row(1)
        transaction_detail.complete_transfer_house()
        assert main_topview.find_notification_content() == '操作成功'
        main_leftview.change_role('经纪人')
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1)
        assert contract_details['contract_status'] == '过户完成'
        assert contract_details['pre_examine'] == '通过'
        # assert contract_details['change_rescind'] == '未知'
        assert contract_details['agency_fee_status'] == '已收齐'
        assert contract_details['achievement_status'] == '审核通过'
        contract_table.go_contract_detail_by_row(1)
        assert contract_detail.transfer_house_icon_is_light()
        logger.info('权证过户后，状态显示正确')
        main_leftview.change_role('权证专员')  # 权证专员结案
        main_leftview.click_on_way_order_label()
        transaction_table.click_contract_code_tab()
        transaction_table.input_search_text(self.contract_code)
        transaction_table.click_search_button()
        assert transaction_table.get_table_count() == 1
        transaction_table.go_to_transaction_detail_by_row(1)
        transaction_detail.close_case()
        assert main_topview.find_notification_content() == '操作成功'
        main_leftview.change_role('经纪人')
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1)
        assert contract_details['contract_status'] == '已完结'
        assert contract_details['pre_examine'] == '通过'
        # assert contract_details['change_rescind'] == '未知'
        assert contract_details['agency_fee_status'] == '已收齐'
        assert contract_details['achievement_status'] == '审核通过'
        contract_table.go_contract_detail_by_row(1)
        assert contract_detail.trade_complete_icon_is_light()
        logger.info('权证结案后，状态显示正确')

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
        if ini.environment in ['sz', 'ks', 'zjg']:
            contract_create_order.choose_district_contract(env)
            contract_create_order.click_confirm_button_in_dialog()
        contract_create_order.input_sale_contract_content(env, test_data)
        contract_create_order.click_submit_button()
        assert main_topview.find_notification_content() == '提交成功'
        logger.info('合同创建成功')
        main_upview.clear_all_title()
