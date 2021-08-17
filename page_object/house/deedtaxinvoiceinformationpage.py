#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: deedtaxinvoiceinformationpage.py
@time: 2021/06/22
"""

from page.webpage import WebPage
from common.readelement import Element
from utils.timeutil import sleep
from utils.uploadfile import upload_file

deed_tax_invoice_information = Element('house/deedtaxinvoiceinformation')


class DeedTaxInvoiceInformationPage(WebPage):

    def upload_picture(self, file_path):
        for file in file_path:
            self.is_click(deed_tax_invoice_information['上传图片按钮'])
            upload_file(file)
            sleep(2)

    def input_filling_date(self, filling_date):
        self.is_click(deed_tax_invoice_information['填发日期输入框'])
        self.input_text(deed_tax_invoice_information['填发日期输入框'], filling_date)
        self.send_enter_key(deed_tax_invoice_information['填发日期输入框'])

    def input_tax_money(self, tax_money):
        self.input_text(deed_tax_invoice_information['计税金额输入框'], tax_money)

    def input_remark(self, remark):
        self.input_text(deed_tax_invoice_information['备注输入框'], remark)

    def click_close_button(self):
        self.is_click(deed_tax_invoice_information['关闭按钮'])

    def click_submit_button(self):
        self.is_click(deed_tax_invoice_information['提交按钮'])
