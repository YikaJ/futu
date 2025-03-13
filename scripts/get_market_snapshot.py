import argparse
import sys
from utils import (
    setup_logger, create_quote_context, process_dataframe,
    print_json_result, handle_exception, RET_OK
)

# 设置日志
setup_logger()

def get_market_snapshot(quote_ctx, code_list):
    """获取多个股票的市场快照数据"""
    results = {}
    
    # 使用SDK提供的批量查询功能，一次性获取所有股票的快照
    ret_code, data_frame = quote_ctx.get_market_snapshot(code_list)
    
    if ret_code == RET_OK:
        # 处理数据
        processed_data = process_dataframe(data_frame)
        
        # 将结果按股票代码组织
        for item in processed_data:
            code = item.get('code', '')
            if code not in results:
                results[code] = []
            results[code].append(item)
    else:
        results["error"] = {"message": "获取数据失败", "ret_code": ret_code}
    
    return results

def main():
    parser = argparse.ArgumentParser(description='获取股票市场快照数据')
    parser.add_argument('--code_list', nargs='+', type=str, required=True,
                        help='股票代码列表, 例如: HK.00700 US.AAPL')
    
    args = parser.parse_args()
    code_list = args.code_list
    
    quote_ctx = None
    try:
        # 创建行情对象
        quote_ctx = create_quote_context()
        results = get_market_snapshot(quote_ctx, code_list)
        
        # 输出结果
        print_json_result(results)
        
    except Exception as e:
        handle_exception(e)
    finally:
        if quote_ctx:
            quote_ctx.close()  # 关闭对象，防止连接条数用尽

if __name__ == "__main__":
    main()
