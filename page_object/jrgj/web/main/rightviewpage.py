#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: rightviewpage.py
@time: 2021/06/22
"""

from page.webpage import WebPage
from common.readelement import Element
from utils.timeutil import sleep

right_view = Element('jrgj/web/main/rightview')


class MainRightViewPage(WebPage):

    def get_login_person_brand(self):
        return self.get_element_text(right_view['登录人品牌标签'])

    def get_login_person_name(self):
        sleep(1)
        value = self.get_element_text(right_view['登录人姓名标签'])
        return value.split(' ')[0]

    def get_login_person_shop_group(self):
        return self.get_element_text(right_view['登录人店组标签'])

    def get_login_person_phone(self):
        sleep(1)
        return self.get_element_text(right_view['登录人电话标签'])

    def click_invalid_house(self):
        self.click_element(right_view['房源待办_无效房源'])

    def click_certificate_examine(self):
        self.click_element(right_view['房源待办_证件审批'])

    def click_review_house_state(self):
        self.click_element(right_view['房源待办_房源状态审核'], 3)

    def click_review_house_report(self):
        self.click_element(right_view['房源待办_房源举报审核'], 3)
