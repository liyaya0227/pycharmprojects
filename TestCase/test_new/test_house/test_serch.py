# #!/usr/bin/env python3
# # -*- coding: UTF-8 -*-
# """
# @author: caijj
# @version: V1.0
# @file: test_serch.py
# @date: 2021/8/24
# """
#
# import pytest
# import allure
# from config.conf import cm
# from page_object.web.house.tablepage import HouseTablePage
# from page_object.web.main.leftviewpage import MainLeftViewPage
# from utils.jsonutil import get_data
#
#
# @allure.feature("测试新房源搜索功能模块")
# class TestAdd(object):
#
#     json_file_path = cm.test_data_dir + "/test_new/test_house/test_add.json"
#     test_data = get_data(json_file_path)
#
#     @pytest.fixture(scope="function", autouse=True)
#     def test_prepare(self, web_driver):
#
#         main_leftview = MainLeftViewPage(web_driver)
#         main_leftview.change_role('超级管理员')
#         main_leftview.click_all_house_label()
#
#     @allure.story("测试根据新房类型、区域等字段搜索功能")
#     @pytest.mark.new
#     @pytest.mark.house
#     @pytest.mark.run(order=2)
#     @pytest.mark.flaky(reruns=2, reruns_delay=2)
#     def test_serch_new(self, web_driver):
#         house_table = HouseTablePage(web_driver)
#         house_table.click_new_tab()  # 点击新房tab
#         if self.test_data['是否外网呈现'] == '是': # 根据创建时是否外网呈现，确定所属种类
#             house_table.click_all_house_tab()
#         else:
#             house_table.click_off_shelf_house_tab()
#         house_table.choose_option('区域','工业园区')
#         house_table.choose_option('类型', self.test_data['楼盘状态'])
#         house_table.choose_option('房源渠道', self.test_data['房源渠道'])
#         house_table.click_search_button()
#         res = house_table.verify_house_exist(self.test_data['楼盘名称'])
#         assert res
#
#
#
#
