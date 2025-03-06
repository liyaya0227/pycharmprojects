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
    '''def test_Login(self):
        self.driver.get("https://uat-passport.jingrizf.com/login")
        self.driver.find_element(By.CSS_SELECTOR, '.ant-input-affix-wrapper input').send_keys('127csjjr')
        self.driver.find_element(By.CSS_SELECTOR, '.ant-input-password input').send_keys('111111')
        self.driver.find_element(By.CSS_SELECTOR, '.lgbutton').click()'''

    #通过数据驱动来执行多个测试用例
    #第一种是：不同的测试数据，统一的检查点
    #参数的数据驱动化
    condition = '冒烟'
    @pytest.mark.skipif(condition=='冒烟', reason='不进行冒烟测试')
    #@pytest.mark.smoke1
    @pytest.mark.parametrize('username,password,state', (["atstudy", "51testing", 0], ["lijiahui", "111111", 1]))
    def test_Login01(self, username, password, state):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/input').click()
        time.sleep(3)
        #print(self.driver.current_url)

        #解决异常的三种方法

        #2、知道有异常无法登陆，可以直接判断url和之前的一致就可以了
        if state == 0:
            assert self.driver.current_url != self.url
        else:
            assert self.driver.current_url == self.url

if __name__ == '__main__':
    pytest.main("-v")







