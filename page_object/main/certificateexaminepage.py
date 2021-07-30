#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: certificateexaminepage.py
@date: 2021/7/14 0014
"""

from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element

certificate_examine = Element('main/certificateexamine')


class CertificateExaminePage(WebPage):

    def __click_pass_examine_button(self, house_code, certificate_name):
        self.is_click(certificate_examine['第一页标签'])
        self.scroll_to_top()
        tab_count = self.find_elements(certificate_examine['翻页标签'])
        for _ in range(len(tab_count)):
            locator = "xpath",\
                      "//table/tbody//div[@class='houseCode' and text()='" \
                      + house_code + "']/ancestor::tr/td[6]//div[text()='" + certificate_name + \
                      "']/ancestor::tr/td[8]//a[text()='通过']"
            if self.find_element_with_wait_time(locator):
                self.is_click(locator)
                sleep()
                return True
            if 'ant-pagination-disabled' in self.get_element_attribute(certificate_examine['下一页标签'], 'class'):
                break
            self.is_click(certificate_examine['下一页标签'])
        return False

    def pass_written_entrustment_agreement_examine(self, house_code):
        self.__click_pass_examine_button(house_code, '书面委托协议')

    def pass_key_entrustment_certificate_examine(self, house_code):
        self.__click_pass_examine_button(house_code, '钥匙委托凭证')

    def pass_vip_service_entrustment_agreement_examine(self, house_code):
        self.__click_pass_examine_button(house_code, 'VIP服务委托协议')

    def pass_property_ownership_certificate_examine(self, house_code):
        self.__click_pass_examine_button(house_code, '房产证')

    def scroll_to_top(self):
        js = "var q=document.documentElement.scrollTop=0"
        self.execute_js_script(js)
        sleep(3)

    def get_table_count(self):
        locator = 'xpath', "//table/tbody/tr"
        sleep()
        table_row = self.find_elements(locator)
        if table_row[0].text == '暂无数据':
            return 0
        return len(table_row)
