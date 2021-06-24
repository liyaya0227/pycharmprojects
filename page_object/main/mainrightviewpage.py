#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: vipserviceentrustmentagreementpage.py
@time: 2021/06/22
"""

from page.webpage import WebPage
from common.readelement import Element
from utils.times import sleep

main_rightview = Element('main/mainrightview')


class MainRightViewPage(WebPage):

    def click_invalid_house(self):
        self.is_click(main_rightview['房源待办_无效房源'])
        sleep()
