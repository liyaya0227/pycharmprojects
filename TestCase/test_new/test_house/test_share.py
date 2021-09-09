# #!/usr/bin/env python3
# # -*- coding: UTF-8 -*-
# """
# @author: caijj
# @version: V1.0
# @file: test_share.py
# @date: 2021/8/24
# """
#
# import pytest
# import allure
# from config.conf import cm
# from page_object.web.house.detailpage import HouseDetailPage
# from page_object.web.house.tablepage import HouseTablePage
# from page_object.web.main.leftviewpage import MainLeftViewPage
# from page_object.web.main.rightviewpage import MainRightViewPage
# from utils.jsonutil import get_data
#
# person_info = {}
#
# @allure.feature("测试分享新房源功能模块")
# class TestShare(object):
#
#     json_file_path = cm.test_data_dir + "/test_new/test_house/test_add.json"
#     test_data = get_data(json_file_path)
#
#     @pytest.fixture(scope="function", autouse=True)
#     def test_prepare(self, web_driver):
#         global person_info
#
#         main_leftview = MainLeftViewPage(web_driver)
#         main_leftview.change_role('超级管理员')
#         main_leftview.click_all_house_label()
#         main_rightview = MainRightViewPage(web_driver)
#         login_name = main_rightview.get_login_person_name()
#         login_phone = main_rightview.get_login_person_phone()
#         person_info = {'姓名': login_name, '电话': login_phone}
#
#     @allure.story("测试分享功能")
#     @pytest.mark.new
#     @pytest.mark.house
#     @pytest.mark.run(order=2)
#     # @pytest.mark.flaky(reruns=2, reruns_delay=2)
#     def test_share_house(self, web_driver):
#         house_table = HouseTablePage(web_driver)
#         house_table.click_new_tab()  # 点击新房tab
#         house_table.input_building_name_search(self.test_data['楼盘名称'])
#         # house_table.input_building_name_search('露露露楼盘')
#         house_table.click_search_button()
#         house_table.go_new_house_detail_by_row()
#         house_detail = HouseDetailPage(web_driver)
#         house_detail.get_house_type_in_detail_page()
#         # house_detail.click_share_btn()
#
#
#
#
#
#
#
