#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: writtenentrustmentagreementpage.py
@time: 2021/06/22
"""

from page.webpage import WebPage
from common.readelement import Element
from utils.uploadfile import upload_file
from utils.timeutil import dt_strftime, dt_strftime_with_delta, sleep

written_entrustment_agreement = Element('web/house/writtenentrustmentagreement')


class WrittenEntrustmentAgreementPage(WebPage):

    def input_entrustment_agreement_number(self, entrustment_agreement_number):
        self.input_text(written_entrustment_agreement['委托协议编号输入框'], entrustment_agreement_number)

    def input_entrustment_start_date(self, start_date):
        if start_date == '':
            start_date = dt_strftime('%Y-%m-%d')
        self.is_click(written_entrustment_agreement['委托日期开始日期输入框'])
        self.input_text(written_entrustment_agreement['委托日期开始日期输入框'], start_date)
        self.send_enter_key(written_entrustment_agreement['委托日期开始日期输入框'])

    def input_entrustment_end_date(self, end_date):
        if end_date == '':
            end_date = dt_strftime_with_delta(10, '%Y-%m-%d')
        self.is_click(written_entrustment_agreement['委托日期结束日期输入框'])
        self.input_text(written_entrustment_agreement['委托日期结束日期输入框'], end_date)
        self.send_enter_key(written_entrustment_agreement['委托日期结束日期输入框'])

    def input_remark(self, remark):
        self.input_text(written_entrustment_agreement['备注输入框'], remark)

    def upload_picture(self, file_path):
        for file in file_path:
            self.is_click(written_entrustment_agreement['上传图片按钮'])
            upload_file(file)
            sleep(2)

    def click_close_button(self):
        self.is_click(written_entrustment_agreement['关闭按钮'])

    def click_submit_button(self):
        self.is_click(written_entrustment_agreement['提交按钮'], sleep_time=1)
