#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: jsonutil.py
@time: 2021/08/18
"""

import json


def get_data(json_file_path):
    with open(json_file_path, 'r', encoding="utf-8") as f:
        dict_data = json.load(f)
    return dict_data


def get_value(json_file_path, key):
    with open(json_file_path, 'r', encoding="utf-8") as f:
        dict_data = json.load(f)
    return dict_data[key]


def change_key_value_with_file(file_name, params_dict):
    params = get_data(file_name)
    return change_key_value(params, params_dict)


def change_key_value(params, update_params):
    if type(params) is dict and type(update_params) is dict:
        for key, value in update_params.items():
            if type(value) is dict and len(params[key]) > 0:
                for sub_key, sub_value in value.items():
                    if type(sub_value) is dict and len(params[key][sub_key]) > 0:
                        for n_sub_key, n_sub_value in sub_value.items():
                            params[key][sub_key][n_sub_key] = n_sub_value
                    else:
                        params[key][sub_key] = sub_value
            else:
                params[key] = value
        return params
    else:
        raise ValueError('参数错误')


if __name__ == '__main__':
    file = r"/TestData/house/business/test_add.json"
    print(change_key_value_with_file(file))
