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
from config.conf import cm
from common.readconfig import ini
from page_object.jrgj.web.contract.tablepage import ContractTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from utils.jsonutil import get_data
from page_object.jrgj.web.main.topviewpage import MainTopViewPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage
from page_object.jrgj.web.house.tablepage import HouseTablePage
from page_object.jrgj.web.house.addpage import HouseAddPage

driver = None


@allure.feature("测试房源模块")
class TestAdd(object):
    json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_add.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global driver
        driver = web_driver
        self.main_up_view = MainUpViewPage(web_driver)
        self.house_add_page = HouseAddPage(web_driver)
        self.house_detail_page = HouseDetailPage(web_driver)
        self.main_top_view = MainTopViewPage(web_driver)
        self.main_left_view = MainLeftViewPage(web_driver)
        self.contract_table = ContractTablePage(web_driver)
        self.house_table_page = HouseTablePage(web_driver)
        yield
        self.main_up_view.clear_all_title()

    @allure.step("验证房源状态")
    def check_house_state(self):
        self.house_info = self.house_table_page.get_house_status_by_db('买卖')  # 验证房源是否存在
        if len(self.house_info) != 0:
            house_id = self.house_info[0][0]
            house_status = self.house_info[0][1]
            house_code = self.house_info[0][2]
            contract_no_list = self.contract_table.get_contract_no(house_id)
            if len(contract_no_list) != 0:  # 执行删除合同操作
                self.main_left_view.change_role('超级管理员')
                self.main_left_view.click_contract_management_label()
                for contract_no in contract_no_list[0]:
                    self.contract_table.click_sale_contract_tab()
                    self.contract_table.input_contract_code_search(contract_no)
                    self.contract_table.click_search_button()
                    self.contract_table.delete_contract_by_row()
                    self.contract_table.tooltip_click_confirm_button()
            if house_status == 2:  # 执行转真操作
                house_type = self.house_table_page.get_house_type_in_pool(house_id, '买卖')
                table_name = self.house_table_page.get_tab_name(house_type)
                self.main_left_view.click_data_disk_label()
                self.house_table_page.click_sale_tab_in_data_disk()
                self.house_table_page.switch_house_type_tab(table_name)
                self.house_table_page.input_house_code_search(house_code)
                self.house_table_page.enter_sale_house_detail(ini.house_community_name)
                self.house_detail_page.click_transfer_to_sale_btn()
                self.house_detail_page.transfer_house(ini.super_verify_code)

    @allure.story("测试新增买卖房源，查看搜索结果用例")
    @pytest.mark.rent
    @pytest.mark.house
    @pytest.mark.run(order=1)
    @pytest.mark.dependency()
    # @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_add(self):
        self.check_house_state()
        self.main_left_view.click_all_house_label()
        self.house_table_page.click_sale_tab()  # 点击买卖标签
        if len(self.house_info) != 0:  # 如房源已存在，不执行新增房源的操作
            assert True
        else:
            self.house_table_page.click_add_house_button()  # 点击新增房源按钮
            assert self.house_add_page.check_sale_radio()  # 判断新增界面委托类型的默认勾选
            self.house_add_page.input_property_address('买卖')  # 填写物业地址
            self.house_add_page.input_owner_info_and_house_info(self.test_data, '买卖')
            assert '新增成功' in self.main_top_view.find_notification_content()
            house_code = self.house_table_page.get_house_code_by_db(flag='买卖')
            assert house_code != ''
        house_code = self.house_table_page.get_house_code_by_db(flag='买卖')
        self.house_table_page.choose_estate_name_search(ini.house_community_name)  # 验证搜索
        self.house_table_page.choose_building_name_search(ini.house_building_id)
        self.house_table_page.click_search_button()
        res = self.house_table_page.house_code_in_house_list(house_code)
        assert res
