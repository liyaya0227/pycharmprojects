import time
import pytest
from selenium import webdriver

from selenium.webdriver.common.by import By

#from test_case.test_base_case import TestBaseCase
#使用pytest的注意事项
#1，文件名必须以test_为开头
#2，类名必须以Test为开头
#3，方法名必须以test_为开头
from test_case.test_base_case import TestBaseCase


class TestLogin(TestBaseCase):
    '''def test_Login(self):
        self.driver.get("https://uat-passport.jingrizf.com/login")
        self.driver.find_element(By.CSS_SELECTOR, '.ant-input-affix-wrapper input').send_keys('127csjjr')
        self.driver.find_element(By.CSS_SELECTOR, '.ant-input-password input').send_keys('111111')
        self.driver.find_element(By.CSS_SELECTOR, '.lgbutton').click()'''

    #通过数据驱动来执行多个测试用例
    #第二种是：不同的测试数据，不同的处理过程
    #参数的数据驱动化
    @pytest.mark.parametrize('username,password', (["atstudy", "51testing"], ["lijiahui", "111111"]))
    def test_Login01(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/input').click()
        time.sleep(3)

        #print(self.driver.current_url)

        #解决异常的三种方法

        try:
            usr = self.driver.find_element(By.CSS_SELECTOR, '#user-tools > strong').text
            assert usr == "ATSTUDY"
        except Exception as e:
            print(e)
            usr = self.driver.find_element(By.CSS_SELECTOR, '.site-nav-right > a:nth-child(1)').text
            assert "登录" in usr


if __name__ == '__main__':
    pytest.main("-v")







