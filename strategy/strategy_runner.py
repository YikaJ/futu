from futu import *
import sys
import time
sys.path.append('/Users/yikazhu/code/futu/scripts')
from main import run_ma_strategy

if __name__ == "__main__":
    # 策略参数配置
    config = {
        "code": "HK.09988",      # 腾讯股票
        "short_period": 5,       # 短期均线周期
        "long_period": 20,       # 长期均线周期
    }
    
    print(f"开始运行双均线策略，股票代码: {config['code']}")
    print(f"参数: 短期均线={config['short_period']}日, 长期均线={config['long_period']}日")
    
    run_ma_strategy(
        code=config["code"], 
        short_period=config["short_period"], 
        long_period=config["long_period"]
    )
