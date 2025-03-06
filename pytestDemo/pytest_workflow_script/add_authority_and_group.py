import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class Add_authority_and_group():
    # 登录
    def test_Login(self):
        self.driver = webdriver.Chrome(r'/Users/liyaya/Downloads/chromedriver')
        self.url = "http://testplt.share.atstudy.com/admin/login/?next=/admin/"
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)
        self.driver.find_element(By.NAME, 'username').send_keys('atstudy')
        self.driver.find_element(By.NAME, 'password').send_keys('51testing')
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/input').click()

    # 添加随机数

    def test_random_generate(self):
        num = random.randint(0, 88)
        print(num)
        return num

    # 添加权限
    def add_authority(self):
        authorlist = []
        self.url = "http://testplt.share.atstudy.com/admin/auth/permission/"
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)
        for i in range(1, 4):
            author = self.driver.find_element(By.XPATH, '//*[@id="result_list"]/tbody/tr[' + str(i) + ']/th/a').text
            authorlist.append(author)
        print(authorlist)
        return authorlist

    # 添加组
    def test_Add_Group(self, authorlist):
        self.url = "http://testplt.share.atstudy.com/admin/auth/group/add/"
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)
        self.driver.find_element(By.CLASS_NAME, 'vTextField').send_keys('piggy')
        select = Select(self.driver.find_element(By.ID, 'id_permissions_from'))
        for author in authorlist:
            select.select_by_visible_text(author)
        self.driver.find_element(By.XPATH, '//*[@id="id_permissions_add_link"]').click()
        # self.driver.find_element(By.XPATH, '//*[@id="group_form"]/div/div/input[1]').click()


if __name__ == '__main__':
    obj = Add_authority_and_group()
    # obj.test_Login()
    # authorlist = obj.add_authority()
    # obj.test_Add_Group(authorlist)
    obj.random_generate()
