import unittest2
from selenium.webdriver.common.by import By

from func.csvFileManager2 import reader
from test_case.BaseTestCase import BaseTestCase


class RegisterTest(BaseTestCase):
    def test_Register(self):
        table = reader("register_data_cases.csv")
        for item in table:
            self.driver.get("http://129.211.129.101:9007/index.php?m=user&c=public&a=reg")
            self.driver.find_element(By.NAME, 'username').send_keys(item[0])
            self.driver.find_element(By.NAME, 'password').send_keys(item[1])
            self.driver.find_element(By.NAME, 'userpassword2').send_keys(item[2])
            self.driver.find_element(By.NAME, 'mobile_phone').send_keys(item[3])
            self.driver.find_element(By.NAME, 'email').send_keys(item[4])
            #self.driver.find_element(By.CSS_SELECTOR, '.reg_btn').click()