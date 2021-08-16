#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@date: 2021/7/8 0008
"""

from utils.timeutil import sleep
from page.webpage import WebPage
from common.readelement import Element

transaction_detail = Element('transaction/detail')


class TransactionDetailPage(WebPage):

    def complete_transfer_house(self):
        if 'done' not in self.get_element_attribute(transaction_detail['综合办理按钮'], 'class'):
            raise Exception("不能办理过户流程")
        self.is_click(transaction_detail['综合办理按钮'])
        self.is_click(transaction_detail['完成按钮'])
        sleep(2)

    def close_case(self):
        if 'done' not in self.get_element_attribute(transaction_detail['结案按钮'], 'class'):
            raise Exception("不能办理结案流程")
        self.is_click(transaction_detail['结案按钮'])
        self.is_click(transaction_detail['完成按钮'])
        sleep(2)

    def show_sensitive_info(self):
        flag = self.element_text(transaction_detail['显示隐藏敏感信息按钮'])
        if flag == '显示敏感信息':
            self.is_click(transaction_detail['显示隐藏敏感信息按钮'])
            sleep()
        else:
            pass

    def click_transaction_order_info_tab(self):
        self.is_click(transaction_detail['交易单信息标签'])

    def click_attachment_info_tab(self):
        self.is_click(transaction_detail['备件信息标签'])

    def click_operation_record_tab(self):
        self.is_click(transaction_detail['操作记录标签'])

    def get_transaction_info(self):
        transaction_order_info = {'交易管理': self.element_text(transaction_detail['交易单信息_交易管理标签']),
                                  '交易编号': self.element_text(transaction_detail['交易单信息_交易编号标签']),
                                  '合同编号': self.element_text(transaction_detail['交易单信息_合同编号标签']),
                                  '创建日期': self.element_text(transaction_detail['交易单信息_创建日期标签']),
                                  '签约日期': self.element_text(transaction_detail['交易单信息_签约日期标签']),
                                  '合同约定办理资金托管日期': self.element_text(transaction_detail['交易单信息_合同约定办理资金托管日期标签']),
                                  '备注': self.element_text(transaction_detail['交易单信息_备注标签'])}
        if transaction_order_info['交易管理'] == '商贷':
            transaction_order_info['合同约定贷款审批通过日期'] = self.element_text(transaction_detail['交易单信息_合同约定贷款审批通过日期标签'])
        return transaction_order_info

    def get_fund_info(self):
        locator = 'xpath', "//div[@style='']/div[@class='detail-transaction']//h3[text()='资金信息']" \
                           "/parent::div[@class='info-box']//div[@class='item']"
        info_list = self.find_elements(locator)
        fund_info = {}
        for info_ele in info_list:
            value = info_ele.text
            fund_info[value.split('：')[0]] = value.split('：')[1]
        # fund_info = {'成交总价': self.element_text(transaction_detail['资金信息_成交总价标签']),
        #              '网签价': self.element_text(transaction_detail['资金信息_网签价标签']),
        #              '首期款总额': self.element_text(transaction_detail['资金信息_首期款总额标签']),
        #              '定金总额': self.element_text(transaction_detail['资金信息_定金总额标签']),
        #              '首付款总金额': self.element_text(transaction_detail['资金信息_首付款总金额标签']),
        #              '购房款/首付款(第一笔)': self.element_text(transaction_detail['资金信息_购房款/首付款(第一笔)标签']),
        #              '交房保证金': self.element_text(transaction_detail['资金信息_交房保证金标签']),
        #              '户口迁出保证金': self.element_text(transaction_detail['资金信息_户口迁出保证金标签'])}
        # if self.element_text(transaction_detail['交易单信息_交易管理标签']) == '商贷':
        #     fund_info['拟贷款金额'] = self.element_text(transaction_detail['资金信息_拟贷款金额标签'])
        return fund_info

    def get_buyer_info(self):
        self.is_click(transaction_detail['买方信息标签'])
        buyer_info = {'姓名': self.element_text(transaction_detail['买方信息_姓名标签']),
                      '性质': self.element_text(transaction_detail['买方信息_性质标签']),
                      '性别': self.element_text(transaction_detail['买方信息_性别标签']),
                      '国籍': self.element_text(transaction_detail['买方信息_国籍标签']),
                      '证件类型': self.element_text(transaction_detail['买方信息_证件类型标签']),
                      '证件号码': self.element_text(transaction_detail['买方信息_证件号码标签']),
                      '联系电话': self.element_text(transaction_detail['买方信息_联系电话标签']),
                      '其他联系方式': self.element_text(transaction_detail['买方信息_其他联系方式标签']),
                      '户籍': self.element_text(transaction_detail['买方信息_户籍标签']),
                      '婚姻状况': self.element_text(transaction_detail['买方信息_婚姻状况标签']),
                      '买方家庭住房套数': self.element_text(transaction_detail['买方信息_买方家庭住房套数标签'])}
        return buyer_info

    def get_buyer_share_person(self):
        self.is_click(transaction_detail['买方共有人标签'])
        locator = 'xpath', "//div[@style='']/div[@class='detail-transaction']//div[text()='买方共有人']" \
                           "/ancestor::div[@class='info-box']//div[@class='item']"
        info_list = self.find_elements(locator)
        buyer_share_person_info = {}
        for info_ele in info_list:
            value = info_ele.text
            buyer_share_person_info[value.split('：')[0]] = value.split('：')[1]
        # buyer_share_person_info = {'姓名': self.element_text(transaction_detail['买方共有人_姓名标签']),
        #                            '联系电话': self.element_text(transaction_detail['买方共有人_联系电话标签']),
        #                            '证件类型': self.element_text(transaction_detail['买方共有人_证件类型标签']),
        #                            '证件号码': self.element_text(transaction_detail['买方共有人_证件号码标签']),
        #                            '国籍': self.element_text(transaction_detail['买方共有人_国籍标签'])}
        return buyer_share_person_info

    def get_seller_info(self):
        seller_info = {'姓名': self.element_text(transaction_detail['卖方信息_姓名标签']),
                       '性质': self.element_text(transaction_detail['卖方信息_性质标签']),
                       '性别': self.element_text(transaction_detail['卖方信息_性别标签']),
                       '国籍': self.element_text(transaction_detail['卖方信息_国籍标签']),
                       '证件类型': self.element_text(transaction_detail['卖方信息_证件类型标签']),
                       '证件号码': self.element_text(transaction_detail['卖方信息_证件号码标签']),
                       '联系电话': self.element_text(transaction_detail['卖方信息_联系电话标签']),
                       '其他联系方式': self.element_text(transaction_detail['卖方信息_其他联系方式标签']),
                       '婚姻状况': self.element_text(transaction_detail['卖方信息_婚姻状况标签'])}
        return seller_info

    def get_house_info(self):
        house_info = {'房源编号': self.element_text(transaction_detail['房源信息_房源编号标签']),
                      '规划用途': self.element_text(transaction_detail['房源信息_规划用途标签']),
                      '建筑面积': self.element_text(transaction_detail['房源信息_建筑面积标签']),
                      '建成年代': self.element_text(transaction_detail['房源信息_建成年代标签']),
                      '房屋性质': self.element_text(transaction_detail['房源信息_房屋性质标签']),
                      '楼盘名称': self.element_text(transaction_detail['房源信息_楼盘名称标签']),
                      '房本类型': self.element_text(transaction_detail['房源信息_房本类型标签']),
                      '产权证号': self.element_text(transaction_detail['房源信息_产权证号标签']),
                      '共有权证号': self.element_text(transaction_detail['房源信息_共有权证号标签']),
                      '房屋现状': self.element_text(transaction_detail['房源信息_房屋现状标签']),
                      '物业地址': self.element_text(transaction_detail['房源信息_物业地址标签']),
                      '行政区域': self.element_text(transaction_detail['房源信息_行政区域标签']),
                      '是否有抵押': self.element_text(transaction_detail['房源信息_是否有抵押标签']),
                      '合同约定的注销抵押日期': self.element_text(transaction_detail['房源信息_合同约定的注销抵押日期标签']),
                      '是否唯一': self.element_text(transaction_detail['房源信息_是否唯一标签']),
                      '产证年限': self.element_text(transaction_detail['房源信息_产证年限标签']),
                      '是否限售房': self.element_text(transaction_detail['房源信息_是否限售房标签'])}
        return house_info
