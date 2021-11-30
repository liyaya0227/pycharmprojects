#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: table_page.py
@date: 2021/8/11 0011
"""
import re
from page.webpage import WebPage
from common.readelement import Element
from utils.timeutil import sleep

survey_table = Element('jrgj/web/survey/table')


class SurveyTablePage(WebPage):

    def click_normal_survey_tab(self):  # 点击普通实勘标签
        self.click_element(survey_table['普通实勘标签'])

    def click_vr_survey_tab(self):  # 点击VR实勘标签
        self.click_element(survey_table['VR实勘标签'])

    def input_house_code_search(self, house_code):
        sleep(2)
        self.input_text(survey_table['房源编号搜索框'], house_code)
        sleep(2)

    def input_survey_code_search(self, survey_code):
        self.input_text(survey_table['实勘编号搜索框'], survey_code)

    def click_search_button(self):  # 点击查询按钮
        self.click_element(survey_table['查询按钮'], 3)

    def click_reset_button(self):  # 点击重置按钮
        self.click_element(survey_table['重置按钮'])

    def get_order_status_by_row(self, row=1):
        """根据行，获取订单状态"""
        column = self.__get_column_by_title('订单状态')
        locator = 'xpath', "//div[@style='' or not(@style)]/div[contains(@class,'surveyManagement')]//tbody" \
                           "/tr[" + str(row) + "]/td[" + str(column + 1) + "]/div"
        return self.get_element_text(locator)

    def get_survey_code_by_row(self, row=1):
        """根据行，获取实勘编号"""
        column = self.__get_column_by_title('实勘编号')
        locator = 'xpath', "//div[@style='' or not(@style)]/div[contains(@class,'surveyManagement')]//tbody" \
                           "/tr[" + str(row) + "]/td[" + str(column + 1) + "]"
        return self.get_element_text(locator)

    def get_survey_person_name_by_row(self, row=1):
        """根据行，获取摄影师信息"""
        column = self.__get_column_by_title('摄影师信息')
        locator = 'xpath', "//div[@style='' or not(@style)]/div[contains(@class,'surveyManagement')]//tbody" \
                           "/tr[" + str(row) + "]/td[" + str(column + 1) + "]//li[1]"
        return re.search(r"：(\w+)/", self.get_element_text(locator)).group(1)

    def click_cancel_the_order(self):  # 取消实勘
        ele_list = self.find_elements(survey_table['取消实勘按钮'])
        for ele in ele_list:
            ele.click()
            sleep(1.5)

    def dialog_click_confirm_button(self):  # 弹窗确定按钮
        self.click_element(survey_table['弹窗_确定按钮'], sleep_time=3)

    def click_upload_survey_button_by_row(self, row=1):  # 根据行，点击上传实勘
        column = self.__get_column_by_title('操作')
        locator = 'xpath', "//div[@style='' or not(@style)]/div[contains(@class,'surveyManagement')]//tbody" \
                           "/tr[" + str(row) + "]/td[" + str(column + 1) + "]/a[text()='上传实勘']"
        self.click_element(locator)

    def get_survey_person_phone_by_row(self, row=1):  # 根据行，获取摄影师电话
        column = self.__get_column_by_title('摄影师信息')
        locator = 'xpath', "//div[@style='' or not(@style)]/div[contains(@class,'surveyManagement')]//tbody" \
                           "/tr[" + str(row) + "]/td[" + str(column + 1) + "]//li[1]"
        return self.get_element_text(locator).split('/')[1]

    def click_cancel_order_button_by_row(self, row=1):  # 根据行，点击取消订单按钮
        column = self.__get_column_by_title('操作')
        locator = 'xpath', "//div[@style='' or not(@style)]/div[contains(@class,'surveyManagement')]//tbody" \
                           "/tr[" + str(row) + "]/td[" + str(column + 1) + "]//span[text()='取消订单']"
        self.click_element(locator)

    def click_back_order_button_by_row(self, row=1):  # 根据行，点击退单按钮
        column = self.__get_column_by_title('操作')
        locator = 'xpath', "//div[@style='' or not(@style)]/div[contains(@class,'surveyManagement')]//tbody" \
                           "/tr[" + str(row) + "]/td[" + str(column + 1) + "]//span[text()='退单']"
        self.click_element(locator)

    def click_order_detail_button_by_row(self, row=1):  # 根据行，点击订单详情
        column = self.__get_column_by_title('操作')
        locator = 'xpath', "//div[@style='' or not(@style)]/div[contains(@class,'surveyManagement')]//tbody" \
                           "/tr[" + str(row) + "]/td[" + str(column + 1) + "]//span[text()='订单详情']"
        self.click_element(locator)

    def back_order_dialog_choose_reason(self, reason):  # 实勘退单弹窗选择退单原因
        self.click_element(survey_table['退单弹窗_退单原因选择框'])
        reason_list = self.find_elements(survey_table['下拉框'])
        for reason_ele in reason_list:
            if reason_ele.text == reason:
                reason_ele.click()
                break

    def back_order_dialog_click_back_order_button(self):  # 点击实勘退单弹窗退单按钮
        self.click_element(survey_table['退单弹窗_退单按钮'], sleep_time=1)

    def click_change_time_by_row(self, row=1):  # 根据行，点击取消订单按钮
        column = self.__get_column_by_title('操作')
        locator = 'xpath', "//div[@style='' or not(@style)]/div[contains(@class,'surveyManagement')]//tbody" \
                           "/tr[" + str(row) + "]/td[" + str(column + 1) + "]//span[text()='修改预约时间']"
        self.click_element(locator)

    def dialog_click_cancel_button(self):
        """弹窗，点击取消按钮"""
        self.click_element(survey_table['弹窗_取消按钮'])

    def dialog_click_confirm_button(self):
        """弹窗，点击取消按钮"""
        self.click_element(survey_table['弹窗_确定按钮'])

    def dialog_click_known_button(self):
        """弹窗，点击知道了按钮"""
        self.click_element(survey_table['弹窗_知道了按钮'])

    def change_time_dialog_choose_time(self, date_time):
        """修改实勘时间弹窗，修改时间"""
        self.click_element(survey_table['修改时间弹窗_' + date_time[0] + '日期单选'])
        self.click_element(survey_table['修改时间弹窗_时间选择框'], sleep_time=0.5)
        time_list = self.find_elements(survey_table['下拉框'])
        for time_ele in time_list:
            if date_time[1].split('-')[0] in time_ele.text and date_time[1].split('-')[1] in time_ele.text:
                if "ant-select-item-option-disabled" not in time_ele.get_attribute('class'):
                    time_ele.click()
                    return
        for time_ele in time_list:
            if "ant-select-item-option-disabled" not in time_ele.get_attribute('class'):
                time_ele.click()
                break

    def __get_column_by_title(self, title):  # 获取表格title在第几列
        locator = 'xpath', \
                  "//div[@style='' or not(@style)]/div[contains(@class,'surveyManagement')]//table/thead//th"
        title_list = self.find_elements(locator)
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele)
