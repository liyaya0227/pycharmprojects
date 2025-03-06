import csv
import requests

list = []
class Test():
    # 数据
    def __init__(self):
        file = open("test2.csv", "r", encoding="utf-8")
        table = csv.reader(file)

        for row in table:
            self.url = row[1]
            self.expresult = row[3]
            self.interfacename = row[5]
            # print(self.url,"    ",self.expresult,"   ", self.interfacename)
            userinfo = {}
            j = int(row[6])
            for i in range(7, 2 * j + 7, 2):
                userinfo[row[i]] = row[i + 1]
            list.append(userinfo)
        print("列表：", list)
        #return list

    # 接口
    def sy_test(self):
            print("接受的列表：", list)
            for row in list:
                print("接受的数据:", row)
                response = requests.post(self.url, row).text
                print(response)
                r = response.find(self.expresult)
                if r > 0:
                    print(self.interfacename, "测试通过")
                else:
                    print(self.interfacename, "测试不通过")

if __name__ == '__main__':
        # 实例化类，传入参数
    obj = Test()
    obj.sy_test()