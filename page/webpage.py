#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: webpage.py
@time: 2021/06/22
"""

from config.conf import cm
from utils.logger import log
from utils.timeutil import sleep
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class WebPage(object):

    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        """打开网址并验证"""
        self.driver.set_page_load_timeout(60)
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            log.info("打开网页：%s" % url)
        except TimeoutException:
            raise TimeoutException("打开%s超时请检查网络或网址服务器" % url)

    @staticmethod
    def element_locator(func, locator):
        """元素定位器"""
        name, value = locator
        return func(cm.LOCATE_MODE[name], value)

    def find_element(self, locator, wait_time=10):
        """
        寻找单个元素
        """
        name, value = locator
        name = cm.LOCATE_MODE[name]
        try:
            # WebPage.element_locator(lambda *args: WebDriverWait(self.driver, wait_time).
            #                         until(EC.visibility_of_element_located(args)), locator)
            WebPage.element_locator(lambda *args: WebDriverWait(self.driver, timeout=wait_time, poll_frequency=0.4)
                                    .until(EC.presence_of_element_located(args)), locator)
            sleep(0.5)
            element = self.driver.find_element(name, value)
        # size = self.driver.get_window_size()
        # if element.location['y'] < size['height'] / 4:
        #     self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
        # if element.location['y'] > size['height'] - size['height'] / 10:
        #     self.driver.execute_script("arguments[0].scrollIntoView();", element)
            return element
        except TimeoutException:
            raise TimeoutException("未找到元素")

    def find_elements(self, locator, wait_time=10):
        """查找多个相同的元素"""
        name, value = locator
        name = cm.LOCATE_MODE[name]
        try:
            WebPage.element_locator(lambda *args: WebDriverWait(self.driver, timeout=wait_time, poll_frequency=0.4)
                                    .until(EC.presence_of_all_elements_located(args)), locator)
            sleep(0.5)
            elements = self.driver.find_elements(name, value)
            return elements
        except TimeoutException:
            return ''

    def element_is_exist(self, locator, wait_time=2):
        try:
            WebPage.element_locator(lambda *args: WebDriverWait(self.driver, wait_time, 0.5).
                                    until(EC.presence_of_element_located(args)), locator)
            return True
        except TimeoutException:
            return False

    def input_text(self, locator, txt, clear=False, enter=False):
        """
        输入
        clear: False不清空，True清空
        enter: False不回车，True回车
        """
        log.info("元素{}输入文本：{}".format(locator, txt))
        ele = self.find_element(locator)
        if clear:
            ele.send_keys(Keys.CONTROL + 'A')
            ele.send_keys(Keys.DELETE)
        ele.send_keys(txt)
        if enter:
            ele.send_keys(Keys.ENTER)

    def input_text_with_enter(self, locator, txt):
        """输入后回车"""
        log.info("元素{}输入文本：{}".format(locator, txt))
        ele = self.find_element(locator)
        ele.send_keys(txt)
        ele.send_keys(Keys.ENTER)

    def clear_text(self, locator):
        """清空文本"""
        log.info("元素{}文本清空".format(locator))
        ele = self.find_element(locator)
        ele.send_keys(Keys.CONTROL + 'A')
        ele.send_keys(Keys.DELETE)

    def send_enter_key(self, locator):  # 按回车键
        """输入回车键"""
        log.info("元素{}输入回车键".format(locator))
        ele = self.find_element(locator)
        ele.send_keys(Keys.ENTER)

    def send_key(self, locator, file_path):
        """上传文件"""
        log.info("元素{}".format(locator))
        ele = self.find_element(locator)
        ele.send_keys(file_path)

    def is_click(self, locator, sleep_time=0):
        """点击"""
        log.info("点击元素：{}".format(locator))
        ele = self.find_element(locator)
        ele.click()
        if sleep_time != 0:
            sleep(sleep_time)

    def element_text(self, locator):
        """获取当前的text"""
        ele = self.find_element(locator)
        _text = ele.text
        log.info("获取元素{}文本：{}".format(locator, _text))
        return _text

    def get_element_attribute(self, locator, attribute):
        """获取当前的text"""
        ele = self.find_element(locator)
        _text = ele.get_attribute(attribute)
        log.info("获取元素{}属性的{}：{}".format(locator, attribute, _text))
        return _text
    #
    # @property
    # def get_source(self):
    #     """获取页面源代码"""
    #     return self.driver.page_source

    def refresh(self):
        """刷新页面F5"""
        self.driver.refresh()
        sleep()
        self.driver.implicitly_wait(30)

    def move_mouse_to_element(self, locator):
        ele = self.find_element(locator)
        action = ActionChains(self.driver)
        action.move_to_element(ele).perform()

    def move_mouse_to_offset(self, x, y):
        action = ActionChains(self.driver)
        action.move_by_offset(x, y).perform()

    def mouse_left_click(self):
        ActionChains(self.driver).click().release().perform()

    def keyboard_send_esc(self):
        ActionChains(self.driver).key_down(Keys.ESCAPE).key_up(Keys.ESCAPE).perform()

    def execute_js_script(self, js):
        self.driver.execute_script(js)
        sleep()

    def wait_page_loading_complete(self):
        log.info("等待页面加载完成")
        while self.driver.execute_script("return document.readyState") != 'complete':
            sleep()

    def scroll_to_top(self):
        self.execute_js_script("var q=document.documentElement.scrollTop=0")
        sleep()

    def scroll_to_bottom(self):
        self.execute_js_script("var q=document.documentElement.scrollTop=100000")
        sleep()

    def select_element_choose_by_value(self, locator, value):
        """Select元素选择"""
        self.is_click(locator)
        ele = self.find_element(locator)
        Select(ele).select_by_value(value)

    def is_exists(self, locator):
        """
        元素是否存在(DOM)
        如元素不存在直接返回false，程序不退出
        """
        try:
            WebPage.element_locator(lambda *args: EC.presence_of_element_located(args)(self.driver), locator)
            return True
        except NoSuchElementException:
            return False

    def click_blank_area(self):
        """点击页面空白区域"""
        actions = ActionChains(self.driver)
        actions.move_by_offset(0, 0).click().perform()

    def alert_exists(self):
        """判断弹框是否出现，并返回弹框的文字"""
        alert = EC.alert_is_present()(self.driver)
        if alert:
            text = alert.text
            # log.info("Alert弹窗提示为：%s" % text)
            alert.accept()
            return text
        else:
            return False
