import time

import pytest
from selenium.webdriver.common.by import By

#from test_case.test_base_case import TestBaseCase
#使用pytest的注意事项
#1，文件名必须以test_为开头
#2，类名必须以Test为开头
#3，方法名必须以test_为开头
from test_script.login.test_base_case import TestBaseCase


class TestLogin(TestBaseCase):

    #正确登陆测试
    def test_Login01(self):

        self.driver.find_element(By.NAME, 'username').send_keys('atstudy')
        self.driver.find_element(By.NAME, 'password').send_keys('51testing')
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/input').click()
        time.sleep(3)
        print(self.driver.current_url)
        usr = self.driver.find_element(By.CSS_SELECTOR, '#user-tools > strong').text
        print(usr)
        assert self.driver.current_url == "http://testplt.share.atstudy.com/admin/"
        assert usr == "ATSTUDY"


    # 异常登陆测试
    def test_Login02(self):

        self.driver.find_element(By.NAME, 'username').send_keys('lijiahui')
        self.driver.find_element(By.NAME, 'password').send_keys('111111')
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/input').click()
        time.sleep(3)
        print(self.driver.current_url)

        #解决异常的三种方法
        #1、try： except Exception as e：
        '''try:
            usr = self.driver.find_element(By.CSS_SELECTOR, '#user-tools > strong').text
            print(usr)
            assert self.driver.current_url == "http://testplt.share.atstudy.com/admin/"
            assert usr == "ATSTUDY"
        except Exception as e:
            print(e)
        else:
            print('程序有错误哦')'''
        #2、知道有异常无法登陆，可以直接判断url和之前的一致就可以了
        assert self.driver.current_url == self.url
        #3、重新获取失败后会出现的断言
        '''assert a in b'''





