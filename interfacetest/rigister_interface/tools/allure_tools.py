#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: chenjianquan
@version: V1.0
@file: allure_tools.py
@time: 2022/11/29
"""
import json
import allure
from functools import wraps


def allure_step_no(step: str):
    """
    无附件的操作步骤
    :param step: 步骤名称
    :return:
    """
    with allure.step(step):
        pass


def allure_step(step: str, var: str) -> None:
    """
    :param step: 步骤及附件名称
    :param var: 附件内容
    :return:
    """
    with allure.step(step):
        allure.attach(
            json.dumps(
                str(var),
                ensure_ascii=False,
                indent=4),
            step,
            allure.attachment_type.JSON)


def allure_step2(var: str, en_name: str) -> None:
    """
    :param var: 附件内容
    :param en_name: 附件名称
    :return:
    """
    allure.attach(
        json.dumps(
            str(var),
            ensure_ascii=False,
            indent=4),
        en_name,
        allure.attachment_type.JSON)

# def allure_step(step: str, var: str, key=True) -> None:
#     """
#     :param step: 步骤及附件名称
#     :param var: 附件内容
#     :param key: 是否作为步骤
#     :return:
#     """
#     attachment_type = allure.attachment_type.JSON
#     attachment_data = json.dumps(var, ensure_ascii=False, indent=4)
#
#     if key:
#         with allure.step(step):
#             allure.attach(attachment_data, step, attachment_type)
#     else:
#         allure.attach(attachment_data, step, attachment_type)