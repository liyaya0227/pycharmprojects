import random

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class Test_add_authority_and_group():
    # 登录
    def setup_class(self):
        self.driver = webdriver.Chrome(r'/Users/liyaya/Downloads/chromedriver')
        self.url = "http://testplt.share.atstudy.com/admin/login/?next=/admin/"
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)
        self.driver.find_element(By.NAME, 'username').send_keys('atstudy')
        self.driver.find_element(By.NAME, 'password').send_keys('51testing')
        self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[3]/input').click()
    '''#添加随机数
    @pytest.fixture()
    def test_random_generate(self):
        num = random.randint(0, 88)
        print(num)
        return num
        
    #添加权限
    @pytest.fixture()
    def test_add_authority(self, test_random_generate):
        authorlist = []
        self.url = "http://testplt.share.atstudy.com/admin/auth/permission/"
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)
        for i in range(1, 4):
            author = self.driver.find_element(By.XPATH, '//*[@id="result_list"]/tbody/tr[' + str(i) + ']/th/a').text
            authorlist.append(author)
        author = self.driver.find_element(By.XPATH, '//*[@id="result_list"]/tbody/tr[' + str(test_random_generate) + ']/th/a').text
        print(authorlist)
        return author'''

    # 添加组
    def test_Add_Group(self):
        self.url = "http://testplt.share.atstudy.com/admin/auth/group/add/"
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)
        self.driver.find_element(By.CLASS_NAME, 'vTextField').send_keys('piggy')
        select = Select(self.driver.find_element(By.ID, 'id_permissions_from'))
        #读取ddt文件
        # 打开文件
        file = open("../../DDT_test/author.txt", 'r', encoding='utf-8')
        # 读取文件
        content = file.read()
        # 读取文件的内容为str
        print(type(content))
        # 通过分隔符切割字符串，得到每个值
        list = content.split(',')
        #print(list)
        # 前后字符串包含【】号，采用截取的方式，去除【】号
        for author in list[1:-1]:
            # 得到的每个值，都带了''号，要把''去掉
            # print(author)
            #print(author[2:-1])
            select.select_by_visible_text(author[2:-1])
        # 关闭文件
        file.close()

        #select.select_by_visible_text(test_add_authority)
        self.driver.find_element(By.XPATH, '//*[@id="id_permissions_add_link"]').click()
        #self.driver.find_element(By.XPATH, '//*[@id="group_form"]/div/div/input[1]').click()

'''if __name__ == '__main__':
    obj = Test_add_authority_and_group()
    obj.test_login()
    obj.test_Add_Group()'''


