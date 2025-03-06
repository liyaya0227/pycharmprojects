#脚本说明：用于项目自动化测试平台冒烟测试驱动
#冒烟测试说明：基本业务流程的正常测试
#执行所有的用例
import pytest

if __name__ == '__main__':
    #pytest.main(['-vs', '-m smoke1'])
    pytest.main(["./test_allure_report/test_add_author_and_delete.py", '-v'])
