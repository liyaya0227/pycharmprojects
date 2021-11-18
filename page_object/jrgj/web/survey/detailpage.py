#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@date: 2021/8/11 0011
"""

from utils.uploadfile import upload_file
from page.webpage import WebPage
from common.readelement import Element

survey_detail = Element('jrgj/web/survey/detail')


class SurveyDetailPage(WebPage):

    def click_upload_picture_button(self):  # 点击普通实勘标签
        self.click_element(survey_detail['上传图片按钮'])

    def upload_picture(self, pictures):  # 上传图片
        for picture in pictures:
            self.click_upload_picture_button()
            upload_file(picture)

    def set_title_picture_by_index(self, index=1):  # 根据index，设为标题图
        locator = 'xpath', \
                  "(//div[@style='' or not(@style)]/div[contains(@class,'bulkUpload')]//span[text()='设为标题图']" \
                  "/parent::label//input[@type='checkbox'])[" + str(index) + "]"
        self.click_element(locator, 2)

    def input_feedback(self, feedback):
        """填写反馈信息"""
        self.input_text_into_element(survey_detail['反馈意见输入框'], feedback)

    def click_close_button(self):  # 点击关闭按钮
        self.click_element(survey_detail['关闭按钮'])

    def click_save_button(self):  # 点击保存按钮
        self.click_element(survey_detail['保存按钮'], sleep_time=2)

    def click_submit_button(self):  # 点击提交按钮
        self.click_element(survey_detail['提交按钮'])
