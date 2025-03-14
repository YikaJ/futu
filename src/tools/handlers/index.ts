import { handleGetMarketSnapshot } from './getMarketSnapshot.js';
import { handleRequestHistoryKline } from './requestHistoryKline.js';
import { handleRequestTradingDays } from './requestTradingDays.js';
import { handleCalculateMovingAverage } from './calculateMovingAverage.js';
import { handleSubscriptionManager } from './subscriptionManager.js';

// 导出处理函数映射表
export const handlers = {
  'get_market_snapshot': handleGetMarketSnapshot,
  'request_history_kline': handleRequestHistoryKline,
  'request_trading_days': handleRequestTradingDays,
  'calculate_moving_average': handleCalculateMovingAverage,
  'subscription_manager': handleSubscriptionManager
};
