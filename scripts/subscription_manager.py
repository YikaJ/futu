import argparse
import time
from futu import SubType, RET_OK
from utils import (
    setup_logger, create_quote_context, 
    print_json_result, handle_exception
)

# 设置日志
setup_logger()

def parse_subtype(subtype_str_list):
    """
    将字符串形式的订阅类型列表转换为 SubType 枚举类型
    
    Args:
        subtype_str_list (list): 字符串形式的订阅类型列表
        
    Returns:
        list: SubType 枚举类型列表
    """
    subtype_map = {
        'QUOTE': SubType.QUOTE,                   # 基础报价
        'ORDER_BOOK': SubType.ORDER_BOOK,         # 摆盘
        'TICKER': SubType.TICKER,                 # 逐笔
        'K_1M': SubType.K_1M,                     # 1分钟K线
        'K_3M': SubType.K_3M,                     # 3分钟K线
        'K_5M': SubType.K_5M,                     # 5分钟K线
        'K_15M': SubType.K_15M,                   # 15分钟K线
        'K_30M': SubType.K_30M,                   # 30分钟K线
        'K_60M': SubType.K_60M,                   # 60分钟K线
        'K_DAY': SubType.K_DAY,                   # 日K线
        'K_WEEK': SubType.K_WEEK,                 # 周K线
        'K_MON': SubType.K_MON,                   # 月K线
        'K_YEAR': SubType.K_YEAR,                 # 年K线
        'RT_DATA': SubType.RT_DATA,               # 分时
        'BROKER': SubType.BROKER,                 # 经纪队列
        'NONE': SubType.NONE,                     # 未知
    }
    
    subtypes = []
    for subtype_str in subtype_str_list:
        if subtype_str.upper() in subtype_map:
            subtypes.append(subtype_map[subtype_str.upper()])
        else:
            raise ValueError(f"不支持的订阅类型: {subtype_str}, 支持的类型: {list(subtype_map.keys())}")
    
    return subtypes

def subscribe_stocks(quote_ctx, code_list, subtype_list, is_first_push=True, 
                    subscribe_push=True, is_detailed_orderbook=False, extended_time=False):
    """
    订阅股票行情
    
    Args:
        quote_ctx: 富途行情上下文
        code_list (list): 股票代码列表
        subtype_list (list): SubType 枚举类型列表
        is_first_push (bool): 订阅成功之后是否立即推送一次缓存数据
        subscribe_push (bool): 订阅后是否推送
        is_detailed_orderbook (bool): 是否订阅详细的摆盘订单明细
        extended_time (bool): 是否允许美股盘前盘后数据
        
    Returns:
        dict: 包含订阅结果的字典
    """
    results = {}
    
    # 执行订阅
    ret_code, err_message = quote_ctx.subscribe(
        code_list, subtype_list, is_first_push, subscribe_push, 
        is_detailed_orderbook, extended_time
    )
    
    if ret_code == RET_OK:
        # 查询订阅状态
        query_ret, subscription_info = quote_ctx.query_subscription()
        if query_ret == RET_OK:
            results["success"] = True
            results["message"] = "订阅成功"
            results["subscription_info"] = {
                "total_used": subscription_info["total_used"],
                "remain": subscription_info["remain"],
                "own_used": subscription_info["own_used"],
                "sub_list": subscription_info["sub_list"]
            }
        else:
            results["success"] = True
            results["message"] = "订阅成功，但查询订阅状态失败"
    else:
        results["success"] = False
        results["message"] = f"订阅失败: {err_message}"
    
    return results

def unsubscribe_stocks(quote_ctx, code_list=None, subtype_list=None, unsubscribe_all=False):
    """
    取消订阅股票行情
    
    Args:
        quote_ctx: 富途行情上下文
        code_list (list): 股票代码列表，取消订阅时为None则表示取消所有股票
        subtype_list (list): SubType 枚举类型列表，取消订阅时为None则表示取消所有类型
        unsubscribe_all (bool): 是否取消所有订阅
        
    Returns:
        dict: 包含取消订阅结果的字典
    """
    results = {}
    
    # 执行取消订阅
    if unsubscribe_all:
        ret_code, err_message = quote_ctx.unsubscribe_all()
    else:
        ret_code, err_message = quote_ctx.unsubscribe(code_list, subtype_list)
    
    if ret_code == RET_OK:
        # 查询订阅状态
        query_ret, subscription_info = quote_ctx.query_subscription()
        if query_ret == RET_OK:
            results["success"] = True
            results["message"] = "取消订阅成功"
            results["subscription_info"] = {
                "total_used": subscription_info["total_used"],
                "remain": subscription_info["remain"],
                "own_used": subscription_info["own_used"],
                "sub_list": subscription_info["sub_list"]
            }
        else:
            results["success"] = True
            results["message"] = "取消订阅成功，但查询订阅状态失败"
    else:
        results["success"] = False
        results["message"] = f"取消订阅失败: {err_message}"
    
    return results

def query_subscription_status(quote_ctx):
    """
    查询当前订阅状态
    
    Args:
        quote_ctx: 富途行情上下文
        
    Returns:
        dict: 包含订阅状态的字典
    """
    results = {}
    
    ret_code, subscription_info = quote_ctx.query_subscription()
    
    if ret_code == RET_OK:
        results["success"] = True
        results["subscription_info"] = {
            "total_used": subscription_info["total_used"],
            "remain": subscription_info["remain"],
            "own_used": subscription_info["own_used"],
            "sub_list": subscription_info["sub_list"]
        }
    else:
        results["success"] = False
        results["message"] = f"查询订阅状态失败"
    
    return results

def main():
    parser = argparse.ArgumentParser(description='股票订阅与取消订阅')
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 订阅命令
    subscribe_parser = subparsers.add_parser('subscribe', help='订阅股票行情')
    subscribe_parser.add_argument('--code_list', nargs='+', type=str, required=True,
                        help='股票代码列表, 例如: HK.00700 US.AAPL')
    subscribe_parser.add_argument('--subtype_list', nargs='+', type=str, required=True,
                        help='订阅类型列表, 例如: QUOTE ORDER_BOOK TICKER')
    subscribe_parser.add_argument('--no_first_push', action='store_false', dest='is_first_push',
                        help='不需要立即推送一次缓存数据')
    subscribe_parser.add_argument('--no_push', action='store_false', dest='subscribe_push',
                        help='订阅后不需要推送数据')
    subscribe_parser.add_argument('--detailed_orderbook', action='store_true', dest='is_detailed_orderbook',
                        help='订阅详细的摆盘订单明细')
    subscribe_parser.add_argument('--extended_time', action='store_true', dest='extended_time',
                        help='允许美股盘前盘后数据')
    
    # 取消订阅命令
    unsubscribe_parser = subparsers.add_parser('unsubscribe', help='取消订阅股票行情')
    unsubscribe_parser.add_argument('--code_list', nargs='+', type=str,
                        help='取消订阅的股票代码列表, 例如: HK.00700 US.AAPL')
    unsubscribe_parser.add_argument('--subtype_list', nargs='+', type=str,
                        help='取消订阅的类型列表, 例如: QUOTE ORDER_BOOK TICKER')
    unsubscribe_parser.add_argument('--all', action='store_true', dest='unsubscribe_all',
                        help='取消所有订阅')
    
    # 查询订阅状态命令
    subparsers.add_parser('query', help='查询当前订阅状态')
    
    args = parser.parse_args()
    
    quote_ctx = None
    try:
        # 创建行情对象
        quote_ctx = create_quote_context()
        
        if args.command == 'subscribe':
            # 解析订阅类型
            subtypes = parse_subtype(args.subtype_list)
            # 执行订阅
            results = subscribe_stocks(
                quote_ctx, args.code_list, subtypes, 
                args.is_first_push, args.subscribe_push, 
                args.is_detailed_orderbook, args.extended_time
            )
        elif args.command == 'unsubscribe':
            # 处理取消所有订阅的情况
            if args.unsubscribe_all:
                results = unsubscribe_stocks(quote_ctx, unsubscribe_all=True)
            else:
                # 确保至少提供了代码列表或类型列表
                if not args.code_list and not args.subtype_list:
                    raise ValueError("取消订阅时必须提供股票代码列表或订阅类型列表")
                # 解析订阅类型(如果有)
                subtypes = None
                if args.subtype_list:
                    subtypes = parse_subtype(args.subtype_list)
                # 执行取消订阅
                results = unsubscribe_stocks(quote_ctx, args.code_list, subtypes)
        elif args.command == 'query':
            # 查询订阅状态
            results = query_subscription_status(quote_ctx)
        else:
            results = {"error": {"message": "无效的命令，请使用 subscribe、unsubscribe 或 query"}}
        
        # 输出结果
        print_json_result(results)
        
    except Exception as e:
        handle_exception(e)
    finally:
        if quote_ctx:
            quote_ctx.close()  # 关闭对象，防止连接条数用尽

if __name__ == "__main__":
    main()
