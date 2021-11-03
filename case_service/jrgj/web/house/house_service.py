#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: house_service.py
@date: 2021/11/3 0003
"""
from config.conf import cm
from common.readconfig import ini
from page_object.jrgj.web.house.addpage import HouseAddPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.contract.tablepage import ContractTablePage
from utils.sqlutil import select_sql
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

    def check_house_for_contract(self, web_driver, flag='买卖'):
        house_info = self.get_house_info_by_db(flag=flag)
        if house_info:
            if house_info[1] in [1, 3]:  # 在售以及签约中
                self.delete_contract_by_house_code(web_driver, house_info[0], flag=flag)
            elif house_info[1] == 2:  # 在资料盘
                self.verify_house(web_driver, house_info[0], house_info[2], flag=flag)
            else:
                raise ValueError('房源该状态暂不支持')
        else:  # 没有该房源信息
            self.add_house(web_driver, flag=flag)

    @staticmethod
    def get_house_info_by_db(flag='买卖'):
        estate_sql = "select id from estate_new_base_info where [name]='" + ini.house_community_name + "'"
        estate_id = select_sql(estate_sql)[0][0]
        if flag == '买卖':
            house_sql = "select house_code,status,house_id from trade_house where location_estate_id='" \
                        + str(estate_id) + "' and location_building_number='" + ini.house_building_id + \
                        "' and location_building_cell='" + ini.house_building_cell + \
                        "' and location_floor='" + ini.house_floor + \
                        "' and location_doorplate='" + ini.house_doorplate + "' and is_valid='1' and [status]!='1'"
        elif flag == '租赁':
            house_sql = "select house_code,status,house_id from rent_house where location_estate_id='" \
                        + str(estate_id) + "' and location_building_number='" + ini.house_building_id + \
                        "' and location_building_cell='" + ini.house_building_cell + \
                        "' and location_floor='" + ini.house_floor + \
                        "' and location_doorplate='" + ini.house_doorplate + "' and is_valid='1' and [status]!='1'"
        else:
            raise "传值错误"
        try:
            return select_sql(house_sql)[0][0], select_sql(house_sql)[0][1]
        except IndexError:
            return None

    @staticmethod
    def delete_contract_by_house_code(web_driver, house_code, flag='买卖'):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        contract_table = ContractTablePage(web_driver)

        main_leftview.change_role('超级管理员')
        main_leftview.click_contract_management_label()
        if flag == '买卖':
            contract_table.click_sale_contract_tab()
        elif flag == '租赁':
            contract_table.click_rent_contract_tab()
        else:
            raise ValueError('传值错误')
        contract_table.input_house_code_search(house_code)
        contract_table.click_search_button()
        for _ in range(contract_table.get_contract_table_count()):
            contract_table.delete_contract_by_row(1)
            contract_table.tooltip_click_confirm_button()
            main_topview.close_notification()
        main_leftview.change_role('经纪人')

    @staticmethod
    def verify_house(web_driver, house_code, house_id, flag='买卖'):
        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)

        house_type = house_table.get_house_type_in_pool(house_id, flag)
        table_name = house_table.get_tab_name(house_type)
        main_leftview.click_data_disk_label()
        house_table.click_rent_tab_in_data_disk()
        house_table.switch_house_type_tab(table_name)
        house_table.input_house_code_search(house_code)
        house_table.enter_rent_house_detail(house_code)
        house_detail.click_transfer_to_rent_btn()
        house_detail.transfer_house(ini.super_verify_code)
        main_upview.clear_all_title()

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

