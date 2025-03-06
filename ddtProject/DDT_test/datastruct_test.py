#测试的数据结构一般有：列表、字典、json串
#1、列表
#list = [1, 2, 3, 4, 'good']
#读取列表
#for i in list:
#    print(i)
#添加列表字段
#list.append('study')
#print(list)
print('---------------------------------------')
#2、字典
#dict1 = {'name': 'zhangsan', 'age': 20}
#dict2 = dict(name='lisi', age=22)
#print(dict1)
#print(dict2)
#读取字典key（）、value（）、item（）
#for key in dict1.keys():
#    print(key)
#for value in dict1.values():
#    print(value)
#获取的值类型为元组
#for item in dict1.items():
#    print(item)
#    print(type(item))
#可以直接获取值
#for item in dict1:
#    print(item, dict1[item])
#添加字典字段
#dict1['gender'] = '男'
#print(dict1)
print('---------------------------------------')
#3、json串
#读取json文件
#import json
#jsonfile = open('interface.json', 'r', encoding='utf-8')
#print(jsonfile)
#转换json类型为字典类型
#jsondict = json.load(jsonfile)
#print(jsondict)
#print(jsondict['contractBase'])
#print(type(jsondict['contractBase']))
#print(type(jsondict['contractBase']['baseInfo']))
#读取内容
#for data in jsondict['contractBase']:
#    print(type(data))
#for d in jsondict['contractBase']['baseInfo']:
#    print(d, jsondict['contractBase']['baseInfo'][d])
print('---------------------------------------')



