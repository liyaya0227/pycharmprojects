#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: job_service.py
@date: 2021/10/15 0015
"""
from common.readconfig import ini
from page_object.jrjob.main.upviewpage import MainUpViewPage
from utils.timeutil import sleep, dt_strftime
from page_object.jrjob.login.loginpage import LoginPage
from page_object.jrjob.main.leftviewpage import MainLeftViewPage
from page_object.jrjob.jobmanagement.tablepage import JobManagementTablePage


class JobService(object):

    def generate_account_statement_job(self, web_driver):
        param = 'topNum=200&execTime=' + dt_strftime("%Y-%m-%d")
        self.__exec_job(web_driver, job_type='苏州job', job_description='', job_handler='GenerateAccountStatementJob',
                        exec_param=param)

    def certificate_out_date_job(self, web_driver):
        self.__exec_job(web_driver, job_type='苏州job', job_description='VIP书面委托到期提示',
                        job_handler='CertificateDelegateAndVipJob')

    def house_verify_out_date_job(self, web_driver):
        self.__exec_job(web_driver, job_type='苏州job', job_description='房源验真过期', job_handler='')

    def house_follow_up_remind_job(self, web_driver, flag='买卖'):
        if flag == '买卖':
            self.__exec_job(web_driver, job_type='苏州job', job_description='共享池_买卖房源维护跟进提醒',
                            job_handler='TradeHouseRemindJob')
        elif flag == '租赁':
            self.__exec_job(web_driver, job_type='苏州job', job_description='共享池_租赁房源维护跟进提醒',
                            job_handler='RentHouseRemindJob')
        else:
            raise ValueError('传值错误')

    def house_into_share_pool_remind_job(self, web_driver, flag='买卖'):
        if flag == '买卖':
            self.__exec_job(web_driver, job_type='苏州job', job_description='共享池_买卖房源即将进入共享池提醒',
                            job_handler='TradeSharePoolRemindJob')
        elif flag == '租赁':
            self.__exec_job(web_driver, job_type='苏州job', job_description='共享池_租赁房源即将进入共享池提醒',
                            job_handler='RentSharePoolRemindJob')
        else:
            raise ValueError('传值错误')

    def house_into_store_share_pool_job(self, web_driver):
        self.__exec_job(web_driver, job_type='苏州job', job_description='共享池_进入门店', job_handler='share_pool_store_entry')

    def house_into_region_share_pool_job(self, web_driver):
        self.__exec_job(web_driver, job_type='苏州job', job_description='共享池_进入运营区',
                        job_handler='share_pool_region_entry')

    @staticmethod
    def __exec_job(web_driver, job_type='苏州job', job_description='', job_handler='', exec_param=None):
        job_login = LoginPage(web_driver)
        main_left_view = MainLeftViewPage(web_driver)
        # main_up_view = MainUpViewPage(web_driver)
        job_management_table = JobManagementTablePage(web_driver)

        current_handle = web_driver.current_window_handle
        js = "window.open('" + ini.job_url + "');"  # 通过执行js，开启一个新的窗口
        web_driver.execute_script(js)
        sleep(4)
        all_handles = web_driver.window_handles  # 获取当前窗口句柄
        for handle in all_handles:
            if handle != current_handle:
                web_driver.switch_to_window(handle)  # 切换窗口
                break
        if job_login.get_current_url() == ini.job_url:
            # main_up_view.log_out()
            job_login.input_account(ini.job_user_account)
            job_login.input_password(ini.job_user_password)
            job_login.click_login_button()
        main_left_view.click_job_management()
        job_management_table.choose_job(job_type)
        job_management_table.input_handler_description_search(job_description)
        job_management_table.input_executor_handler_search(job_handler)
        job_management_table.click_search_button()
        job_management_table.execute_once_job_by_row(1, exec_param)
        web_driver.close()
        web_driver.switch_to_window(current_handle)  # 切换窗口
        sleep(2)
