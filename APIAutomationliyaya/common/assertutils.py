#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
:@desc:封装断言类
:@author cjj
:@since:2021/8/18
"""

import json
from tools.logger import log


class AssertUtil:

    def assert_code(self, code, expected_code):
        """
        验证返回状态码
        :param code:
        :param expected_code:
        :return:
        """
        try:
            assert int(code) == int(expected_code)
            return True
        except:
            log.error("code error,code is %s,expected_code is %s" % (code, expected_code))
            raise

    def assert_body(self, body, expected_body):
        """
        验证返回结果内容相等
        :param body:
        :param expected_body:
        :return:
        """
        try:
            assert body == expected_body
            return True
        except:
            log.error("body error,body is %s,expected_body is %s" % (body, expected_body))
            raise

    def assert_in_body(self, body, expected_body):
        """
        验证返回结果是否包含期望的结果
        :param body:
        :param expected_body:
        :return:
        """
        try:
            body = json.dumps(body)
            print(body)
            assert expected_body in body
            return True
        except:
            log.error("不包含或者body是错误，body is %s,expected_body is %s" % (body, expected_body))
            raise


    def assert_lenth(self, value):
        """
        验证长度大于0
        :param value:
        :return:
        """
        try:
            assert len(value) > 0
            return True
        except:
            log.error("数据长度小于或等于0，数据获取失败")
            raise
