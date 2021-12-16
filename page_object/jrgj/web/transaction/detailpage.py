#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: detailpage.py
@date: 2021/7/8 0008
"""
import random
import string
from page.webpage import WebPage
from common.readelement import Element

transaction_detail = Element('jrgj/web/transaction/detail')


class TransactionDetailPage(WebPage):

    def complete_report_examine(self):
        """完成报单审核流程"""
        if 'done' not in self.get_element_attribute(transaction_detail['报单审核按钮'], 'class'):
            raise Exception("不能办理报单审核流程")
        self.click_element(transaction_detail['报单审核按钮'])
        self.click_element(transaction_detail['完成按钮'], sleep_time=1)

    def complete_submit_online_sign_attachment(self):
        """完成提交网签备件流程"""
        if 'done' not in self.get_element_attribute(transaction_detail['提交网签备件按钮'], 'class'):
            raise Exception("不能办理提交网签备件流程")
        self.click_element(transaction_detail['提交网签备件按钮'])
        self.click_element(transaction_detail['完成按钮'], sleep_time=1)

    def complete_online_sign(self):
        """完成网签流程"""
        if 'done' not in self.get_element_attribute(transaction_detail['登记网签申请按钮'], 'class'):
            raise Exception("不能办理登记网签申请流程")
        self.click_element(transaction_detail['登记网签申请按钮'])
        self.click_element(transaction_detail['完成按钮'], sleep_time=1)
        if 'done' not in self.get_element_attribute(transaction_detail['登记网签结果按钮'], 'class'):
            raise Exception("不能办理登记网签结果流程")
        self.click_element(transaction_detail['登记网签结果按钮'])
        self.click_element(transaction_detail['完成按钮'], sleep_time=1)

    def complete_fund_custody(self):
        """完成资金托管流程"""
        if 'done' not in self.get_element_attribute(transaction_detail['资金托管按钮'], 'class'):
            raise Exception("不能办理资金托管流程")
        self.click_element(transaction_detail['资金托管按钮'])
        self.click_element(transaction_detail['上传材料清单按钮'], sleep_time=1)
        self.input_text_into_element(transaction_detail['材料清单弹窗_出卖方输入框'],
                                     "".join(map(lambda x: random.choice(string.digits), range(5))))
        self.input_text_into_element(transaction_detail['材料清单弹窗_买受方输入框'],
                                     "".join(map(lambda x: random.choice(string.digits), range(5))))
        self.click_element(transaction_detail['材料清单弹窗_提交按钮'])
        self.click_element(transaction_detail['资金托管按钮'])
        self.click_element(transaction_detail['完成按钮'], sleep_time=1)

    def complete_face_sign(self):
        """完成面签流程"""
        if 'done' not in self.get_element_attribute(transaction_detail['登记面签结果按钮'], 'class'):
            raise Exception("不能办理登记面签结果流程")
        self.click_element(transaction_detail['登记面签结果按钮'])
        self.click_element(transaction_detail['上传材料清单按钮'], sleep_time=1)
        self.input_text_into_element(transaction_detail['材料清单弹窗_出卖方输入框'],
                                     "".join(map(lambda x: random.choice(string.digits), range(5))))
        self.input_text_into_element(transaction_detail['材料清单弹窗_买受方输入框'],
                                     "".join(map(lambda x: random.choice(string.digits), range(5))))
        self.click_element(transaction_detail['材料清单弹窗_提交按钮'])
        self.click_element(transaction_detail['登记面签结果按钮'])
        self.click_element(transaction_detail['完成按钮'], sleep_time=1)

    def complete_grant_load(self):
        """完成放款流程"""
        if 'done' not in self.get_element_attribute(transaction_detail['登记批贷结果按钮'], 'class'):
            raise Exception("不能办理登记批贷结果流程")
        self.click_element(transaction_detail['登记批贷结果按钮'])
        self.click_element(transaction_detail['上传材料清单按钮'], sleep_time=1)
        self.input_text_into_element(transaction_detail['材料清单弹窗_出卖方输入框'],
                                     "".join(map(lambda x: random.choice(string.digits), range(5))))
        self.input_text_into_element(transaction_detail['材料清单弹窗_买受方输入框'],
                                     "".join(map(lambda x: random.choice(string.digits), range(5))))
        self.click_element(transaction_detail['材料清单弹窗_提交按钮'])
        self.click_element(transaction_detail['登记批贷结果按钮'])
        self.click_element(transaction_detail['完成按钮'], sleep_time=1)

    def complete_load(self):
        """完成放款流程"""
        if 'done' not in self.get_element_attribute(transaction_detail['登记放款结果按钮'], 'class'):
            raise Exception("不能办理登记放款结果流程")
        self.click_element(transaction_detail['登记放款结果按钮'])
        self.click_element(transaction_detail['完成按钮'], sleep_time=1)

    def complete_transfer_house(self):
        if 'done' not in self.get_element_attribute(transaction_detail['综合办理按钮'], 'class'):
            raise Exception("不能办理过户流程")
        self.click_element(transaction_detail['综合办理按钮'])
        self.click_element(transaction_detail['上传材料清单按钮'], sleep_time=1)
        self.input_text_into_element(transaction_detail['材料清单弹窗_出卖方输入框'],
                                     "".join(map(lambda x: random.choice(string.digits), range(5))))
        self.input_text_into_element(transaction_detail['材料清单弹窗_买受方输入框'],
                                     "".join(map(lambda x: random.choice(string.digits), range(5))))
        self.click_element(transaction_detail['材料清单弹窗_提交按钮'])
        self.click_element(transaction_detail['综合办理按钮'])
        self.click_element(transaction_detail['完成按钮'], sleep_time=1)

    def complete_receive_certificates(self):
        """完成领证流程"""
        if 'done' not in self.get_element_attribute(transaction_detail['领取新不动产/他项证按钮'], 'class'):
            raise Exception("不能办理领取新不动产/他项证流程")
        self.click_element(transaction_detail['领取新不动产/他项证按钮'])
        self.click_element(transaction_detail['完成按钮'], sleep_time=1)

    def complete_receive_house_payment(self):
        """完成领款流程"""
        if 'done' not in self.get_element_attribute(transaction_detail['领取房款按钮'], 'class'):
            raise Exception("不能办理领取房款流程")
        self.click_element(transaction_detail['领取房款按钮'])
        self.click_element(transaction_detail['完成按钮'], sleep_time=1)

    def complete_close_case(self):
        if 'done' not in self.get_element_attribute(transaction_detail['结案按钮'], 'class'):
            raise Exception("不能办理结案流程")
        self.click_element(transaction_detail['结案按钮'])
        self.click_element(transaction_detail['完成按钮'], sleep_time=1)

    def show_sensitive_info(self):
        flag = self.get_element_text(transaction_detail['显示隐藏敏感信息按钮'])
        if flag == '显示敏感信息':
            self.click_element(transaction_detail['显示隐藏敏感信息按钮'], sleep_time=0.5)
        else:
            pass

    def click_transaction_order_info_tab(self):
        self.click_element(transaction_detail['交易单信息标签'])

    def click_attachment_info_tab(self):
        self.click_element(transaction_detail['备件信息标签'])

    def click_operation_record_tab(self):
        self.click_element(transaction_detail['操作记录标签'])

    def get_transaction_info(self):
        transaction_order_info = {'交易管理': self.get_element_text(transaction_detail['交易单信息_交易管理标签']),
                                  '交易编号': self.get_element_text(transaction_detail['交易单信息_交易编号标签']),
                                  '合同编号': self.get_element_text(transaction_detail['交易单信息_合同编号标签']),
                                  '创建日期': self.get_element_text(transaction_detail['交易单信息_创建日期标签']),
                                  '签约日期': self.get_element_text(transaction_detail['交易单信息_签约日期标签']),
                                  '合同约定办理资金托管日期': self.get_element_text(transaction_detail['交易单信息_合同约定办理资金托管日期标签']),
                                  '备注': self.get_element_text(transaction_detail['交易单信息_备注标签'])}
        if transaction_order_info['交易管理'] == '商贷':
            transaction_order_info['合同约定贷款审批通过日期'] = self.get_element_text(transaction_detail['交易单信息_合同约定贷款审批通过日期标签'])
        return transaction_order_info

    def get_fund_info(self):
        locator = 'xpath', "//div[@style='']/div[@class='detail-transaction']//h3[text()='资金信息']" \
                           "/parent::div[@class='info-box']//div[@class='item']"
        info_list = self.find_elements(locator)
        fund_info = {}
        for info_ele in info_list:
            value = info_ele.text
            fund_info[value.split('：')[0]] = value.split('：')[1]
        return fund_info

    def get_buyer_info(self):
        self.click_element(transaction_detail['买方信息标签'])
        buyer_info = {'姓名': self.get_element_text(transaction_detail['买方信息_姓名标签']),
                      '性质': self.get_element_text(transaction_detail['买方信息_性质标签']),
                      '性别': self.get_element_text(transaction_detail['买方信息_性别标签']),
                      '国籍': self.get_element_text(transaction_detail['买方信息_国籍标签']),
                      '证件类型': self.get_element_text(transaction_detail['买方信息_证件类型标签']),
                      '证件号码': self.get_element_text(transaction_detail['买方信息_证件号码标签']),
                      '联系电话': self.get_element_text(transaction_detail['买方信息_联系电话标签']),
                      '其他联系方式': self.get_element_text(transaction_detail['买方信息_其他联系方式标签']),
                      '户籍': self.get_element_text(transaction_detail['买方信息_户籍标签']),
                      '婚姻状况': self.get_element_text(transaction_detail['买方信息_婚姻状况标签']),
                      '买方家庭住房套数': self.get_element_text(transaction_detail['买方信息_买方家庭住房套数标签'])}
        return buyer_info

    def get_buyer_share_person(self):
        self.click_element(transaction_detail['买方共有人标签'])
        locator = 'xpath', "//div[@style='']/div[@class='detail-transaction']//div[text()='买方共有人']" \
                           "/ancestor::div[@class='info-box']//div[@class='item']"
        info_list = self.find_elements(locator)
        buyer_share_person_info = {}
        for info_ele in info_list:
            value = info_ele.text
            buyer_share_person_info[value.split('：')[0]] = value.split('：')[1]
        return buyer_share_person_info

    def get_seller_info(self):
        seller_info = {'姓名': self.get_element_text(transaction_detail['卖方信息_姓名标签']),
                       '性质': self.get_element_text(transaction_detail['卖方信息_性质标签']),
                       '性别': self.get_element_text(transaction_detail['卖方信息_性别标签']),
                       '国籍': self.get_element_text(transaction_detail['卖方信息_国籍标签']),
                       '证件类型': self.get_element_text(transaction_detail['卖方信息_证件类型标签']),
                       '证件号码': self.get_element_text(transaction_detail['卖方信息_证件号码标签']),
                       '联系电话': self.get_element_text(transaction_detail['卖方信息_联系电话标签']),
                       '其他联系方式': self.get_element_text(transaction_detail['卖方信息_其他联系方式标签']),
                       '婚姻状况': self.get_element_text(transaction_detail['卖方信息_婚姻状况标签'])}
        return seller_info

    def get_house_info(self):
        house_info = {'房源编号': self.get_element_text(transaction_detail['房源信息_房源编号标签']),
                      '规划用途': self.get_element_text(transaction_detail['房源信息_规划用途标签']),
                      '建筑面积': self.get_element_text(transaction_detail['房源信息_建筑面积标签']),
                      '建成年代': self.get_element_text(transaction_detail['房源信息_建成年代标签']),
                      '房屋性质': self.get_element_text(transaction_detail['房源信息_房屋性质标签']),
                      '楼盘名称': self.get_element_text(transaction_detail['房源信息_楼盘名称标签']),
                      '房本类型': self.get_element_text(transaction_detail['房源信息_房本类型标签']),
                      '产权证号': self.get_element_text(transaction_detail['房源信息_产权证号标签']),
                      '共有权证号': self.get_element_text(transaction_detail['房源信息_共有权证号标签']),
                      '房屋现状': self.get_element_text(transaction_detail['房源信息_房屋现状标签']),
                      '物业地址': self.get_element_text(transaction_detail['房源信息_物业地址标签']),
                      '行政区域': self.get_element_text(transaction_detail['房源信息_行政区域标签']),
                      '是否有抵押': self.get_element_text(transaction_detail['房源信息_是否有抵押标签']),
                      '合同约定的注销抵押日期': self.get_element_text(transaction_detail['房源信息_合同约定的注销抵押日期标签']),
                      '是否唯一': self.get_element_text(transaction_detail['房源信息_是否唯一标签']),
                      '产证年限': self.get_element_text(transaction_detail['房源信息_产证年限标签']),
                      '是否限售房': self.get_element_text(transaction_detail['房源信息_是否限售房标签'])}
        return house_info
