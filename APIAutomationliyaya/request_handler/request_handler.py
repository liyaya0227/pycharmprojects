# -*- coding:utf-8 -*-
"""
@author: caijj
@file: RequestHandler.py
@time: 2021/8/18
@desc:
"""
import requests
from tools.logger import log
from tools.times import sleep


class RequestHandler(object):

    @staticmethod
    def requests_api(method, url, header, json=None, params=None, cookies=None, files=None):
        log.info('method: ' + method)
        log.info('url: ' + url)
        log.info('headers: ' + str(header))
        if json is not None:
            log.info('json: ' + str(json))
        if params is not None:
            log.info('params: ' + str(params))
        res = None
        requests.packages.urllib3.disable_warnings()
        while res is None:
            try:
                if method == "GET":
                    res = requests.get(url=url, params=params, json=json, headers=header, cookies=cookies, files=None,
                                       verify=False)
                elif method == "POST":
                    res = requests.post(url=url, params=params, json=json, headers=header, cookies=cookies, files=files,
                                        verify=False)
                else:
                    raise ValueError('not support now')
            except requests.exceptions.ConnectionError:
                log.info('连接失败，进行重新连接')
                sleep()
        response = res.json()
        log.info('response: ' + str(response))
        return response
