from selenium import webdriver
from selenium.webdriver.common.by import By
import time

wd = webdriver.Chrome(r'/Users/liyaya/Downloads/chromedriver')
wd.get('http://cdn1.python3.vip/files/selenium/sample1.html')

wd.implicitly_wait(5)

element = wd.find_element(By.ID, 'kw')
element.send_keys('今天晚上吃什么？')


#wd.quit()