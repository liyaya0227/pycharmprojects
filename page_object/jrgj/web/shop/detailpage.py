#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@date: 2021/8/27 0027
"""

from page.webpage import WebPage
from common.readelement import Element

detail = Element('jrgj/web/store/detail')


class ShopDetailPage(WebPage):

    def get_region(self):
        if self.element_is_exist(detail['运营大区显示框'], wait_time=1):
            return self.element_text(detail['运营大区显示框'])
        else:
            return ''

    def get_od_name(self):
        if self.element_is_exist(detail['OD显示标签'], wait_time=1):
            value = (self.element_text(detail['OD显示标签']).split('，')[0]).split(':')[1]
            return value[:-10]
        else:
            return ''

    def get_district(self):
        if self.element_is_exist(detail['运营商圈显示框'], wait_time=1):
            return self.element_text(detail['运营商圈显示框'])
        else:
            return ''

    def get_om_name(self):
        if self.element_is_exist(detail['OM显示标签'], wait_time=1):
            value = (self.element_text(detail['OM显示标签']).split('，')[0]).split(':')[1]
            return value[:-10]
        else:
            return ''

    def click_cancel_button(self):
        self.is_click(detail['取消按钮'])
