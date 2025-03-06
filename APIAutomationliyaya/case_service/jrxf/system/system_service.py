#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: system_service.py
@date: 2021/9/17 0017
"""
from api_object.jrxf.system.system_api_object import SystemApiObject

system_api = SystemApiObject()


class SystemService(object):

    @staticmethod
    def upload_img(file_name):
        """上传图片"""
        upload_img_res = system_api.upload_file_request(file_name, "image/jpeg")
        return upload_img_res

    @staticmethod
    def upload_pdf_file(file_name):
        """上传pdf文件"""
        upload_file_res = system_api.upload_file_request(file_name, "application/pdf")
        return upload_file_res



