#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: listpage.py
@time: 2021/06/23
"""

import re
from page.webpage import WebPage
from common.readelement import Element
from utils.fileutil import *
from utils.timeutil import sleep
from config.conf import cm
from common.readconfig import ini

agreement_list = Element('jrgj/web/agreement/list')


class AgreementListPage(WebPage):

    def input_agreement_name_search(self, agreement_name):
        self.clear_text(agreement_list['协议名称搜索框'])
        self.input_text(agreement_list['协议名称搜索框'], agreement_name)

    def click_query_button(self):
        self.click_element(agreement_list['查询按钮'], sleep_time=2)

    def click_download_button_by_row(self, row=1):
        locator = 'xpath', "//div[@class='ant-row protocolApplication']//table//tr[" + str(row) + "]//a[text()='下载']"
        self.click_element(locator, sleep_time=4)

    @staticmethod
    def get_written_entrustment_agreement_number():
        while True:
            file_path = search_file_in_dir(cm.tmp_dir, '一般委托书')
            if file_path == '':
                sleep()
                continue
            content = get_docx_file_content(file_path)
            delete_file(file_path)
            number = re.search(r"编号：(.+?)\n", content).group(1)
            return number

    @staticmethod
    def get_key_entrustment_certificate_number():
        while True:
            file_path = search_file_in_dir(cm.tmp_dir, '钥匙托管协议')
            if file_path == '':
                sleep()
                continue
            content = get_docx_file_content(file_path)
            delete_file(file_path)
            number = re.search(r"编号：(.+?)\n", content).group(1)
            return number

    @staticmethod
    def get_vip_service_entrustment_agreement_number():
        while True:
            file_path = search_file_in_dir(cm.tmp_dir, '房屋出售委托协议VIP版')
            if file_path == '':
                sleep()
                continue
            content = get_docx_file_content(file_path)
            delete_file(file_path)
            number = re.search(r"编号：(.+?)\n", content).group(1)
            return number

    def get_agreement_number_certificate_name(self, certificate_name):
        """根据证书名称获取证书编号"""
        if certificate_name == '书面委托协议':
            name = '一般委托书'
        elif certificate_name == '钥匙委托凭证':
            name = '钥匙托管协议'
        elif certificate_name == 'VIP服务委托协议':
            name = '房屋出售委托协议VIP版'
        else:
            raise ValueError('传值错误')
        self.input_agreement_name_search(name)
        self.click_query_button()
        self.click_download_button_by_row(1)
        while True:
            file_path = search_file_in_dir(cm.tmp_dir, name)
            if file_path == '':
                sleep()
                continue
            content = get_docx_file_content(file_path)
            delete_file(file_path)
            number = re.search(r"编号：(.+?)\n", content).group(1)
            return number
