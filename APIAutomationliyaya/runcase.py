import os
import shutil
import subprocess

import pytest

from config.conf import cm
from tools.logger import log

if __name__ == '__main__':
    pytest.main()

    # result_path = os.path.join(cm.BASE_DIR, 'report', 'allure_result')
    # report_path = os.path.join(cm.BASE_DIR, 'report', 'allure_report')
    # if not os.path.exists(result_path):
    #     os.makedirs(result_path)
    # shutil.rmtree(result_path)
    # try:
    #     # pytest_cmd = f'pytest -q ./test_case/jrxf/web/house --alluredir {result_path}'
    #     pytest_cmd = f'pytest -q -m "contract" --alluredir {result_path}'
    #     p1 = subprocess.Popen(pytest_cmd, shell=True, stdout=subprocess.PIPE)
    #     out = p1.communicate()[0]
    # except Exception as e:
    #     log.error("脚本批量执行失败！", e)
    #
    # try:
    #     allure_cmd = f'allure generate {result_path} -o {report_path} --clean'
    #     p2 = subprocess.Popen(allure_cmd, shell=True, stdout=subprocess.PIPE)
    #     out1 = p2.communicate()[0]
    #     out1 = str(out1, 'utf-8')
    #     if 'successfully' in out1:
    #         print(f'报告已生成成功，请到{report_path}中查看 index.html')
    # except Exception as e:
    #     log.error("报告生成失败，请重新执行", e)
    #     log.error('执行用例失败，请检查环境配置')
    #     raise
