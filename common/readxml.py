#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
:@desc:读取xml文件类
:@author caijj
:@since:2021/9/18
"""
import xml.dom.minidom
from config.conf import cm


class ReadXml:
    """读取xml"""

    def __init__(self, name):
        self.name = name
        self.file_path = cm.xml_file(self.name)
        try:
            dom = xml.dom.minidom.parse(self.file_path)  # 打开xml文档  # 打开xml文档
            self.root = dom.documentElement  # 得到文档元素对象
        except Exception as e:
            print("Error: 无法打开文件，{}！", format(e))

    def get_sql(self, table_name, sql_id):
        """获取sql"""
        for table in self.root.getElementsByTagName('table'):
            name = table.getAttribute('name')
            if name == table_name:
                for sql in table.getElementsByTagName('sql'):
                    id = sql.getAttribute('id')
                    if sql_id == id:
                        captions = sql.getElementsByTagName('caption')
                        sql_data = captions[0].firstChild.data
                        sql_data = sql_data.replace('\n', '')
                        sql_data = sql_data.strip()
                        return sql_data


if __name__ == '__main__':
    read = ReadXml("/web/house/house_sql")
    sql = read.get_sql('trander_house', 'select_house_info')
    print(sql)
