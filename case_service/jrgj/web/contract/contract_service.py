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

    def agent_add_contract(self, house_code, house_info, customer_code, env, test_data, flag='买卖'):
        """经纪人创建合同"""
        self.main_leftview.click_contract_management_label()
        if flag == '买卖':
            self.contract_table.click_sale_contract_tab()
        elif flag == '租赁':
            self.contract_table.click_rent_contract_tab()
        else:
            raise ValueError('传值错误')
        self.contract_table.click_create_order_button()
        if flag == '租赁':
            self.contract_create_order.choose_business_type('租赁')
        self.contract_create_order.input_house_code(house_code)
        self.contract_create_order.click_get_house_info_button()
        self.contract_create_order.verify_house_info(house_info)
        self.contract_create_order.click_verify_house_button()
        assert self.main_topview.find_notification_content() == '房源信息校验通过！'
        logger.info('房源信息校验通过')
        self.contract_create_order.input_customer_code(customer_code)
        self.contract_create_order.click_get_customer_info_button()
        self.contract_create_order.click_next_step_button()
        if env in ['sz', 'ks', 'zjg']:
            self.contract_create_order.choose_district_contract(env)
            self.contract_create_order.click_confirm_button_in_dialog()
        if flag == '买卖':
            self.contract_create_order.input_sale_contract_content(env, test_data)
        if flag == '租赁':
            self.contract_create_order.input_rent_contract_content(test_data)
        self.contract_create_order.click_submit_button()
        assert self.main_topview.find_notification_content() == '提交成功'
        logger.info('合同创建成功')
        self.main_upview.clear_all_title()
        self.main_leftview.click_contract_management_label()
        if flag == '买卖':
            self.contract_table.click_sale_contract_tab()
        if flag == '租赁':
            self.contract_table.click_rent_contract_tab()
        self.contract_table.input_house_code_search(house_code)
        self.contract_table.input_customer_code_search(customer_code)
        self.contract_table.click_search_button()
        contract_code = self.contract_table.get_contract_code_by_row(1)
        self.main_upview.clear_all_title()
        return contract_code

    def agent_submit_examine(self, contract_code):
        """经纪人提交审核"""
        self.main_leftview.change_role('经纪人')
        self.main_leftview.click_contract_management_label()
        self.contract_table.click_sale_contract_tab()
        self.contract_table.input_contract_code_search(contract_code)
        self.contract_table.click_search_button()
        self.contract_table.go_contract_detail_by_row(1)
        self.contract_detail.click_go_examine_button()
        self.contract_detail.dialog_click_confirm_button()

    def super_admin_delete_contract(self, contract_code, flag='买卖'):
        """超级管理员删除合同"""
        self.main_leftview.change_role('超级管理员')
        self.main_leftview.click_contract_management_label()
        if flag == '买卖':
            self.contract_table.click_sale_contract_tab()
        elif flag == '租赁':
            self.contract_table.click_rent_contract_tab()
        else:
            raise ValueError('传值错误')
        self.contract_table.input_contract_code_search(contract_code)
        self.contract_table.click_search_button()
        self.contract_table.delete_contract_by_row(1)
        self.contract_table.tooltip_click_confirm_button()
        self.main_topview.close_notification()
        self.main_leftview.change_role('经纪人')
