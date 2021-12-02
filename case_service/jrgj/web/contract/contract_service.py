#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: contract_service.py
@date: 2021/10/13 0013
"""
from utils.logger import logger
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.contract.detailpage import ContractDetailPage
from page_object.jrgj.web.contract.tablepage import ContractTablePage
from page_object.jrgj.web.contract.createorderpage import ContractCreateOrderPage


class ContractService(MainUpViewPage, MainTopViewPage, MainLeftViewPage, ContractTablePage, ContractCreateOrderPage,
                      ContractDetailPage):

    def agent_add_contract(self, house_code, house_info, customer_code, env, test_data, flag='买卖'):
        """经纪人创建合同"""
        super(MainTopViewPage, self).click_contract_management_label()
        if flag == '买卖':
            super(MainLeftViewPage, self).click_sale_contract_tab()
        elif flag == '租赁':
            super(MainLeftViewPage, self).click_rent_contract_tab()
        else:
            raise ValueError('传值错误')
        super(MainLeftViewPage, self).click_create_order_button()
        if flag == '租赁':
            super(ContractTablePage, self).choose_business_type('租赁')
        super(ContractTablePage, self).input_house_code(house_code)
        super(ContractTablePage, self).click_get_house_info_button()
        super(ContractTablePage, self).verify_house_info(house_info)
        super(ContractTablePage, self).click_verify_house_button()
        assert super(MainUpViewPage, self).find_notification_content() == '房源信息校验通过！'
        logger.info('房源信息校验通过')
        super(ContractTablePage, self).input_customer_code(customer_code)
        super(ContractTablePage, self).click_get_customer_info_button()
        super(ContractTablePage, self).click_next_step_button()
        if env in ['sz', 'ks', 'zjg']:
            super(ContractTablePage, self).choose_district_contract(env)
            super(ContractTablePage, self).click_confirm_button_in_dialog()
        if flag == '买卖':
            super(ContractTablePage, self).input_sale_contract_content(env, test_data)
        if flag == '租赁':
            super(ContractTablePage, self).input_rent_contract_content(test_data)
        super(ContractTablePage, self).click_submit_button()
        assert super(MainUpViewPage, self).find_notification_content() == '提交成功'
        logger.info('合同创建成功')
        super().clear_all_title()
        super(MainTopViewPage, self).click_contract_management_label()
        if flag == '买卖':
            super(MainLeftViewPage, self).click_sale_contract_tab()
        if flag == '租赁':
            super(MainLeftViewPage, self).click_rent_contract_tab()
        super(MainLeftViewPage, self).input_house_code_search(house_code)
        super(MainLeftViewPage, self).input_customer_code_search(customer_code)
        super(MainLeftViewPage, self).click_search_button()
        contract_code = super(MainLeftViewPage, self).get_contract_code_by_row(1)
        super().clear_all_title()
        return contract_code

    def agent_submit_examine(self, contract_code):
        """经纪人提交审核"""
        super(MainTopViewPage, self).change_role('经纪人')
        super(MainTopViewPage, self).click_contract_management_label()
        super(MainLeftViewPage, self).click_sale_contract_tab()
        super(MainLeftViewPage, self).input_contract_code_search(contract_code)
        super(MainLeftViewPage, self).click_search_button()
        super(MainLeftViewPage, self).go_contract_detail_by_row(1)
        super(ContractCreateOrderPage, self).click_go_examine_button()
        super(ContractCreateOrderPage, self).dialog_click_confirm_button()

    def super_admin_delete_contract(self, contract_code, flag='买卖'):
        """超级管理员删除合同"""
        super(MainTopViewPage, self).change_role('超级管理员')
        super(MainTopViewPage, self).click_contract_management_label()
        if flag == '买卖':
            super(MainLeftViewPage, self).click_sale_contract_tab()
        elif flag == '租赁':
            super(MainLeftViewPage, self).click_rent_contract_tab()
        else:
            raise ValueError('传值错误')
        super(MainLeftViewPage, self).input_contract_code_search(contract_code)
        super(MainLeftViewPage, self).click_search_button()
        super(MainLeftViewPage, self).delete_contract_by_row(1)
        super(MainLeftViewPage, self).tooltip_click_confirm_button()
        super(MainUpViewPage, self).close_notification()
        super(MainTopViewPage, self).change_role('经纪人')
