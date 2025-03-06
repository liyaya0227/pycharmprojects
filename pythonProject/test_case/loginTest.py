import time
import unittest2
from selenium import webdriver

from selenium.webdriver.common.by import By

from test_case.BaseTestCase import BaseTestCase


class TestLogin(BaseTestCase):
    '''def test_Login(self):
        self.driver.get("https://uat-passport.jingrizf.com/login")
        self.driver.find_element(By.CSS_SELECTOR, '.ant-input-affix-wrapper input').send_keys('127csjjr')
        self.driver.find_element(By.CSS_SELECTOR, '.ant-input-password input').send_keys('111111')
        self.driver.find_element(By.CSS_SELECTOR, '.lgbutton').click()'''

    def test_Login(self):
        self.driver.get("http://129.211.129.101:9007/index.php?m=user&c=public&a=login")
        self.driver.find_element(By.ID, 'username').send_keys('liyaya')
        self.driver.find_element(By.ID, 'password').send_keys('111111')
        self.driver.find_element(By.CLASS_NAME, 'login_btn').click()
        time.sleep(3)
        print(self.driver.title)
        print(self.driver.current_url)
        usr = self.driver.find_element(By.CSS_SELECTOR, '.site-nav-right > a:nth-child(1)').text
        search = self.driver.find_element(By.CSS_SELECTOR, '.btn1').get_attribute("value")
        print(usr)
        print(search)
        self.assertEqualsa("我的会员中心 - 道e坊商城 - Powered by Haidao", self.driver.title)
        self.assertEqualsa("http://129.211.129.101:9007/index.php?m=user&c=public&a=login", self.driver.current_url)
        self.assertEqualsa("您好 liyaya", usr)
        self.assertEqualsa("搜    索", search)


