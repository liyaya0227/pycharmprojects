import pytest


condition = '回归'
class Test_pytest02():
    #自定义那些方法可以跳过不执行
    @pytest.mark.skip('冒烟测试')
    def test_01(self):
        print('这是测试方法1')

    @pytest.mark.run(order=1)
    def test_02(self):
        print('这是测试方法2')

    @pytest.mark.skipif(condition == '回归', reason='回归测试哈')
    def test_03(self):
        print('这是测试方法3')