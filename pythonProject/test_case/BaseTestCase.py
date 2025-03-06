import time

import unittest2
from selenium import webdriver


class BaseTestCase(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(r'/Users/liyaya/Downloads/chromedriver')
        # cls.dirver.maximize_window()
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        #time.sleep(1)
        cls.driver.quit()