#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: detail_page.py
@time: 2021/10/26
"""
import re

from common.readconfig import ini
from page.webpage import WebPage
from common.readelement import Element
from page_object.jrxf.web.house.table_page import house_sql
from utils.databaseutil import DataBaseUtil
from utils.logger import logger
from utils.timeutil import sleep

house_detail = Element('jrxf/web/house/detail')


class HouseDetailPage(WebPage):

    def click_see_more(self):
        """新房详情查看更多"""
        self.is_click(house_detail['查看更多'])

    def get_image_list_lenth(self):
        """获取相册列表中的图片数量"""
        ele_list = self.find_elements(house_detail['相册列表_图片'])
        return len(ele_list)

    def click_upload_btn(self):
        """点击上传图片按钮"""
        self.is_click(house_detail['上传按钮'])

    def switch_lab_by_name(self, lab_name):
        """上传图片弹窗根据名字切换lab"""
        locator = 'xpath', "//div[@class='ant-modal-wrap uploadModal']//span[text()='" + lab_name + "']"
        self.is_click(locator)

    def upload_image(self, pictures_path, lab_name):
        """楼盘相册-上传图片"""
        self.switch_lab_by_name(lab_name)
        for picture_path in pictures_path:
            if lab_name == '效果图':
                self.send_key(house_detail['首图input'], picture_path)
            else:
                self.send_key(house_detail['其他图片input'], picture_path)

    def click_confirm_upload_btn(self):
        """确定上传"""
        self.is_click(house_detail['弹窗_上传按钮'])

    def get_dialog_text(self):
        """获取右上角弹窗提示信息"""
        text = self.element_text(house_detail['右上角弹窗_内容'])
        return text

    def click_batch_delete_btn(self):
        """点击批量删除按钮"""
        self.is_click(house_detail['批量删除按钮'])

    def select_some_image_to_delete(self):
        """选取要删除的照片,默认选择第一张"""
        self.is_click(house_detail['弹窗_选中图片按钮'])

    def get_deleted_image_number(self):
        """获取删除图片数量"""
        text = self.element_text(house_detail['弹窗_删除按钮'])
        number = int(re.findall(r'[(](.*?)[)]', text)[0])
        return number

    def click_delete_btn(self):
        """点击删除按钮"""
        self.is_click(house_detail['弹窗_删除按钮'])

    def click_select_all_btn(self):
        """点击全选按钮"""
        self.is_click(house_detail['弹窗_全选按钮'])

    def select_all_image_to_delete(self):
        """选取所有照片"""
        label_list = self.find_elements(house_detail['删除弹窗_label'])
        for ele in label_list:
            ele.click()
            self.click_select_all_btn()

    def switch_tab_by_name(self, tab_name):
        """新房详情页根据tab名字切换tab"""
        locator = 'xpath', "//div[@class='ant-row ant-tabs-nav-list']/div[text()='" + tab_name + "']"
        self.is_click(locator)

    def get_house_model_number(self):
        """获取户型介绍数量"""
        text = self.element_text(house_detail['户型介绍数量'])
        number = int(re.findall(r'[(](.*?)[)]', text)[0][1:-1])
        return number

    def get_house_img_number(self):
        """获取房源图片数量"""
        text = self.element_text(house_detail['查看更多'])
        # number = int(re.findall(".*共(.*)张.*", text)[0][1:-1])
        number = re.sub("[A-Za-z\u4e00-\u9fa5\，\。]", "", text)
        return number

    def click_upload_house_model_btn(self):
        """点击上传户型介绍按钮"""
        self.is_click(house_detail['上传户型介绍按钮'])

    def house_model_content(self, params):
        """户型介绍内容"""
        self.input_text(house_detail['户型名称输入框'], params['house_type_name'])
        self.is_click(house_detail['户型_室输入框'])
        house_type_name = self.element_text(house_detail['户型名称输入框'])
        self.select_item_option(option=str(params['rooms']))
        # self.is_click(house_detail['户型_厅输入框'])
        # self.select_item_option(option=str(params['parlor']))
        # self.is_click(house_detail['户型_卫输入框'])
        # self.select_item_option(option=str(params['bathroom']))
        # self.is_click(house_detail['户型_厨输入框'])
        # self.select_item_option(option=str(params['kitchen']))
        self.input_text(house_detail['面积输入框'], params['area'])
        self.input_text(house_detail['户型朝向输入框'], params['orientation'])
        self.input_text(house_detail['户型最小价格输入框'], params['sale_price_start'])
        self.input_text(house_detail['户型最大价格输入框'], params['sale_price_end'])
        self.send_key(house_detail['户型图片input'], params['pictures_path'])
        self.is_click(house_detail['弹窗_确定按钮'])
        sleep(1)
        return house_type_name

    def get_building_info_number(self):
        """获取楼盘信息数量"""
        ele_list = self.find_elements(house_detail['楼栋信息tab'])
        return len(ele_list)

    def click_add_building_info(self):
        """点击维护楼盘信息"""
        self.is_click(house_detail['维护楼栋信息'])

    def building_info_content(self, building_name, unit, floor_num, family_num):
        """楼盘信息内容"""
        self.input_text(house_detail['楼栋号输入框'], building_name)
        self.is_click(house_detail['楼盘状态输入框'])
        self.select_item_option(option='不限')
        self.is_click(house_detail['开盘时间_暂无勾选框'])
        self.is_click(house_detail['交房时间_暂无勾选框'])
        self.input_text(house_detail['单元输入框'], unit)
        self.input_text(house_detail['层数输入框'], floor_num)
        self.input_text(house_detail['户数输入框'], family_num)
        self.is_click(house_detail['建筑类型输入框'])
        self.select_item_option('平房')
        self.is_click(house_detail['户型选择框'])
        self.is_click(house_detail['弹窗_确定按钮'])

    def house_dynamic_content(self, trend_title, trend_explain):
        """楼盘动态内容"""
        self.is_click(house_detail['发布动态按钮'])
        self.input_text(house_detail['动态标题输入框'], trend_title, True)
        self.input_text(house_detail['动态说明输入框'], trend_explain, True)
        self.is_click(house_detail['动态弹窗_确定按钮'])
        return trend_explain

    def verify_dynamic_list_update(self, trend_explain):
        """验证动态列表是否更新"""
        self.scroll_to_bottom()
        locator = 'xpath', "//div[@class ='statetimeBox']/div[@class='stateNote' and text()='" + trend_explain + "']"
        res = self.is_exists(locator)
        return res

    def house_selling_point_content(self, push_plate, detailed_description):
        """楼盘卖点内容"""
        self.is_click(house_detail['编辑卖点按钮'])
        self.input_text(house_detail['一句话推盘输入框'], push_plate, True)
        self.input_text(house_detail['详细描述输入框'], detailed_description, True)
        self.is_click(house_detail['保存按钮'])
        return push_plate

    def verify_celling_point_list_update(self):
        """验证卖点列表是否更新"""
        self.scroll_to_bottom()
        actual_result = self.element_text(house_detail['卖点列表_推盘'])
        return actual_result

    def click_share(self):
        """点击分享"""
        self.is_click(house_detail['分享按钮'])

    def get_user_info_in_share_page(self):
        """分享页面用户信息"""
        account_name = self.element_text(house_detail['分享弹窗_登录人账号'])
        account_phone = self.element_text(house_detail['分享弹窗_登录人手机号'])
        return account_name, account_phone

    def get_model_info_in_share_page(self):
        """分享页面户型信息"""
        model_info = self.element_text(house_detail['分享弹窗_户型'])
        area = self.element_text(house_detail['分享弹窗_面积']).split('m')[0]
        orientation = self.element_text(house_detail['分享弹窗_朝向'])
        sale_price = self.element_text(house_detail['分享弹窗_价格']).split('\n')[0]
        return model_info, area, orientation, sale_price

    # def choose_image_in_share_page(self):
    #     """分享页面选择图片"""
    #     self.is_click(house_detail['分享弹窗_效果图'])
    #
    # def click_generate_code_btn(self):
    #     """点击生成二维码按钮"""
    #     self.is_click(house_detail['生成海报二维码按钮'])
    #     sleep(12)

    def generate_code(self):
        """生成二维码"""
        self.is_click(house_detail['分享弹窗_效果图'])
        self.is_click(house_detail['生成海报二维码按钮'])
        sleep(12)

    def verify_generate_code_success(self):
        """验证生成二维码成功"""
        sleep(3)
        res = self.is_exists(house_detail['海报二维码弹窗'])
        return res

    def close_dialog(self):
        """关闭弹窗"""
        self.is_click(house_detail['弹窗_关闭按钮'])

    def close_code_dialog(self):
        """关闭二维码弹窗"""
        self.is_click(house_detail['二维码弹窗_关闭按钮'])

    def select_item_option(self, option=None, index=None):
        if option:
            locator = 'xpath', "//div[@style='' or not(@style)]//div[@class='rc-virtual-list']//div[contains(@class," \
                               "'ant-select-item ant-select-item-option') and @title='" + option + "'] "
            self.is_click(locator)
        else:
            locator = 'xpath', "//div[@style='' or not(@style)]//div[@class='rc-virtual-list']//div[contains(@class," \
                               "'ant-select-item ant-select-item-option')] "
            options = self.find_elements(locator)
            options[index].click()

    @staticmethod
    def get_user_info_from_db(account):
        database_util = DataBaseUtil('Xf My SQL', ini.xf_database_name)
        get_user_info = house_sql.get_sql('sys_framework_users', 'get_user_info').format(it_code=account)
        user_info = database_util.select_sql(get_user_info)[0]
        if len(user_info) > 0:
            return user_info
        else:
            log.error('获取用户信息失败')
