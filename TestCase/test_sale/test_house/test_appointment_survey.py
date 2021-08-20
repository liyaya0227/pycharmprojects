#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: test_appointment_survey.py
@time: 2021/06/22
"""

import pytest
import allure
from utils.logger import log
from config.conf import cm
from common.readconfig import ini
from utils.jsonutil import get_data
from utils.jsonutil import get_value
from page_object.web.main.upviewpage import MainUpViewPage
from page_object.web.main.topviewpage import MainTopViewPage
from page_object.web.main.leftviewpage import MainLeftViewPage
from page_object.web.house.tablepage import HouseTablePage
from page_object.web.house.detailpage import HouseDetailPage

house_code = ''


@allure.feature("测试房源模块")
class TestAppointmentSurvey(object):

    json_file_path = cm.test_data_dir + "/test_sale/test_house/test_appointment_survey.json"
    test_data = get_data(json_file_path)
    survey_person_info = get_value(json_file_path, ini.environment)

    @pytest.fixture(scope="function", autouse=True)
    def test_prepare(self, web_driver):
        global house_code

        main_upview = MainUpViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)

        main_leftview.change_role('经纪人')
        house_code = house_table.get_house_code_by_db(flag='买卖')
        assert house_code != ''
        log.info('房源编号为：' + house_code)
        main_leftview.click_all_house_label()
        yield
        main_upview.clear_all_title()

    @allure.story("测试房源预约实勘用例")
    @pytest.mark.sale
    @pytest.mark.house
    @pytest.mark.run(order=11)
    def test_001(self, web_driver):
        main_topview = MainTopViewPage(web_driver)
        main_leftview = MainLeftViewPage(web_driver)
        house_table = HouseTablePage(web_driver)
        house_detail = HouseDetailPage(web_driver)

        house_table.click_sale_tab()
        house_table.click_all_house_tab()
        house_table.click_reset_button()
        house_table.clear_filter(flag='买卖')
        house_table.input_house_code_search(house_code)
        house_table.click_search_button()
        house_table.go_house_detail_by_row(1)
        if house_detail.check_survey_status() == '已预约':
            log.info('实勘已预约,实勘退单')
            house_detail.click_back_survey_button()
            house_detail.dialog_choose_back_exploration_reason('其他')
            house_detail.dialog_click_back_exploration_return_button()
            assert main_topview.find_notification_content() == '退单成功'
        elif house_detail.check_survey_status() == '已上传':
            main_leftview.change_role('超级管理员')
            main_leftview.click_all_house_label()
            house_table.click_sale_tab()
            house_table.click_all_house_tab()
            house_table.click_reset_button()
            house_table.clear_filter(flag='买卖')
            house_table.input_house_code_search(house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row(1)
            house_detail.click_delete_survey_button()
            house_detail.dialog_click_confirm_button()
            main_leftview.change_role('经纪人')
            main_leftview.click_all_house_label()
            house_table.click_sale_tab()
            house_table.click_all_house_tab()
            house_table.click_reset_button()
            house_table.clear_filter(flag='买卖')
            house_table.input_house_code_search(house_code)
            house_table.click_search_button()
            house_table.go_house_detail_by_row(1)
        else:
            pass
        house_detail.click_survey_appointment_button()
        house_detail.dialog_choose_normal_survey()
        house_detail.dialog_choose_photographer(self.survey_person_info['photographer'])
        house_detail.dialog_choose_exploration_time(self.test_data['exploration_time'])
        house_detail.dialog_input_appointment_instructions(self.test_data['appointment_instructions'])
        house_detail.dialog_click_confirm_button()
        log.info('预约实勘申请已提交')
