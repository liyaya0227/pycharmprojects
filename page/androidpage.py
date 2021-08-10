# -*- coding:utf-8 -*-
"""
Author: zoro ju
"""
import time
from selenium.webdriver.support.wait import WebDriverWait


class AndroidPage(object):
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, wait_time=30):  # 单个元素定位
        try:
            element = WebDriverWait(self.driver, wait_time).until(lambda x: x.find_element(*locator))
            return element
        except Exception as e:
            raise e

    def find_elements(self, locator, wait_time=30):  # 多个元素定位
        try:
            elements = WebDriverWait(self.driver, wait_time).until(lambda x: x.find_elements(*locator))
            return elements
        except Exception as e:
            raise e

    def is_click(self, locator):  # 点击元素
        print("[info:clicking element '{}']".format(locator))
        try:
            element = self.find_element(locator)
            element.click()
            time.sleep(2)
        except Exception as e:
            raise e

    def clear_text(self, locator):  # 清空元素内容
        print("[info:clearing element '{}' value]".format(locator))
        try:
            element = self.find_element(locator)
            element.clear()
        except Exception as e:
            raise e

    def input_text(self, locator, value='', click=False, clear=False):  # 元素输入内容
        print("[info:input value '{}' in element '{}']".format(value, locator))
        try:
            element = self.find_element(locator)
            if click:
                element.click()
                time.sleep(1)
            if clear:
                element.clear()
                time.sleep(1)
            element.send_keys(value)
            time.sleep(1)
        except AttributeError as e:
            raise e

    def swipe(self, start_x, start_y, end_x, end_y, duration=1000):  # 滑动
        try:
            self.driver.swipe(start_x, start_y, end_x, end_y, duration)
            time.sleep(1)
        except Exception as e:
            raise e

    def down_swipe(self):  # 下滑
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']
        self.swipe(width / 2, height * 4 / 8, width / 2, height * 7 / 8)
        time.sleep(1)

    def up_swipe(self):  # 上滑
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']
        self.swipe(width / 2, height * 7 / 8, width / 2, height * 4 / 8)
        time.sleep(1)

    def get_element_attribute(self, locator, attribute=None):  # 获取元素属性值
        try:
            element = self.find_element(locator)
            if attribute:
                return element.get_attribute(attribute)
            else:
                return element.text
        except Exception as e:
            raise e
