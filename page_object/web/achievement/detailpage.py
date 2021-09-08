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

detail = Element('web/achievement/detail')


class AchievementDetailPage(WebPage):

    def click_submit_button(self):  # 点击提交按钮
        self.is_click(detail['提交按钮'])

    def get_examine_time(self):  # 获取审核时间
        return self.element_text(detail['审核时间标签']).split('\n')[1]

    def click_add_role_button(self):  # 点击新增角色人按钮
        self.is_click(detail['新增角色人按钮'])

    def input_customer_partner_proportion_by_index(self, proportion, index=1):  # 输入客源合作人比例
        locator = 'xpath', \
                  "(//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                  "//div[contains(@class,'roleTable')]//table//td[text()='客源合作人']/parent::tr)[" + str(index) + "]/td[" \
                  + str(self.__get_proportion_table_column_by_title('分配比例')) + "]//input"
        self.input_text(locator, proportion)

    def input_customer_partner_name_by_index(self, customer_partner_info, index=1):  # 输入客源合作人姓名
        locator = 'xpath', \
                  "(//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                  "//div[contains(@class,'roleTable')]//table//td[text()='客源合作人']/parent::tr)[" + str(index) + "]/td[" \
                  + str(self.__get_proportion_table_column_by_title('角色人')) + "]//input"
        self.input_text(locator, customer_partner_info['姓名'])
        sleep(0.5)
        role_list = self.find_elements(detail['下拉框'])
        for role_ele in role_list:
            if customer_partner_info['姓名'] in role_ele.text and customer_partner_info['店组'] in role_ele.text:
                role_ele.click()
                return

    def add_customer_partner(self, customer_partners):  # 添加客源合作人
        for m in range(len(customer_partners)):
            self.click_add_role_button()
            self.input_customer_partner_proportion_by_index(customer_partners[m]['比例'], m + 1)
            customer_partner_info = {'姓名': customer_partners[m]['姓名'],
                                     "店组": customer_partners[m]['店组']}
            self.input_customer_partner_name_by_index(customer_partner_info, m + 1)

    def get_proportion_table_data(self):  # 获取比例列表所有数据
        data = []
        table_rows = self.find_elements(detail['比例列表行数'])
        for m in range(len(table_rows)):
            row_data = {}
            role_type_locator = 'xpath', \
                                "//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                                "//div[contains(@class,'roleTable')]//table/tbody/tr[" + str(m+1) + "]/td[" \
                                + str(self.__get_proportion_table_column_by_title('角色类型')) + "]"
            row_data['角色类型'] = self.element_text(role_type_locator)
            proportion_locator = 'xpath', \
                                 "//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                                 "//div[contains(@class,'roleTable')]//table/tbody/tr[" + str(m+1) + "]/td[" \
                                 + str(self.__get_proportion_table_column_by_title('分配比例')) + "]"
            row_data['分配比例'] = self.element_text(proportion_locator).split('%')[0]
            role_name_locator = 'xpath', \
                                "//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                                "//div[contains(@class,'roleTable')]//table/tbody/tr[" + str(m+1) + "]/td[" \
                                + str(self.__get_proportion_table_column_by_title('角色人')) + "]/span"
            row_data['角色人'] = self.element_text(role_name_locator)
            role_shop_group_locator = 'xpath', \
                                      "//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                                      "//div[contains(@class,'roleTable')]//table/tbody/tr[" + str(m+1) + "]/td[" \
                                      + str(self.__get_proportion_table_column_by_title('角色人店组')) + "]"
            row_data['角色人店组'] = self.element_text(role_shop_group_locator)
            role_manager_locator = 'xpath', \
                                   "//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                                   "//div[contains(@class,'roleTable')]//table/tbody/tr[" + str(m+1) + "]/td[" \
                                   + str(self.__get_proportion_table_column_by_title('商圈经理')) + "]/a"
            row_data['商圈经理'] = self.element_text(role_manager_locator)
            role_company_locator = 'xpath', \
                                   "//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                                   "//div[contains(@class,'roleTable')]//table/tbody/tr[" + str(m+1) + "]/td[" \
                                   + str(self.__get_proportion_table_column_by_title('加盟商')) + "]"
            row_data['加盟商'] = self.element_text(role_company_locator)
            data.append(row_data)
        return data

    def __get_proportion_table_column_by_title(self, title):  # 根据标题名获取列数
        title_list = self.find_elements(detail['比例列表头'])
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele) + 1

    def click_receivable_achievement_tab(self):  # 点击应收业绩标签
        self.is_click(detail['应收业绩标签'], sleep_time=1)

    def click_received_achievement_tab(self):  # 点击实收业绩标签
        self.is_click(detail['实收业绩标签'], sleep_time=1)

    def get_achievement_table_data(self):  # 获取业绩列表所有数据
        data = []
        table_rows = self.find_elements(detail['业绩列表行数'])
        for m in range(len(table_rows)):
            row_data = {}
            settlement_month_locator = 'xpath', \
                                       "//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                                       "//div[contains(@class,'achievementTable')]" \
                                       "//div[@role='tabpanel' and @aria-hidden='false']//table/tbody/tr[" + str(m+1) \
                                       + "]/td[" + str(self.__get_achievement_table_column_by_title('结算月')) + "]"
            row_data['结算月'] = self.element_text(settlement_month_locator)
            trade_type_locator = 'xpath', \
                                 "//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                                 "//div[contains(@class,'achievementTable')]" \
                                 "//div[@role='tabpanel' and @aria-hidden='false']//table/tbody/tr[" + str(m+1) \
                                 + "]/td[" + str(self.__get_achievement_table_column_by_title('业务类型')) + "]"
            row_data['业务类型'] = self.element_text(trade_type_locator)
            fee_name_locator = 'xpath', \
                               "//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                               "//div[contains(@class,'achievementTable')]" \
                               "//div[@role='tabpanel' and @aria-hidden='false']//table/tbody/tr[" + str(m+1) \
                               + "]/td[" + str(self.__get_achievement_table_column_by_title('费用项')) + "]"
            row_data['费用项'] = self.element_text(fee_name_locator)
            role_type_locator = 'xpath', \
                                "//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                                "//div[contains(@class,'achievementTable')]" \
                                "//div[@role='tabpanel' and @aria-hidden='false']//table/tbody/tr[" + str(m+1) \
                                + "]/td[" + str(self.__get_achievement_table_column_by_title('角色类型')) + "]"
            row_data['角色类型'] = self.element_text(role_type_locator)
            proportion_locator = 'xpath', \
                                 "//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                                 "//div[contains(@class,'achievementTable')]" \
                                 "//div[@role='tabpanel' and @aria-hidden='false']//table/tbody/tr[" + str(m+1) \
                                 + "]/td[" + str(self.__get_achievement_table_column_by_title('分配比例')) + "]"
            row_data['分配比例'] = self.element_text(proportion_locator).split('%')[0]
            role_name_locator = 'xpath', \
                                "//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                                "//div[contains(@class,'achievementTable')]" \
                                "//div[@role='tabpanel' and @aria-hidden='false']//table/tbody/tr[" + str(m+1) \
                                + "]/td[" + str(self.__get_achievement_table_column_by_title('角色人')) + "]"
            row_data['角色人'] = self.element_text(role_name_locator)
            role_shop_group_locator = 'xpath', \
                                      "//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                                      "//div[contains(@class,'achievementTable')]" \
                                      "//div[@role='tabpanel' and @aria-hidden='false']//table/tbody/tr[" + str(m+1) \
                                      + "]/td[" + str(self.__get_achievement_table_column_by_title('角色人店组')) + "]"
            row_data['角色人店组'] = self.element_text(role_shop_group_locator)
            role_manager_locator = 'xpath', \
                                   "//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                                   "//div[contains(@class,'achievementTable')]" \
                                   "//div[@role='tabpanel' and @aria-hidden='false']//table/tbody/tr[" + str(m+1) \
                                   + "]/td[" + str(self.__get_achievement_table_column_by_title('商圈经理')) + "]"
            row_data['商圈经理'] = self.element_text(role_manager_locator)
            achievement_locator = 'xpath', \
                                  "//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                                  "//div[contains(@class,'achievementTable')]" \
                                  "//div[@role='tabpanel' and @aria-hidden='false']//table/tbody/tr[" + str(m+1) \
                                  + "]/td[" + str(self.__get_achievement_table_column_by_title('业绩额')) + "]"
            row_data['业绩额'] = self.element_text(achievement_locator).replace(',', '')
            role_company_locator = 'xpath', \
                                   "//div[@style='' or not(@style)]/div[contains(@class,'achievementDetail')]" \
                                   "//div[contains(@class,'achievementTable')]" \
                                   "//div[@role='tabpanel' and @aria-hidden='false']//table/tbody/tr[" + str(m+1) \
                                   + "]/td[" + str(self.__get_achievement_table_column_by_title('加盟商')) + "]"
            row_data['加盟商'] = self.element_text(role_company_locator)
            data.append(row_data)
        return data

    def __get_achievement_table_column_by_title(self, title):  # 根据标题名获取列数
        title_list = self.find_elements(detail['业绩列表头'])
        for title_ele in title_list:
            if title_ele.text == title:
                return title_list.index(title_ele) + 1
