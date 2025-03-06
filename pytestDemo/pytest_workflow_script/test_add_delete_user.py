import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

#添加用户场景&删除用户场景pytest封装
#传递username这个参数，并删除
class Test_Add_Delete_User():
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
    #添加固件标签，不添加不能传递参数
    @pytest.fixture()
    def test_Add_User(self):
        self.url = "http://testplt.share.atstudy.com/admin/auth/user/add/"
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)
        username = 'liyaya1'
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password1').send_keys('li111111')
        self.driver.find_element(By.NAME, 'password2').send_keys('li111111')
        self.driver.find_element(By.XPATH, '//*[@id="user_form"]/div/div/input[1]').click()
        return username

    # 删除用户
    def test_Delete_User(self, test_Add_User):
        self.url = "http://testplt.share.atstudy.com/admin/auth/user/"
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)
        # 在页面上的列表如何获取想要的元素
        # 需要遍历列表中的元素，获取与自己想要元素相匹配的
        # 遍历列表：获取列表长度
        num = len(self.driver.find_elements(By.CLASS_NAME, 'field-username'))
        # 遍历列表
        for i in range(1, num + 1):
            time.sleep(1)
            # 查看每个元素的值 ：因为无法定位，只能根据xpath，来获取每个值：//*[@id="result_list"]/tbody/tr[1]/th/a
            usrname = self.driver.find_element(By.XPATH, '//*[@id="result_list"]/tbody/tr[' + str(i) + ']/th/a').text
            print(usrname)
            if usrname == test_Add_User:
                time.sleep(1)
                # 找到元素之后点击元素
                self.driver.find_element(By.XPATH, '//*[@id="result_list"]/tbody/tr[' + str(i) + ']/th/a').click()
                # 点击删除按钮
                time.sleep(1)
                self.driver.find_element(By.XPATH, '//*[@id="user_form"]/div/div/p/a').click()
                # 找到元素之后点击，会进入新的页面，需要切换窗口：用switch_to.window(handle)
                # 获取新页面的句柄
                self.driver.switch_to.window(self.driver.window_handles[-1])
                # 点击确认按钮
                self.driver.find_element(By.XPATH, '//*[@id="content"]/form/div/input[2]').click()
                break


    #setup方法，每条用例执行之前都会执行一次
    def setup_method(self):
        pass

    # teardown方法，每条用例执行之后都会执行一次
    def teardown_method(self):
        pass

    # teardown类，每次文件执行之后只执行一次
    def teardown_class(self):
        self.driver.quit()



