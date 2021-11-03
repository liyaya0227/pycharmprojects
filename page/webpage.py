#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: webpage.py
@time: 2021/06/22
"""
from utils.logger import logger
from utils.timeutil import sleep
from page.driveraction import DriverAction
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class WebPage(DriverAction):

    def open_url(self, url):
        """打开网址并验证"""
        self.driver.set_page_load_timeout(60)
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            logger.info("打开网页：%s" % url)
        except TimeoutException:
            raise TimeoutException("打开%s超时请检查网络或网址服务器" % url)

    def get_current_url(self):
        """获取当前URL"""
        return self.driver.current_url

    # @staticmethod
    # def element_locator(func, locator):
    #     """元素定位器"""
    #     name, value = locator
    #     return func(cm.LOCATE_MODE[name], value)
    #
    # def find_element(self, locator, wait_time=10):
    #     """
    #     寻找单个元素
    #     """
    #     name, value = locator
    #     name = cm.LOCATE_MODE[name]
    #     try:
    #         # WebPage.element_locator(lambda *args: WebDriverWait(self.driver, wait_time).
    #         #                         until(EC.visibility_of_element_located(args)), locator)
    #         WebPage.element_locator(lambda *args: WebDriverWait(self.__driver, timeout=wait_time, poll_frequency=0.4)
    #                                 .until(EC.presence_of_element_located(args)), locator)
    #         sleep(0.5)
    #         element = self.__driver.find_element(name, value)
    #     # size = self.driver.get_window_size()
    #     # if element.location['y'] < size['height'] / 4:
    #     #     self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
    #     # if element.location['y'] > size['height'] - size['height'] / 10:
    #     #     self.driver.execute_script("arguments[0].scrollIntoView();", element)
    #         return element
    #     except TimeoutException:
    #         raise TimeoutException("未找到元素")
    #
    # def find_elements(self, locator, timeout=10):
    #     """查找多个相同的元素"""
    #     name, value = locator
    #     name = cm.LOCATE_MODE[name]
    #     try:
    #         WebPage.element_locator(lambda *args: WebDriverWait(self.__driver, timeout=timeout, poll_frequency=0.4)
    #                                 .until(EC.presence_of_all_elements_located(args)), locator)
    #         sleep(0.5)
    #         elements = self.__driver.find_elements(name, value)
    #         return elements
    #     except TimeoutException:
    #         return ''

    def element_is_exist(self, locator, timeout=2):
        """
        判断元素存不存在
        """
        try:
            WebPage.element_locator(lambda *args: WebDriverWait(self.driver, timeout, 0.5).
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
        logger.info("元素{}输入文本：{}".format(locator, txt))
        ele = self.find_element(locator)
        if clear:
            ele.send_keys(Keys.CONTROL + 'A')
            ele.send_keys(Keys.DELETE)
        ele.send_keys(txt)
        if enter:
            ele.send_keys(Keys.ENTER)

    def input_text_with_enter(self, locator, txt):
        """输入后回车"""
        logger.info("元素{}输入文本：{}".format(locator, txt))
        ele = self.find_element(locator)
        ele.send_keys(txt)
        ele.send_keys(Keys.ENTER)

    def clear_text(self, locator):
        """清空文本"""
        logger.info("元素{}文本清空".format(locator))
        ele = self.find_element(locator)
        ele.send_keys(Keys.CONTROL + 'A')
        ele.send_keys(Keys.DELETE)

    def send_enter_key(self, locator):  # 按回车键
        """输入回车键"""
        logger.info("元素{}输入回车键".format(locator))
        ele = self.find_element(locator)
        ele.send_keys(Keys.ENTER)

    def send_key(self, locator, file_path):
        """上传文件"""
        logger.info("元素{}输入".format(locator))
        ele = self.find_element(locator)
        ele.send_keys(file_path)

    def click_element(self, locator, sleep_time=0.5):
        """点击元素"""
        logger.info("点击元素:{}".format(locator))
        self.find_element(locator).click()
        sleep(sleep_time)
    #
    # def get_element_text(self, locator):
    #     """获取元素的text"""
    #     logger.info("获取({})元素文本值".format(locator))
    #     return self.find_element(locator).text
    #
    # def get_element_attribute(self, locator, attribute_name):
    #     """获取元素属性的值"""
    #     logger.info("获取({})元素属性的{}".format(locator, attribute_name))
    #     return self.find_element(locator).get_attribute(attribute_name)

    def remove_element_attribute(self, locator, attribute):
        """移除元素属性"""
        ele = self.find_element(locator)
        self.driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", ele, 'class',
                                   'ant-input')
        self.driver.execute_script("arguments[0].removeAttribute(arguments[1])",
                                   ele, attribute)

    def set_element_attribute(self, locator, attribute, value):
        """修改元素属性"""
        ele = self.find_element(locator)
        self.driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", ele, attribute,
                                   value)

    # @property
    # def get_source(self):
    #     """获取页面源代码"""
    #     return self.driver.page_source

    def browser_refresh(self):
        """刷新页面F5"""
        self.driver.refresh()
        self.driver.implicitly_wait(30)

    def move_mouse_to_element(self, locator):
        """鼠标移动到元素"""
        ele = self.find_element(locator)
        ActionChains(self.driver).move_to_element(ele).perform()

    def move_mouse_to_offset(self, x, y):
        """鼠标移动到像素"""
        ActionChains(self.driver).move_by_offset(x, y).perform()

    def mouse_left_click(self):
        """鼠标左击"""
        ActionChains(self.driver).click().release().perform()

    def keyboard_send_esc(self):
        ActionChains(self.driver).key_down(Keys.ESCAPE).key_up(Keys.ESCAPE).perform()

    def execute_js_script(self, js):
        return self.driver.execute_script(js)

    def wait_page_loading_complete(self):
        logger.info("等待页面加载完成")
        while self.driver.execute_script("return document.readyState") != 'complete':
            sleep()

    def scroll_to_top(self):
        self.execute_js_script("var q=document.documentElement.scrollTop=0")

    def scroll_to_bottom(self):
        self.execute_js_script("var q=document.documentElement.scrollTop=100000")

    def is_exists(self, locator):
        """
        元素是否存在(DOM)
        如元素不存在直接返回false
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
        """
        判断弹框是否出现
        """
        try:
            WebDriverWait(self.driver, 10, 1).until(EC.alert_is_present())
            return True
        except TimeoutException:
            return False
