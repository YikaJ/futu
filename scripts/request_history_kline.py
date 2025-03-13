import argparse
from futu import KLType, AuType, KL_FIELD
from utils import (
    setup_logger, create_quote_context, process_dataframe,
    print_json_result, handle_exception, RET_OK
)

# 设置日志
setup_logger()

def request_history_kline(quote_ctx, code, start=None, end=None, ktype=KLType.K_DAY, 
                          autype=AuType.QFQ, fields=[KL_FIELD.ALL], max_count=1000, 
                          extended_time=False):
    """获取股票的历史K线数据"""
    results = {}
    page_req_key = None
    all_data = []
    
    while True:
        # 调用SDK提供的历史K线查询接口
        ret_code, data_frame, next_page_req_key = quote_ctx.request_history_kline(
            code=code, start=start, end=end, ktype=ktype, autype=autype,
            fields=fields, max_count=max_count, page_req_key=page_req_key,
            extended_time=extended_time
        )
        
        if ret_code == RET_OK:
            # 处理数据
            if not data_frame.empty:
                processed_data = process_dataframe(data_frame)
                all_data.extend(processed_data)
            
            # 检查是否还有更多数据需要获取
            if next_page_req_key is None:
                break
            else:
                page_req_key = next_page_req_key
        else:
            results["error"] = {"message": "获取K线数据失败", "ret_code": ret_code}
            return results
    
    # 按股票代码组织结果
    results[code] = all_data
    return results

def main():
    parser = argparse.ArgumentParser(description='获取股票历史K线数据')
    parser.add_argument('--code', type=str, required=True,
                        help='股票代码, 例如: HK.00700')
    parser.add_argument('--start', type=str, default=None,
                        help='开始时间, 格式: yyyy-MM-dd')
    parser.add_argument('--end', type=str, default=None,
                        help='结束时间, 格式: yyyy-MM-dd')
    parser.add_argument('--ktype', type=str, default='K_DAY',
                        help='K线类型: K_DAY=日K线, K_WEEK=周K线, K_MON=月K线, K_YEAR=年K线, K_1M=1分钟, K_5M=5分钟, K_15M=15分钟, K_30M=30分钟, K_60M=60分钟, K_3M=3分钟, K_QUARTER=季K线')
    parser.add_argument('--autype', type=int, default=1,
                        help='复权类型: 0=不复权, 1=前复权, 2=后复权')
    parser.add_argument('--fields', type=str, nargs='+', default=['ALL'],
                        help='需返回的字段列表, 例如: ALL DATE_TIME HIGH OPEN LOW CLOSE LAST_CLOSE TRADE_VOL TRADE_VAL TURNOVER_RATE PE_RATIO CHANGE_RATE')
    parser.add_argument('--max_count', type=int, default=1000,
                        help='单次请求最大数据条数')
    parser.add_argument('--extended_time', action='store_true',
                        help='是否允许美股盘前盘后数据')
    
    args = parser.parse_args()
    
    # 转换K线类型参数
    ktype_map = {
        'K_DAY': KLType.K_DAY,
        'K_WEEK': KLType.K_WEEK,
        'K_MON': KLType.K_MON,
        'K_YEAR': KLType.K_YEAR,
        'K_1M': KLType.K_1M,
        'K_5M': KLType.K_5M,
        'K_15M': KLType.K_15M,
        'K_30M': KLType.K_30M,
        'K_60M': KLType.K_60M,
        'K_3M': KLType.K_3M,
        'K_QUARTER': KLType.K_QUARTER,
        'NONE': KLType.NONE
    }
    ktype = ktype_map.get(args.ktype, KLType.K_DAY)
    
    # 转换复权类型参数
    autype_map = {
        0: AuType.NONE,
        1: AuType.QFQ,
        2: AuType.HFQ
    }
    autype = autype_map.get(args.autype, AuType.QFQ)
    
    # 转换字段参数
    fields = []
    for field in args.fields:
        if field == 'ALL':
            fields.append(KL_FIELD.ALL)
        elif hasattr(KL_FIELD, field):
            fields.append(getattr(KL_FIELD, field))
    
    # 如果fields为空，则使用默认值
    if not fields:
        fields = [KL_FIELD.ALL]
    
    quote_ctx = None
    try:
        # 创建行情对象
        quote_ctx = create_quote_context()
        results = request_history_kline(
            quote_ctx, args.code, args.start, args.end, ktype, autype, 
            fields, args.max_count, args.extended_time
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
