#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: vipserviceentrustmentagreementpage.py
@time: 2021/06/22
"""

import os
import sys
import shutil
import subprocess
from config.conf import cm

WIN = sys.platform.startswith('win')


def main():
    result_path = os.path.join(cm.BASE_DIR, 'allure', 'allure_result')
    report_path = os.path.join(cm.BASE_DIR, 'allure', 'allure_report')
    shutil.rmtree(result_path)

    pytest_cmd = f'pytest -s ./TestCase/test_process/test_house.py --alluredir {result_path}'
    p1 = subprocess.Popen(pytest_cmd, shell=True, stdout=subprocess.PIPE)
    out = p1.communicate()[0]
    allure_cmd = f'allure generate {result_path} -o {report_path} --clean'
    p2 = subprocess.Popen(allure_cmd, shell=True, stdout=subprocess.PIPE)
    out1 = p2.communicate()[0]
    out1 = str(out, 'utf-8')
    if 'successfully' in out1:
        print(f'报告已生成成功，请到{report_path}中查看 index.html')


if __name__ == "__main__":
    main()
