#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: test_house_task.py
@date: 2021/11/30
"""
import allure
import pytest
from case_service.jrxf.house.house_service import HouseService
from common.readconfig import ini
from config.conf import cm
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage as GjMainLeftViewPage
from page_object.jrgj.web.main.upviewpage import MainUpViewPage as GjMainUpViewPage
from page_object.jrgj.web.task.add_page import AddHouseTaskPage as GjAddHouseTaskPage
from page_object.jrgj.web.task.table_page import HouseTaskTablePage
from page_object.jrxf.web.main.leftviewpage import MainLeftViewPage as XfMainLeftViewPage
from page_object.jrxf.web.main.upviewpage import MainUpViewPage as XfMainUpViewPage
from page_object.jrxf.web.task.add_page import AddHouseTaskPage as XfAddHouseTaskPage
from page_object.jrxf.web.task.table_page import HouseTaskTablePage as XfHouseTaskTablePage
from utils.jsonutil import get_data

gl_xf_web_driver = None
gl_gj_web_driver = None


@allure.feature("新房作业流程模块")
class TestBusinessProcesses(object):
    task_json_file_path = cm.test_data_dir + "/jrxf/task/test_house_task.json"
    json_file_path = cm.test_data_dir + "/jrxf/house/test_add.json"
    test_house_task_data = get_data(task_json_file_path)
    test_add_data = get_data(json_file_path)
    house_name = ini.new_house_name

    @pytest.fixture(scope="class", autouse=True)
    def check_house(self, xf_web_driver, web_driver):
        global gl_xf_web_driver, gl_gj_web_driver
        gl_gj_web_driver = web_driver
        gl_xf_web_driver = xf_web_driver
        json_file_path = cm.test_data_dir + "/jrxf/house/test_add.json"
        test_add_data = get_data(json_file_path)
        house_service = HouseService(gl_xf_web_driver)
        self.xf_main_left_view = XfMainLeftViewPage(gl_gj_web_driver)
        house_service.check_current_role('平台管理员')
        house_service.prepare_house(test_add_data, self.house_name)  # 验证房源状态

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self):
        self.gj_main_up_view = GjMainUpViewPage(gl_gj_web_driver)
        self.gj_main_left_view = GjMainLeftViewPage(gl_gj_web_driver)
        self.gj_add_house_task_page = GjAddHouseTaskPage(gl_gj_web_driver)
        self.gj_house_task_table_page = HouseTaskTablePage(gl_gj_web_driver)
        # self.gj_main_up_view = GjMainUpViewPage(gl_gj_web_driver)
        self.xf_main_left_view = XfMainLeftViewPage(gl_xf_web_driver)
        self.xf_add_house_task_page = XfAddHouseTaskPage(gl_xf_web_driver)
        self.xf_house_task_table_page = XfHouseTaskTablePage(gl_xf_web_driver)
        yield
        # self.gj_main_up_view.clear_all_title()

    # @allure.step("进入楼盘作业列表")
    # def enter_house_task_list(self, role_name, tab_name):
    #     self.main_up_view.clear_all_title()
    #     self.main_left_view.change_role(role_name)
    #     self.main_left_view.click_new_house_operation_label()
    #     self.house_task_table_page.switch_tab_by_tab_name(tab_name)

    @allure.step("增加报备")
    def add_report(self, house_name):
        add_house_base_info_params = self.test_add_data['tc01_add_house_base_info'][0]
        house_info = self.house_name + ' - ' + add_house_base_info_params['country'] + add_house_base_info_params[
            'trade']
        self.gj_main_left_view.check_current_role('超级管理员')
        self.gj_main_left_view.click_new_house_operation_label()
        self.gj_house_task_table_page.delete_records(house_name)  # 删除已有报备
        self.gj_house_task_table_page.click_add_report_btn()
        self.gj_add_house_task_page.add_report(house_name, house_info)

    @allure.step("新房案场审核报备")
    def audit_report(self, record_no):
        self.xf_main_left_view.check_current_role('新房案场')
        self.xf_main_left_view.click_house_task_label()
        self.xf_house_task_table_page.search_records_by_report_no(record_no)
        self.xf_house_task_table_page.click_view_report_btn(record_no)
        self.xf_add_house_task_page.click_approved_btn()

    @allure.step("增加带看")
    def add_take_look(self, house_name, record_no, picture_path):
        self.gj_house_task_table_page.switch_tab_by_tab_name('带看')
        self.gj_house_task_table_page.delete_records(house_name)  # 删除已有带看
        self.gj_house_task_table_page.switch_tab_by_tab_name('报备')
        self.gj_house_task_table_page.search_records_by_report_no(record_no)
        self.gj_house_task_table_page.click_save_take_look_btn(record_no)
        self.gj_add_house_task_page.save_take_look([cm.tmp_picture_file])

    @allure.step("新房案场审核带看")
    def audit_take_look(self, record_no):
        self.xf_house_task_table_page.switch_tab_by_tab_name('带看')
        self.xf_house_task_table_page.search_records_by_report_no(record_no)
        self.xf_house_task_table_page.click_view_record_btn(record_no)
        self.xf_add_house_task_page.click_approved_btn()

    @allure.step("增加认购")
    def save_subscribe(self, house_name, record_no, picture_path):
        save_subscribe_params = self.test_house_task_data['tc01_save_subscribe'][0]
        save_subscribe_params['picture_path'] = picture_path
        self.gj_house_task_table_page.switch_tab_by_tab_name('认购')
        self.gj_house_task_table_page.delete_records(house_name)  # 删除已有认购
        self.gj_house_task_table_page.switch_tab_by_tab_name('带看')
        self.gj_house_task_table_page.search_records_by_report_no(record_no)
        self.gj_house_task_table_page.click_save_subscribe_btn(record_no)
        self.gj_add_house_task_page.save_subscribe(**save_subscribe_params)

    @allure.step("新房案场审核认购")
    def audit_subscribe(self, record_no):
        audit_subscribe_params = self.test_house_task_data['tc01_audit_subscribe'][0]
        self.xf_house_task_table_page.switch_tab_by_tab_name('认购')
        self.xf_house_task_table_page.search_records_by_report_no(record_no)
        self.xf_house_task_table_page.click_view_record_btn(record_no)
        self.xf_add_house_task_page.audit_subscribe(**audit_subscribe_params)

    # @allure.step("上传草网签")
    # def upload_sign(self, house_name, record_no):
    #     self.house_task_table_page.search_records_by_report_no(record_no)
    #     self.house_task_table_page.click_upload_sign_btn(record_no)
    #     self.add_house_task_page.upload_sign(100, 100)
    #
    # @allure.step("审核草网签")
    # def audit_sign(self, report_no):
    #     self.enter_house_task_list('平台管理员', '草网签')
    #     self.house_task_table_page.search_records_by_report_no(report_no)
    #     self.house_task_table_page.click_view_record_btn(report_no)
    #     self.add_house_task_page.click_approved_btn()
    #
    # @allure.step("录入成销")
    # def save_sell(self, report_no, picture_path):
    #     self.house_task_table_page.search_records_by_report_no(report_no)
    #     self.house_task_table_page.click_save_cell_btn(report_no)
    #     self.add_house_task_page.save_sell(picture_path)
    #
    # @allure.step("审核成销")
    # def audit_cell(self, report_no):
    #     self.enter_house_task_list('平台管理员', '成销')
    #     self.house_task_table_page.search_records_by_report_no(report_no)
    #     self.house_task_table_page.click_view_record_btn(report_no)
    #     self.add_house_task_page.click_approved_btn()

    @allure.story("测试楼盘作业流程")
    @pytest.mark.run(order=2)
    def test_house_task(self):
        self.add_report(self.house_name)  # 增加报备
        report_list = self.gj_house_task_table_page.get_records_ele_by_house_name(self.house_name)
        assert len(report_list) == 1  # 校验增加报备成功
        report_no = self.gj_house_task_table_page.get_record_no_by_house_name(self.house_name)  # 获取报备编号
        self.audit_report(report_no)  # 新房案场审核报备
        self.gj_house_task_table_page.search_records_by_report_no(report_no)
        assert self.gj_house_task_table_page.check_report_records_approved(report_no)  # 校验报备审核成功
        self.add_take_look(self.house_name, report_no, [cm.tmp_picture_file])  # 录入带看
        self.gj_house_task_table_page.switch_tab_by_tab_name('带看')
        self.gj_house_task_table_page.search_records_by_report_no(report_no)
        assert self.gj_house_task_table_page.check_records_to_be_reviewed(report_no)  # 校验增加带看成功
        self.audit_take_look(report_no)  # 新房案场审核带看
        self.gj_house_task_table_page.search_records_by_report_no(report_no)
        assert self.gj_house_task_table_page.check_records_approved(report_no)  # 校验带看审核成功
        self.save_subscribe(self.house_name, report_no, [cm.tmp_picture_file])  # 增加认购
        self.gj_house_task_table_page.switch_tab_by_tab_name('认购')
        self.gj_house_task_table_page.search_records_by_report_no(report_no)
        assert self.gj_house_task_table_page.check_records_to_be_reviewed(report_no)  # 校验增加认购成功
        self.audit_subscribe(report_no)  # 新房案场审核认购
        self.gj_house_task_table_page.search_records_by_report_no(report_no)
        assert self.gj_house_task_table_page.check_records_approved(report_no)  # 校验认购审核成功
        # self.upload_sign(self.house_name, report_no)  # 新房案场上传草签
        # self.house_task_table_page.switch_tab_by_tab_name('草网签')
        # self.house_task_table_page.search_records_by_report_no(report_no)
        # self.house_task_table_page.search_records_by_report_no(report_no)
        # assert self.house_task_table_page.check_records_to_be_reviewed(report_no)
        # self.audit_sign(report_no)  # 超管审核草网签
        # self.house_task_table_page.search_records_by_report_no(report_no)
        # assert self.house_task_table_page.check_records_approved(report_no)  # 校验草签审核成功
        # self.save_sell(report_no, [cm.tmp_picture_file])  # 新房案场录入成销
        # self.house_task_table_page.switch_tab_by_tab_name('成销')
        # self.house_task_table_page.search_records_by_report_no(report_no)
        # self.house_task_table_page.search_records_by_report_no(report_no)
        # assert self.house_task_table_page.check_records_to_be_reviewed(report_no)
        # self.audit_cell(report_no)  # 审核成销
        # self.house_task_table_page.switch_tab_by_tab_name('成销')
        # self.house_task_table_page.search_records_by_report_no(report_no)
        # assert self.house_task_table_page.check_records_approved(report_no)  # 校验成销审核成功
