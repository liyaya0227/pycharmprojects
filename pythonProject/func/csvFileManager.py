#1、倒入代码库
import csv
#2、指定csv文件所在路径
path = r"/Users/liyaya/Downloads/register_data_cases.csv"
#3、打开csv文件
file = open(path)
#4、读取csv文件内容
table = csv.reader(file)
#5、打印csv文件的内容
for item in table:
    print(item)