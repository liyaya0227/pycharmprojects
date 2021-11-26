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

    @staticmethod
    def generate_account_statement_job(web_driver):
        job_login = LoginPage(web_driver)
        main_left_view = MainLeftViewPage(web_driver)
        main_up_view = MainUpViewPage(web_driver)
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
        if job_login.get_current_url() != ini.job_url:
            main_up_view.log_out()
        job_login.input_account(ini.job_user_account)
        job_login.input_password(ini.job_user_password)
        job_login.click_login_button()
        main_left_view.click_job_management()
        job_management_table.choose_job('苏州job')
        job_management_table.input_executor_handler_search('GenerateAccountStatementJob')
        job_management_table.click_search_button()
        param = 'topNum=200&execTime=' + dt_strftime("%Y-%m-%d")
        job_management_table.execute_once_job_by_row(1, param)
        web_driver.close()
        web_driver.switch_to_window(current_handle)  # 切换窗口
        sleep(2)

    @staticmethod
    def certificate_out_date_job(web_driver):
        job_login = LoginPage(web_driver)
        main_left_view = MainLeftViewPage(web_driver)
        main_up_view = MainUpViewPage(web_driver)
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
        if job_login.get_current_url() != ini.job_url:
            main_up_view.log_out()
        job_login.input_account(ini.job_user_account)
        job_login.input_password(ini.job_user_password)
        job_login.click_login_button()
        main_left_view.click_job_management()
        job_management_table.choose_job('苏州job')
        job_management_table.input_executor_handler_search('CertificateExpiredJob')
        job_management_table.click_search_button()
        job_management_table.execute_once_job_by_row(1)
        web_driver.close()
        web_driver.switch_to_window(current_handle)  # 切换窗口
        sleep(2)

    @staticmethod
    def house_verify_out_date_job(web_driver):
        job_login = LoginPage(web_driver)
        main_left_view = MainLeftViewPage(web_driver)
        main_up_view = MainUpViewPage(web_driver)
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
        if job_login.get_current_url() != ini.job_url:
            main_up_view.log_out()
        job_login.input_account(ini.job_user_account)
        job_login.input_password(ini.job_user_password)
        job_login.click_login_button()
        main_left_view.click_job_management()
        job_management_table.choose_job('苏州job')
        job_management_table.input_handler_description_search('房源验真过期')
        job_management_table.input_executor_handler_search('HouseVerifyJob')
        job_management_table.click_search_button()
        job_management_table.execute_once_job_by_row(1)
        web_driver.close()
        web_driver.switch_to_window(current_handle)  # 切换窗口
        sleep(2)
