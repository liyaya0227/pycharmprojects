#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@date: 2021/11/17 0017
"""
from page.webpage import WebPage
from common.readelement import Element

detail = Element('jrgj/web/vrexamine/detail')


class VrExamineDetailPage(WebPage):

    def check_first_house_layout_diagram(self):
        """选择第一张户型图"""
        self.click_element(detail['户型图1_勾选框'])

    def check_first_survey_layout_diagram(self):
        """选择第一张户型图"""
        self.click_element(detail['实勘图1_标题图勾选框'])

    def click_examine_reject_button(self):
        """点击审核驳回按钮"""
        self.click_element(detail['审核驳回按钮'])

    def click_examine_pass_button(self):
        """点击审核通过按钮"""
        self.click_element(detail['审核通过按钮'])

    def reject_vr_examine(self, reject_reason):
        """审核驳回"""
        self.click_examine_reject_button()
        self.input_text_into_element(detail['审核驳回弹窗_原因输入框'], reject_reason)
        self.click_element(detail['弹窗_确定按钮'])

    def pass_vr_examine(self):
        """审核通过"""
        self.check_first_house_layout_diagram()
        self.check_first_survey_layout_diagram()
        self.click_examine_pass_button()
