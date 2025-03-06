import time
import pytest
from selenium import webdriver

from selenium.webdriver.common.by import By

#from test_case.test_base_case import TestBaseCase
#使用pytest的注意事项
#1，文件名必须以test_为开头
#2，类名必须以Test为开头
#3，方法名必须以test_为开头
from DDT_test.ddtfilereader1 import get_userinfo


class TestLogin():
    def setup_method(self):
        self.driver = webdriver.Chrome(r'/Users/liyaya/Downloads/chromedriver')
        self.url = "http://testplt.share.atstudy.com/admin/login/?next=/admin/"
        self.driver.get(self.url)
        #self.driver.implicitly_wait(2)

    #通过数据驱动来执行多个测试用例
    #第一种是：不同的测试数据，统一的检查点
    #参数的数据驱动化
    #condition = '冒烟'
    #@pytest.mark.skipif(condition=='冒烟', reason='不进行冒烟测试')
    #@pytest.mark.smoke1
    #@pytest.mark.parametrize('username,password,state', (["atstudy", "51testing", 0], ["lijiahui", "111111", 1]))
    @pytest.mark.parametrize("userinfo", get_userinfo())
    def test_Login01(self, userinfo):
        print(userinfo["username"])
        self.driver.find_element(By.NAME, 'username').send_keys(userinfo["username"])
        self.driver.find_element(By.NAME, 'password').send_keys(userinfo["password"])
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/input').click()
        time.sleep(3)
        #print(self.driver.current_url)

        #解决异常的三种方法

        #2、知道有异常无法登陆，可以直接判断url和之前的一致就可以了
        '''if state == 0:
            assert self.driver.current_url != self.url
        else:
            assert self.driver.current_url == self.url'''
    def teardown_method(self):
        self.driver.quit()

if __name__ == '__main__':
    pytest.main("-v")







