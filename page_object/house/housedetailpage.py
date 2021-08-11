#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: housedetailpage.py
@time: 2021/08/10
"""

from page_object.main.leftviewpage import MainLeftViewPage
from page.webpage import WebPage
from common.readelement import Element
from page_object.main.rightviewpage import MainRightViewPage

house_detail = Element('house/housedetail')


class HouseDetailPage1(WebPage):

    main_leftview = None


    def change_role(self, role_name):
        """切换角色"""
        global main_leftview
        main_leftview = MainLeftViewPage(self.driver)
        main_leftview.change_role(role_name)

    def get_house_num(self):
        """获取当前维护人下的房源数量"""
        main_leftview.click_all_house_label()
        account_name = self.element_text(house_detail['当前账号名字'])
        self.input_text(house_detail['维护人输入框'], account_name)
        self.is_click(house_detail['搜索按钮'])
        num = self.element_text(house_detail['搜索结果总数'])[8:][:-1]
        return num

    def enter_house_detail(self):
        """进入房源详情页面，并获取房源编号、房源面积等信息"""
        self.is_click(house_detail['楼盘名称'])
        house_no = self.element_text(house_detail['房源详情页面的房源编号'])[5:]
        initial_price = self.element_text(house_detail['房源初始价格'])[:-1]
        return house_no, initial_price

    def click_more_btn(self):
        """点击详情页面的更多按钮"""
        self.move_mouse_to_element(house_detail['更多按钮'])

    def view_basic_information(self):
        """查看房源基础信息"""
        self.is_click(house_detail['房源基础信息按钮'])

    def verify_can_modify(self):
        """验证是否可以修改"""
        self.move_mouse_to_element(house_detail['房源状态按钮'])
        res = self.is_exists(house_detail['是否可修改状态提示'])
        return res

    def is_view_success(self):
        """验证查看房源基础信息是否成功"""
        res = self.is_exists(house_detail['房源基础信息弹窗title'])
        self.click_blank_area()
        return res

    def submit_modify_state_application(self):
        """提交修改房源状态申请"""
        self.is_click(house_detail['房源状态按钮'])
        self.is_click(house_detail['暂缓出售选项'])
        self.is_click(house_detail['房源状态弹窗确定按钮'])

    def is_submit_success(self):
        """验证提交申请是否成功"""
        res = self.is_exists(house_detail['申请提交成功提示'])
        if res:
            self.is_click(house_detail['申请提交成功弹窗确定按钮'])
        return res

    def is_get_application_success(self, role_name, house_no):
        """验证商圈经理收到修改房源状态申请"""
        self.change_role(role_name)
        main_rightrview = MainRightViewPage(self.driver)
        main_rightrview.click_review_house_state()
        self.is_click(house_detail['暂缓房源审核选项'])
        xpath = "// span[contains(., '" + house_no + "')]"
        # print('HouseDetailPage1-xpath', xpath)
        res = self.is_exists(('xpath', xpath))
        return res

    def is_reject_application_sucess(self):
        """驳回申请并验证驳回成功"""
        self.is_click(house_detail['驳回按钮'])
        self.input_text(house_detail['驳回理由输入框'], '驳回')
        self.is_click(house_detail['驳回弹窗确定按钮'])
        res = self.is_exists(house_detail['审核成功驳回提示框'])
        self.click_blank_area()
        return res

















