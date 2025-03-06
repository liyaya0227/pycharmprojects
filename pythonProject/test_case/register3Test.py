import unittest2
from selenium.webdriver.common.by import By

from func.csvFileManager2 import reader
from test_case.BaseTestCase import BaseTestCase

#由于for循环的执行，如果其中有一个测试用例有问题，就不会再执行下去
#改进方法：使用ddt这个类，不会因为其中的一个测试用例错误，而影响其他的测试用例
#方法
#1、导包
import ddt


#3、在类前面加装饰器ddt.ddt，表示这个类是一个数据驱动测试类
@ddt.ddt
class RegisterTest(BaseTestCase):

#2、指定数据源
    table = reader("register_data_cases.csv")

#4、方法前面加装饰器@ddt.data（*），用来指定测试数据源，*表示测试源里面的每条数据都是一个测试用例
    @ddt.data(*table)
    def test_Register(self, item):
        self.driver.get("http://129.211.129.101:9007/index.php?m=user&c=public&a=reg")
        self.driver.find_element(By.NAME, 'username').send_keys(item[0])
        self.driver.find_element(By.NAME, 'password').send_keys(item[1])
        self.driver.find_element(By.NAME, 'userpassword2').send_keys(item[2])
        self.driver.find_element(By.NAME, 'mobile_phone').send_keys(item[3])
        self.driver.find_element(By.NAME, 'email').send_keys(item[4])
        # self.driver.find_element(By.CSS_SELECTOR, '.reg_btn').click()

if __name__ == '__main__':
    unittest2.main()