#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: driveraction.py
@date: 2021/10/29 0029
"""
import allure
from config.conf import cm
from utils.logger import logger
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DriverAction(object):

    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def element_locator(func, locator):
        """元素定位器"""
        name, value = locator
        return func(cm.LOCATE_MODE[name], value)

    def get_window_size(self):
        """
        获取屏幕分辨率
        """
        return self.driver.get_window_size()

    def screen_shot(self, file_path):
        """
        截取当前窗口，保存为图片
        :param  file_path 图片保存路径
        """
        self.driver.get_screenshot_as_file(file_path)

    def implicitly_wait(self, second):
        """
        隐式等待
        :param second 等待时间，单位：s
        """
        self.driver.implicitly_wait(second)

    def find_element(self, locator, timeout=10, poll_frequency=0.5):
        """
        查找单个元素
        :param locator 元素定位
        :param  timeout 查找元素的过期时间，单位：s
        :param  poll_frequency 查找元素频率 单位：s
        """
        try:
            return self.element_locator(lambda *args: WebDriverWait(self.driver, timeout=timeout,
                                                                    poll_frequency=poll_frequency)
                                        .until(EC.presence_of_element_located(args)), locator)
        except TimeoutException:
            screen_path = cm.screen_path
            self.screen_shot(screen_path)
            allure.attach.file(screen_path, "失败截图", allure.attachment_type.PNG)
            raise TimeoutException("未找到元素({})".format(locator))

    def find_elements(self, locator, timeout: int = 10, poll_frequency=0.5):
        """查找多个相同的元素"""
        try:
            return self.element_locator(lambda *args: WebDriverWait(self.driver, timeout=timeout,
                                                                    poll_frequency=poll_frequency)
                                        .until(EC.presence_of_all_elements_located(args)), locator)
        except TimeoutException:
            return []

    def check_element_is_exist(self, locator, timeout=2):
        """
        判断元素存不存在
        """
        try:
            self.element_locator(lambda *args: WebDriverWait(self.driver, timeout, 0.5)
                                 .until(EC.presence_of_element_located(args)), locator)
            return True
        except TimeoutException:
            return False

    def click_element(self, locator):
        """
        点击元素
        :param locator 元素定位
        """
        logger.info('点击元素({})'.format(locator))
        self.find_element(locator).click()

    def input_text_into_element(self, locator, text):
        """
        对元素输入文本内容，或上传图片
        :param locator 元素定位
        :param text 输入内容
        """
        logger.info("元素({})输入文本：{}".format(locator, text))
        self.find_element(locator).send_keys(text)

    def clear_element_text(self, locator):
        """
        清空元素文本内容
        :param locator 元素定位
        """
        logger.info("元素({})清空文本内容".format(locator))
        self.find_element(locator).claer()

    def get_element_attribute(self, locator, attribute_name):
        """
        获取元素属性的值
        :param locator 元素定位
        :param  attribute_name 属性名
        """
        logger.info("获取({})元素属性的{}".format(locator, attribute_name))
        return self.find_element(locator).get_attribute(attribute_name)

    def get_element_text(self, locator):
        """
        获取元素文本内容
        :param locator 元素定位
        """
        logger.info("获取({})元素文本内容".format(locator))
        return self.find_element(locator).text

    def get_element_location(self, locator):
        """
        获取元素位置
        :param locator 元素定位
        """
        logger.info("获取({})元素文本内容".format(locator))
        return self.find_element(locator).location

    def get_element_size(self, locator):
        """
        获取元素大小
        :param locator 元素定位
        """
        logger.info("获取({})元素文本内容".format(locator))
        return self.find_element(locator).size
