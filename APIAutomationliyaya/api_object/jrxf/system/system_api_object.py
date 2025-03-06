#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: system_api_object.py
@date: 2021/9/30 0014
"""
from api_decorator.api_decorator import set_header
from config.conf import cm
from common.readconfig import ini
from common.readyaml import ReadYaml
from common.globalvar import GlobalVar
from request_handler.request_handler import RequestHandler

host = ini.schema + '://' + ini.xf_host
system_api = ReadYaml('jrxf/system/system_api')


class SystemApiObject(RequestHandler):

    @staticmethod
    @set_header(host, system_api)
    def upload_img_request(method, url, img_name, content_type):
        """上传图片"""
        header = {'Authorization': GlobalVar.header['Authorization']}
        files = {"file": (img_name, open(cm.tmp_file_path(img_name), "rb"), "image/jpeg")}
        return RequestHandler().requests_api(method, url, header, files=files)

    @staticmethod
    @set_header(host, system_api)
    def upload_file_request(method, url, file_name, content_type):
        """上传文件"""
        header = {'Authorization': GlobalVar.header['Authorization']}
        files = {"file": (file_name, open(cm.tmp_file_path(file_name), "rb"), content_type)}
        return RequestHandler().requests_api(method, url, header, files=files)

    @staticmethod
    @set_header(host, system_api)
    def query_poster_background_request(method, url, query_poster_background_params):
        """获取分享背景api"""
        return RequestHandler().requests_api(method, url, GlobalVar.header, json=query_poster_background_params)

    @staticmethod
    @set_header(host, system_api)
    def current_users_info_request(method, url):
        """获取当前用户信息api"""
        return RequestHandler().requests_api(method, url, GlobalVar.header)

    @staticmethod
    @set_header(host, system_api)
    def use_poster_background_id_request(method, url, poster_background_id):
        """分享api"""
        url = url.replace('@poster_background_id', poster_background_id)
        return RequestHandler().requests_api(method, url, GlobalVar.header)
