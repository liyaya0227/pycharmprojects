#测试登录的借口
#初级测试：参数正确，不同的参数得出不同的结果
#参数：username，password
#接口：http://localhost:8080/jwshoplogin/user/login.do
#参数的返回值：登录成功，用户名不存在，密码错误
import requests

#调用接口
url = "http://localhost:8080/jwshoplogin/user/login.do"
userinfo = {"username": "张三", "password": 123456}
#传入接口参数
#获取返回值: text用来获取返回值的内容
response = requests.post(url, data=userinfo).text
print(response)
#进行比对，得出测试的结果
msg = response.find("用户名不存在")
if msg > 0:
    print("测试通过")
else:
    print("测试不通过")
