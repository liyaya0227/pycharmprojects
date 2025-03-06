#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
:@desc:读取yaml文件类
:@author caijj
:@since:2021/8/18
"""
import yaml
from string import Template
from config.conf import cm


class ReadYaml:
    """获取元素"""

    def __init__(self, name):
        self.name = name
        self.file_path = cm.yaml_file(self.name)
        with open(self.file_path, encoding='utf-8') as f:
            self.data = yaml.safe_load(f)

    def __getitem__(self, item):
        """获取属性"""
        data = self.data.get(item)
        if data:
            # name, value = data.split('==')
            return data
        raise ArithmeticError("{}.yaml中不存在关键字：{}".format(self.name, item))

    def update(self, item, value):
        """更新yaml文件"""
        self.data[item] = value
        with open(self.file_path, 'w', encoding='utf-8') as fp:
            yaml.safe_dump(self.data, fp, default_flow_style=False)

    def get_data(self,  value):
        """获取yaml数据"""
        # self.name = name
        # self.testdata_path = cm.testdata_file(self.name)
        with open(self.file_path, encoding='utf-8') as fp:
            read_yml_str = fp.read()
            tempTemplate1 = Template(read_yml_str)
            c = tempTemplate1.safe_substitute({"login_host": value})
            # yml 文件数据，转 python 类型
            yaml_data = yaml.safe_load(c)
        return yaml_data


if __name__ == '__main__':
    search = ReadYaml('login/login_sz')

