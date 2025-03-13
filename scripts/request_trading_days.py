import argparse
from futu import TradeDateMarket, RET_OK
from utils import (
    setup_logger, create_quote_context, process_dataframe,
    print_json_result, handle_exception
)

# 设置日志
setup_logger()

def request_trading_days(quote_ctx, market=None, start=None, end=None, code=None):
    """获取交易日历"""
    results = {}
    
    # 调用SDK提供的交易日历查询接口
    ret_code, data_frame = quote_ctx.request_trading_days(
        market=market, start=start, end=end, code=code
    )
    
    if ret_code == RET_OK:
        if isinstance(data_frame, list):
            # 如果返回的是列表
            if data_frame:
                results["trading_days"] = data_frame
            else:
                results["trading_days"] = []
        else:
            # 如果返回的是DataFrame
            if not data_frame.empty:
                processed_data = process_dataframe(data_frame)
                results["trading_days"] = processed_data
            else:
                results["trading_days"] = []
    else:
        results["error"] = {"message": "获取交易日历失败", "ret_code": ret_code}
    
    return results

def main():
    parser = argparse.ArgumentParser(description='获取交易日历')
    parser.add_argument('--market', type=str, default=None,
                        help='市场类型: HK=香港市场, US=美国市场, CN=A股市场, NT=深(沪)股通, ST=港股通(深、沪), JP_FUTURE=日本期货, SG_FUTURE=新加坡期货')
    parser.add_argument('--start', type=str, default=None,
                        help='起始日期, 格式: yyyy-MM-dd')
    parser.add_argument('--end', type=str, default=None,
                        help='结束日期, 格式: yyyy-MM-dd')
    parser.add_argument('--code', type=str, default=None,
                        help='股票代码, 例如: HK.00700, 当code参数存在时会忽略market参数')
    
    args = parser.parse_args()
    
    # 转换市场类型参数
    market_map = {
        'HK': TradeDateMarket.HK,
        'US': TradeDateMarket.US,
        'CN': TradeDateMarket.CN,
        'NT': TradeDateMarket.NT,
        'ST': TradeDateMarket.ST,
        'JP_FUTURE': TradeDateMarket.JP_FUTURE,
        'SG_FUTURE': TradeDateMarket.SG_FUTURE,
        'NONE': TradeDateMarket.NONE
    }
    
    market = None
    if args.market in market_map:
        market = market_map[args.market]
    
    quote_ctx = None
    try:
        # 创建行情对象
        quote_ctx = create_quote_context()
        results = request_trading_days(
            quote_ctx, market, args.start, args.end, args.code
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
