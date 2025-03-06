#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: chenjianquan
@version: V1.0
@file: request_handler.py
@time: 2022/7/12
"""
import allure
import requests
from tools.allure_tools import allure_step_no, allure_step, allure_step2
from tools.logger import log
from tools.times import sleep


class RequestHandler(object):

    @staticmethod
    def requests_api(method, url, header, json=None, params=None, cookies=None, files=None, data=None, key=None):
        allure_step_no(f"请求URL: {url}")
        allure_step_no(f"请求方式: {method}")
        with allure.step("请求参数: "):
            for row in locals().items():
                if row[1]:
                    log.info(f'{row[0]}: {row[1]}')
                    if row[0] not in ['method', 'url', 'key']:
                        allure_step2(row[1], f"{row[0]}参数:")
        res = None
        while res is None:
            try:
                if method in ['GET', 'POST', 'PUT', 'DELETE']:
                    res = requests.request(method=method.lower(), url=url, params=params, json=json, headers=header,
                                           cookies=cookies, data=data, files=files, verify=False)
                else:
                    raise ValueError('not support now')
            except requests.exceptions.ConnectionError:
                log.info('连接失败，进行重新连接')
                sleep()
        code = res.status_code
        if key == 'initial':
            return res
        else:
            # noinspection PyBroadException
            try:
                json = res.json()
                json['res_code'] = code
                response = json
            except Exception:
                response = res.text
            allure_step("响应结果: ", response)
            log.info('response: ' + str(response))
            time_consuming = f"响应耗时(ms): {round(res.elapsed.total_seconds() * 1000, 2)}"
            allure_step_no(time_consuming)
            log.info(time_consuming)
            log.info('=' * 95)
            return response
