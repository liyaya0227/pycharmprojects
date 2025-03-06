#注册接口的测试
#接口参数："1、username 2、password 3、email 4、phone 5、question 6、answer
#接口url：http://localhost:8080/jwshoplogin//user/register.do

import requests


class Test_register():
    def __init__(self):
        self.url = "http://localhost:8080/jwshoplogin//user/register.do"
        self.userinfo = {
            "username": "李四",
            "password": "123456",
            "email": "zhangsan.qq.com",
            "phone": "16372819283",
            "question": "现在最想吃什么",
            "answer": "火锅"
        }
    def test_register(self):
        #发送接口请求
        s = requests.session()
        #获取接口返回值
        response = s.post(self.url, data=self.userinfo).json()
        print(response)
        #判断测试结果

        if response["msg"] == "注册成功":
            print("测试通过")
        else:
            print("测试不通过")
if __name__ == '__main__':
    obj = Test_register()
    obj.test_register()