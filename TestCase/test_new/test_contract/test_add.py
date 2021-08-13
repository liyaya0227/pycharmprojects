#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_add.py
@date: 2021/7/20 0020
"""

import pytest
import allure

from common.readconfig import ini
from utils.logger import log
from config.conf import cm
from utils.jsonutil import get_data
from page_object.main.topviewpage import MainTopViewPage
from page_object.main.leftviewpage import MainLeftViewPage
from page_object.main.upviewpage import MainUpViewPage
from page_object.customer.detailpage import CustomerDetailPage
from page_object.customer.tablepage import CustomerTablePage
from page_object.newhouseoperation.tablepage import NewHouseOperationTablePage

customer_info = {}


@allure.feature("测试新房作业模块")
class TestAdd(object):

    json_file_path = cm.test_data_dir + "/test_new/test_contract/test_add.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="class", autouse=True)
    def test_prepare(self, web_driver):
        global customer_info

        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        customer_table = CustomerTablePage(web_driver)
        customer_detail = CustomerDetailPage(web_driver)

        main_leftview.change_role('经纪人')
        if self.test_data['客户联系方式'][0] == '' and self.test_data['客户联系方式'][1] == '':
            main_leftview.click_my_customer_label()
            customer_table.click_all_tab()
            customer_table.choose_customer_wish('不限')
            customer_table.input_search_text(ini.custom_telephone)
            customer_table.click_search_button()
            assert customer_table.get_customer_table_count() == 1
            customer_table.go_customer_detail_by_row(1)
            customer_info['customer_name'] = customer_detail.get_customer_name()
            customer_info['customer_phone'] = ini.custom_telephone
            main_upview.clear_all_title()
        else:
            customer_info['customer_name'] = self.test_data['客户联系方式'][0]
            customer_info['customer_phone'] = self.test_data['客户联系方式'][1]
        log.info('获取客户联系方式')
        main_leftview.click_new_house_operation_label()

    @allure.story("测试新增新房楼盘，查看搜索结果用例")
    @pytest.mark.new
    @pytest.mark.house
    @pytest.mark.run(order=2)
    @pytest.mark.dependency()
    @pytest.mark.flaky(reruns=5, reruns_delay=2)
    def test_001(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        new_house_operation_table = NewHouseOperationTablePage(web_driver)

        new_house_operation_table.click_report_tab()  # 点击报备tab
        new_house_operation_table.input_building_name_search(self.test_data['楼盘信息'])
        new_house_operation_table.input_customer_phone_search(customer_info['customer_phone'])
        new_house_operation_table.click_search_button()
        table_count = new_house_operation_table.get_table_count()
        if table_count != 0:
            log.info('已存在相同客户，进行删除操作')
            main_leftview.change_role('超级管理员')
            main_leftview.click_new_house_operation_label()
            new_house_operation_table.click_report_tab()  # 点击报备tab
            new_house_operation_table.input_building_name_search(self.test_data['楼盘信息'])
            new_house_operation_table.input_customer_phone_search(customer_info['customer_phone'])
            new_house_operation_table.click_search_button()
            if new_house_operation_table.get_table_count() != 0:
                new_house_operation_table.delete_report_by_row(1)
                new_house_operation_table.dialog_click_delete_button()
                assert main_topview.find_notification_content() == '删除成功'
            new_house_operation_table.click_take_look_tab()
            new_house_operation_table.input_building_name_search(self.test_data['楼盘信息'])
            new_house_operation_table.input_customer_phone_search(customer_info['customer_phone'])
            new_house_operation_table.click_search_button()
            if new_house_operation_table.get_table_count() != 0:
                new_house_operation_table.delete_report_by_row(1)
                new_house_operation_table.dialog_click_delete_button()
                assert main_topview.find_notification_content() == '删除成功'
            new_house_operation_table.click_subscription_tab()
            new_house_operation_table.input_building_name_search(self.test_data['楼盘信息'])
            new_house_operation_table.input_customer_phone_search(customer_info['customer_phone'])
            new_house_operation_table.click_search_button()
            if new_house_operation_table.get_table_count() != 0:
                new_house_operation_table.delete_report_by_row(1)
                new_house_operation_table.dialog_click_delete_button()
                assert main_topview.find_notification_content() == '删除成功'
            main_leftview.change_role('经纪人')
            main_leftview.click_new_house_operation_label()
            new_house_operation_table.click_report_tab()
        new_house_operation_table.click_add_button()
        new_house_operation_table.dialog_input_building_info(self.test_data['楼盘信息'])
        new_house_operation_table.dialog_input_customer_info(customer_info)
        new_house_operation_table.dialog_input_expect_arrive_time(self.test_data['预计到访时间'])
        new_house_operation_table.dialog_input_remark(self.test_data['备注'])
        new_house_operation_table.dialog_click_confirm_button()
        assert main_topview.find_notification_content() == '报备新增成功'
        log.info('报备新增成功')
        main_leftview.change_role('新房案场')
        main_leftview.click_new_house_operation_label()
        new_house_operation_table.click_report_tab()  # 点击报备tab
        new_house_operation_table.input_building_name_search(self.test_data['楼盘信息'])
        new_house_operation_table.input_customer_phone_search(customer_info['customer_phone'])
        new_house_operation_table.click_search_button()
        assert new_house_operation_table.get_table_count() == 1
        new_house_operation_table.watch_report_by_row(1)
        new_house_operation_table.dialog_click_examine_pass_button()
        assert main_topview.find_notification_content() == '报备审核成功'
        log.info('报备审核成功')
        main_leftview.change_role('经纪人')
        main_leftview.click_new_house_operation_label()
        new_house_operation_table.click_report_tab()  # 点击报备tab
        new_house_operation_table.input_building_name_search(self.test_data['楼盘信息'])
        new_house_operation_table.input_customer_phone_search(customer_info['customer_phone'])
        new_house_operation_table.click_search_button()
        assert new_house_operation_table.get_table_count() == 1
        new_house_operation_table.enter_take_look_by_row(1)
        new_house_operation_table.dialog_input_take_look_time(self.test_data['带看日期'])
        new_house_operation_table.dialog_upload_picture([cm.tmp_picture_file])
        new_house_operation_table.dialog_click_confirm_button()
        assert main_topview.find_notification_content() == '带看新增成功'
        log.info('带看新增成功')
        main_leftview.change_role('新房案场')
        main_leftview.click_new_house_operation_label()
        new_house_operation_table.click_take_look_tab()  # 点击带看tab
        new_house_operation_table.input_building_name_search(self.test_data['楼盘信息'])
        new_house_operation_table.input_customer_phone_search(customer_info['customer_phone'])
        new_house_operation_table.click_search_button()
        assert new_house_operation_table.get_table_count() == 1
        new_house_operation_table.watch_report_by_row(1)
        new_house_operation_table.dialog_click_examine_pass_button()
        assert main_topview.find_notification_content() == '带看审核成功'
        log.info('带看审核成功')
        main_leftview.change_role('经纪人')
        main_leftview.click_new_house_operation_label()
        new_house_operation_table.click_take_look_tab()  # 点击带看tab
        new_house_operation_table.input_building_name_search(self.test_data['楼盘信息'])
        new_house_operation_table.input_customer_phone_search(customer_info['customer_phone'])
        new_house_operation_table.click_search_button()
        assert new_house_operation_table.get_table_count() == 1
        new_house_operation_table.enter_subscribe_by_row(1)
        new_house_operation_table.dialog_input_block(self.test_data['楼栋'])
        new_house_operation_table.dialog_input_block_cell(self.test_data['单元'])
        new_house_operation_table.dialog_input_floor(self.test_data['楼层'])
        new_house_operation_table.dialog_input_room_number(self.test_data['房间号'])
        new_house_operation_table.dialog_input_building_area(self.test_data['建筑面积'])
        new_house_operation_table.dialog_input_subscribe_price(self.test_data['认购金额'])
        new_house_operation_table.dialog_input_subscribe_time(self.test_data['认购日期'])
        new_house_operation_table.dialog_upload_subscribe_form([cm.tmp_picture_file])
        new_house_operation_table.dialog_upload_customer_certificate([cm.tmp_picture_file])
        new_house_operation_table.dialog_upload_payment_voucher([cm.tmp_picture_file])
        new_house_operation_table.dialog_click_confirm_button()
        assert main_topview.find_notification_content() == '认购新增成功'
        log.info('认购新增成功')
        main_leftview.change_role('新房案场')
        main_leftview.click_new_house_operation_label()
        new_house_operation_table.click_subscription_tab()  # 点击认购tab
        new_house_operation_table.input_building_name_search(self.test_data['楼盘信息'])
        new_house_operation_table.input_customer_phone_search(customer_info['customer_phone'])
        new_house_operation_table.click_search_button()
        assert new_house_operation_table.get_table_count() == 1
        new_house_operation_table.watch_report_by_row(1)
        new_house_operation_table.input_commission_price(self.test_data['佣金金额'])
        new_house_operation_table.input_company_income(self.test_data['公司收入'])
        new_house_operation_table.dialog_click_examine_pass_button()
        assert main_topview.find_notification_content() == '认购审核成功'
        log.info('认购审核成功')
        main_leftview.change_role('经纪人')
        main_leftview.click_new_house_operation_label()
        new_house_operation_table.click_subscription_tab()  # 点击认购tab
        new_house_operation_table.input_building_name_search(self.test_data['楼盘信息'])
        new_house_operation_table.input_customer_phone_search(customer_info['customer_phone'])
        new_house_operation_table.click_search_button()
        assert new_house_operation_table.get_table_count() == 1
