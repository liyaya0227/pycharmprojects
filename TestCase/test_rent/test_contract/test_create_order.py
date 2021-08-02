#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_create_order.py
@time: 2021/7/2
"""

import pytest
import allure
from page_object.customer.detail import CustomerDetailPage
from page_object.customer.tablepage import CustomerTablePage
from utils.logger import log
from config.conf import cm
from common.readconfig import ini
from utils.jsonutil import get_data
from page_object.main.topviewpage import MainTopViewPage
from page_object.main.leftviewpage import MainLeftViewPage
from page_object.main.upviewpage import MainUpViewPage
from page_object.house.tablepage import HouseTablePage
from page_object.house.detailpage import HouseDetailPage
from page_object.contract.tablepage import ContractTablePage
from page_object.contract.createorderpage import ContractCreateOrderPage

house_info = {}
customer_info = {}


@allure.feature("测试合同模块")
class TestCreateOrder(object):

    json_file_path = cm.test_data_dir + "/test_rent/test_contract/test_create_order.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="class", autouse=True)
    def test_prepare(self, web_driver):
        global house_info
        global customer_info
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        customer_table = CustomerTablePage(web_driver)
        customer_detail = CustomerDetailPage(web_driver)
        contract_table = ContractTablePage(web_driver)

        main_leftview.change_role('经纪人')
        main_leftview.click_all_house_label()
        house_table.click_rent_tab()
        house_table.click_reset_button()
        house_table.clear_filter(flag='租赁')
        house_table.choose_estate_name_search(ini.house_community_name)
        house_table.choose_building_name_search(ini.house_building_id)
        house_table.click_search_button()
        table_count = house_table.get_house_table_count()
        assert table_count > 0
        for row in range(table_count):
            house_table.go_house_detail_by_row(row + 1)
            house_property_address = house_detail.get_house_property_address()
            if house_property_address['estate_name'] == ini.house_community_name \
                    and house_property_address['building_name'] == ini.house_building_id \
                    and house_property_address['door_name'] == ini.house_doorplate:
                house_info = house_property_address
                house_info['house_code'] = house_detail.get_house_code()
                house_info['house_type'] = house_detail.get_house_type()
                house_info['orientations'] = house_detail.get_orientations()
                house_info['floor'] = house_detail.get_floor()
                house_info['renovation_condition'] = house_detail.get_renovation_condition()
                house_info['enable_watch_time'] = house_detail.get_enable_watch_time()
                main_upview.close_title_by_name(house_property_address['estate_name'])
                break
            main_upview.close_title_by_name(house_property_address['estate_name'])
        assert house_info != {}
        log.info('获取房源信息，新建合同校验需要')
        main_upview.clear_all_title()
        main_leftview.click_my_customer_label()
        customer_table.click_all_tab()
        customer_table.choose_customer_wish('不限')
        customer_table.input_search_text(ini.custom_telephone)
        customer_table.click_search_button()
        table_count = customer_table.get_customer_table_count()
        assert table_count == 1
        customer_table.go_customer_detail_by_row(1)
        customer_info['customer_code'] = customer_detail.get_customer_code()
        customer_info['customer_name'] = customer_detail.get_customer_name()
        assert customer_info != {}
        log.info('获取客源信息，新建合同校验需要')
        main_upview.clear_all_title()
        main_leftview.click_contract_management_label()
        contract_table.click_rent_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_house_code_search(house_info['house_code'])
        contract_table.input_customer_code_search(customer_info['customer_code'])
        contract_table.click_search_button()
        if contract_table.get_contract_table_count() > 0:
            main_leftview.change_role('超级管理员')
            main_leftview.click_contract_management_label()
            contract_table.click_rent_contract_tab()
            contract_table.input_house_code_search(house_info['house_code'])
            contract_table.input_customer_code_search(customer_info['customer_code'])
            contract_table.click_search_button()
            count = contract_table.get_contract_table_count()
            for _ in range(count):
                contract_table.delete_contract_by_row(1)
                contract_table.click_dialog_confirm_button()
                assert main_topview.find_notification_content() == '操作成功'
            main_leftview.change_role('经纪人')
        log.info('删除房源客源相关合同，保证新建的唯一')
        main_leftview.click_contract_management_label()

    @allure.story("测试创建买卖合同，查看搜索结果用例")
    @pytest.mark.rent
    @pytest.mark.contract
    @pytest.mark.run(order=-4)
    @pytest.mark.dependency()
    @pytest.mark.flaky(reruns=5, reruns_delay=2)
    def test_001(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        contract_create_order = ContractCreateOrderPage(web_driver)

        contract_table.click_rent_contract_tab()
        contract_table.click_create_order_button()
        contract_create_order.choose_business_type('租赁')
        contract_create_order.input_house_code(house_info['house_code'])
        contract_create_order.click_get_house_info_button()
        contract_create_order.verify_house_info(house_info)
        contract_create_order.click_verify_house_button()
        assert main_topview.find_notification_content() == '房源信息校验通过！'
        contract_create_order.input_customer_code(customer_info['customer_code'])
        contract_create_order.click_get_customer_info_button()
        assert contract_create_order.get_customer_name() == customer_info['customer_name']
        contract_create_order.click_next_step_button()
        if ini.environment == 'sz' or ini.environment == 'ks':
            contract_create_order.choose_district_contract()
            contract_create_order.click_confirm_button_in_dialog()
        contract_create_order.input_contract_content(self.test_data, flag='租赁')
        contract_create_order.click_submit_button()
        assert main_topview.wait_notification_content_exist() == '提交成功'
        contract_table.click_rent_contract_tab()
        contract_table.click_reset_button()
        contract_table.input_house_code_search(house_info['house_code'])
        contract_table.input_customer_code_search(customer_info['customer_code'])
        contract_table.click_search_button()
        assert contract_table.get_contract_table_count() == 1
        main_upview.clear_all_title()
