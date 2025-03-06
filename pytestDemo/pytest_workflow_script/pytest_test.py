import pytest


class Test_pytest01():
    #自定义排序
    @pytest.mark.run(order=2)
    def test_01(self):
        print('这是测试方法1')

    @pytest.mark.run(order=1)
    def test_02(self):
        print('这是测试方法2')

    @pytest.mark.run(order=3)
    def test_03(self):
        print('这是测试方法3')