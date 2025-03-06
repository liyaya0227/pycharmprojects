import pandas as pd
import requests
import json
import os
from jsonpath import jsonpath
from tools.logger import log
import warnings


filedir = os.path.dirname(__file__)
warnings.simplefilter(action='ignore', category=FutureWarning)
host = 'https://www.uat.juyyds.com/api/'

# 读取 Excel 文件
def read_test_cases(file_path):
    return pd.read_excel(filedir + "/" + file_path)

# 发送 HTTP 请求
def send_request(method, url, headers=None, params=None, data=None, files=None):
    log.info('method: ' + method)
    log.info('url: ' + host + url)
    log.info('headers: ' + str(headers))
    if data is not None:
        log.info('data: ' + str(data))
    if params is not None:
        log.info('params: ' + str(params))
    res = None
    while res is None:
        try:
            res = requests.request(method, host+url, headers=headers, params=params, json=data, files=files)
            response = res.json()
            log.info('response: ' + str(response))
            return response
        except Exception as e:
            return None, str(e)

# 运行测试用例并更新结果
def run_tests(excel_file, output_file):
    # 读取测试用例
    test_cases = read_test_cases(excel_file)

    # 遍历每一行进行测试
    for index, row in test_cases.iterrows():
        method = row['Method']
        url = row['URL']
        
        # 解析 Headers, Params 和 Body
        headers = json.loads(row['Headers']) if pd.notna(row['Headers']) else None
        params = json.loads(row['Params']) if pd.notna(row['Params']) else None
        body = json.loads(row['Body']) if pd.notna(row['Body']) else None


        # 发送请求并获取结果
        response = send_request(method, url, headers=headers, params=params, data=body)
        #获取校验值
        # status_code = jsonpath(response, '$.code')[0]
        msg = jsonpath(response, '$.msg')[0]
        # print(status_code, type(status_code))
        print(msg, type(msg))


        # 将结果写入 DataFrame
        # test_cases.at[index, 'ActualResult'] = status_code
        test_cases.at[index, 'ActualResult'] = msg
        # print(json.loads(row['ExpectedResult']), type(json.loads(row['ExpectedResult'])))
        # expected_status = int(json.loads(row['ExpectedResult'])['code'])
        expected_msg = row['ExpectedResult']
        test_cases.at[index, 'Status'] = 'Pass' if msg == expected_msg else 'Fail'

    # 将结果保存到新的 Excel 文件
    test_cases.to_excel(filedir + "/" + output_file, index=False)

# 执行测试
if __name__ == '__main__':
    input_excel = 'api_test_cases.xlsx'
    output_excel = 'api_test_results.xlsx'
    run_tests(input_excel, output_excel)
