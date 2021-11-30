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
from common.readconfig import ini
from config.conf import cm
from page_object.jrxf.web.house.add_page import AddHousePage
from page_object.jrxf.web.house.audit_page import AuditHousePage
from page_object.jrxf.web.house.table_page import HouseTablePage
from page_object.jrxf.web.main.leftviewpage import MainLeftViewPage
from utils.jsonutil import get_data
from utils.logger import logger


@allure.feature("测试房源模块")
class TestAdd(object):
    json_file_path = cm.test_data_dir + "/jrxf/house/test_add.json"
    test_add_data = get_data(json_file_path)
    main_left_view = None
    add_house_page = None
    house_table_page = None
    audit_house_page = None

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, xf_web_driver):
        self.add_house_page = AddHousePage(xf_web_driver)
        self.main_left_view = MainLeftViewPage(xf_web_driver)
        self.house_table_page = HouseTablePage(xf_web_driver)
        self.audit_house_page = AuditHousePage(xf_web_driver)

    # @allure.step("验证房源状态")
    # def check_house_state(self, house_name):
    #     self.main_left_view.change_role('平台管理员')
    #     self.main_left_view.click_house_management_label()
    #     tab_list = ['待办楼盘菜单', '合作楼盘菜单', '合同审核菜单', '待上架楼盘菜单', '非合作楼盘菜单']
    #     for tab in tab_list:
    #         if tab == '待办楼盘菜单':
    #             self.house_table_page.click_unhandle_house_tab()
    #             house_number = int(self.house_table_page.get_house_number_by_name(house_name))
    #             if house_number >= 1:
    #                 self.self.house_table_page.del_unhandle_house(house_name)
    #                 break
    #         elif tab == '合作楼盘菜单':
    #             self.house_table_page.click_coop_house_tab()
    #             house_number = int(self.house_table_page.get_house_number_by_name(house_name))
    #             if house_number >= 1:
    #                 self.house_table_page.del_released_house(house_name)
    #                 break
    #         elif tab == '合同审核菜单':
    #             self.house_table_page.click_audit_house_contract_tab()
    #             house_number = int(self.house_table_page.get_house_number_by_name(house_name))
    #             if house_number >= 1:
    #                 if self.house_table_page.check_contract_approved_status():
    #                     pass
    #                 else:
    #                     if self.house_table_page.check_contract_audit_status():
    #                         self.audit_house_contract(house_name)
    #                         self.release_house(house_name)
    #                         self.audit_release_house(house_name)
    #                         self.main_left_view.click_house_management_label()  # 删除
    #                         self.house_table_page.click_coop_house_tab()
    #                         self.house_table_page.serch_released_audit_records(house_name)
    #                         self.house_table_page.del_released_house(house_name)
    #                         break
    #         elif tab == '待上架楼盘菜单':
    #             self.house_table_page.click_unreleased_house_tab()
    #             house_number = int(self.house_table_page.get_house_number_by_name(house_name))
    #             if house_number >= 1:
    #                 if self.house_table_page.check_release_approved_status():
    #                     pass
    #                 else:
    #                     if self.house_table_page.check_release_audit_status():
    #                         self.release_house(house_name)
    #                     self.audit_release_house(house_name)
    #                     self.main_left_view.click_house_management_label()  # 删除
    #                     self.house_table_page.click_coop_house_tab()
    #                     self.house_table_page.serch_unhandle_house(house_name)
    #                     self.house_table_page.del_released_house(house_name)
    #                     break

    @allure.step("验证房源状态")
    def check_house_state(self, house_name):
        self.main_left_view.change_role('平台管理员')
        self.main_left_view.click_house_management_label()
        house_status = self.house_table_page.get_house_status_by_db(house_name)
        if house_status:
            if house_status == 1:  # 待办
                self.house_table_page.serch_unhandle_house(house_name)
                self.self.house_table_page.del_unhandle_house(house_name)
            elif house_status == 2:  # 合同审核
                self.house_table_page.click_audit_house_contract_tab()
                self.house_table_page.serch_unhandle_house(house_name)
                if self.house_table_page.check_contract_audit_status(house_name):
                    self.audit_house_contract(house_name)
                    self.release_house(house_name)
                    self.audit_release_house(house_name)
                    self.main_left_view.click_house_management_label()  # 删除
                    self.house_table_page.click_coop_house_tab()
                    self.house_table_page.serch_released_audit_records(house_name)
                    self.house_table_page.del_released_house(house_name)
            elif house_status == 3:  # 待上架楼盘
                self.house_table_page.click_unreleased_house_tab()
                self.house_table_page.serch_unhandle_house(house_name)
                if self.house_table_page.check_release_audit_status(house_name):
                    self.release_house(house_name)
                self.audit_release_house(house_name)
                self.main_left_view.click_house_management_label()  # 删除
                self.house_table_page.click_coop_house_tab()
                self.house_table_page.serch_unhandle_house(house_name)
                self.house_table_page.del_released_house(house_name)
            elif house_status == 4:  # 合作楼盘
                self.house_table_page.click_coop_house_tab()
                self.house_table_page.serch_unhandle_house(house_name)
                self.house_table_page.del_released_house(house_name)
            elif house_status == 5:  # 非合作楼盘
                pass
            else:
                logger.info('不需要处理')

    @allure.step("增加房源基础信息")
    def add_house_base_info(self):
        add_house_base_info_params = self.test_add_data['tc01_add_house_base_info'][0]
        self.main_left_view.click_house_management_label()
        self.house_table_page.click_unhandle_house_tab()
        self.house_table_page.click_add_house_btn()
        self.add_house_page.add_house_base_info(**add_house_base_info_params)

    @allure.step("上传房源合同")
    def upload_house_contract(self, house_name):
        self.house_table_page.serch_unhandle_house(house_name)
        self.house_table_page.click_edit_btn(house_name)  # 编辑房源
        self.add_house_page.click_follow_up_tab()  # 填写跟进信息
        self.add_house_page.add_follow_up()
        self.add_house_page.click_upload_contract_btn()  # 上传合同
        self.add_house_page.upload_contract([cm.tmp_picture_file])

    @allure.step("审核房源合同")
    def audit_house_contract(self, house_name):
        self.main_left_view.click_house_contract_audit_label()  # 审核合同
        self.house_table_page.serch_contract_audit_records(house_name)
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
        self.house_table_page.serch_unhandle_house(house_name)
        self.house_table_page.click_edit_unreleased_house_btn(house_name)  # 编辑房源
        self.add_house_page.input_house_preferential()
        self.add_house_page.add_customer_rules()  # 客户规则
        self.add_house_page.add_planning_info()  # 规划信息
        self.add_house_page.add_support_info()  # 配套信息
        self.add_house_page.add_contract(contract_name, contract_phone)  # 联系人
        self.add_house_page.click_save_btn()  # 保存详细信息

    @allure.step("审核上架房源")
    def audit_release_house(self, house_name):
        self.main_left_view.click_house_released_audit_label()  # 上架审核
        self.house_table_page.serch_released_audit_records(house_name)
        self.house_table_page.click_audit_released_house_btn(house_name)
        self.audit_house_page.audit_release()

    @allure.step("获取合作楼盘数量")
    def get_coop_house_number(self, house_name):
        self.main_left_view.click_house_management_label()
        self.house_table_page.click_coop_house_tab()
        self.house_table_page.serch_unhandle_house(house_name)
        house_number = self.house_table_page.get_serch_result()
        return house_number

    @allure.story("增加并上架房源")
    @pytest.mark.house
    @pytest.mark.run(order=1)
    @pytest.mark.dependency()
    # @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_add_new_house(self):
        house_name = ini.house_community_name
        self.check_house_state(house_name)
        self.add_house_base_info()
        self.upload_house_contract(house_name)
        self.audit_house_contract(house_name)
        self.release_house(house_name)
        self.audit_release_house(house_name)
        house_number = self.get_coop_house_number(house_name)
        assert int(house_number) == 1
