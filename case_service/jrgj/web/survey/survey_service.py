#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: survey_service.py
@date: 2021/10/29 0026
"""
from random import randint
from common.readconfig import ini
from config.conf import cm
from page_object.jrgj.app.order.detailpage import AppOrderDetailPage
from page_object.jrgj.app.order.tablepage import AppOrderTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.survey.detailpage import SurveyDetailPage
from page_object.jrgj.web.survey.tablepage import SurveyTablePage
from utils.jsonutil import get_data, get_value
from utils.timeutil import dt_strftime, dt_strftime_with_delta

gl_web_driver = None
gl_app_driver = None
main_left_view = None
app_order_table = None
app_order_detail = None
house_detail_page = None
survey_table_page = None
survey_detail_page = None


class SurveyService(object):
    # json_file_path = cm.test_data_dir + "/jrgj/test_sale/test_house/test_appointment_survey.json"
    # test_data = get_data(json_file_path)
    # survey_person_info = get_value(json_file_path, ini.environment)

    @staticmethod
    def order_survey(web_driver, survey_person_info, exploration_time, appointment_instructions):
        global gl_web_driver, house_detail_page
        gl_web_driver = web_driver
        house_detail_page = HouseDetailPage(gl_web_driver)
        house_detail_page.click_survey_appointment_button()
        house_detail_page.dialog_choose_normal_survey()
        house_detail_page.dialog_choose_photographer(survey_person_info)
        house_detail_page.dialog_choose_exploration_time(exploration_time)
        house_detail_page.dialog_input_appointment_instructions(appointment_instructions)
        house_detail_page.dialog_click_confirm_button()

    @staticmethod
    def shoot_survey(android_driver, house_code, exploration_time):
        global gl_app_driver, app_order_table, app_order_detail
        gl_app_driver = android_driver
        app_order_table = AppOrderTablePage(gl_app_driver)
        app_order_detail = AppOrderDetailPage(android_driver)
        app_order_table.click_search_button()
        app_order_table.input_search_content(house_code)
        if exploration_time == '今天':
            date = dt_strftime("%d %m %Y")
        elif exploration_time == '明天':
            date = dt_strftime_with_delta(1, "%d %m %Y")
        else:
            raise '传值错误'
        app_order_table.choose_date(date)
        app_order_table.go_order_detail_by_index(1)
        app_order_detail.click_start_shot_button()
        app_order_detail.click_end_shot_button()

    @staticmethod
    def upload_survey(web_driver, house_code):
        global gl_web_driver, main_left_view, survey_table_page, survey_detail_page
        main_left_view = MainLeftViewPage(web_driver)
        survey_table_page = SurveyTablePage(web_driver)
        survey_detail_page = SurveyDetailPage(web_driver)
        main_left_view.change_role('实勘人员')
        main_left_view.click_survey_management_label()
        survey_table_page.click_reset_button()
        survey_table_page.input_house_code_search(house_code)
        survey_table_page.click_search_button()
        survey_table_page.click_upload_survey_button_by_row(1)
        upload_pictures = [cm.tmp_picture_file, cm.tmp_picture_file]
        survey_detail_page.upload_picture(upload_pictures)
        survey_detail_page.set_title_picture_by_index(randint(1, len(upload_pictures)))
        survey_detail_page.click_save_button()
