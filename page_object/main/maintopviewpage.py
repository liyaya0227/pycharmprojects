# -*- coding:utf-8 -*-
from selenium.common.exceptions import NoSuchElementException

from page.webpage import WebPage
from common.readelement import Element
from utils.times import sleep

main_topview = Element('main/maintopview')


class MainTopViewPage(WebPage):

    def click_close_button(self):
        sleep()
        try:
            ele = self.find_element(main_topview['关闭按钮'])
            ele.click()
            # self.is_click(main_topview['关闭按钮'])
        except:
            pass

    def find_notification_content(self):
        try:
            return self.element_text(main_topview['右上角弹窗'])
        except:
            return ''
