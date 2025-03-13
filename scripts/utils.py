from futu import *
import json
import numpy as np
import sys
import logging

# 配置日志
def setup_logger():
    """配置日志设置，将FuTu的日志输出重定向到stderr"""
    logging.getLogger('futu').setLevel(logging.ERROR)
    logging.basicConfig(level=logging.ERROR, stream=sys.stderr)

# 创建行情连接上下文
def create_quote_context():
    """创建并返回行情对象"""
    return OpenQuoteContext(host='127.0.0.1', port=11111)

# 处理DataFrame为JSON兼容格式
def process_dataframe(data_frame):
    """将DataFrame处理为JSON兼容的格式"""
    # 处理NaN值等
    data_dict = data_frame.replace({np.nan: None, np.inf: None, -np.inf: None}).to_dict(orient='records')
    
    # 处理numpy类型
    result = []
    for item in data_dict:
        processed_item = {}
        for key, value in item.items():
            if isinstance(value, (np.integer, np.floating)):
                processed_item[key] = value.item()  # 转换numpy类型为Python原生类型
            else:
                processed_item[key] = value
        result.append(processed_item)
    return result

# 打印JSON结果
def print_json_result(results):
    """以标准格式打印JSON结果"""
    print("###JSON_BEGIN###")
    print(json.dumps(results, ensure_ascii=False))
    print("###JSON_END###")

# 处理异常并打印错误
def handle_exception(e):
    """处理异常并以标准格式输出错误"""
    error_result = {"error": str(e)}
    print_json_result(error_result)
    sys.exit(1)
