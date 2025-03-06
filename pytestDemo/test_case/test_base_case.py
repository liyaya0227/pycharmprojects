import time

import pytest
from selenium import webdriver


class TestBaseCase():
    # 将初始化的代码封装，提高代码的复用性
    #setup类，每次项目执行之前只执行一次的操作
    def setup_class(self):
        self.driver = webdriver.Chrome(r'/Users/liyaya/Downloads/chromedriver')
    #setup方法，每条用例执行之前都会执行一次
    def setup_method(self):
        self.url = "http://testplt.share.atstudy.com/admin/login/?next=/admin/"
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)

    # teardown方法，每条用例执行之后都会执行一次
    def teardown_method(self):
        pass

    # teardown类，每次文件执行之后只执行一次
    def teardown_class(self):
        self.driver.quit()
