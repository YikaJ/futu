import argparse
import numpy as np
import pandas as pd
from futu import KLType, AuType, KL_FIELD
from utils import (
    setup_logger, create_quote_context, process_dataframe,
    print_json_result, handle_exception, RET_OK
)

# 设置日志
setup_logger()

def calculate_ma(data, periods):
    """计算指定周期的移动平均线
    
    Args:
        data (list): 股票价格数据列表
        periods (list): 移动平均线周期列表 [5, 10, 20]等
        
    Returns:
        dict: 包含不同周期移动平均线的字典
    """
    if not data:
        return {}
    
    # 转换为pandas DataFrame以便计算
    df = pd.DataFrame(data)
    result = {}
    
    # 使用'close'字段而非'close_price'
    if 'close' not in df.columns:
        print(f"警告: 数据中无close字段，可用字段: {df.columns.tolist()}")
        return result
    
    # 按日期排序
    if 'time_key' in df.columns:
        df = df.sort_values('time_key')
    
    # 计算每个周期的移动平均线
    for period in periods:
        if len(df) >= period:
            ma_key = f'ma{period}'
            df[ma_key] = df['close'].rolling(window=period).mean().round(3)
            
            # 将结果转为日期为键的字典
            ma_dict = {}
            for idx, row in df.iterrows():
                if not pd.isna(row[ma_key]):
                    ma_dict[row['time_key']] = float(row[ma_key])
            result[ma_key] = ma_dict
    
    return result

def get_stock_ma(quote_ctx, code_list, ma_periods):
    """获取股票数据并计算移动平均线
    
    Args:
        quote_ctx: 富途行情上下文
        code_list (list): 股票代码列表
        ma_periods (list): 移动平均线周期列表 [5, 10, 20]等
    
    Returns:
        dict: 包含每只股票移动平均线数据的字典
    """
    results = {}
    
    for code in code_list:
        # 获取历史K线数据
        ret_code, data_frame, _ = quote_ctx.request_history_kline(
            code=code,
            ktype=KLType.K_DAY,  # 固定使用日K线
            autype=AuType.QFQ,
            fields=[KL_FIELD.DATE_TIME, KL_FIELD.CLOSE],
            max_count=1000
        )
        
        if ret_code == RET_OK and not data_frame.empty:
            # 处理成JSON格式
            processed_data = []
            for _, row in data_frame.iterrows():
                # 直接使用SDK返回的字段名
                item = {
                    'code': row['code'],
                    'name': row['name'] if 'name' in row else '',
                    'time_key': row['time_key'],
                    'close': float(row['close'])
                }
                processed_data.append(item)
            
            # 计算移动平均线
            ma_data = calculate_ma(processed_data, ma_periods)
            
            # 只返回MA数据
            if ma_data:
                results[code] = ma_data
            else:
                results[code] = {"error": {"message": "计算移动平均线失败"}}
        else:
            results[code] = {
                "error": {"message": f"获取{code}数据失败", "ret_code": ret_code}
            }
            
    return results

def main():
    parser = argparse.ArgumentParser(description='计算股票移动平均线')
    parser.add_argument('--code_list', nargs='+', type=str, required=True,
                        help='股票代码列表, 例如: HK.00700 US.AAPL')
    parser.add_argument('--ma_periods', nargs='+', type=int, default=[5, 10, 20],
                        help='移动平均线周期列表, 例如: 5 10 20 30 60')
    
    args = parser.parse_args()
    
    quote_ctx = None
    try:
        # 创建行情对象
        quote_ctx = create_quote_context()
        results = get_stock_ma(
            quote_ctx, args.code_list, args.ma_periods
        )
        
        # 输出结果
        print_json_result(results)
        
    except Exception as e:
        handle_exception(e)
    finally:
        if quote_ctx:
            quote_ctx.close()  # 关闭对象，防止连接条数用尽

if __name__ == "__main__":
    main()
