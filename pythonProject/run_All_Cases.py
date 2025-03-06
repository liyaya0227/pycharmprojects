import unittest2

from lib.HTMLTestRunner import HTMLTestRunner

if __name__ == '__main__':
    #1、找到学要执行的测试用例
    sunit = unittest2.defaultTestLoader.discover("./test_case", "*Test.py")
    #2、执行找到的测试用例集
    #unittest2.TextTestRunner().run(sunit)
    #3、生成测试用例报告
    #3.1指定测试报告生成的位置
    path = "report/TestReport.html"
    file = open(path, 'wb')
    #实例化HTMLTestRunner这个类，括号里面的参数（二进制文件：，日志的详细程度：默认为1，报告的标题：，报告的正文：，报告的测试人：）
    HTMLTestRunner(stream=file, verbosity=1, title='自动化测试报告', description='测试环境：chrome', tester='liyaya').run(sunit)

