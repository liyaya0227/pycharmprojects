import time

from selenium import webdriver
from selenium.webdriver.common.by import By



class Add_Group_User():
    #登录
    def test_Login(self):
        self.driver = webdriver.Chrome(r'/Users/liyaya/Downloads/chromedriver')
        self.url = "http://testplt.share.atstudy.com/admin/login/?next=/admin/"
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)
        self.driver.find_element(By.NAME, 'username').send_keys('atstudy')
        self.driver.find_element(By.NAME, 'password').send_keys('51testing')
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/input').click()
    #添加组
    def test_Add_Group(self):
        self.url = "http://testplt.share.atstudy.com/admin/auth/group/add/"
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)
        self.driver.find_element(By.CLASS_NAME, 'vTextField').send_keys('pig')
        self.driver.find_element(By.XPATH, '//*[@id="group_form"]/div/div/input[1]').click()

    #添加用户
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
    def test_Delete_User(self, username):
        self.url = "http://testplt.share.atstudy.com/admin/auth/user/"
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)
        #在页面上的列表如何获取想要的元素
        #需要遍历列表中的元素，获取与自己想要元素相匹配的
        #遍历列表：获取列表长度
        num = len(self.driver.find_elements(By.CLASS_NAME, 'field-username'))
        #遍历列表
        for i in range(1, num+1):
            time.sleep(1)
            #查看每个元素的值 ：因为无法定位，只能根据xpath，来获取每个值：//*[@id="result_list"]/tbody/tr[1]/th/a
            usrname = self.driver.find_element(By.XPATH, '//*[@id="result_list"]/tbody/tr[' + str(i) + ']/th/a').text
            print(usrname)
            if usrname == username:
                time.sleep(1)
                #找到元素之后点击元素
                self.driver.find_element(By.XPATH, '//*[@id="result_list"]/tbody/tr[' + str(i) + ']/th/a').click()
                #点击删除按钮
                time.sleep(1)
                self.driver.find_element(By.XPATH, '//*[@id="user_form"]/div/div/p/a').click()
                # 找到元素之后点击，会进入新的页面，需要切换窗口：用switch_to.window(handle)
                # 获取新页面的句柄
                self.driver.switch_to.window(self.driver.window_handles[-1])
                #点击确认按钮
                self.driver.find_element(By.XPATH, '//*[@id="content"]/form/div/input[2]').click()
                break


if __name__ == '__main__':
    obj = Add_Group_User()
    obj.test_Login()
    user = obj.test_Add_User()
    #obj.test_Add_Group()
    obj.test_Delete_User(user)


