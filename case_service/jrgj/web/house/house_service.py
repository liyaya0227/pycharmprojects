#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: house_service.py
@date: 2021/11/3 0003
"""
from common.globalvar import GlobalVar
from common.readconfig import ini
from page_object.common.web.login.loginpage import LoginPage
from page_object.jrgj.web.house.addpage import HouseAddPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.contract.tablepage import ContractTablePage
from utils.logger import logger
from utils.sqlutil import select_sql


class HouseService(object):

    def __init__(self, web_driver):
        self.login_page = LoginPage(web_driver)
        self.main_up_view = MainUpViewPage(web_driver)
        self.main_top_view = MainTopViewPage(web_driver)
        self.main_left_view = MainLeftViewPage(web_driver)
        self.house_add_page = HouseAddPage(web_driver)
        self.house_table_page = HouseTablePage(web_driver)
        self.house_detail_page = HouseDetailPage(web_driver)
        self.contract_table_page = ContractTablePage(web_driver)

    def prepare_house(self, test_add_data, flag):
        flag_dist = {'sale': "买卖", 'rent': "租赁"}
        get_house_info_flg = flag_dist[flag]
        house_info = self.get_house_info_by_db(get_house_info_flg)
        if house_info is not None:
            contract_no_list = self.contract_table_page.get_contract_no(house_info[2])
            if len(contract_no_list) != 0:  # 删除合同
                self.delete_contract(contract_no_list)
            if house_info[1] == 2:  # 认领房源
                self.claim_house(house_info[2], house_info[0], flag)
        else:  # 新增房源
            self.add_house(test_add_data, flag)
        self.main_up_view.clear_all_title()
        self.check_current_role('经纪人')
        house_info = self.get_house_info_by_db(get_house_info_flg)
        return house_info

    @staticmethod
    def update_global_file(house_info, flag):
        """更新global文件"""
        if len(house_info) > 0:
            if flag == 'sale':
                GlobalVar.sale_house_id = str(house_info[2])
                GlobalVar.sale_house_code = house_info[0]
            elif flag == 'rent':
                GlobalVar.rent_house_id = str(house_info[2])
                GlobalVar.rent_house_code = house_info[0]
            else:
                GlobalVar.new_house_id = str(house_info[0])
        else:
            logger.info('暂无房源')

    def check_house_for_contract(self, flag='买卖'):
        house_info = self.get_house_info_by_db(flag)
        if house_info:
            if house_info[1] in [1, 3]:  # 在售以及签约中
                self.delete_contract_by_house_code(house_info[0], flag)
            elif house_info[1] == 2:  # 在资料盘
                self.verify_house(house_info[0], house_info[2], flag)
            else:
                raise ValueError('房源该状态暂不支持')
        else:  # 没有该房源信息
            self.add_house(flag)

    @staticmethod
    def get_house_info_by_db(flag='买卖'):
        estate_sql = "select id from estate_new_base_info where [name]='" + ini.house_community_name + "'"
        estate_id = select_sql(estate_sql)[0][0]
        if flag == '买卖':
            house_sql = "select house_code,status,id from trade_house where location_estate_id='" \
                        + str(estate_id) + "' and location_building_number='" + ini.house_building_id + \
                        "' and location_building_cell='" + ini.house_building_cell + \
                        "' and location_floor='" + ini.house_floor + \
                        "' and location_doorplate='" + ini.house_doorplate + "' and is_valid='1' and [status]!='1'"
        elif flag == '租赁':
            house_sql = "select house_code,status,id from rent_house where location_estate_id='" \
                        + str(estate_id) + "' and location_building_number='" + ini.house_building_id + \
                        "' and location_building_cell='" + ini.house_building_cell + \
                        "' and location_floor='" + ini.house_floor + \
                        "' and location_doorplate='" + ini.house_doorplate + "' and is_valid='1' and [status]!='1'"
        else:
            raise "传值错误"
        try:
            return select_sql(house_sql)[0][0], select_sql(house_sql)[0][1], select_sql(house_sql)[0][2]
        except IndexError:
            return None

    def delete_contract_by_house_code(self, house_code, flag='买卖'):
        # main_topview = MainTopViewPage(web_driver)
        # main_leftview = MainLeftViewPage(web_driver)
        # contract_table = ContractTablePage(web_driver)
        self.main_left_view.change_role('超级管理员')
        self.main_left_view.click_contract_management_label()
        if flag == '买卖':
            self.contract_table_page.click_sale_contract_tab()
        elif flag == '租赁':
            self.contract_table_page.click_rent_contract_tab()
        else:
            raise ValueError('传值错误')
        self.contract_table_page.input_house_code_search(house_code)
        self.contract_table_page.click_search_button()
        for _ in range(self.contract_table_page.get_contract_table_count()):
            self.contract_table_page.delete_contract_by_row(1)
            self.contract_table_page.tooltip_click_confirm_button()
            self.main_top_view.close_notification()
        self.main_left_view.change_role('经纪人')

    def verify_house(self, house_code, house_id, flag='买卖'):
        # main_upview = MainUpViewPage(web_driver)
        # main_leftview = MainLeftViewPage(web_driver)
        # house_table = HouseTablePage(web_driver)
        # house_detail = HouseDetailPage(web_driver)
        house_type = self.house_table_page.get_house_type_in_pool(house_id, flag)
        table_name = self.house_table_page.get_tab_name(house_type)
        self.main_left_view.click_data_disk_label()
        self.house_table_page.click_rent_tab_in_data_disk()
        self.house_table_page.switch_house_type_tab(table_name)
        self.house_table_page.input_house_code_search(house_code)
        self.house_table_page.enter_rent_house_detail(house_code)
        self.house_detail_page.click_transfer_to_rent_btn()
        self.house_detail_page.transfer_house(ini.super_verify_code)
        self.main_up_view.clear_all_title()

    def add_house(self, test_add_data, flag='sale'):
        self.main_left_view.click_all_house_label()
        if flag == 'sale':
            self.house_table_page.click_sale_tab()
        elif flag == 'rent':
            self.house_table_page.click_rent_tab()
        else:
            raise '传值错误'
        self.house_table_page.click_add_house_button()
        self.house_add_page.input_property_address(flag)  # 填写物业地址
        self.house_add_page.input_owner_info_and_house_info(test_add_data, flag)

    def check_house_state(self, house_info, flag):
        contract_no_list = self.contract_table_page.get_contract_no(house_info[2])
        if len(contract_no_list) != 0:  # 删除合同
            self.delete_contract(contract_no_list)
        else:
            logger.info('该房源暂无对应合同')
        if house_info[1] == 2:  # 认领房源
            self.claim_house(house_info[2], house_info[0], flag)
        else:
            logger.info('该房源不需认领')

    def delete_contract(self, contract_no_list):
        self.main_left_view.change_role('超级管理员')
        self.main_left_view.click_contract_management_label()
        for contract_no in contract_no_list[0]:
            self.contract_table_page.click_sale_contract_tab()
            self.contract_table_page.input_contract_code_search(contract_no)
            self.contract_table_page.click_search_button()
            self.contract_table_page.delete_contract_by_row()
            self.contract_table_page.tooltip_click_confirm_button()

    def claim_house(self, house_id, house_code, flag):  # 认领房源
        self.main_left_view.change_role('经纪人')
        house_type = self.house_table_page.get_house_type_in_pool(house_id, flag)
        table_name = self.house_table_page.get_tab_name(house_type)
        self.main_left_view.click_data_disk_label()
        if flag == 'sale':
            self.house_table_page.click_sale_tab_in_data_disk()
        elif flag == 'rent':
            self.house_table_page.click_rent_tab_in_data_disk()
        else:
            raise "传值错误"
        self.house_table_page.switch_house_type_tab(table_name)
        self.house_table_page.input_house_code_search(house_code)
        self.house_table_page.enter_sale_house_detail(ini.house_community_name)
        if flag == 'sale':
            self.house_detail_page.click_transfer_to_sale_btn()
        elif flag == 'rent':
            self.house_detail_page.click_transfer_to_rent_btn()
        else:
            raise "传值错误"
        self.house_detail_page.transfer_house(ini.super_verify_code)

    def check_current_role(self, expect_role_name):
        if expect_role_name not in self.main_left_view.get_current_role_name():
            self.main_left_view.change_role(expect_role_name)

    def enter_house_detail(self, house_code, flag):
        self.main_left_view.click_all_house_label()
        if flag == 'rent':
            self.house_table_page.click_rent_tab()
        self.house_table_page.input_house_code_search(house_code)
        for i in range(4):
            number = self.house_table_page.get_house_number()
            if int(number) > 0:
                self.house_detail_page.enter_house_detail()
                break
            else:
                self.house_table_page.click_search_button()

    def replace_house_maintainer(self, account, password, house_code, replace_account, flag):
        self.login_page.log_in(account, 'Autotest1')
        self.main_top_view.click_close_button()
        self.check_current_role('经纪人')
        self.enter_house_detail(house_code, flag)
        self.house_detail_page.replace_maintainer(replace_account)
        self.main_left_view.log_out()
        self.login_page.log_in(ini.user_account, ini.user_password)
        self.check_current_role('经纪人')
        self.enter_house_detail(house_code, flag)
