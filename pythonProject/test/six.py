#定义类：登录测试点

class  Test():
    #定义属性：username,password,在初始化方法中定义
    def __init__(self, username, password):
        self.username = username
        self.password = password


    def test_case(self):
        print("用户名", self.username)
        print("密码", self.password)
    #定义方法：提取测试点


#类的调用
if __name__ == '__main__':
    # 实例化
    login = Test('zhangsan', '111111')
    # 调用类方法,对象名.类方法名
    login.test_case()