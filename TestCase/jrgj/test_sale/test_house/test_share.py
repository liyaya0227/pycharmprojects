# #!/usr/bin/env python3
# # -*- coding: UTF-8 -*-
# """
# @author: jutao
# @version: V1.0
# @file: test_share.py
# @date: 2021/8/9 0009
# """
#
# import pytest
# import allure
# from case_service.jrgj.web.house.house_service import HouseService
# from config.conf import cm
# from utils.jsonutil import get_data
# from common.readconfig import ini
# from page_object.jrgj.web.main.upviewpage import MainUpViewPage
# from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
# from page_object.jrgj.web.main.rightviewpage import MainRightViewPage
# from page_object.jrgj.web.house.tablepage import HouseTablePage
# from page_object.jrgj.web.house.detailpage import HouseDetailPage
#
# HOUSE_TYPE = 'sale'
# gl_driver = None
# house_info = ''
# login_person_name = ''
# login_person_phone = ''
#
#
# @allure.feature("买卖房源详情模块-分享")
# class TestShare(object):
#     json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_add.json"
#     test_data = get_data(json_file_path)
#
#     @pytest.fixture(scope="class", autouse=True)
#     def prepare_house(self, web_driver):
#         global gl_driver, house_info
#         gl_driver = web_driver
#         house_service = HouseService(gl_driver)
#         house_info = house_service.prepare_house(self.test_data, HOUSE_TYPE)
#
#     @pytest.fixture(scope="function", autouse=True)
#     def test_prepare(self):
#         global login_person_name, login_person_phone
#         self.main_up_view = MainUpViewPage(gl_driver)
#         self.main_left_view = MainLeftViewPage(gl_driver)
#         self.main_right_view = MainRightViewPage(gl_driver)
#         self.house_table_page = HouseTablePage(gl_driver)
#         self.house_detail_page = HouseDetailPage(gl_driver)
#         self.main_left_view.click_homepage_overview_label()
#         login_person_name = self.main_right_view.get_login_person_name()
#         login_person_phone = self.main_right_view.get_login_person_phone()
#         yield
#         self.main_up_view.clear_all_title()
#
#     # @allure.step("进入房源详情")
#     # def enter_house_detail(self, house_code):
#     #     self.main_left_view.click_all_house_label()
#     #     self.house_table_page.input_house_code_search(house_code)
#     #     self.house_detail_page.enter_house_detail()
#     @allure.step("进入房源详情")
#     def enter_house_detail(self, house_code):
#         self.main_left_view.click_all_house_label()
#         self.house_table_page.input_house_code_search(house_code)
#         for i in range(4):
#             number = self.house_table_page.get_house_number()
#             if int(number) > 0:
#                 self.house_detail_page.enter_house_detail()
#                 break
#             else:
#                 self.house_table_page.click_search_button()
#
#     @allure.story("测试房源详情右侧分享用例")
#     @pytest.mark.sale
#     @pytest.mark.house
#     @pytest.mark.run(order=4)
#     def test_share(self):
#         self.enter_house_detail(house_info[0])
#         house_type = self.house_detail_page.get_house_type()
#         size = self.house_detail_page.get_size()
#         orientations = self.house_detail_page.get_orientations()
#         self.house_detail_page.click_share_button()
#         dialog_community_name = self.house_detail_page.share_dialog_get_community_name()
#         dialog_house_type = self.house_detail_page.share_dialog_get_house_type()
#         dialog_size = self.house_detail_page.share_dialog_get_size()
#         dialog_orientations = self.house_detail_page.share_dialog_get_orientations()
#         dialog_name = self.house_detail_page.share_dialog_get_name()
#         dialog_phone = self.house_detail_page.share_dialog_get_phone()
#         self.house_detail_page.dialog_click_cancel_button()
#         pytest.assume(ini.house_community_name == dialog_community_name)
#         pytest.assume(house_type == dialog_house_type)
#         pytest.assume(size == dialog_size)
#         pytest.assume(orientations == dialog_orientations)
#         pytest.assume(login_person_name == dialog_name)
#         pytest.assume(login_person_phone == dialog_phone)
