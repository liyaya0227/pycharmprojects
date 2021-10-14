#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: conftest.py
@date: 2021/9/29 0029
"""
import pytest
from common.globalvar import GlobalVar
from common.readconfig import ini
from page_object.jrgj.web.contract.tablepage import ContractTablePage
from page_object.jrgj.web.customer.detailpage import CustomerDetailPage
from page_object.jrgj.web.customer.tablepage import CustomerTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from utils.logger import log


@pytest.fixture(scope='package', autouse=True)
def prepare_for_add_contract(web_driver):
    main_topview = MainTopViewPage(web_driver)
    main_leftview = MainLeftViewPage(web_driver)
    main_upview = MainUpViewPage(web_driver)
    house_table = HouseTablePage(web_driver)
    house_detail = HouseDetailPage(web_driver)
    customer_table = CustomerTablePage(web_driver)
    customer_detail = CustomerDetailPage(web_driver)
    contract_table = ContractTablePage(web_driver)

    main_leftview.change_role('经纪人')
    GlobalVar.house_code = house_table.get_house_code_by_db(flag='租赁')
    assert GlobalVar.house_code != '', '租赁房源不存在'
    log.info('房源编号为：' + GlobalVar.house_code)
    main_leftview.click_all_house_label()
    house_table.click_rent_tab()
    house_table.clear_filter('买卖')
    house_table.input_house_code_search(GlobalVar.house_code)
    house_table.click_search_button()
    house_table.go_house_detail_by_row(1)
    GlobalVar.house_info = house_detail.get_address_dialog_house_property_address()
    GlobalVar.house_info['house_code'] = GlobalVar.house_code
    GlobalVar.house_info['house_type'] = house_detail.get_house_type()
    GlobalVar.house_info['orientations'] = house_detail.get_orientations()
    GlobalVar.house_info['floor'] = house_detail.get_detail_floor()
    GlobalVar.house_info['renovation_condition'] = house_detail.get_renovation_condition()
    GlobalVar.house_info['enable_watch_time'] = house_detail.get_enable_watch_time()
    log.info('获取房源信息，新建租赁合同校验需要')
    main_upview.clear_all_title()
    main_leftview.click_my_customer_label()
    customer_table.click_all_tab()
    customer_table.choose_customer_wish('不限')
    customer_table.input_search_text(ini.custom_telephone)
    customer_table.click_search_button()
    assert customer_table.get_customer_table_count() == 1, '客源不存在'
    customer_table.go_customer_detail_by_row(1)
    GlobalVar.customer_code = customer_detail.get_customer_code()
    GlobalVar.customer_name = customer_detail.get_customer_name()
    log.info('获取客源信息，新建合同校验需要')
    main_upview.clear_all_title()
    main_leftview.click_contract_management_label()
    contract_table.click_rent_contract_tab()
    contract_table.input_house_code_search(GlobalVar.house_code)
    contract_table.input_customer_code_search(GlobalVar.customer_code)
    contract_table.click_search_button()
    if contract_table.get_contract_table_count() > 0:
        main_leftview.change_role('超级管理员')
        main_leftview.click_contract_management_label()
        contract_table.click_rent_contract_tab()
        contract_table.input_house_code_search(GlobalVar.house_code)
        contract_table.input_customer_code_search(GlobalVar.customer_code)
        contract_table.click_search_button()
        count = contract_table.get_contract_table_count()
        for _ in range(count):
            contract_table.delete_contract_by_row(1)
            contract_table.tooltip_click_confirm_button()
            main_topview.close_notification()
    main_leftview.change_role('经纪人')
