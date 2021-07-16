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
from page_object.main.upviewpage import MainUpViewPage
from page_object.main.topviewpage import MainTopViewPage
from page_object.main.leftviewpage import MainLeftViewPage
from page_object.main.rightviewpage import MainRightViewPage
from page_object.main.invalidhousepage import InvalidHousePage
from page_object.house.tablepage import HouseTablePage
from page_object.house.addpage import HouseAddPage
from page_object.house.detailpage import HouseDetailPage


@allure.feature("测试房源模块")
class TestAdd(object):

    json_file_path = cm.test_data_dir + "/test_rent/test_house/test_add.json"
    test_data = get_data(json_file_path)

    @pytest.fixture(scope="class", autouse=True)
    def test_prepare(self, web_driver):
        main_leftview = MainLeftViewPage(web_driver)

        main_leftview.click_all_house_label()

    @allure.story("测试新增租赁房源，查看搜索结果用例")
    @pytest.mark.rent
    @pytest.mark.house
    @pytest.mark.run(order=-6)
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

        house_table.click_rent_tab()  # 点击租赁标签
        house_table.click_add_house_button()  # 点击新增房源按钮
        assert house_add.check_rent_radio()  # 判断新增界面委托类型的默认勾选
        house_add.input_property_address('租赁')  # 填写物业地址
        dialog_title = main_topview.find_notification_title()  # 若房源已录入，则右上角弹窗显示已录入的房源编号
        if dialog_title != '':
            log.info('房源已存在')
            house_code = re.search(r"房源编号(\d+?)，", dialog_title).group(1)  # 获取房源编号
            main_leftview.click_all_house_label()
            house_table.clear_filter('租赁')
            house_table.input_house_code_search(house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row()
            house_detail.click_invalid_house_button()  # 执行房源无效操作
            house_detail.input_invalid_reason("测试需要")
            house_detail.click_invalid_reason_confirm_button()
            dialog_content = main_topview.find_notification_content()  # 若房源已经提交无效申请，则弹窗显示已提交
            if '该房源已提交了无效申请' in dialog_content:
                log.info('无效申请已提交')
                main_topview.close_notification()
                house_detail.click_invalid_reason_cancel_button()
            main_leftview.change_role('超级管理员')  # 切换超管无效房源
            main_rightview.click_invalid_house()
            invalid_house_page.click_pass_by_housecode(house_code)
            invalid_house_page.click_invalid_house_confirm_button()
            assert main_topview.find_notification_title() == '成功'
            main_leftview.change_role('经纪人')  # 切回经纪人，重新执行新增操作
            main_leftview.click_all_house_label()
            house_table.click_rent_tab()
            house_table.click_add_house_button()
            house_add.input_property_address('租赁')
            assert main_topview.find_notification_content() == ''
        house_add.input_owner_info_and_house_info(self.test_data, '租赁')
        assert '新增成功' in main_topview.find_notification_content()
        log.info('填写房源信息成功')
        main_leftview.click_all_house_label()
        house_table.click_rent_tab()
        house_table.clear_filter('租赁')
        house_table.choose_estate_name_search(ini.house_community_name)
        house_table.choose_building_name_search(ini.house_building_id)
        house_table.click_search_button()
        table_count = house_table.get_house_table_count()
        assert table_count > 0
        house_code = ''
        for row in range(table_count):
            house_table.go_house_detail_by_row(row+1)
            house_property_address = house_detail.get_house_property_address()
            if house_property_address['estate_name'] == ini.house_community_name \
                    and house_property_address['building_name'] == ini.house_building_id \
                    and house_property_address['door_name'] == ini.house_doorplate:
                house_code = house_detail.get_house_code()
                main_upview.close_title_by_name(house_property_address['estate_name'])
                break
            main_upview.close_title_by_name(house_property_address['estate_name'])
        assert house_code != ''
        log.info('搜索结果正确')
        main_upview.clear_all_title()
