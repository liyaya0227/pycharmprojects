#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: leftviewpage.py
@date: 2021/10/15 0015
"""
from page.webpage import WebPage
from common.readelement import Element

main_leftview = Element('jrjob/main/leftview')


class MainLeftViewPage(WebPage):

    def click_job_management(self):
        """选择job"""
        self.click_element(main_leftview['任务管理标签'])
