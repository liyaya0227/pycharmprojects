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
from config.conf import cm
from utils.logger import log
from common.readconfig import ini
from page_object.main.topviewpage import MainTopViewPage
from page_object.main.leftviewpage import MainLeftViewPage
from page_object.main.upviewpage import MainUpViewPage
from page_object.house.tablepage import HouseTablePage
from page_object.house.detailpage import HouseDetailPage
from page_object.customer.detailpage import CustomerDetailPage
from page_object.customer.tablepage import CustomerTablePage
from page_object.contract.tablepage import ContractTablePage
from page_object.contract.detailpage import ContractDetailPage
from page_object.contract.previewpage import ContractPreviewPage
from page_object.achievement.detailpage import AchievementDetailPage
from page_object.achievement.tablepage import AchievementTablePage

house_code = ''
customer_code = ''


@allure.feature("测试合同模块")
class TestOrderProcess(object):

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global house_code
        global customer_code

        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        customer_table = CustomerTablePage(web_driver)
        customer_detail = CustomerDetailPage(web_driver)

        main_leftview.change_role('经纪人')
        house_code = house_table.get_house_code_by_db(flag='租赁')
        assert house_code != ''
        log.info('创建合同的房源编号: ' + house_code)
        main_upview.clear_all_title()
        main_leftview.click_my_customer_label()
        customer_table.click_all_tab()
        customer_table.choose_customer_wish('不限')
        customer_table.input_search_text(ini.custom_telephone)
        customer_table.click_search_button()
        table_count = customer_table.get_customer_table_count()
        assert table_count == 1
        customer_table.go_customer_detail_by_row(1)
        customer_code = customer_detail.get_customer_code()
        assert customer_code != ''
        log.info('创建合同的客源编号: ' + customer_code)
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()

    @allure.story("测试买卖合同流程")
    @pytest.mark.rent
    @pytest.mark.contract
    @pytest.mark.run(order=-3)
    @pytest.mark.flaky(reruns=5, reruns_delay=2)
    def test_001(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_detail = ContractDetailPage(web_driver)
        contract_preview = ContractPreviewPage(web_driver)
        achievement_table = AchievementTablePage(web_driver)
        achievement_detail = AchievementDetailPage(web_driver)

        contract_table.click_rent_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_house_code_search(house_code)
        contract_table.input_customer_code_search(customer_code)
        contract_table.click_search_button()
        assert contract_table.get_contract_table_count() > 0
        contract_details = contract_table.get_contract_detail_by_row(1, flag='租赁')
        contract_code = contract_details['contract_code']
        assert contract_details['contract_status'] == '起草中'
        assert contract_details['attachment_examine'] == '未知'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '未知'
        contract_table.go_contract_detail_by_row(1)
        assert contract_detail.create_contract_icon_is_light()
        log.info('初始状态显示正确')
        contract_detail.click_preview_button()  # 签章
        contract_preview.click_signature_button()
        assert main_topview.find_notification_content() == '操作成功'
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_rent_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1, flag='租赁')
        assert contract_details['contract_status'] == '已盖章'
        assert contract_details['attachment_examine'] == '未知'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '未知'
        contract_table.go_contract_detail_by_row(1)
        assert contract_detail.last_sign_icon_is_light()
        log.info('经纪人盖章后，状态显示正确')
        contract_detail.click_preview_button()  # 经纪人有章打印
        contract_preview.click_print_with_sign_button()
        contract_preview.cancel_print()
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_rent_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1, flag='租赁')
        assert contract_details['contract_status'] == '已盖章'
        assert contract_details['attachment_examine'] == '未知'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '未知'
        contract_table.go_contract_detail_by_row(1)
        assert contract_detail.last_sign_print_icon_is_light()
        log.info('经纪人有章打印后，状态显示正确')
        contract_detail.click_subject_contract()  # 经纪人签约时间
        contract_detail.upload_two_sign_contract()
        assert main_topview.find_notification_content() == '操作成功'
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_rent_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1, flag='租赁')
        assert contract_details['contract_status'] == '已签约'
        assert contract_details['attachment_examine'] == '未知'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '未知'
        contract_table.go_contract_detail_by_row(1)
        assert contract_detail.sign_time_icon_is_light()
        log.info('经纪人填写签约时间后，状态显示正确')
        contract_detail.click_subject_contract()  # 经纪人上传主体合同
        contract_detail.upload_pictures([cm.tmp_picture_file])
        contract_detail.click_submit_button()
        assert contract_detail.check_dialog_exist()
        contract_detail.click_close_button()
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_rent_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1, flag='租赁')
        assert contract_details['contract_status'] == '已签约'
        assert contract_details['attachment_examine'] == '未知'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '未知'
        contract_table.go_contract_detail_by_row(1)
        assert contract_detail.upload_contract_icon_is_light()
        log.info('经纪人上传合同后，状态显示正确')
        contract_detail.click_attachment_info()  # 提交备件审核
        contract_detail.upload_lessor_identification([cm.tmp_picture_file])
        contract_detail.upload_lessor_house_identification([cm.tmp_picture_file])
        contract_detail.upload_tenantry_identification([cm.tmp_picture_file])
        contract_detail.upload_other_attachment([cm.tmp_picture_file])
        contract_detail.upload_other_registration_form([cm.tmp_picture_file])
        contract_detail.upload_other_delivery_note([cm.tmp_picture_file])
        contract_detail.click_submit_examine_button()
        assert main_topview.find_notification_content() == '操作成功'
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_rent_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1, flag='租赁')
        assert contract_details['contract_status'] == '已签约'
        assert contract_details['attachment_examine'] == '待审核'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '未知'
        contract_table.go_contract_detail_by_row(1)
        assert not contract_detail.pass_attachment_examine_icon_is_light()
        log.info('经纪人提交备件审核后，状态显示正确')
        main_leftview.change_role('商圈经理')  # 商圈经理备件审核
        main_leftview.click_contract_management_label()
        contract_table.click_rent_contract_examine_tab()
        contract_table.click_wait_examine()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        assert contract_table.get_contract_table_count() == 1
        contract_table.pass_examine_by_row(1)
        # assert main_topview.wait_notification_content_exist() == '操作成功'
        contract_table.click_had_examine()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        assert contract_table.get_contract_table_count() == 1
        main_leftview.change_role('经纪人')
        main_leftview.click_contract_management_label()
        contract_table.click_rent_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1, flag='租赁')
        assert contract_details['contract_status'] == '备件审核通过'
        assert contract_details['attachment_examine'] == '通过'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '未知'
        contract_table.go_contract_detail_by_row(1)
        assert contract_detail.pass_attachment_examine_icon_is_light()
        log.info('商圈经理备件审核通过后，状态显示正确')
        contract_detail.click_subject_contract()  # 经纪人提交业绩审核
        contract_detail.click_submit_button()
        contract_detail.click_report_achievement_button()
        achievement_detail.click_submit_button()
        assert main_topview.find_notification_content() == '操作成功'
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_rent_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1, flag='租赁')
        assert contract_details['contract_status'] == '备件审核通过'
        assert contract_details['attachment_examine'] == '通过'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '初始'
        log.info('经纪人提交业绩审核后，状态显示正确')
        main_leftview.change_role('商圈经理')  # 商圈经理业绩审核
        main_leftview.click_achievement_label()
        achievement_table.click_achievement_examine_tab()
        achievement_table.click_to_examine_tab()
        achievement_table.input_contract_code_search(contract_code)
        achievement_table.click_search_button()
        assert achievement_table.get_achievement_table_count() == 1
        achievement_table.click_pass_examine_button_by_row(1)
        assert main_topview.find_notification_content() == '操作成功'
        main_upview.clear_all_title()
        main_leftview.click_achievement_label()
        achievement_table.click_achievement_examine_tab()
        achievement_table.click_pass_examine_tab()
        achievement_table.input_contract_code_search(contract_code)
        achievement_table.click_search_button()
        assert achievement_table.get_achievement_table_count() == 1
        main_leftview.change_role('经纪人')
        main_leftview.click_contract_management_label()
        contract_table.click_rent_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1, flag='租赁')
        assert contract_details['contract_status'] == '备件审核通过'
        assert contract_details['attachment_examine'] == '通过'
        assert contract_details['agency_fee_status'] == '未收齐'
        assert contract_details['achievement_status'] == '审核通过'
        log.info('商圈经理审核业绩后，状态显示正确')
        contract_table.update_agency_fee(contract_code)  # 数据库修改代理费
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_rent_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_details = contract_table.get_contract_detail_by_row(1, flag='租赁')
        assert contract_details['contract_status'] == '备件审核通过'
        assert contract_details['attachment_examine'] == '通过'
        assert contract_details['agency_fee_status'] == '已收齐'
        assert contract_details['achievement_status'] == '审核通过'
        log.info('代理费收取后，状态显示正确')
        main_upview.clear_all_title()
