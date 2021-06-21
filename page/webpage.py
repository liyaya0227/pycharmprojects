# -*- coding:utf-8 -*-
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from config.conf import cm
from utils.times import sleep
from utils.logger import log


class WebPage(object):

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 20
        self.wait = WebDriverWait(self.driver, self.timeout)

    def open_url(self, url):
        """打开网址并验证"""
        self.driver.maximize_window()
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

    def find_element(self, locator):
        """寻找单个元素"""
        element = WebPage.element_locator(lambda *args: self.wait.until(EC.presence_of_element_located(args)), locator)
        # size = self.driver.get_window_size()
        # if element.location['y'] < size['height'] / 4:
        #     self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
        # if element.location['y'] > size['height'] - size['height'] / 10:
        #     self.driver.execute_script("arguments[0].scrollIntoView();", element)
        return element

    def find_elements(self, locator):
        """查找多个相同的元素"""
        return WebPage.element_locator(lambda *args: self.wait.until(
            EC.presence_of_all_elements_located(args)), locator)

    def elements_num(self, locator):
        """获取相同元素的个数"""
        number = len(self.find_elements(locator))
        log.info("相同元素：{}".format((locator, number)))
        return number

    def input_text(self, locator, txt):
        """输入(输入前先清空)"""
        log.info("元素{}输入文本：{}".format(locator, txt))
        sleep(0.5)
        ele = self.find_element(locator)
        ele.clear()
        ele.send_keys(txt)

    def send_enter_key(self, locator):  # 按回车键
        """输入回车键"""
        log.info("元素{}输入回车键".format(locator))
        ele = self.find_element(locator)
        ele.send_keys(Keys.ENTER)
        sleep()

    def is_click(self, locator):
        """点击"""
        log.info("点击元素：{}".format(locator))
        self.find_element(locator).click()
        sleep()

    def element_text(self, locator):
        """获取当前的text"""
        _text = self.find_element(locator).text
        log.info("获取元素{}文本：{}".format(locator, _text))
        return _text

    def get_element_attribute(self, locator, attribute):
        """获取当前的text"""
        _text = self.find_element(locator).get_attribute(attribute)
        log.info("获取元素{}属性的{}：{}".format(locator, attribute, _text))
        return _text

    @property
    def get_source(self):
        """获取页面源代码"""
        return self.driver.page_source

    def refresh(self):
        """刷新页面F5"""
        self.driver.refresh()
        self.driver.implicitly_wait(30)

    def move_mouse_to_element(self, locator):
        ele = self.find_element(locator)
        action = ActionChains(self.driver)
        action.move_to_element(ele).perform()
        sleep(0.5)

    def move_mouse_to_offset(self, x, y):
        action = ActionChains(self.driver)
        action.move_by_offset(x, y).perform()
        sleep(0.5)
