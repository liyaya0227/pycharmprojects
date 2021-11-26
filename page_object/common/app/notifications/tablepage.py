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


class AppNotificationsTablePage(AndroidPage):

    def get_notification_title_by_row(self, row=1):
        """根据行，获取通知标题"""
        locator_xpath = 'xpath', "(//*[@resource-id='com.android.systemui:id/notification_stack_scroller']" \
                                 "//*[@resource-id='com.android.systemui:id/notification_title' " \
                                 "or @resource-id='android:id/title'])[" + str(row) + "]"
        return self.get_element_text(locator_xpath)

    def get_notification_content_by_row(self, row=1):
        """根据行，获取通知内容"""
        locator_xpath = "(//*[@resource-id='com.android.systemui:id/notification_stack_scroller']" \
                        "//*[@resource-id='com.android.systemui:id/notification_text' " \
                        "or @resource-id='android:id/text'])[" + str(row) + "]"
        return self.get_element_text(('xpath', locator_xpath))

    def dismiss_all_notification(self):
        """清除所有通知"""
        no_notifications_xpath = "//*[@resource-id='com.android.systemui:id/no_notifications']"
        if self.check_element_exist(('xpath', no_notifications_xpath)):
            self.up_swipe()
            sleep()
        else:
            locator_xpath = "//*[@resource-id='com.android.systemui:id/clear_all_port' " \
                            "or @resource-id='com.android.systemui:id/dismiss_text']"
            while not self.check_element_exist(('xpath', locator_xpath)):
                self.up_swipe()
                sleep()
            self.click_element(('xpath', locator_xpath))
            sleep(2)
