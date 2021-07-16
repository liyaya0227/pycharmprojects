#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: loginpage.py
@time: 2021/06/24
"""

from page.webpage import WebPage
from common.readelement import Element
from utils.timeutil import sleep
from config.conf import cm
from PIL import Image
from utils.fileutil import delete_file
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

login = Element('login/login')


class LoginPage(WebPage):

    def input_account(self, account):
        self.input_text(login['账号输入框'], account)

    def input_password(self, password):
        self.input_text(login['密码输入框'], password)

    def click_verify_button(self):
        self.is_click(login['校验点击按钮'])

    def verify(self):
        while True:
            verify_picture = self.find_element(login['验证图片'])
            self.driver.get_screenshot_as_file(cm.tmp_dir + "/全屏截图.png")
            location_x = verify_picture.location['x']
            location_y = verify_picture.location['y']
            size_height = verify_picture.size['height']
            size_width = verify_picture.size['width']
            picture_scope = (location_x, location_y, location_x + size_width, location_y + size_height)
            img = Image.open(cm.tmp_dir + "/全屏截图.png")
            img = img.convert('RGB')
            frame = img.crop(picture_scope)
            data = frame.getdata()  # 获取rgb
            x_coordinates = 0
            for x in range(63, size_width - 1):
                for y in range(1, size_height - 1):
                    mid_pixel = data[size_width * y + x]  # 中央像素点像素值
                    if mid_pixel[0] > 230 and mid_pixel[1] > 230 and mid_pixel[2] > 230:  # 找出上下左右四个方向像素点像素值
                        top_pixel = data[size_width * (y - 1) + x]  # 上
                        down_pixel = data[size_width * (y + 1) + x]  # 下
                        if top_pixel[0] > 230 and top_pixel[1] > 230 and top_pixel[2] > 230\
                                and down_pixel[0] > 230 and down_pixel[1] > 230 and down_pixel[2] > 230:
                            x_coordinates = x
            x_coordinates = x_coordinates - 35
            slide_button = self.find_element(login['滑动按钮'])
            action = ActionChains(self.driver)
            action.click_and_hold(on_element=slide_button).perform()
            action.move_by_offset(x_coordinates, 0).perform()
            sleep(1)
            action.release().perform()
            sleep()
            delete_file(cm.tmp_dir + "/全屏截图.png")
            try:
                self.find_element_with_wait_time(login['验证图片'])
            except TimeoutException:
                return

    def click_login_button(self):
        self.is_click(login['立即登录按钮'])
