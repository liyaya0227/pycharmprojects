#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: test_add_house_info.py
@date: 2021/11/3
"""
import allure
import pytest
from selenium import webdriver
from case_service.jrxf.house.house_service import HouseService
from common.readconfig import ini
from config.conf import cm
from page_object.common.web.login.loginpage import LoginPage
from page_object.jrxf.web.main.leftviewpage import MainLeftViewPage
from page_object.jrxf.web.main.upviewpage import MainUpViewPage
from page_object.jrxf.web.task.add_page import AddHouseTaskPage
from page_object.jrxf.web.task.table_page import HouseTaskTablePage
from utils.jsonutil import get_data

gl_house_address = ''
gl_xf_web_driver = None
gl_xf_operators_driver = None


@allure.feature("新房作业流程模块")
class TestBusinessProcesses(object):
    task_json_file_path = cm.test_data_dir + "/jrxf/task/test_house_task.json"
    json_file_path = cm.test_data_dir + "/jrxf/house/test_add.json"
    test_house_task_data = get_data(task_json_file_path)
    test_add_data = get_data(json_file_path)
    new_house_name = ini.new_house_name

    @pytest.fixture(scope='class', autouse=True)
    def xf_operators_login(self):
        global gl_xf_operators_driver
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": cm.tmp_dir,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'load-extension'])
        gl_xf_operators_driver = webdriver.Chrome(options=chrome_options)
        gl_xf_operators_driver.maximize_window()
        gl_xf_operators_driver.get(ini.xf_url)
        login_page = LoginPage(gl_xf_operators_driver)
        login_page.log_in(ini.xf_user_account, ini.xf_user_password)
        yield gl_xf_operators_driver
        main_left_view = MainLeftViewPage(gl_xf_operators_driver)
        main_left_view.log_out()
        gl_xf_operators_driver.quit()

    @pytest.fixture(scope="class", autouse=True)
    def check_house(self, xf_web_driver):
        global gl_xf_web_driver, gl_house_address
        gl_xf_web_driver = xf_web_driver
        house_service = HouseService(gl_xf_web_driver)
        house_service.check_current_role('平台管理员')
        gl_house_address = house_service.prepare_house(self.test_add_data, self.new_house_name)  # 验证房源状态

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self):
        self.main_up_view = MainUpViewPage(gl_xf_web_driver)
        self.main_left_view = MainLeftViewPage(gl_xf_web_driver)
        self.add_house_task_page = AddHouseTaskPage(gl_xf_web_driver)
        self.house_task_table_page = HouseTaskTablePage(gl_xf_web_driver)
        yield
        self.main_up_view.clear_all_title()

    @pytest.fixture(scope="function", autouse=True)
    def test_operators_prepare(self):
        self.operators_main_up_view = MainUpViewPage(gl_xf_operators_driver)
        self.operators_main_left_view = MainLeftViewPage(gl_xf_operators_driver)
        self.operators_add_house_task_page = AddHouseTaskPage(gl_xf_operators_driver)
        self.operators_house_task_table_page = HouseTaskTablePage(gl_xf_operators_driver)
        yield
        self.main_up_view.clear_all_title()

    @allure.step("进入楼盘作业列表")
    def enter_house_task_list(self, role_name, tab_name):
        self.main_up_view.clear_all_title()
        self.main_left_view.change_role(role_name)
        self.main_left_view.click_house_task_label()
        self.house_task_table_page.switch_tab_by_tab_name(tab_name)

    @allure.step("进入楼盘作业列表")
    def operators_enter_house_task_list(self, role_name, tab_name):
        self.operators_main_up_view.clear_all_title()
        self.operators_main_left_view.change_role(role_name)
        self.operators_main_left_view.click_house_task_label()
        self.operators_house_task_table_page.switch_tab_by_tab_name(tab_name)

    @allure.step("增加报备")
    def add_report(self, house_name):
        self.operators_main_left_view.change_role('经纪人')
        house_info = house_name + ' - ' + gl_house_address
        self.enter_house_task_list('平台管理员', '报备')
        self.house_task_table_page.delete_records(house_name)  # 删除已有报备
        self.operators_main_left_view.click_house_task_label()
        self.operators_house_task_table_page.click_add_report_btn()
        self.operators_add_house_task_page.add_report(house_name, house_info)

    @allure.step("审核报备")
    def audit_report(self, house_name, record_no):
        self.enter_house_task_list('新房案场', '报备')
        self.house_task_table_page.search_records_by_name(house_name)
        self.house_task_table_page.click_view_report_btn(record_no)
        self.add_house_task_page.click_approved_btn()

    @allure.step("增加带看")
    def add_take_look(self, house_name, record_no, picture_path):
        # self.enter_house_task_list('平台管理员', '带看')
        self.operators_house_task_table_page.switch_tab_by_tab_name('带看')
        self.operators_house_task_table_page.delete_records(house_name)  # 删除已有带看
        self.operators_house_task_table_page.switch_tab_by_tab_name('报备')
        self.operators_house_task_table_page.search_records_by_name(house_name)
        self.operators_house_task_table_page.click_save_take_look_btn(record_no)
        self.operators_add_house_task_page.save_take_look([cm.tmp_picture_file])

    @allure.step("审核带看")
    def audit_take_look(self, house_name, record_no):
        # self.enter_house_task_list('新房案场', '带看')
        self.house_task_table_page.switch_tab_by_tab_name('带看')
        self.house_task_table_page.search_records_by_report_no(record_no)
        self.house_task_table_page.click_view_record_btn(record_no)
        self.add_house_task_page.click_approved_btn()

    @allure.step("增加认购")
    def save_subscribe(self, house_name, record_no, picture_path):
        save_subscribe_params = self.test_house_task_data['tc01_save_subscribe'][0]
        save_subscribe_params['picture_path'] = picture_path
        self.operators_house_task_table_page.switch_tab_by_tab_name('认购')
        self.operators_house_task_table_page.delete_records(house_name)  # 删除已有认购
        self.operators_house_task_table_page.switch_tab_by_tab_name('带看')
        self.operators_house_task_table_page.search_records_by_report_no(record_no)
        self.operators_house_task_table_page.click_save_subscribe_btn(record_no)
        self.operators_add_house_task_page.save_subscribe(**save_subscribe_params)

    @allure.step("审核认购")
    def audit_subscribe(self, house_name, record_no):
        audit_subscribe_params = self.test_house_task_data['tc01_audit_subscribe'][0]
        self.house_task_table_page.switch_tab_by_tab_name('认购')
        self.house_task_table_page.search_records_by_report_no(record_no)
        self.house_task_table_page.click_view_record_btn(record_no)
        self.add_house_task_page.audit_subscribe(**audit_subscribe_params)

    @allure.step("上传草网签")
    def upload_sign(self, house_name, record_no):
        self.house_task_table_page.search_records_by_report_no(record_no)
        self.house_task_table_page.click_upload_sign_btn(record_no)
        self.add_house_task_page.upload_sign(100, 100)

    @allure.step("审核草网签")
    def audit_sign(self, report_no):
        self.enter_house_task_list('平台管理员', '草网签')
        self.house_task_table_page.search_records_by_report_no(report_no)
        self.house_task_table_page.click_view_record_btn(report_no)
        self.add_house_task_page.click_approved_btn()

    @allure.step("录入成销")
    def save_sell(self, report_no, picture_path):
        self.house_task_table_page.search_records_by_report_no(report_no)
        self.house_task_table_page.click_save_cell_btn(report_no)
        self.add_house_task_page.save_sell(picture_path)

    @allure.step("审核成销")
    def audit_cell(self, report_no):
        self.enter_house_task_list('平台管理员', '成销')
        self.house_task_table_page.search_records_by_report_no(report_no)
        self.house_task_table_page.click_view_record_btn(report_no)
        self.add_house_task_page.click_approved_btn()

    @allure.story("测试楼盘作业流程")
    @pytest.mark.run(order=3)
    def test_house_task(self):
        self.add_report(self.new_house_name)  # 增加报备
        self.house_task_table_page.search_records_by_name(self.new_house_name)
        report_list = self.house_task_table_page.get_records_ele_by_house_name(self.new_house_name)
        assert len(report_list) == 1  # 经纪人校验增加报备成功
        report_no = self.house_task_table_page.get_record_no_by_house_name(self.new_house_name)  # 获取报备编号
        self.audit_report(self.new_house_name, report_no)  # 新房案场审核报备
        self.operators_house_task_table_page.search_records_by_report_no(report_no)
        assert self.operators_house_task_table_page.check_report_records_approved(report_no)  # 经纪人校验报备审核成功
        self.add_take_look(self.new_house_name, report_no, [cm.tmp_picture_file])  # 录入带看
        self.operators_house_task_table_page.switch_tab_by_tab_name('带看')
        self.operators_house_task_table_page.search_records_by_report_no(report_no)
        assert self.operators_house_task_table_page.check_records_to_be_reviewed(report_no)
        self.audit_take_look(self.new_house_name, report_no)  # 新房案场审核带看
        self.operators_house_task_table_page.search_records_by_report_no(report_no)
        assert self.operators_house_task_table_page.check_records_approved(report_no)  # 校验带看审核成功
        self.save_subscribe(self.new_house_name, report_no, [cm.tmp_picture_file])  # 增加认购
        self.operators_house_task_table_page.switch_tab_by_tab_name('认购')
        self.operators_house_task_table_page.search_records_by_report_no(report_no)
        assert self.operators_house_task_table_page.check_records_to_be_reviewed(report_no)
        self.audit_subscribe(self.new_house_name, report_no)  # 新房案场审核认购
        self.operators_house_task_table_page.search_records_by_report_no(report_no)
        assert self.operators_house_task_table_page.check_records_approved(report_no)  # 经纪人校验认购审核成功
        self.upload_sign(self.new_house_name, report_no)  # 新房案场上传草签
        self.house_task_table_page.switch_tab_by_tab_name('草网签')
        self.house_task_table_page.search_records_by_report_no(report_no)
        self.house_task_table_page.search_records_by_report_no(report_no)
        assert self.house_task_table_page.check_records_to_be_reviewed(report_no)
        self.audit_sign(report_no)  # 超管审核草网签
        self.house_task_table_page.search_records_by_report_no(report_no)
        assert self.house_task_table_page.check_records_approved(report_no)  # 校验草签审核成功
        self.save_sell(report_no, [cm.tmp_picture_file])  # 新房案场录入成销
        self.house_task_table_page.switch_tab_by_tab_name('成销')
        self.house_task_table_page.search_records_by_report_no(report_no)
        self.house_task_table_page.search_records_by_report_no(report_no)
        assert self.house_task_table_page.check_records_to_be_reviewed(report_no)
        self.audit_cell(report_no)  # 审核成销
        self.house_task_table_page.switch_tab_by_tab_name('成销')
        self.house_task_table_page.search_records_by_report_no(report_no)
        assert self.house_task_table_page.check_records_approved(report_no)  # 校验成销审核成功
