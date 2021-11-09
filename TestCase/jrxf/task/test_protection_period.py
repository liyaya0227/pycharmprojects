#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: test_protection_period.py
@date: 2021/11/8
"""
import allure
import pytest
import datetime
from case_service.jrxf.house.house_service import HouseService
from common.readconfig import ini
from common.readxml import ReadXml
from config.conf import cm
from page_object.jrxf.web.main.leftviewpage import MainLeftViewPage
from page_object.jrxf.web.main.upviewpage import MainUpViewPage
from page_object.jrxf.web.task.add_page import AddHouseTaskPage
from page_object.jrxf.web.task.table_page import HouseTaskTablePage
from utils.databaseutil import DataBaseUtil
from utils.jsonutil import get_data

task_sql = ReadXml("jrxf/task/task_sql")


@allure.feature("新房作业流程")
class TestProtectionPeriod(object):
    task_json_file_path = cm.test_data_dir + "/jrxf/task/test_house_task.json"
    json_file_path = cm.test_data_dir + "/jrxf/house/test_add.json"
    test_house_task_data = get_data(task_json_file_path)
    test_add_data = get_data(json_file_path)
    house_name = ''
    main_up_view = None
    main_left_view = None
    add_house_page = None
    house_table_page = None
    audit_house_page = None
    house_detail_page = None
    add_house_task_page = None
    house_task_table_page = None

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, xf_web_driver):
        house_service = HouseService(xf_web_driver)
        self.house_name = ini.house_community_name
        self.main_up_view = MainUpViewPage(xf_web_driver)
        self.main_left_view = MainLeftViewPage(xf_web_driver)
        self.add_house_task_page = AddHouseTaskPage(xf_web_driver)
        self.house_task_table_page = HouseTaskTablePage(xf_web_driver)
        self.main_left_view.change_role('平台管理员')
        house_service.prepare_house(self.test_add_data, self.house_name)  # 验证房源状态
        yield
        self.main_up_view.clear_all_title()

    @allure.step("进入楼盘作业列表")
    def enter_house_task_list(self, role_name, tab_name):
        self.main_up_view.clear_all_title()
        self.main_left_view.change_role(role_name)
        self.main_left_view.click_house_task_label()
        self.house_task_table_page.switch_tab_by_tab_name(tab_name)

    @allure.step("更新报备保护截止时间")
    def update_report_protect_end_time(self, report_no):
        time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        update_sql = task_sql.get_sql('custom_new_house_report', 'update_protect_end_time').format(time=time,
                                                                                                   report_no=report_no)
        DataBaseUtil('Xf My SQL', ini.xf_database_name).update_sql(update_sql)

    @allure.step("增加报备")
    def add_report(self, house_name):
        add_house_base_info_params = self.test_add_data['tc01_add_house_base_info'][0]
        house_info = self.house_name + ' - ' + add_house_base_info_params['country'] + add_house_base_info_params[
            'trade']
        self.main_left_view.click_house_task_label()
        self.house_task_table_page.delete_records(house_name)  # 删除已有报备
        self.house_task_table_page.click_add_report_btn()
        self.add_house_task_page.add_report(house_name, house_info)

    @allure.step("审核报备")
    def audit_report(self, house_name, record_no):
        self.enter_house_task_list('新房案场', '报备')
        self.house_task_table_page.search_records_by_name(house_name)
        self.house_task_table_page.click_view_report_btn(record_no)
        self.add_house_task_page.click_approved_btn()

    @allure.step("增加带看")
    def add_take_look(self, house_name, record_no, picture_path):
        self.enter_house_task_list('平台管理员', '带看')
        self.house_task_table_page.delete_records(house_name)  # 删除已有带看
        self.house_task_table_page.switch_tab_by_tab_name('报备')
        self.house_task_table_page.search_records_by_name(house_name)
        self.house_task_table_page.click_save_take_look_btn(record_no)
        self.add_house_task_page.save_take_look([cm.tmp_picture_file])

    @allure.step("审核带看")
    def audit_take_look(self, record_no):
        self.enter_house_task_list('新房案场', '带看')
        self.house_task_table_page.search_records_by_report_no(record_no)
        self.house_task_table_page.click_view_record_btn(record_no)
        self.add_house_task_page.click_approved_btn()

    @allure.step("更新带看保护截止时间")
    def update_take_look_protect_end_time(self, report_no):
        time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        update_sql = task_sql.get_sql('custom_new_house_take_look', 'update_protect_end_time'). \
            format(time=time, report_no=report_no)
        DataBaseUtil('Xf My SQL', ini.xf_database_name).update_sql(update_sql)

    @allure.story("测试报备保护期")
    @pytest.mark.run(order=3)
    def test_report_protection_period(self):
        self.add_report(self.house_name)  # 增加报备
        report_no = self.house_task_table_page.get_record_no_by_house_name(self.house_name)  # 获取报备编号
        self.audit_report(self.house_name, report_no)  # 新房案场审核报备
        self.update_report_protect_end_time(report_no)  # 更新数据库中报备保护截至时间
        self.enter_house_task_list('平台管理员', '报备')
        self.house_task_table_page.search_records_by_report_no(report_no)
        assert self.house_task_table_page.check_report_protection_period(report_no)

    @allure.story("测试带看保护期")
    @pytest.mark.run(order=3)
    def test_take_look_protection_period(self):
        self.add_report(self.house_name)  # 增加报备
        report_no = self.house_task_table_page.get_record_no_by_house_name(self.house_name)  # 获取报备编号
        self.audit_report(self.house_name, report_no)  # 新房案场审核报备
        self.add_take_look(self.house_name, report_no, [cm.tmp_picture_file])  # 录入带看
        self.audit_take_look(report_no)
        self.update_take_look_protect_end_time(report_no)
        self.enter_house_task_list('平台管理员', '带看')
        self.house_task_table_page.search_records_by_report_no(report_no)
        assert self.house_task_table_page.check_take_look_protection_period(report_no)





