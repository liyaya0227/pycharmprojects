#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: house_service.py
@date: 2021/10/25
"""
from config.conf import cm
from page_object.jrxf.web.house.add_page import AddHousePage
from page_object.jrxf.web.house.audit_page import AuditHousePage
from page_object.jrxf.web.house.table_page import HouseTablePage
from page_object.jrxf.web.main.leftviewpage import MainLeftViewPage
from utils.logger import logger


class HouseService(object):

    def __init__(self, xf_w_driver):
        self.add_house_page = AddHousePage(xf_w_driver)
        self.main_left_view = MainLeftViewPage(xf_w_driver)
        self.house_table_page = HouseTablePage(xf_w_driver)
        self.audit_house_page = AuditHousePage(xf_w_driver)

    def prepare_house(self, test_add_data, house_name):
        house_status = self.house_table_page.get_house_status_by_db(house_name)
        if house_status != '':
            self.check_house_state(house_name, house_status)
        else:
            self.add_house(test_add_data, house_name)

    def add_house(self, test_add_data, house_name):
        self.add_house_base_info(test_add_data)
        self.upload_house_contract(house_name)
        self.audit_house_contract(house_name)
        self.release_house(test_add_data, house_name)
        self.audit_release_house(house_name)

    def check_house_state(self, house_name, house_status):
        # self.main_left_view.click_house_management_label()
        if house_status:
            if house_status == 1:  # 待办
                self.main_left_view.click_house_management_label()
                self.house_table_page.serch_unhandle_house(house_name)
                self.house_table_page.del_unhandle_house(house_name)
            elif house_status == 2:  # 合同审核
                self.main_left_view.click_house_management_label()
                self.house_table_page.click_audit_house_contract_tab()
                self.house_table_page.serch_unhandle_house(house_name)
                if self.house_table_page.check_contract_audit_status(house_name):
                    self.audit_house_contract(house_name)
                    self.release_house(house_name)
                    self.audit_release_house(house_name)
            elif house_status == 3:  # 待上架楼盘
                self.main_left_view.click_house_management_label()
                self.house_table_page.click_unreleased_house_tab()
                self.house_table_page.serch_unhandle_house(house_name)
                if self.house_table_page.check_release_audit_status(house_name):
                    self.release_house(house_name)
                self.audit_release_house(house_name)
            elif house_status in [4, 5]:  # 合作楼盘、非合作楼盘
                logger.info('不需要处理')
            else:
                logger.info('不需要处理')
                logger.info('不需要处理')
        else:
            logger.info('暂无新房房源')

    def add_house_base_info(self, test_add_data):
        """增加房源基础信息"""
        add_house_base_info_params = test_add_data['tc01_add_house_base_info'][0]
        self.main_left_view.click_house_management_label()
        self.house_table_page.click_unhandle_house_tab()
        self.house_table_page.click_add_house_btn()
        self.add_house_page.add_house_base_info(**add_house_base_info_params)

    def upload_house_contract(self, house_name):
        """上传房源合同"""
        self.house_table_page.serch_unhandle_house(house_name)
        self.house_table_page.click_edit_btn(house_name)  # 编辑房源
        self.add_house_page.click_follow_up_tab()  # 填写跟进信息
        self.add_house_page.add_follow_up()
        self.add_house_page.click_upload_contract_btn()  # 上传合同
        self.add_house_page.upload_contract([cm.tmp_picture_file])

    def audit_house_contract(self, house_name):
        """审核合同"""
        self.main_left_view.click_house_contract_audit_label()  # 审核合同
        self.house_table_page.serch_contract_audit_records(house_name)
        self.house_table_page.click_audit_contract_btn(house_name)
        self.audit_house_page.audit_contract()

    def release_house(self, test_add_data, house_name):
        """上架房源"""
        edit_house_base_info_params = test_add_data['tc01_edit_house_base_info'][0]
        contract_name = edit_house_base_info_params['contract_name']
        contract_phone = edit_house_base_info_params['contract_phone']
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

    def audit_release_house(self, house_name):
        """审核上架房源"""
        self.main_left_view.click_house_released_audit_label()  # 上架审核
        self.house_table_page.serch_released_audit_records(house_name)
        self.house_table_page.click_audit_released_house_btn(house_name)
        self.audit_house_page.audit_release()
