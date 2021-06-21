# -*- coding:utf-8 -*-
from page.webpage import WebPage
from common.readelement import Element
from utils.times import sleep

main_rightview = Element('main/mainrightview')


class MainRightViewPage(WebPage):

    def click_invalid_house(self):
        self.is_click(main_rightview['房源待办_无效房源'])
        sleep()
