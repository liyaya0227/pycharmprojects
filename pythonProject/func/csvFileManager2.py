
import csv
import os.path


def reader(filename):
    #path = r"../test_data/" + filename
    #获取当前所在文件夹的名称
    basepath = os.path.dirname(__file__)
    path = basepath.replace("func", "test_data/"+filename)
    file = open(path)
    table = csv.reader(file)
    #表格中的第一行不是有效内容，要去掉第一行，类型是[]
    #定义一个空列表
    list = []
    i = 0
    for item in table:
        if i == 0:
            pass
        else:
            list.append(item)
        i = i + 1
    return list