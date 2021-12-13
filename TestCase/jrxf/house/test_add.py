#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: test_add.py
@time: 2021/10/14
"""
import allure
import pytest
from case_service.jrxf.house.house_service import HouseService
from common.readconfig import ini
from config.conf import cm
from page_object.jrgj.web.house.tablepage import HouseTablePage as GjHouseTablePage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage as GjMainLeftViewPage
from page_object.jrxf.web.house.add_page import AddHousePage
from page_object.jrxf.web.house.audit_page import AuditHousePage
from page_object.jrxf.web.house.table_page import HouseTablePage
from page_object.jrxf.web.main.leftviewpage import MainLeftViewPage
from utils.jsonutil import get_data

gl_xf_web_driver = None


@allure.feature("测试房源模块")
class TestAdd(object):
    json_file_path = cm.test_data_dir + "/jrxf/house/test_add.json"
    test_add_data = get_data(json_file_path)
    new_house_name = ini.new_house_name

    @pytest.fixture(scope="function", autouse=False)
    def check_house(self):
        house_service = HouseService(gl_xf_web_driver)
        house_info = self.house_table_page.get_house_info_by_db(self.new_house_name)
        if house_info != '':
            house_status = house_info['house_status']
            show_outside_status = house_info['show_outside_status']
            if house_status != '' and house_status != 4:
                house_service.check_house_state(self.test_add_data, self.new_house_name, house_status)
                house_info = self.house_table_page.get_house_info_by_db(self.new_house_name)
                show_outside_status = house_info['show_outside_status']
            self.main_left_view.click_house_management_label()  # 删除
            if show_outside_status == 0:
                self.house_table_page.click_uncoop_house_tab()
            else:
                self.house_table_page.click_coop_house_tab()
            self.house_table_page.search_unhandle_house(self.new_house_name)
            self.house_table_page.del_released_house(self.new_house_name)

    @pytest.fixture(scope="function", autouse=False)
    def house_prepare(self):
        house_service = HouseService(gl_xf_web_driver)
        house_service.check_current_role('平台管理员')
        house_service.prepare_house(self.test_add_data, self.new_house_name)  # 验证房源状态

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, xf_web_driver):
        global gl_xf_web_driver
        gl_xf_web_driver = xf_web_driver
        self.add_house_page = AddHousePage(gl_xf_web_driver)
        self.main_left_view = MainLeftViewPage(gl_xf_web_driver)
        self.house_table_page = HouseTablePage(gl_xf_web_driver)
        self.audit_house_page = AuditHousePage(gl_xf_web_driver)

    @allure.step("增加房源基础信息")
    def add_house_base_info(self, house_name):
        add_house_base_info_params = self.test_add_data['tc01_add_house_base_info'][0]
        add_house_base_info_params['house_name'] = house_name
        house_address_key = ini.environment + '_house_address'
        house_address = self.test_add_data[house_address_key][0]
        self.main_left_view.click_house_management_label()
        self.house_table_page.click_unhandle_house_tab()
        self.house_table_page.click_add_house_btn()
        self.add_house_page.add_house_base_info(house_address, **add_house_base_info_params)

    @allure.step("上传房源合同")
    def upload_house_contract(self, house_name):
        self.house_table_page.search_unhandle_house(house_name)
        self.house_table_page.click_edit_btn(house_name)  # 编辑房源
        self.add_house_page.click_follow_up_tab()  # 填写跟进信息
        self.add_house_page.add_follow_up()
        self.add_house_page.click_upload_contract_btn()  # 上传合同
        self.add_house_page.upload_contract([cm.tmp_picture_file])

    @allure.step("审核房源合同")
    def audit_house_contract(self, house_name):
        self.main_left_view.click_house_contract_audit_label()  # 审核合同
        self.house_table_page.search_contract_audit_records(house_name)
        self.house_table_page.click_audit_contract_btn(house_name)
        self.audit_house_page.audit_contract()

    @allure.step("上架房源")
    def release_house(self, house_name):
        # edit_house_base_info_params = self.test_add_data['tc01_edit_house_base_info'][0]
        contract_field_key = ini.environment + '_contract_field'
        contract_field_params = self.test_add_data[contract_field_key][0]
        contract_name = contract_field_params['contract_name']
        contract_phone = contract_field_params['contract_phone']
        self.main_left_view.click_house_management_label()
        self.house_table_page.click_unreleased_house_tab()
        self.house_table_page.search_unhandle_house(house_name)
        self.house_table_page.click_edit_unreleased_house_btn(house_name)  # 编辑房源
        self.add_house_page.input_house_preferential()
        self.add_house_page.add_customer_rules()  # 客户规则
        self.add_house_page.add_planning_info()  # 规划信息
        self.add_house_page.add_support_info()  # 配套信息
        self.add_house_page.add_contract(contract_name, contract_phone)  # 联系人
        self.add_house_page.add_incentive_policy()  # 激励政策
        self.add_house_page.click_save_btn()  # 保存详细信息

    @allure.step("审核上架房源")
    def audit_release_house(self, house_name):
        self.main_left_view.click_house_released_audit_label()  # 上架审核
        self.house_table_page.search_released_audit_records(house_name)
        self.house_table_page.click_audit_released_house_btn(house_name)
        self.audit_house_page.audit_release()

    @allure.step("获取合作楼盘数量")
    def get_coop_house_number(self, house_name):
        self.main_left_view.click_house_management_label()
        self.house_table_page.click_coop_house_tab()
        self.house_table_page.search_unhandle_house(house_name)
        house_number = self.house_table_page.get_search_result()
        return house_number

    @allure.story("增加并上架房源")
    @pytest.mark.house
    @pytest.mark.run(order=1)
    @pytest.mark.dependency()
    # @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_add_new_house(self, check_house):
        self.add_house_base_info(self.new_house_name)
        self.upload_house_contract(self.new_house_name)
        self.audit_house_contract(self.new_house_name)
        self.release_house(self.new_house_name)
        self.audit_release_house(self.new_house_name)
        house_number = self.get_coop_house_number(self.new_house_name)
        assert int(house_number) == 1

    @allure.story("房源数据同步")
    @pytest.mark.run(order=1)
    def test_house_data_synchronization(self, house_prepare, gj_web_driver):
        house_table = GjHouseTablePage(gj_web_driver)
        main_left_view = GjMainLeftViewPage(gj_web_driver)
        house_status, show_outside_status = self.house_table_page.get_house_info_by_db(self.new_house_name)  # 获取外网呈现状态
        main_left_view.change_role('超级管理员')
        main_left_view.click_all_house_label()
        house_table.click_new_tab()  # 点击新房tab
        if show_outside_status == 0:
            house_table.click_off_shelf_house_tab()
        house_table.input_building_name_search(self.new_house_name)
        house_table.click_search_button()
        #TODO 搜索功能有bug
        assert house_table.get_house_table_count() == 1




