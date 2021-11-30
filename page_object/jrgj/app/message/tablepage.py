#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: tablepage.py
@date: 2021/11/12 0012
"""
from utils.timeutil import sleep
from page.androidpage import AndroidPage
from common.readelement import Element

message_table = Element('jrgj/app/message/table')


class AppMessageTablePage(AndroidPage):

    def click_message_tab(self):
        """点击消息标签"""
        self.click_element(message_table['消息标签'])

    def click_notification_tab(self):
        """点击通知标签"""
        self.click_element(message_table['通知标签'])

    def click_clear_message_button(self):
        """点击清除消息按钮"""
        self.click_element(message_table['清除消息按钮'])
        sleep(2)

    def go_system_message_list(self):
        """进入系统消息列表"""
        self.click_element(message_table['系统消息标签'])
        sleep(2)

    def go_house_message_list(self):
        """进入房源消息列表"""
        self.click_element(message_table['房源消息标签'])
        sleep(2)

    def go_customer_message_list(self):
        """进入客源消息列表"""
        self.click_element(message_table['客源消息标签'])
        sleep(2)

    def go_estate_dictionary_list(self):
        """进入楼盘字典列表"""
        self.click_element(message_table['楼盘字典标签'])
        sleep(2)

    def go_contract_message_list(self):
        """进入签约消息列表"""
        self.click_element(message_table['签约消息标签'])
        sleep(2)

    def get_system_message(self):
        """获取系统消息最新消息"""
        return self.get_element_text(message_table['系统消息最新内容'])

    def get_house_message(self):
        """获取房源消息最新消息"""
        return self.get_element_text(message_table['房源消息最新内容'])

    def get_customer_message(self):
        """获取客源消息最新消息"""
        return self.get_element_text(message_table['客源消息最新内容'])

    def get_estate_dictionary(self):
        """获取楼盘字典最新消息"""
        return self.get_element_text(message_table['楼盘字典最新内容'])

    def get_contract_message(self):
        """获取签约消息最新消息"""
        return self.get_element_text(message_table['签约消息最新内容'])

    def get_message_list_message_title_by_row(self, row: int = 1):
        """根据行，获取消息列表列表标题"""
        locator_xpath = "//*[@class='android.view.ViewGroup' and @index='4']" \
                        "//*[@class='android.view.ViewGroup' and @index='" + str(2 * row - 1) \
                        + "']//*[@class='android.widget.TextView' and @index=0]"
        return self.get_element_text(("xpath", locator_xpath))

    def get_message_list_message_content_by_row(self, row: int = 1):
        """根据行，获取消息列表列表内容"""
        locator_xpath = "//*[@class='android.view.ViewGroup' and @index='4']" \
                        "//*[@class='android.view.ViewGroup' and @index='" + str(2 * row - 1) \
                        + "']//*[@class='android.widget.TextView' and @index=1]"
        return self.get_element_text(("xpath", locator_xpath))

    def go_message_list_message_detail_by_row(self, row: int = 1):
        """根据行，进入消息详情界面"""
        locator_xpath = "//*[@class='android.view.ViewGroup' and @index='4']" \
                        "//*[@class='android.view.ViewGroup' and @index='" + str(2 * row - 1) \
                        + "']//*[@class='android.view.ViewGroup' and @index=0]"
        self.click_element(("xpath", locator_xpath))
        sleep(2)

    def get_message_detail_message_title(self):
        """获取消息详情界面消息标题"""
        return self.get_element_text(message_table['消息详情_标题标签'])

    def get_message_detail_message_type(self):
        """获取消息详情界面消息类型"""
        return self.get_element_text(message_table['消息详情_类型标签'])

    def get_message_detail_message_time(self):
        """获取消息详情界面消息时间"""
        return self.get_element_text(message_table['消息详情_时间标签'])

    def get_message_detail_message_content(self):
        """获取消息详情界面消息内容"""
        return self.get_element_text(message_table['消息详情_内容标签'])
