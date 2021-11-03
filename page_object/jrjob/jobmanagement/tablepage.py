#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/10/15 0015
"""
from utils.timeutil import dt_strftime
from page.webpage import WebPage
from common.readelement import Element

table = Element('jrjob/jobmanagement/table')


class JobManagementTablePage(WebPage):

    def choose_job(self, job_name):
        """选择job"""
        self.click_element(table['执行器选择框'])
        job_locator = 'xpath', "//select[@id='jobGroup']/option[text()='" + job_name + "']"
        self.click_element(job_locator, sleep_time=1)

    def input_executor_handler_search(self, executor_handler):
        """输入JobHandler搜索输入框"""
        self.input_text(table['JobHandler搜索输入框'], executor_handler)

    def click_search_button(self):
        """点击搜索按钮"""
        self.click_element(table['搜索按钮'], sleep_time=2)

    def execute_once_job_by_row(self, row=1):
        drop_down_locator = 'xpath', "//table[@id='job_list']//tr[" + str(row) \
                            + "]/td[7]//button[@data-toggle='dropdown']"
        if not self.get_element_attribute(drop_down_locator, 'aria-expanded'):
            self.click_element(drop_down_locator)
        execute_once_locator = 'xpath', "//table[@id='job_list']//tr[" + str(row) + "]/td[7]//ul//a[text()='执行一次']"
        self.click_element(execute_once_locator, sleep_time=1)
        param = 'topNum=200&execTime=' + dt_strftime("%Y-%m-%d")
        self.input_text(table['弹窗_任务参数输入框'], param, clear=True)
        self.click_element(table['弹窗_保存按钮'], sleep_time=2)
