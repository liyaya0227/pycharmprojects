#测试登录的借口
#初级测试：参数正确，不同的参数得出不同的结果
#参数：username，password
#接口：http://localhost:8080/jwshoplogin/user/login.do
#参数的返回值：登录成功，用户名不存在，密码错误
#通过csv文件，进行用例参数的传入
import requests
import csv


#调用接口
url = "http://localhost:8080/jwshoplogin/user/login.do"
#userinfo = {"username": "张三", "password": 123456}
#传入接口参数
#读取csv文件
file = open("userinfo.csv", "r", encoding="utf-8")
file2 = open("logintestreport.csv", "w", encoding="utf-8")
table = csv.reader(file)
#跳过第一行
#table.__next__()
table2 = csv.writer(file2)
rowhead = ["username", "password", "预期结果", "实际结果"]
table2.writerow(rowhead)
userinfo = {}
for row in table:
    #print(row[0])
    userinfo["username"] = row[0]
    userinfo["password"] = row[1]

    #print(userinfo)
#获取返回值: text用来获取返回值的内容
    response = requests.post(url, data=userinfo).text
    print(response)
#进行比对，得出测试的结果
    msg = response.find(row[2])
    if msg > 0:
        print("测试通过")
        # 写进文件
        row.append("测试通过")
        table2.writerow(row)
        #print(type(row))
    else:
        print("测试不通过")
        row.append("测试不通过")
        table2.writerow(row)

file.close()
file2.close()
#将结果生成报告，写进csv文件里，有一条结果就写进文件里，写完之后就关闭文件
