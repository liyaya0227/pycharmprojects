#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: audit_page.py
@time: 2021/10/14
"""
from page.webpage import WebPage
from common.readelement import Element


add_house = Element('jrxf/web/house/audit')


class AuditHousePage(WebPage):

    def audit_contract(self):
        self.is_click(add_house['审核通过按钮'])
        self.is_click(add_house['审核确定按钮'])
        # self.is_click(add_house['上传合同tab'])
        # self.is_click(add_house['审核通过按钮'])
        # self.is_click(add_house['审核确定按钮'])

    def audit_release(self):
        self.is_click(add_house['上架_审核通过按钮'])
        self.is_click(add_house['审核确定按钮'])

    def select_item_option(self, option=None, index=None):
        if option:
            locator = 'xpath', "//div[@style='' or not(@style)]//div[@class='rc-virtual-list']//div[contains(@class," \
                               "'ant-select-item ant-select-item-option') and @title='" + option + "'] "
            self.is_click(locator)
        else:
            locator = 'xpath', "//div[@style='' or not(@style)]//div[@class='rc-virtual-list']//div[contains(@class," \
                               "'ant-select-item ant-select-item-option')] "
            options = self.find_elements(locator)
            options[index].click()
