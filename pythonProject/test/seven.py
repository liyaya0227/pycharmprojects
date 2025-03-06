#定义类：登录测试点
class  Test_login :
    #定义属性：username,password,在初始化方法中定义
    def __init__(self, a, b):
        self.username = a
        self.password = b

    # 定义方法：提取测试点
    def test_case(self):
        print("用户名", self.username, end="   ")
        print("密码", self.password)

#定义类：注册测试
class Test_register(Test_login):
    #定义属性:email
    def __init__(self, a, b):
        #使用父类属性
        super().__init__(a, b)
        #定义子类属性
        self.email = "123@qq.com"


# 定义方法：提取测试点
    def test_case(self):
        #调用父类的方法
        super().test_case()
        #打印邮箱的测试数据
        print("邮箱", self.email)


#类的调用
if __name__ == '__main__':
    # # 以只读的方式打开csv文件
    # file = open("yy.csv", "r")
    # # 获取文件内容
    # content = csv.reader(file)
    # for i in content:
    #     # 实例化
    #     login = Test_login(i[0], i[1])
    #     # 调用类方法,对象名.类方法名
    #     login.test_case()
    register = Test_register('zhanfsan', '111111')
    register.test_case()