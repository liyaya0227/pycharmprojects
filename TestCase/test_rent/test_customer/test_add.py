#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_add.py
@date: 2021/7/16 0016
"""

import pytest
import allure
from config.conf import cm
from page_object.customer.detail import CustomerDetailPage
from utils.logger import log
from common.readconfig import ini
from utils.jsonutil import get_data
from page_object.main.upviewpage import MainUpViewPage
from page_object.main.topviewpage import MainTopViewPage
from page_object.main.leftviewpage import MainLeftViewPage
from page_object.main.rightviewpage import MainRightViewPage
from page_object.customer.tablepage import CustomerTablePage
from page_object.customer.addpage import CustomerAddPage


@allure.feature("测试房源模块")
class TestAdd(object):

    json_file_path = cm.test_data_dir + "/test_rent/test_customer/test_add_" + ini.environment + ".json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="class", autouse=True)
    def test_prepare(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        customer_table = CustomerTablePage(web_driver)
        customer_detail = CustomerDetailPage(web_driver)

        main_leftview.change_role('经纪人')
        main_leftview.click_my_customer_label()
        customer_table.click_all_tab()
        customer_table.choose_customer_wish('不限')
        customer_table.input_search_text(ini.custom_telephone)
        customer_table.click_search_button()
        table_count = customer_table.get_customer_table_count()
        if table_count != 0:
            customer_table.go_customer_detail_by_row(1)
            customer_detail.click_invalid_customer_button()
            customer_detail.choose_invalid_customer_type('其他原因')
            customer_detail.input_invalid_customer_reason('自动化测试需要')
            customer_detail.click_dialog_confirm_button()
            assert main_topview.find_notification_title() == '客源无效成功'
            main_upview.clear_all_title()
            main_leftview.click_my_customer_label()

    @allure.story("测试新增租赁房源，查看搜索结果用例")
    @pytest.mark.rent
    @pytest.mark.house
    @pytest.mark.run(order=-6)
    @pytest.mark.dependency()
    @pytest.mark.flaky(reruns=5, reruns_delay=2)
    def test_001(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        customer_table = CustomerTablePage(web_driver)
        customer_add = CustomerAddPage(web_driver)

        customer_table.click_add_button()
        customer_add.input_customer_name(self.test_data['姓名'])
        customer_add.choose_customer_sex(self.test_data['性别'])
        customer_add.choose_phone_area(self.test_data['电话号_区域'])
        customer_add.input_customer_phone(ini.custom_telephone)
        customer_add.choose_customer_wish(self.test_data['客户意愿'])
        customer_add.add_customer_requirements(self.test_data['需求类型'])
        assert customer_add.get_all_requirement() == self.test_data['需求类型']
        customer_add.click_next_step_button()
        customer_add.choose_rent_type(self.test_data['租赁方式'])
        customer_add.input_psychology_price(self.test_data['心理价位'])
        customer_add.input_area(self.test_data['面积'])
        customer_add.input_room(self.test_data['居室'])
        customer_add.choose_business_district(self.test_data['商圈'])
        customer_add.input_check_in_date(self.test_data['入住日期'])
        customer_add.choose_pay_type(self.test_data['付款方式'])
        customer_add.choose_rent_range(self.test_data['租期'])
        customer_add.choose_decoration(self.test_data['装修'])
        customer_add.choose_orientation(self.test_data['朝向'])
        customer_add.choose_floor(self.test_data['楼层'])
        customer_add.choose_floor_year(self.test_data['楼龄'])
        customer_add.click_complete_button()
        assert main_topview.find_notification_content() == '添加客源成功'
        main_upview.clear_all_title()
        main_leftview.click_my_customer_label()
        customer_table.click_all_tab()
        customer_table.choose_customer_wish('不限')
        customer_table.input_search_text(ini.custom_telephone)
        customer_table.click_search_button()
        assert customer_table.get_customer_table_count() == 1
