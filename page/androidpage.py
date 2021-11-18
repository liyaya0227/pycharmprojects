#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: androidpage.py
@date: 2021/09/29 0029
"""
from utils.logger import logger
from page.driveraction import DriverAction
from appium.webdriver.common.touch_action import TouchAction


class AndroidPage(DriverAction):

    def get_current_package(self):
        """
        获取当前包名
        """
        logger.info("获取当前包名")
        return self.driver.current_package

    def get_current_activity(self):
        """
        获取当前界面名
        """
        logger.info("获取当前界面名")
        return self.driver.current_activity

    def check_app_is_install(self, app_id):
        """
        查看App是否安装
        :param app_id AppID
        """
        logger.info("查看App是否安装")
        return self.driver.is_app_installed(app_id)

    def install_app(self, app_path):
        """
        安装APP
        :param app_path APP路径
        """
        logger.info("安装APP")
        self.driver.install_app(app_path)

    def uninstall_app(self, app_id):
        """
        卸载APP
        :param app_id AppID
        """
        logger.info("卸载APP")
        self.driver.remove_app(app_id)

    def open_app_activity(self, app_package, app_activity):
        """
        打开App
        :param app_package App包名
        :param app_activity App界面名
        """
        logger.info("打开App")
        self.driver.start_activity(app_package, app_activity)

    def back_previous_step(self):
        """
        设备按下返回键
        """
        logger.info("按下返回键")
        self.driver.press_keycode(4)

    def send_enter_key(self):
        """
        设备按下回车键
        """
        logger.info("按下回车键")
        self.driver.press_keycode(66)

    def __swipe(self, start_x, start_y, end_x, end_y, duration=1000):
        """
        滑动
        """
        try:
            self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        except Exception as e:
            raise e

    def down_swipe(self):
        """
        向下滑动
        """
        logger.info("向下滑动")
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']
        self.__swipe(width / 2, height * 4 / 8, width / 2, height * 7 / 8)

    def up_swipe(self):
        """
        向上滑动
        """
        logger.info("向上滑动")
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']
        self.__swipe(width / 2, height * 7 / 8, width / 2, height * 4 / 8)

    def move_element_to_offset(self, locator, x, y):
        """
        将元素移动过
        :param locator 元素定位
        :param x 横向移动像素
        :param y 纵向移动像素
        """
        logger.info("将元素移动过")
        element = self.find_element(locator)
        TouchAction(self.driver).press(element).move_to(x=x, y=y).release().perform()

    def open_notification(self):
        """打开手机通知栏"""
        self.driver.open_notifications()
