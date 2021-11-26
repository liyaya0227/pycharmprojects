#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: verifypage.py
@date: 2021/11/22 0022
"""
from common.readxml import ReadXml
from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element
from page_object.jrgj.web.main.upviewpage import MainUpViewPage

house_verify = Element('jrgj/web/house/verify')


class HouseVerifyPage(WebPage):

    def click_to_verify_tab(self):
        """点击待举证标签"""
        self.click_element(house_verify['待举证标签'])

    def verify_again_by_house_code(self, house_code):
        """根据房源编号，点击重新举证按钮"""
        locator = "xpath", \
                  "//div[not(contains(@style,'display'))]/div[@class='houseCheck']//div[@class='checkList']//table" \
                  "/tbody//p[text()='" + house_code + "']/ancestor::tr/td[" + self.__get_column_by_title('操作') \
                  + "]//span[text()='重新举证']/parent::a"
        self.click_element(locator)

    def __get_column_by_title(self, title):
        locator = 'xpath', \
                  "//div[not(contains(@style,'display'))]/div[@class='houseCheck']//div[@class='checkList']//table" \
                  "/thead//th"
        return str(list(map(lambda x: x.text, self.find_elements(locator))).index(title) + 1)

    def choose_verify_code_to_verify(self):
        """选择验证码验真"""
        self.click_element(house_verify['房源验证码验证'])

    def click_send_verify_code_button(self):
        """选择验证码验真"""
        self.click_element(house_verify['发送验证码按钮'])

    def input_verify_code(self, verify_code):
        """输入验证码"""
        self.input_text_into_element(house_verify['验证码输入框'], verify_code)

    def click_submit_button(self):
        """点击提交按钮"""
        self.click_element(house_verify['提交按钮'])
