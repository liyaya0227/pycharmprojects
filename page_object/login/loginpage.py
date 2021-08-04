#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: loginpage.py
@time: 2021/06/24
"""
import random

import cv2
import base64
from io import BytesIO
from PIL import Image
from config.conf import cm
from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element
from selenium.webdriver.common.action_chains import ActionChains

login = Element('login/login')


class LoginPage(WebPage):

    def input_account(self, account):
        self.input_text(login['账号输入框'], account)

    def input_password(self, password):
        self.input_text(login['密码输入框'], password)

    def click_verify_button(self):
        self.is_click(login['校验点击按钮'])

    def __save_img(self, picture_css, path):
        get_img_js = 'return document.querySelector("' + picture_css + '").toDataURL("image/jpeg");'
        img = self.driver.execute_script(get_img_js)
        base64_data_img = img[img.find(',') + 1:]
        image_base = base64.b64decode(base64_data_img)
        file_like = BytesIO(image_base)
        image = Image.open(file_like)
        image.save(path)

    def __get_element_slide_distance(self):
        """
        破解滑块验证主程序
        :return:需移动的距离
        """
        # 1、出现滑块验证，获取验证小图片
        slider_img_css = "#verifyCode>canvas[class]"
        self.__save_img(slider_img_css, cm.tmp_dir + "/slider.png")
        # 2、获取有缺口验证图片
        background_img_css = "#verifyCode>canvas"
        self.__save_img(background_img_css, cm.tmp_dir + "/background.png")
        # 二值化图片,进行对比，输出匹配的坐标系
        target_rgb = cv2.imread(cm.tmp_dir + "/background.png")
        target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
        template_rgb = cv2.imread(cm.tmp_dir + "/slider.png", 0)
        res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
        value = cv2.minMaxLoc(res)
        value = value[3][0]+10
        return value

    @staticmethod
    def __get_slide_locus(distance):
        """
        根据移动坐标位置构造移动轨迹,前期移动慢，中期块，后期慢
        :param distance:移动距离
        :type:int
        :return:移动轨迹
        :rtype:list
        """
        remaining_dist = distance
        locus = []
        while remaining_dist > 0:
            ratio = remaining_dist / distance
            if ratio < 0.2:
                span = random.randint(2, 8)
            elif ratio > 0.8:
                span = random.randint(5, 8)
            else:
                span = random.randint(10, 16)
            locus.append(span)
            remaining_dist -= span
        return locus

    def slide_verification(self, count=5):
        """
        :param count:  重试次数
        :type: int
        """
        distance = self.__get_element_slide_distance()
        locus = self.__get_slide_locus(distance)
        slide_button = self.find_element(login['滑动按钮'])
        ActionChains(self.driver).click_and_hold(slide_button).perform()
        sleep(0.5)
        for loc in locus:
            sleep(0.01)
            ActionChains(self.driver).move_by_offset(loc, 0).perform()
        ActionChains(self.driver).release(slide_button).perform()
        sleep(2)
        if self.find_element_with_wait_time(login['验证图片'], wait_time=2):
            count -= 1
            self.slide_verification(count)

    def click_login_button(self):
        self.is_click(login['立即登录按钮'])
