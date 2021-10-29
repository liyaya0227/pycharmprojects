#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: house_service.py
@date: 2021/10/28
"""
from common.readconfig import ini
from config.conf import cm
from page_object.jrgj.web.contract.tablepage import ContractTablePage
from page_object.jrgj.web.house.addpage import HouseAddPage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from utils.jsonutil import get_data

gl_web_driver = None
main_left_view = None
house_add_page = None
house_table_page = None
house_detail_page = None
contract_table_page = None


class HouseService(object):
    json_file_path = cm.test_data_dir + "/jrgj/test_rent/test_house/test_add.json"
    test_data = get_data(json_file_path)

    def add_house(self, web_driver, flag='买卖'):
        global gl_web_driver, main_left_view, house_table_page, house_add_page
        gl_web_driver = web_driver
        main_left_view = MainLeftViewPage(gl_web_driver)
        house_add_page = HouseAddPage(gl_web_driver)
        house_table_page = HouseTablePage(gl_web_driver)
        main_left_view.click_all_house_label()
        if flag == 'sale':
            house_table_page.click_sale_tab()
        elif flag == 'rent':
            house_table_page.click_rent_tab()
        else:
            raise '传值错误'
        house_table_page.click_add_house_button()
        house_add_page.input_property_address(flag)  # 填写物业地址
        house_add_page.input_owner_info_and_house_info(self.test_data, flag)

    def check_house_state(self, web_driver, flag):
        global gl_web_driver, main_left_view, house_table_page, house_detail_page, contract_table_page
        gl_web_driver = web_driver
        main_left_view = MainLeftViewPage(web_driver)
        house_table_page = HouseTablePage(web_driver)
        house_detail_page = HouseDetailPage(web_driver)
        contract_table_page = ContractTablePage(web_driver)
        house_info = house_table_page.get_house_status_by_db(flag)  # 验证房源是否存在
        if len(house_info) != 0:
            house_id = house_info[0][0]
            house_status = house_info[0][1]
            house_code = house_info[0][2]
            contract_no_list = contract_table_page.get_contract_no(house_id)
            if len(contract_no_list) != 0:  # 删除合同
                self.delete_contract(contract_no_list)
            if house_status == 2:  # 认领房源
                self.claim_house(house_id, house_code, flag)
        return house_info

    @staticmethod
    def delete_contract(contract_no_list):
        main_left_view.change_role('超级管理员')
        main_left_view.click_contract_management_label()
        for contract_no in contract_no_list[0]:
            contract_table_page.click_sale_contract_tab()
            contract_table_page.input_contract_code_search(contract_no)
            contract_table_page.click_search_button()
            contract_table_page.delete_contract_by_row()
            contract_table_page.tooltip_click_confirm_button()

    @staticmethod
    def claim_house(house_id, house_code, flag):
        house_type = house_table_page.get_house_type_in_pool(house_id, flag)
        table_name = house_table_page.get_tab_name(house_type)
        main_left_view.click_data_disk_label()
        if flag == 'sale':
            house_table_page.click_sale_tab_in_data_disk()
        elif flag == 'rent':
            house_table_page.click_rent_tab_in_data_disk()
        else:
            raise "传值错误"
        house_table_page.switch_house_type_tab(table_name)
        house_table_page.input_house_code_search(house_code)
        house_table_page.enter_sale_house_detail(ini.house_community_name)
        if flag == 'sale':
            house_detail_page.click_transfer_to_sale_btn()
        elif flag == 'rent':
            house_detail_page.click_transfer_to_rent_btn()
        else:
            raise "传值错误"
        house_detail_page.transfer_house(ini.super_verify_code)
