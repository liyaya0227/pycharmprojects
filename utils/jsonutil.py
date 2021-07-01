#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: jsonutil.py
@time: 2021/06/30
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


if __name__ == '__main__':
    file = r"/TestData/house/business/test_add.json"
    print(get_data(file))
