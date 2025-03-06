import time

from selenium import webdriver
from selenium.webdriver.common.by import By


class Test_Add_Group_User():
    #登录
    def setup_class(self):
        self.driver = webdriver.Chrome(r'/Users/liyaya/Downloads/chromedriver')
        self.url = "http://testplt.share.atstudy.com/admin/login/?next=/admin/"
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)
        self.driver.find_element(By.NAME, 'username').send_keys('atstudy')
        self.driver.find_element(By.NAME, 'password').send_keys('51testing')
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/input').click()


    #添加用户
    def test_Add_User(self):
        self.url = "http://testplt.share.atstudy.com/admin/auth/user/add/"
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)
        self.driver.find_element(By.NAME, 'username').send_keys('liyaya1')
        self.driver.find_element(By.NAME, 'password1').send_keys('li111111')
        self.driver.find_element(By.NAME, 'password2').send_keys('li111111')
        self.driver.find_element(By.XPATH, '//*[@id="user_form"]/div/div/input[1]').click()



    #setup方法，每条用例执行之前都会执行一次
    def setup_method(self):
        pass

    # teardown方法，每条用例执行之后都会执行一次
    def teardown_method(self):
        pass

    # teardown类，每次文件执行之后只执行一次
    def teardown_class(self):
        self.driver.quit()



