#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: chenjianquan
@version: V1.0
@file: write_excel.py
@time: 2023/2/3
"""
import pandas
import pandas as pd
import numpy as np
from config.conf import cm
from tools.driver import dm


class WriteExcel(object):

    @staticmethod
    def get_coordinates(data: pandas.DataFrame, target: str):
        """
        根据要查找的目标，返回其在excel中的位置
        data: excel数据,
        target: 要查找的目标
        return: 返回坐标列表
        """
        data_list = np.array(data).tolist()
        for i in range(len(data_list)):
            for j in range(len(data_list[i])):
                # 字符串模糊匹配
                if target in str(data_list[i][j]):
                    return [i + 1, j + 1]
        return []

    def write_table_data(self, data: dict, table, line=1):
        """
        :param data: 点数据
        :param table: excel表
        :param line: 表头下面第几行
        """
        # 读取excel文件
        test_data = pd.read_excel(table, header=None, sheet_name='Sheet1')
        for row in data.keys():
            # 获取元素位置
            coordinates = self.get_coordinates(test_data, row)
            if coordinates:
                # 写入数据
                json = {row: coordinates}
                dm.write_excel(table, 'Sheet1', json[row][0] + line, json[row][1], data[row])
            else:
                raise ValueError('Excel表字段信息缺失')

    def del_excel_index(self, table, str_: str):
        """
        删除excel表数据(str_)下一行开始的全部数据
        :param table: excel表
        :param str_: 表数据
        """
        data = pd.read_excel(table, header=None, sheet_name='Sheet1')
        index_ = self.get_coordinates(data, str_)
        data.drop(data.index[index_[0]:], inplace=True)
        data.to_excel(table, header=None, index=False)

    def get_excel_list(self, table, column: str):
        """
        读取excel指定列下的数据
        :param table: excel表
        :param column : 列名
        """
        data = pd.read_excel(table, header=None, sheet_name='Sheet1')
        data = self.get_coordinates(data, column)
        excel_data = pd.read_excel(cm.tmp_file_path('计算点导入-专.xlsx'), 'Sheet1', header=data[0]-1)[column].values.tolist()
        return excel_data

    @staticmethod
    def read_result_excel(filename, col_code, col_reason):
        """读取点表导入结果"""
        df = pd.read_excel(filename, header=None, sheet_name='Sheet1')

        # 找到表头位置
        header_row = None
        for i, row in df.iterrows():
            if not row.isnull().all():
                header_row = i
                break

        # 如果表头下有数据，则读取指定列的数据
        if header_row and df.shape[0] > header_row + 1:  # type: ignore
            df = df.iloc[header_row + 1:]  # type: ignore
            data = df.iloc[:, [col_code, col_reason]].dropna(how="all").to_dict("records")
            return data
        else:
            return None


we = WriteExcel()


if __name__ == '__main__':
    column_ = 15
    reason_table = cm.tmp_path_download('edass_failure.xlsx')
    res = WriteExcel().read_result_excel(reason_table, column_ - 1, column_)
    print(res)
