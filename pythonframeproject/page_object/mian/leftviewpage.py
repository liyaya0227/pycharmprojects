"""
@author: lijiahui
@version: V1.0
@file: leftviewpage.py
@time: 2022/1/9
"""

from common.readelement import Element
from page.webpage import WebPage
from utils.timeutil import sleep

leftview_meau = Element('main/leftviewpage')

class LeftViewPage(WebPage):
    def click_role_meau(self):
        self.is_click(leftview_meau['角色信息按钮'], sleep_time=0.5)

    def click_modefy_password(self):
        self.is_click(leftview_meau['修改密码按钮'], sleep_time=0.5)

    def click_change_role_type(self):
        self.is_click(leftview_meau['切换角色按钮'], sleep_time=0.5)

    def click_logout(self):
        self.is_click(leftview_meau['退出登录按钮'], sleep_time=0.5)

    def click_role_type(self, role_name):
        typelist = self.find_elements(leftview_meau['切换的角色'])
        for type_item in typelist:
            #查看一下列表返回的参数
            if role_name in type_item.text:
                type_item.click()
                sleep(0.5)
                break

    def click_ok_button(self):
        self.is_click(leftview_meau['确定按钮'], sleep_time=0.5)

    def click_cancel_button(self):
        self.is_click(leftview_meau['取消按钮'], sleep_time=0.5)

    def click_dialog_cancel_button(self):
        self.is_click(leftview_meau['关闭弹框按钮'], sleep_time=0.5)

    def change_role_name(self, role_name):
        self.click_role_meau()
        self.click_change_role_type()
        self.click_role_type(role_name)
        self.click_ok_button()



