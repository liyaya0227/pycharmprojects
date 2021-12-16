#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_legal_reject_examine.py
@date: 2021/11/23 0023
"""
import random
import pytest
import allure
from config.conf import cm
from utils.logger import logger
from common.readconfig import ini
from utils.jsonutil import get_data
from common.globalvar import GlobalVar
from common_enum.contract_pay_type import ContractPayTypeEnum
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.contract.tablepage import ContractTablePage
from page_object.jrgj.web.contract.detailpage import ContractDetailPage
from page_object.jrgj.web.contract.previewpage import ContractPreviewPage
from case_service.jrgj.web.contract.contract_service import ContractService


@pytest.mark.sale
@pytest.mark.contract
@pytest.mark.run(order=22)
@allure.feature("测试买卖合同法务驳回模块")
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
            contract_table.click_sale_contract_tab()
            contract_table.input_contract_code_search(self.contract_code)
            contract_table.click_search_button()
            contract_table.delete_contract_by_row(1)
            contract_table.tooltip_click_confirm_button()
            main_topview.close_notification()
        main_leftview.change_role('经纪人')

    @allure.story("测试买卖合同法务驳回流程")
    @pytest.mark.parametrize('env', GlobalVar.city_env[ini.environment])
    @pytest.mark.parametrize('pay_type', [random.choice([x for x in ContractPayTypeEnum])])
    def test_001(self, web_driver, env, pay_type):
        main_topview = MainTopViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_detail = ContractDetailPage(web_driver)
        contract_preview = ContractPreviewPage(web_driver)
        contract_service = ContractService(web_driver)

        json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_contract/create_order_" + env + "_" + pay_type.value + ".json"
        test_data = get_data(json_file_path)
        self.contract_code = contract_service.agent_add_contract(GlobalVar.house_code, GlobalVar.house_info,
                                                                 GlobalVar.customer_code, env, test_data, flag='买卖')
        logger.info("创建合同成功")
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        self.contract_code = contract_table.get_contract_code_by_row(1)
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_go_examine_button()  # 经纪人提交审核
        contract_detail.dialog_click_confirm_button()
        logger.info("经纪人提交审核")
        main_leftview.change_role('商圈经理')  # 商圈经理审核
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_examine_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.pass_examine_by_row(1)
        main_topview.close_notification()
        logger.info("商圈经理审核通过")
        main_leftview.change_role('合同法务')  # 法务审核
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_examine_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        contract_table.legal_examine_by_row(1)
        contract_preview.click_reject_button()
        contract_preview.dialog_click_confirm_button()
        assert main_topview.find_notification_content() == '请填写驳回原因'
        for _ in range(9):
            contract_preview.reject_dialog_upload_picture(cm.tmp_picture_file)
        contract_preview.reject_dialog_upload_picture_by_windows(cm.tmp_picture_file)
        assert main_topview.find_notification_content() == '上传的文件不能超过9个，请重新选择'
        contract_preview.dialog_click_confirm_button()
        assert main_topview.find_notification_content() == '操作成功'
        logger.info("法务审核驳回")
        main_leftview.change_role('初级经纪人')
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(self.contract_code)
        contract_table.click_search_button()
        assert contract_table.get_contract_pre_examine_by_row(1) == '驳回'
        logger.info("经纪人校验签前审核状态显示正确")
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_contract_examine_process_tab()
        contract_detail.click_watch_examine_remark_button_by_row(1)
        assert contract_detail.examine_remark_dialog_get_picture_count() == 9
        logger.info("经纪人校验详情驳回备注图片数正确")
        contract_detail.dialog_click_close_button()
        main_upview.clear_all_title()
