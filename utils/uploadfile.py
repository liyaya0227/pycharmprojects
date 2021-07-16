#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: uploadfile.py
@time: 2021/06/22
"""

import win32gui
import win32con
from utils.timeutil import sleep


def upload_file(file_path, browser_type='chrome'):
    if browser_type.lower() == "chrome":
        title = '打开'
    elif browser_type.lower() == "firefox":
        title = '文件上传'
    elif browser_type.lower() == "ie":
        title = '选择要加载的文件'
    else:
        title = ''
    dialog = win32gui.FindWindow('#32770', title)  # 对话框
    combo_box_ex32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
    combo_box = win32gui.FindWindowEx(combo_box_ex32, 0, 'ComboBox', None)
    edit = win32gui.FindWindowEx(combo_box, 0, 'Edit', None)  # 上面三句依次寻找对象，直到找到输入框对象的句柄
    win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, file_path)  # 往输入框输入绝对地址
    button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 确认按钮
    win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击确认按钮
    sleep(2)
