#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: inspect_page_element.py
@time: 2021/06/22
"""

import os
import yaml
from config.conf import cm
from utils.timeutil import running_time


@running_time
def inspect_elements():
    """检查所有的元素是否正确
    只能做一个简单的检查
    """
    for root, dirs, files in os.walk(cm.ELEMENT_PATH):
        for file in files:
            _path = os.path.join(root, file)
            with open(_path, encoding='utf-8') as f:
                data = yaml.safe_load(f)
            for k in data.values():
                try:
                    pattern, value = k.split('==')
                except ValueError:
                    raise Exception("元素表达式中没有`==`")
                if pattern not in cm.LOCATE_MODE:
                    raise Exception('%s中元素[%s]没有指定类型' % (_path, k))
                elif pattern == 'xpath':
                    assert '//' in value,\
                        '%s中元素[%s]xpath类型与值不配' % (_path, k)
                elif pattern == 'css':
                    assert '//' not in value, \
                        '%s中元素[%s]css类型与值不配' % (_path, k)
                else:
                    assert value, '%s中元素[%s]类型与值不匹配' % (_path, k)


if __name__ == '__main__':
    inspect_elements()
