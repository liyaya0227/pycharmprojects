#如何使用unittest2
#第一步：导包
import unittest2

#第二步，继承
#继承unittest2中的TestCase表示我们的类是一个测试用例类
class Unittest2Demo(unittest2.TestCase):

#第三步，声明一个以test开头的方法
    #以test开头的的方法，表示这是一个测试用例方法，这个方法可以直接运行，其他开头的方法是普通方法，需要调用
    def test_login(self):
        print(1)

    def test_register(self):
        print(2)

#第四步：重写父类中的两个方法
#1、setUp（），在每条测试用例开始前，要做的预置条件
#2、tearDown（），在每条测试用例结束后，要做的场景还原
    def setUp(self):
        print(3)
    def tearDown(self):
        print(4)

#第六步：重写父类的两个类方法
#1、setUpClass（），在类调用开始前，要做的预置条件
#2、tearDownClass（），在类调用结束后，要做的场景还原
    @classmethod
    def setUpClass(cls):
        print(5)

    @classmethod
    def tearDownClass(cls):
        print(6)

#第五步，主函数运行,表示在当前文件被运行，其他文件无法运行
