#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: table_page.py
@time: 2021/11/3
"""
from utils.logger import logger
from page.webpage import WebPage
from common.readelement import Element
from utils.timeutil import sleep

task_table = Element('jrxf/web/task/table')


class HouseTaskTablePage(WebPage):

    def switch_tab_by_tab_name(self, tab_name):
        locator = 'xpath', "//div[@style='' or not(@style)]/div[@class='new_house_task']//" \
                           "div[@class='ant-tabs-tab-btn' and contains(text(), '" + tab_name + "')]"
        self.click_element(locator)

    def input_house_name(self, house_name):
        self.input_text(task_table['楼盘名称输入框'], house_name, clear=True)
        sleep(1)

    def input_report_no(self, report_no):
        self.input_text(task_table['报备编号输入框'], report_no, clear=True)
        sleep(1)

    def click_search_btn(self):
        self.click_element(task_table['搜索按钮'], 2)

    def delete_records(self, house_name):
        self.search_records_by_name(house_name)
        ele_list = self.find_elements(task_table['删除按钮'])
        if len(ele_list) > 0:
            for ele in ele_list:
                sleep(1.5)
                ele.click()
                sleep(1)
                self.click_element(task_table['弹窗_删除按钮'], 3)
        else:
            logger.info('当前房源暂无相关数据')

    def click_add_report_btn(self):
        self.click_element(task_table['新增按钮'])

    def search_records_by_name(self, house_name):
        self.input_house_name(house_name)
        self.click_search_btn()

    def search_records_by_report_no(self, report_no):
        self.input_report_no(report_no)
        sleep(1)
        self.click_search_btn()

    def get_records_ele_by_house_name(self, house_name):
        locator = 'xpath', "//div[@style='' or not(@style)]//tbody[@class='ant-table-tbody']" \
                           "//td/div[text()='" + house_name + "']"
        ele_list = self.find_elements(locator)
        return ele_list

    def get_record_no_by_house_name(self, house_name):
        locator = 'xpath', "//div[text()='" + house_name + "']/parent::td/preceding-sibling::td//span"
        record_no = self.get_element_text(locator)
        return record_no

    def click_view_report_btn(self, record_no):
        locator = 'xpath', "//span[text()='" + record_no + "']/parent::td/following-sibling::td//a[contains(text()," \
                                                           "'查看')] "
        self.click_element(locator)

    def click_view_record_btn(self, record_no):
        locator = 'xpath', "//a[text()='" + record_no + "']/parent::td/following-sibling::td//a[contains(text()," \
                                                           "'查看')] "
        self.click_element(locator)

    def check_report_records_approved(self, record_no):
        locator = 'xpath', "//span[text()='" + record_no + "']/parent::td/following-sibling::td[contains(text()," \
                                                           "'审核通过')] "
        sleep(0.5)
        res = self.is_exists(locator)
        return res

    def check_records_to_be_reviewed(self, record_no):
        locator = 'xpath', "//a[text()='" + record_no + "']/parent::td/following-sibling::td[contains(text()," \
                                                           "'待审核')] "
        res = self.is_exists(locator)
        return res

    def check_records_approved(self, record_no):
        locator = 'xpath', "//a[text()='" + record_no + "']/parent::td/following-sibling::td[contains(text()," \
                                                           "'审核通过')] "
        sleep(0.5)
        res = self.is_exists(locator)
        return res

    def click_save_take_look_btn(self, record_no):
        locator = 'xpath', "//span[text()='" + record_no + "']/parent::td/following-sibling::td//a[contains(text()," \
                                                          "'录入带看')] "
        self.click_element(locator)

    def check_report_protection_period(self, record_no):
        locator = 'xpath', "//span[text()='" + record_no + "']/parent::td/following-sibling::td//span[contains(text()," \
                                                          "'录入带看')] "
        self.move_mouse_to_element(locator)
        res = self.is_exists(task_table['已过报备保护期弹窗'])
        return res

    def check_take_look_protection_period(self, record_no):
        locator = 'xpath', "//a[text()='" + record_no + "']/parent::td/following-sibling::td//span[contains(text()," \
                                                          "'录认购')] "
        self.move_mouse_to_element(locator)
        res = self.is_exists(task_table['已过带看保护期弹窗'])
        return res

    def click_save_subscribe_btn(self, record_no):
        locator = 'xpath', "//a[text()='" + record_no + "']/parent::td/following-sibling::td//a[contains(text()," \
                                                          "'录认购')] "
        self.click_element(locator)

    def click_upload_sign_btn(self, record_no):
        locator = 'xpath', "//a[text()='" + record_no + "']/parent::td/following-sibling::td//a[contains(text()," \
                                                          "'上传草网签')] "
        self.click_element(locator)

    def click_save_cell_btn(self, record_no):
        locator = 'xpath', "//a[text()='" + record_no + "']/parent::td/following-sibling::td//a[contains(text()," \
                                                          "'录成销')] "
        self.click_element(locator)

    def get_notice_description(self):
        self.get_element_text(task_table['右上角弹窗_内容'])
