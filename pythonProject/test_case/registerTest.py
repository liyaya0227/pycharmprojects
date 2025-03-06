import unittest2
from selenium.webdriver.common.by import By

from test_case.BaseTestCase import BaseTestCase


class RegisterTest(BaseTestCase):
    def test_Register(self):
        self.driver.get("http://129.211.129.101:9007/index.php?m=user&c=public&a=reg")
        self.driver.find_element(By.NAME, 'username').send_keys('liyaya')
        self.driver.find_element(By.NAME, 'password').send_keys('111111')
        self.driver.find_element(By.NAME, 'userpassword2').send_keys('111111')
        self.driver.find_element(By.NAME, 'mobile_phone').send_keys('18300987709')
        self.driver.find_element(By.NAME, 'email').send_keys('liyaya@123.com')
        self.driver.find_element(By.CSS_SELECTOR, '.reg_btn').click()