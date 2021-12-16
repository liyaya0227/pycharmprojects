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
from page_object.common.web.login.loginpage import LoginPage
from page_object.jrgj.app.order.detailpage import AppOrderDetailPage
from page_object.jrgj.app.order.tablepage import AppOrderTablePage
from page_object.jrgj.web.house.detailpage import HouseDetailPage
from page_object.jrgj.web.main.leftviewpage import MainLeftViewPage
from page_object.jrgj.web.survey.detailpage import SurveyDetailPage
from page_object.jrgj.web.survey.tablepage import SurveyTablePage
from utils.timeutil import dt_strftime, dt_strftime_with_delta, sleep


class SurveyService(object):

    def __init__(self, web_driver, android_driver):
        # self.login_page = LoginPage(web_driver)
        # self.main_up_view = MainUpViewPage(web_driver)
        # self.main_top_view = MainTopViewPage(web_driver)
        # self.main_left_view = MainLeftViewPage(web_driver)
        # self.house_add_page = HouseAddPage(web_driver)
        # self.house_table_page = HouseTablePage(web_driver)
        # self.house_detail_page = HouseDetailPage(web_driver)
        # self.contract_table_page = ContractTablePage(web_driver)
        self.login_page = LoginPage(web_driver)
        self.main_left_view = MainLeftViewPage(web_driver)
        self.survey_table_page = SurveyTablePage(web_driver)
        self.survey_detail_page = SurveyDetailPage(web_driver)
        self.house_detail_page = HouseDetailPage(web_driver)
        self.app_order_table = AppOrderTablePage(android_driver)
        self.app_order_detail = AppOrderDetailPage(android_driver)

    def order_survey(self, survey_person_info, exploration_time, appointment_instructions):
        self.house_detail_page.click_survey_appointment_button()
        self.house_detail_page.dialog_choose_normal_survey()
        self.house_detail_page.dialog_choose_photographer(survey_person_info)
        self.house_detail_page.dialog_choose_exploration_time(exploration_time)
        self.house_detail_page.dialog_input_appointment_instructions(appointment_instructions)
        self.house_detail_page.dialog_click_confirm_button()

    def shoot_survey(self, house_code, exploration_time):
        self.app_order_table.click_search_button()
        self.app_order_table.input_search_content(house_code)
        if exploration_time == '今天':
            date = dt_strftime("%d %m %Y")
        elif exploration_time == '明天':
            date = dt_strftime_with_delta(1, "%d %m %Y")
        else:
            raise '传值错误'
        self.app_order_table.choose_date(date)
        self.app_order_table.go_order_detail_by_index(1)
        self.app_order_detail.click_start_shot_button()
        self.app_order_detail.click_end_shot_button()

    def upload_survey(self, house_code):
        self.main_left_view.change_role('实勘人员')
        self.main_left_view.click_survey_management_label()
        self.survey_table_page.click_reset_button()
        self.survey_table_page.input_house_code_search(house_code)
        self.survey_table_page.click_search_button()
        self.survey_table_page.click_upload_survey_button_by_row(1)
        upload_pictures = [cm.tmp_picture_file, cm.tmp_picture_file]
        self.survey_detail_page.upload_picture(upload_pictures)
        self.survey_detail_page.set_title_picture_by_index(randint(1, len(upload_pictures)))
        self.survey_detail_page.click_save_button()

    def login_and_upload_survey(self, web_driver, survey_person_info, house_code):
        current_handle = web_driver.current_window_handle
        js = "window.open('" + ini.url + "');"  # 通过执行js，开启一个新的窗口
        web_driver.execute_script(js)
        sleep(4)
        all_handles = web_driver.window_handles  # 获取当前窗口句柄
        for handle in all_handles:
            if handle != current_handle:
                web_driver.switch_to_window(handle)  # 切换窗口
                break
        self.login_page.log_in(survey_person_info['photographer_phone'], survey_person_info['photographer_password'])
        self.main_left_view.change_role('实勘人员')
        self.main_left_view.click_survey_management_label()
        self.survey_table_page.click_reset_button()
        self.survey_table_page.input_house_code_search(house_code)
        self.survey_table_page.click_search_button()
        self.survey_table_page.click_upload_survey_button_by_row(1)
        upload_pictures = [cm.tmp_picture_file, cm.tmp_picture_file]
        self.survey_detail_page.upload_picture(upload_pictures)
        self.survey_detail_page.set_title_picture_by_index(randint(1, len(upload_pictures)))
        self.survey_detail_page.click_save_button()
        web_driver.close()
        web_driver.switch_to_window(current_handle)  # 切换窗口
        sleep(2)
