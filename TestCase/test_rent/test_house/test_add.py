#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_add.py
@time: 2021/06/22
"""

import pytest
import allure
from common.readconfig import ini
from page_object.web.contract.tablepage import ContractTablePage
from page_object.web.house.detailpage import HouseDetailPage
from config.conf import cm
from utils.jsonutil import get_data
from page_object.web.main.upviewpage import MainUpViewPage
from page_object.web.main.topviewpage import MainTopViewPage
from page_object.web.main.leftviewpage import MainLeftViewPage
from page_object.web.house.tablepage import HouseTablePage
from page_object.web.house.addpage import HouseAddPage


@allure.feature("测试房源模块")
class TestAdd(object):

    json_file_path = cm.test_data_dir + "/test_rent/test_house/test_add.json"
    test_data = get_data(json_file_path)
    house_info = None

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)
        main_leftview.change_role('经纪人')
        main_upview = MainUpViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        contract_table = ContractTablePage(web_driver)
        self.house_info = house_table.get_house_status_by_db('租赁')  #验证房源是否存在
        if len(self.house_info) !=0:
            house_id = self.house_info[0][0]
            house_status = self.house_info[0][1]
            house_code = self.house_info[0][2]
            contract_no_list = contract_table.get_contract_no(house_id)
            if len(contract_no_list) != 0:  #执行删除合同操作
                main_leftview.change_role('超级管理员')
                main_leftview.click_contract_management_label()
                for contract_no in contract_no_list[0]:
                    contract_table.click_rent_contract_tab()
                    contract_table.input_contract_code_search(contract_no)
                    contract_table.click_search_button()
                    contract_table.delete_contract_by_row()
                    contract_table.tooltip_click_confirm_button()
            if house_status == 2:  # 执行转真操作
                house_type = house_table.get_house_type_in_pool(house_id, '租赁')
                table_name = house_table.get_tab_name(house_type)
                main_leftview.click_data_disk_label()
                house_table.click_rent_tab_in_data_disk()
                house_table.switch_house_type_tab(table_name)
                house_table.input_house_code_search(house_code)
                house_table.enter_rent_house_detail(house_code)
                house_detail.click_transfer_to_rent_btn()
                house_detail.transfer_house(ini.super_verify_code)
        yield
        main_upview.clear_all_title()

    @allure.story("测试新增租赁房源，查看搜索结果用例")
    @pytest.mark.rent
    @pytest.mark.house
    @pytest.mark.run(order=1)
    @pytest.mark.dependency()
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_001(self, web_driver):
        house_add = HouseAddPage(web_driver)
        house_table = HouseTablePage(web_driver)
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_leftview.click_all_house_label()
        house_table.click_rent_tab()  # 点击租赁标签
        if len(self.house_info) !=0:  #如房源已存在，不执行新增房源的操作
            assert True
        else:
            house_table.click_add_house_button()  # 点击新增房源按钮
            assert house_add.check_rent_radio()  # 判断新增界面委托类型的默认勾选
            house_add.input_property_address('租赁')  # 填写物业地址
            house_add.input_owner_info_and_house_info(self.test_data, '租赁')
            assert '新增成功' in main_topview.find_notification_content()
            assert house_table.get_house_code_by_db(flag='租赁') != ''
        house_code = house_table.get_house_code_by_db(flag='租赁')
        house_table.choose_estate_name_search(ini.house_community_name)  # 验证搜索
        house_table.choose_building_name_search(ini.house_building_id)
        house_table.click_search_button()
        res = house_table.house_code_in_house_list(house_code)
        assert res



