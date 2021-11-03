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

    def __init__(self, web_driver):
        self.main_upview = MainUpViewPage(web_driver)
        self.main_topview = MainTopViewPage(web_driver)
        self.main_leftview = MainLeftViewPage(web_driver)
        self.contract_table = ContractTablePage(web_driver)
        self.contract_create_order = ContractCreateOrderPage(web_driver)
        self.contract_detail = ContractDetailPage(web_driver)

    def agent_add_contract(self, house_code, house_info, customer_code, env, test_data):
        self.main_leftview.click_contract_management_label()
        self.contract_table.click_sale_contract_tab()
        self.contract_table.click_create_order_button()
        self.contract_create_order.input_house_code(house_code)
        self.contract_create_order.click_get_house_info_button()
        self.contract_create_order.verify_house_info(house_info)
        self.contract_create_order.click_verify_house_button()
        assert self.main_topview.find_notification_content() == '房源信息校验通过！'
        logger.info('房源信息校验通过')
        self.contract_create_order.input_customer_code(customer_code)
        self.contract_create_order.click_get_customer_info_button()
        self.contract_create_order.click_next_step_button()
        if ini.environment == 'sz':
            self.contract_create_order.choose_district_contract(env)
            self.contract_create_order.click_confirm_button_in_dialog()
        self.contract_create_order.input_sale_contract_content(env, test_data)
        self.contract_create_order.click_submit_button()
        assert self.main_topview.find_notification_content() == '提交成功'
        logger.info('合同创建成功')
        self.main_upview.clear_all_title()
        self.main_leftview.click_contract_management_label()
        self.contract_table.click_sale_contract_tab()
        self.contract_table.input_house_code_search(house_code)
        self.contract_table.input_customer_code_search(customer_code)
        self.contract_table.click_search_button()
        return self.contract_table.get_contract_code_by_row(1)

    def agent_submit_examine(self, contract_code):
        self.main_leftview.change_role('经纪人')
        self.main_leftview.click_contract_management_label()
        self.contract_table.click_sale_contract_tab()
        self.contract_table.input_contract_code_search(contract_code)
        self.contract_table.click_search_button()
        self.contract_table.go_contract_detail_by_row(1)
        self.contract_detail.click_go_examine_button()  # 经纪人提交审核
        self.contract_detail.dialog_click_confirm_button()
