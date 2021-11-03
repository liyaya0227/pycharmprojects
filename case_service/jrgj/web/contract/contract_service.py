#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: contract_service.py
@date: 2021/10/13 0013
"""
from utils.logger import logger
from common.readconfig import ini
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.contract.detailpage import ContractDetailPage
from page_object.jrgj.web.contract.tablepage import ContractTablePage
from page_object.jrgj.web.contract.createorderpage import ContractCreateOrderPage


class ContractService(object):

    @staticmethod
    def agent_add_contract(web_driver, house_code, house_info, customer_code, env, test_data):
        main_upview = MainUpViewPage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_create_order = ContractCreateOrderPage(web_driver)

        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.click_create_order_button()
        contract_create_order.input_house_code(house_code)
        contract_create_order.click_get_house_info_button()
        contract_create_order.verify_house_info(house_info)
        contract_create_order.click_verify_house_button()
        assert main_topview.find_notification_content() == '房源信息校验通过！'
        logger.info('房源信息校验通过')
        contract_create_order.input_customer_code(customer_code)
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
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_house_code_search(house_code)
        contract_table.input_customer_code_search(customer_code)
        contract_table.click_search_button()
        return contract_table.get_contract_code_by_row(1)

    @staticmethod
    def agent_submit_examine(web_driver, contract_code):
        main_leftview = MainLeftViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_detail = ContractDetailPage(web_driver)

        main_leftview.change_role('经纪人')
        main_leftview.click_contract_management_label()
        contract_table.click_sale_contract_tab()
        contract_table.input_contract_code_search(contract_code)
        contract_table.click_search_button()
        contract_table.go_contract_detail_by_row(1)
        contract_detail.click_go_examine_button()  # 经纪人提交审核
        contract_detail.dialog_click_confirm_button()
