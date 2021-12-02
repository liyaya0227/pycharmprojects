# #!/usr/bin/env python3
# # -*- coding: UTF-8 -*-
# """
# @author: caijj
# @version: V1.0
# @file: test_house_photo_album.py
# @date: 2021/8/24
# """
# import random
# import pytest
# import allure
# from config.conf import cm
# from page_object.jrgj.web.house.detailpage import HouseDetailPage
# from page_object.jrgj.web.house.tablepage import HouseTablePage
# from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
# from page_object.jrgj.web.main.upviewpage import MainUpViewPage
# from utils.jsonutil import get_data
#
# gl_web_driver = None
#
#
# @allure.feature("京日管家房源详情模块-更多")
# class TestMore(object):
#     json_file_path = cm.test_data_dir + "/jrgj/test_new/test_house/test_add.json"
#     test_data = get_data(json_file_path)
#
#     @pytest.fixture(scope="function", autouse=True)
#     def test_prepare(self, web_driver):
#         global gl_web_driver
#         gl_web_driver = web_driver
#         self.main_up_view = MainUpViewPage(gl_web_driver)
#         self.main_left_view = MainLeftViewPage(gl_web_driver)
#         self.house_table_page = HouseTablePage(gl_web_driver)
#         self.house_detail_page = HouseDetailPage(gl_web_driver)
#         yield
#         self.main_up_view.clear_all_title()
#
#     @allure.step("进入房源详情")
#     def enter_house_detail(self):
#         self.main_left_view.change_role('超级管理员')
#         self.main_left_view.click_all_house_label()
#         self.house_table_page.click_new_tab()
#         self.house_table_page.click_off_shelf_house_tab()
#         self.house_table_page.input_building_name_search(self.test_data['楼盘名称'])
#         self.house_table_page.click_search_button()
#         self.house_table_page.go_new_house_detail_by_row()
#
#     @allure.story("测试发布楼盘动态")
#     @pytest.mark.new
#     @pytest.mark.house
#     @pytest.mark.run(order=2)
#     # @pytest.mark.flaky(reruns=1, reruns_delay=2)
#     def test_release_house_trend(self):
#         self.enter_house_detail()
#         self.house_detail_page.click_see_more()
#         self.house_detail_page.switch_tab_by_name('楼盘动态')
#         trend_explain = self.house_detail_page.relese_house_trend_content('楼盘动态title', '楼盘动态最新')
#         assert self.house_detail_page.verify_trend_list_update(trend_explain)
#
#     @allure.story("测试编辑楼盘卖点")
#     @pytest.mark.new
#     @pytest.mark.house
#     @pytest.mark.run(order=2)
#     # @pytest.mark.flaky(reruns=1, reruns_delay=2)
#     def test_selling_point(self):
#         self.enter_house_detail()
#         self.house_detail_page.click_see_more()
#         self.house_detail_page.switch_tab_by_name('楼盘卖点')
#         push_plate = self.house_detail_page.edit_house_selling_point('距离地铁二号线100米', '四面通风大平层')
#         actual_result = self.house_detail_page.verify_celling_point_list_update()
#         expect_result = '一句话推盘：' + push_plate
#         assert actual_result == expect_result
#
#     @allure.story("测试上传户型介绍")
#     @pytest.mark.new
#     @pytest.mark.house
#     @pytest.mark.run(order=2)
#     # @pytest.mark.flaky(reruns=1, reruns_delay=2)
#     def test_upload_house_type(self):
#         self.enter_house_detail()
#         initial_house_introduce_number = self.house_detail_page.get_house_type_introduce_number()
#         self.house_detail_page.click_see_more()
#         self.house_detail_page.switch_tab_by_name('户型介绍')
#         self.house_detail_page.click_upload_house_type_btn()
#         self.house_detail_page.house_type_introduce_content('经济型' + str(random.randint(1, 100)), '100', '南',
#                                                   [cm.tmp_picture_file])
#         expect_house_introduce_number = initial_house_introduce_number + 1
#         self.house_detail_page.switch_tab_by_name('楼盘首页')
#         actual_house_introduce_number = self.house_detail_page.get_house_type_introduce_number()
#         assert actual_house_introduce_number == expect_house_introduce_number
#
#
# if __name__ == '__main__':
#     pytest.main(['-q', 'test_more.py'])
