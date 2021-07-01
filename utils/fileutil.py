#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: fileutil.py
@time: 2021/06/23
"""

import os
import docx


def search_file_in_dir(dir_path, file_name):
    for item in os.listdir(dir_path):
        if file_name in item:
            return os.path.join(dir_path, item)
    return ''


def ergodic_dir(dir_path):
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            ergodic_dir(item_path)
        elif os.path.isfile(item_path):
            print(item_path)


def get_docx_file_content(file_path):
    doc = docx.Document(file_path)
    full_content = []
    for i in doc.paragraphs:
        full_content.append(i.text)
    return '\n'.join(full_content)


def delete_file(file_path):
    os.remove(file_path)


if __name__ == '__main__':
    file = search_file_in_dir(r"D:\\PythonProject\\UIAutomation\\ui\\tmp", '一般委托书')
    print(get_docx_file_content(file))
    # delete_file("D:\\PythonProject\\UIAutomation\\ui\\tmp\\【合创】一般委托书 2021-06-23 13-07-44.docx")
