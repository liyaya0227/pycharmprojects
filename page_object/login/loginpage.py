#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: loginpage.py
@time: 2021/06/24
"""
import base64
from io import BytesIO
import random
import time
import cv2
from page.webpage import WebPage
from common.readelement import Element
from utils.timeutil import sleep
from config.conf import cm
from PIL import Image
from utils.fileutil import delete_file
from selenium.webdriver.common.action_chains import ActionChains

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
            if not self.find_element_with_wait_time(login['验证图片']):
                return True


    def save_img(self, class_name):
        """下载滑块图片"""
        getImgJS = 'return document.getElementsByClassName("' + class_name + '")[0].toDataURL("image/jpeg");'
        img = self.driver.execute_script(getImgJS)
        base64_data_img = img[img.find(',') + 1:]
        # j = img[img.find(',') + 1:]
        image_base = base64.b64decode(base64_data_img)
        file_like = BytesIO(image_base)
        image = Image.open(file_like)
        return image

    def save_img_css(self):
        """下载带缺口背景图片"""
        getImgJS = 'return document.getElementsByTagName("canvas")[0].toDataURL("image/jpeg");'
        img = self.driver.execute_script(getImgJS)
        base64_data_img = img[img.find(',') + 1:]
        # j = img[img.find(',') + 1:]
        image_base = base64.b64decode(base64_data_img)
        file_like = BytesIO(image_base)
        image = Image.open(file_like)
        return image

    def get_element_slide_distance(self,slider_pic,background_pic):
        """
        破解滑块验证主程序
        :param slider_pic:保存滑块图片时的名字；background_pic：保存带缺口背景图片时的名字
        :return:需移动的距离
        """
        # log = Log().logger
        print("出现滑块验证，验证中")
        # 1、出现滑块验证，获取验证小图片
        picture1 = self.save_img('sliderVerifyCode_block__2nWM1')
        picture1.save(slider_pic)

        # 2、获取有缺口验证图片
        cut_image = self.save_img_css()
        cut_image.save(background_pic)

        # 二值化图片,进行对比，输出匹配的坐标系
        target_rgb = cv2.imread(background_pic)
        target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
        template_rgb = cv2.imread(slider_pic, 0)
        res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
        value = cv2.minMaxLoc(res)
        value = value[3][0]+10
        # log.info("==================================" + str(value) + "===================================")
        return value

    def get_slide_locus(self, distance):
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

    def slide_verification(self,slider_pic,background_pic,count):
        """
        :param driver: driver对象
        :type driver:webdriver.Chrome
        :param distance:  滑动的距离
        :type: int
        :param count:  重试次数
        :type: int
        """
        distance = self.get_element_slide_distance(slider_pic,background_pic)
        # count = 5
        start_url = self.driver.current_url
        print("需要滑动的距离为：", distance)
        locus = self.get_slide_locus(distance)
        print("生成的滑动轨迹为:{}，轨迹的距离之和为{}".format(locus, distance))
        ActionChains(self.driver).click_and_hold(self.find_element(login['滑动按钮'])).perform()
        time.sleep(0.5)
        for loc in locus:
            time.sleep(0.01)
            ActionChains(self.driver).move_by_offset(loc, random.randint(-5, 5)).perform()
            ActionChains(self.driver).context_click(self.find_element(login['滑动按钮']))
        ActionChains(self.driver).release(on_element=self.find_element(login['滑动按钮'])).perform()
        self.click_login_button()
        time.sleep(1)
        end_url = self.driver.current_url
        if start_url == end_url and count > 0:
            print("第{}次验证失败，开启重试".format(6 - count))
            count -= 1
            self.slide_verification(slider_pic,background_pic,count)

    def click_login_button(self):
        self.is_click(login['立即登录按钮'])
