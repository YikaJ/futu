from futu import *
import json
import numpy as np
import argparse
import sys
import logging

# 将FuTu的日志输出重定向到stderr
logging.getLogger('futu').setLevel(logging.ERROR)
# 配置基本日志
logging.basicConfig(level=logging.ERROR, stream=sys.stderr)

def get_market_snapshots(quote_ctx, code_list):
    """获取多个股票的市场快照数据"""
    results = {}
    
    # 使用SDK提供的批量查询功能，一次性获取所有股票的快照
    ret_code, data_frame = quote_ctx.get_market_snapshot(code_list)
    
    if ret_code == RET_OK:
        # 将DataFrame转换为可序列化的字典，同时处理NaN值
        # 明确将所有可能不兼容JSON的值转换为可序列化的类型
        data_dict = data_frame.replace({np.nan: None, np.inf: None, -np.inf: None}).to_dict(orient='records')
        
        # 将结果按股票代码组织
        for item in data_dict:
            code = item.get('code', '')
            if code not in results:
                results[code] = []
            # 确保所有值都是JSON兼容的
            processed_item = {}
            for key, value in item.items():
                if isinstance(value, (np.integer, np.floating)):
                    processed_item[key] = value.item()  # 转换numpy类型为Python原生类型
                else:
                    processed_item[key] = value
            results[code].append(processed_item)
    else:
        results["error"] = {"message": "获取数据失败", "ret_code": ret_code}
    
    return results

def main():
    parser = argparse.ArgumentParser(description='获取股票市场快照数据')
    parser.add_argument('--code_list', nargs='+', type=str, required=True,
                        help='股票代码列表, 例如: HK.00700 US.AAPL')
    
    args = parser.parse_args()
    code_list = args.code_list
    
    try:
        # 确保所有日志信息不会干扰标准输出
        quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)  # 创建行情对象
        results = get_market_snapshots(quote_ctx, code_list)
        
        # 使用明确的标记，确保JSON输出被准确识别
        print("###JSON_BEGIN###")
        print(json.dumps(results, ensure_ascii=False))
        print("###JSON_END###")
        
    except Exception as e:
        # 发生异常时，确保错误信息也以相同格式输出
        error_result = {"error": str(e)}
        print("###JSON_BEGIN###")
        print(json.dumps(error_result, ensure_ascii=False))
        print("###JSON_END###")
        sys.exit(1)
    finally:
        if 'quote_ctx' in locals():
            quote_ctx.close()  # 关闭对象，防止连接条数用尽

if __name__ == "__main__":
    main()
