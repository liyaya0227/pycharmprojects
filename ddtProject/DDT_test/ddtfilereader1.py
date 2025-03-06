#读取ddt文件
#文件类型是CSV
import csv
import os


def get_userinfo():
     # 打开文件
    ddtlist = []

    filedir = os.path.dirname(__file__)
    file1 = open(filedir+"/testcase.csv", 'r', encoding='utf-8')

    # 读取文件
    readers = csv.reader(file1)
    #读文件的时候跳过第一行
    readers.__next__()
    for row in readers:
        #print(type(row[2]), row[2])
        userinfo = eval(row[2])
        print(type(userinfo))
        #print(author[2:-1])
        ddtlist.append(userinfo)
    print(ddtlist)
    return ddtlist
    # 关闭文件
    file1.close()

    #写文件
def write_csv():
    #打开要读取的文件
    file1 = open("testcase.csv", "r", encoding="utf-8")
    #读取文件内容
    readers = csv.reader(file1)
    #打开要写入的文件
    file2 = open("testreport1.csv", "w", encoding="utf-8")
    #指定要写入的文件夹
    writers = csv.writer(file2)
    for row in readers:
        #逐行写入内容
        row.append("实际结果")
        writers.writerow(row)
    print(writers)

    # 关闭文件
    file2.close()

if __name__ == '__main__':
    #get_userinfo()
    write_csv()