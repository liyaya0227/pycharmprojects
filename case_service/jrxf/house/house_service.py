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
from utils.jsonutil import get_data
from utils.logger import log

gl_web_driver = None
add_house_page = None
main_left_view = None
house_table_page = None
audit_house_page = None


class HouseService(object):

    def check_house_state(self, xf_web_driver, house_name):
        global gl_web_driver, add_house_page, main_left_view, house_table_page, audit_house_page
        gl_web_driver = xf_web_driver
        add_house_page = AddHousePage(gl_web_driver)
        main_left_view = MainLeftViewPage(gl_web_driver)
        house_table_page = HouseTablePage(gl_web_driver)
        audit_house_page = AuditHousePage(gl_web_driver)

        main_left_view.click_house_management_label()
        house_status = house_table_page.get_house_status_by_db(house_name)
        if house_status:
            if house_status == 1:  # 待办
                house_table_page.serch_unhandle_house(house_name)
                house_table_page.del_unhandle_house(house_name)
            elif house_status == 2:  # 合同审核
                house_table_page.click_audit_house_contract_tab()
                house_table_page.serch_unhandle_house(house_name)
                if house_table_page.check_contract_audit_status(house_name):
                    print('审核合同')
                    self.audit_house_contract(house_name)
                    self.release_house(house_name)
                    self.audit_release_house(house_name)
            elif house_status == 3:  # 待上架楼盘
                house_table_page.click_unreleased_house_tab()
                house_table_page.serch_unhandle_house(house_name)
                if house_table_page.check_release_audit_status(house_name):
                    self.release_house(house_name)
                self.audit_release_house(house_name)
            elif house_status in [4, 5]:  # 合作楼盘、非合作楼盘
                log.info('不需要处理')
            else:
                log.info('不需要处理')

    @staticmethod
    def audit_house_contract(house_name):
        """审核合同"""
        main_left_view.click_house_contract_audit_label()  # 审核合同
        house_table_page.serch_contract_audit_records(house_name)
        house_table_page.click_audit_contract_btn(house_name)
        audit_house_page.audit_contract()

    @staticmethod
    def release_house(house_name):
        """上架房源"""
        json_file_path = cm.test_data_dir + "/jrxf/house/test_add.json"
        test_add_data = get_data(json_file_path)
        edit_house_base_info_params = test_add_data['tc01_edit_house_base_info'][0]
        contract_name = edit_house_base_info_params['contract_name']
        contract_phone = edit_house_base_info_params['contract_phone']
        main_left_view.click_house_management_label()
        house_table_page.click_unreleased_house_tab()
        house_table_page.serch_unhandle_house(house_name)
        house_table_page.click_edit_unreleased_house_btn(house_name)  # 编辑房源
        add_house_page.input_house_preferential()
        add_house_page.add_customer_rules()  # 客户规则
        add_house_page.add_planning_info()  # 规划信息
        add_house_page.add_support_info()  # 配套信息
        add_house_page.add_contract(contract_name, contract_phone)  # 联系人
        add_house_page.click_save_btn()  # 保存详细信息

    @staticmethod
    def audit_release_house(house_name):
        """审核上架房源"""
        main_left_view.click_house_released_audit_label()  # 上架审核
        house_table_page.serch_released_audit_records(house_name)
        house_table_page.click_audit_released_house_btn(house_name)
        audit_house_page.audit_release()
