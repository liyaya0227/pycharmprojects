#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_add.py
@time: 2021/06/22
"""

import re
import pytest
import allure
from utils.logger import log
from common.readconfig import ini
from config.conf import cm
from utils.jsonutil import get_data
from page_object.main.topviewpage import MainTopViewPage
from page_object.main.leftviewpage import MainLeftViewPage
from page_object.main.rightviewpage import MainRightViewPage
from page_object.main.upviewpage import MainUpViewPage
from page_object.main.invalidhousepage import InvalidHousePage
from page_object.house.tablepage import HouseTablePage
from page_object.house.addpage import HouseAddPage
from page_object.house.detailpage import HouseDetailPage
from page_object.contract.tablepage import ContractTablePage


@allure.feature("测试房源模块")
class TestAdd(object):

    json_file_path = cm.test_data_dir + "/test_sale/test_house/test_add.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="class", autouse=True)
    def test_prepare(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)

        main_leftview.change_role('经纪人')
        main_leftview.click_all_house_label()

    @allure.story("测试新增买卖房源，查看搜索结果用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=1)
    @pytest.mark.dependency()
    @pytest.mark.flaky(reruns=5, reruns_delay=2)
    def test_001(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        main_rightview = MainRightViewPage(web_driver)
        main_upview = MainUpViewPage(web_driver)
        house_detail = HouseDetailPage(web_driver)
        house_table = HouseTablePage(web_driver)
        invalid_house_page = InvalidHousePage(web_driver)
        house_add = HouseAddPage(web_driver)
        contract_table = ContractTablePage(web_driver)

        house_table.click_sale_tab()  # 点击买卖tab
        house_table.click_add_house_button()
        house_add.choose_sale_radio()
        house_add.choose_estate_name(ini.house_community_name)  # 填写物业地址信息
        house_add.choose_building_id(ini.house_building_id)
        house_add.choose_building_cell(ini.house_building_cell)
        house_add.choose_floor(ini.house_floor)
        house_add.choose_doorplate(ini.house_doorplate)
        if house_add.find_dialog():  # 房源存在资料盘
            house_add.click_dialog_go_button()
            house_add.click_submit_button()
            assert main_topview.find_notification_content() == '认领成功'
            main_upview.clear_all_title()
            main_leftview.click_all_house_label()
            house_table.click_sale_tab()  # 点击买卖tab
            house_table.click_add_house_button()
            house_add.choose_sale_radio()
            house_add.choose_estate_name(ini.house_community_name)  # 填写物业地址信息
            house_add.choose_building_id(ini.house_building_id)
            house_add.choose_building_cell(ini.house_building_cell)
            house_add.choose_floor(ini.house_floor)
            house_add.choose_doorplate(ini.house_doorplate)
        house_add.click_next_button()
        dialog_title = main_topview.find_notification_title()
        if dialog_title != '':
            log.info('房源已存在')
            house_code = re.search(r"房源编号(\d+?)，", dialog_title).group(1)
            main_leftview.click_all_house_label()
            house_table.clear_filter('买卖')
            house_table.input_house_code_search(house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row()
            house_detail.click_invalid_house_button()
            house_detail.input_invalid_reason("测试需要")
            house_detail.click_invalid_reason_confirm_button()
            dialog_content = main_topview.find_notification_content()  # 若房源已经提交无效申请，则弹窗显示已提交
            if '该房源已提交了无效申请' in dialog_content:
                log.info('无效申请已提交')
                main_topview.close_notification()
                house_detail.click_invalid_reason_cancel_button()
            elif dialog_content == '该房源已录入合同，请先无效合同，再执行此操作':
                log.info('该房源已录入合同，请先无效合同，再执行此操作')
                main_topview.close_notification()
                house_detail.click_invalid_reason_cancel_button()
                main_leftview.change_role('超级管理员')
                main_leftview.click_contract_management_label()
                contract_table.input_house_code_search(house_code)
                contract_table.click_search_button()
                count = contract_table.get_contract_table_count()
                for _ in range(count):
                    contract_table.delete_contract_by_row(1)
                    contract_table.click_dialog_confirm_button()
                    assert main_topview.find_notification_content() == '操作成功'
                main_leftview.change_role('经纪人')
                main_leftview.click_all_house_label()
                house_table.clear_filter('买卖')
                house_table.input_house_code_search(house_code)
                house_table.click_search_button()
                house_table.go_house_detail_by_row()
                house_detail.click_invalid_house_button()
                house_detail.input_invalid_reason("测试需要")
                house_detail.click_invalid_reason_confirm_button()
                assert '无效申请提交成功' in main_topview.find_notification_content()
            main_leftview.change_role('超级管理员')
            main_rightview.click_invalid_house()
            invalid_house_page.click_pass_by_housecode(house_code)
            invalid_house_page.click_invalid_house_confirm_button()
            assert main_topview.find_notification_title() == '成功'
            main_leftview.change_role('经纪人')
            main_leftview.click_all_house_label()
            house_table.click_sale_tab()
            house_table.click_add_house_button()
            house_add.input_property_address('买卖')
            assert main_topview.find_notification_content() == ''
        house_add.input_owner_info_and_house_info(self.test_data, '买卖')
        assert '新增成功' in main_topview.find_notification_content()
        log.info('房源新增成功')
        main_leftview.click_all_house_label()
        house_table.click_sale_tab()
        house_table.clear_filter('买卖')
        house_table.choose_estate_name_search(ini.house_community_name)
        house_table.choose_building_name_search(ini.house_building_id)
        house_table.click_search_button()
        table_count = house_table.get_house_table_count()
        assert table_count > 0
        house_code = ''
        for row in range(table_count):
            house_table.go_house_detail_by_row(row + 1)
            house_property_address = house_detail.get_house_property_address()
            if house_property_address['estate_name'] == ini.house_community_name \
                    and house_property_address['building_name'] == ini.house_building_id \
                    and house_property_address['door_name'] == ini.house_doorplate:
                house_code = house_detail.get_house_code()
                main_upview.close_title_by_name(house_property_address['estate_name'])
                break
            main_upview.close_title_by_name(house_property_address['estate_name'])

            house_table.clear_filter('买卖')
            house_table.choose_estate_name_search(ini.house_community_name)
            house_table.choose_building_name_search(ini.house_building_id)
            house_table.click_search_button()
        assert house_code != ''
        log.info('搜索结果正确')
        main_upview.clear_all_title()
