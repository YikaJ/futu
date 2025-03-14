import time
import pandas as pd
import numpy as np
from futu import *
from datetime import datetime, date

class KLineCache:
    """K线数据缓存类"""
    def __init__(self):
        self.cache = {}  # KV 缓存
        self.cache_date = {}  # 缓存日期记录
    
    def generate_key(self, code, ktype, count):
        """生成唯一且可计算的缓存键"""
        return f"{code}_{ktype}_{count}"
    
    def get(self, code, ktype, count):
        """从缓存获取数据"""
        key = self.generate_key(code, ktype, count)
        
        # 检查是否有缓存
        if key in self.cache:
            # 检查缓存是否需要更新（每天更新一次）
            last_update_date = self.cache_date.get(key)
            today = date.today()
            
            if last_update_date == today:
                # 缓存有效
                return True, self.cache[key]
        
        # 缓存不存在或已过期
        return False, None
    
    def set(self, code, ktype, count, data):
        """设置缓存数据"""
        key = self.generate_key(code, ktype, count)
        self.cache[key] = data
        self.cache_date[key] = date.today()

# 全局缓存实例
kline_cache = KLineCache()

class MAStrategy:
    """双均线交叉策略类"""
    def __init__(self, short_period=5, long_period=20, volume_ratio_buy=1.2, volume_ratio_sell=0.85):
        self.short_period = short_period  # 短期均线周期
        self.long_period = long_period    # 长期均线周期
        self.volume_ratio_buy = volume_ratio_buy  # 买入信号成交量放大比例
        self.volume_ratio_sell = volume_ratio_sell  # 卖出信号成交量萎缩比例
        self.history_data = None          # 历史K线数据
        self.last_signal = None           # 最近一次信号
    
    def calculate_ma(self, data):
        """计算移动平均线"""
        if len(data) < self.long_period:
            return None
        
        df = data.copy()
        df[f'ma_{self.short_period}'] = df['close'].rolling(window=self.short_period).mean()
        df[f'ma_{self.long_period}'] = df['close'].rolling(window=self.long_period).mean()
        df['volume_ma'] = df['volume'].rolling(window=self.short_period).mean()
        return df
    
    def check_volume_condition(self, row, is_buy_signal):
        """检查成交量条件"""
        if is_buy_signal:
            # 买入信号需要成交量放大
            return row['volume'] > row['volume_ma'] * self.volume_ratio_buy
        else:
            # 卖出信号需要成交量萎缩
            return row['volume'] < row['volume_ma'] * self.volume_ratio_sell
    
    def check_market_trend(self, quote_ctx, market_code='HSI'):
        """检查大盘趋势"""
        ret, data = quote_ctx.get_market_snapshot([market_code])
        if ret != RET_OK:
            print(f"[错误] 获取大盘数据失败: {data}")
            return False
        
        # 这里简化处理：当前大盘涨幅为正视为上涨趋势
        return data['change_rate'][0] > 0
    
    def check_capital_flow(self, quote_ctx, code):
        """检查资金流向"""
        ret, data = quote_ctx.get_capital_flow(code, period_type=PeriodType.INTRADAY)
        if ret != RET_OK:
            print(f"[错误] 获取资金流向失败: {data}")
            return False
        
        # 检查最新的主力资金流向是否为净流入
        return data['main_inflow'][0] > 0
    
    def generate_signal(self, quote_ctx, code):
        """生成交易信号"""
        # 1. 优先从缓存中获取历史数据
        max_count = self.long_period * 2  # 确保有足够数据计算均线
        has_cache, cache_data = kline_cache.get(code, KLType.K_DAY, max_count)
        
        if has_cache:
            self.history_data = cache_data
        else:
            # 缓存未命中，从接口获取数据
            print(f"[信息] 缓存未命中，从接口获取 {code} 的历史K线数据")
            ret, data, page_req_key = quote_ctx.request_history_kline(
                code, 
                start=None,  # 使用默认起始时间
                end=None,    # 使用默认结束时间
                max_count=max_count,
                ktype=KLType.K_DAY
            )
            
            if ret != RET_OK:
                print(f"[错误] 获取历史K线失败: {data}")
                return None
            
            self.history_data = data
            # 将数据保存到缓存
            kline_cache.set(code, KLType.K_DAY, max_count, data)
        
        # 2. 计算均线
        ma_data = self.calculate_ma(self.history_data)
        if ma_data is None:
            print("[警告] 数据不足，无法计算均线")
            return None
        
        # 3. 判断均线交叉
        current = ma_data.iloc[-1]
        previous = ma_data.iloc[-2]
        
        # 判断是否出现金叉(买入信号)
        is_golden_cross = (previous[f'ma_{self.short_period}'] <= previous[f'ma_{self.long_period}']) and \
                         (current[f'ma_{self.short_period}'] > current[f'ma_{self.long_period}'])
        
        # 判断是否出现死叉(卖出信号)
        is_death_cross = (previous[f'ma_{self.short_period}'] >= previous[f'ma_{self.long_period}']) and \
                        (current[f'ma_{self.short_period}'] < current[f'ma_{self.long_period}'])
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 金叉:{'出现' if is_golden_cross else '未出现'} | 死叉:{'出现' if is_death_cross else '未出现'}")
        
        signal = None
        
        # 4. 根据交叉情况和量价规则生成信号
        if is_golden_cross and self.check_volume_condition(current, True):
            # 验证市场趋势和资金流向
            if self.check_market_trend(quote_ctx) and self.check_capital_flow(quote_ctx, code):
                signal = "BUY"
        elif is_death_cross and self.check_volume_condition(current, False):
            signal = "SELL"
        
        self.last_signal = signal
        return signal


class CurKlineTest(CurKlineHandlerBase):
    def __init__(self, strategy):
        super(CurKlineTest, self).__init__()
        self.strategy = strategy
        self.quote_ctx = None
        self.code = None
    
    def set_context(self, quote_ctx, code):
        self.quote_ctx = quote_ctx
        self.code = code
    
    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(CurKlineTest,self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print(f"[错误] K线数据接收失败: {data}")
            return RET_ERROR, data
        
        # 将新数据添加到历史数据中
        if self.strategy.history_data is not None:
            self.strategy.history_data = pd.concat([self.strategy.history_data, data]).drop_duplicates()
            
            # 更新缓存
            max_count = self.strategy.long_period * 2
            kline_cache.set(self.code, KLType.K_DAY, max_count, self.strategy.history_data)
            
            # 重新生成信号
            signal = self.strategy.generate_signal(self.quote_ctx, self.code)
            if signal:
                print(f"[信号] {self.code} 产生 {signal} 信号")
                # 这里可以添加实际的下单逻辑
        
        return RET_OK, data


class RTDataTest(RTDataHandlerBase):
    def __init__(self, strategy):
        super(RTDataTest, self).__init__()
        self.strategy = strategy
    
    def on_recv_rsp(self, rsp_pb):
        ret_code, data = super(RTDataTest, self).on_recv_rsp(rsp_pb)
        if ret_code != RET_OK:
            print(f"[错误] 分时数据接收失败: {data}")
            return RET_ERROR, data
        
        # 不再打印分时数据，仅处理
        # 这里可以添加对分时成交量的分析逻辑
        
        return RET_OK, data


def run_ma_strategy(code, short_period=5, long_period=20):
    """运行双均线策略"""
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    
    # 创建策略实例
    ma_strategy = MAStrategy(
        short_period=short_period, 
        long_period=long_period, 
        volume_ratio_buy=1.2, 
        volume_ratio_sell=0.85
    )
    
    # 初始化K线处理器
    kline_handler = CurKlineTest(ma_strategy)
    kline_handler.set_context(quote_ctx, code)
    quote_ctx.set_handler(kline_handler)
    
    # 初始化分时数据处理器
    rt_handler = RTDataTest(ma_strategy)
    quote_ctx.set_handler(rt_handler)
    
    # 订阅K线和分时数据
    ret, data = quote_ctx.subscribe([code], [SubType.K_DAY, SubType.RT_DATA])
    if ret == RET_OK:
        print(f"[系统] {code} 数据订阅成功")
    else:
        print(f"[错误] {code} 数据订阅失败: {data}")
        quote_ctx.close()
        return
    
    # 获取初始信号
    initial_signal = ma_strategy.generate_signal(quote_ctx, code)
    if initial_signal:
        print(f"[信号] {code} 初始信号: {initial_signal}")
    
    # 持续运行策略
    print(f"[系统] 策略开始运行，监控 {code}...")
    try:
        while True:
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        print("[系统] 策略停止运行")
    finally:
        quote_ctx.close()


if __name__ == "__main__":
    # 运行双均线策略，以腾讯股票为例
    run_ma_strategy("HK.00700")