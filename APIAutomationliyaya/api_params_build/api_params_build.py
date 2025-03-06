#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: api_params_build.py
@date: 2021/9/9 0009
"""
from tools.jsonutil import change_key_value_with_file, get_data


class ApiParamsBuild(object):

    @staticmethod
    def request_params_build(params_json_file, params):
        """
        :return: request_params
        """
        if params is None:
            return get_data(params_json_file)
        else:
            return change_key_value_with_file(params_json_file, params)
