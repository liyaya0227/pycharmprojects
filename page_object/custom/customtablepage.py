# -*- coding:utf-8 -*-
from page.webpage import WebPage
from common.readelement import Element

custom_table = Element('custom/customtable')


class CustomTablePage(WebPage):

    def click_add(self):
        self.is_click(custom_table['录入客源按钮'])

