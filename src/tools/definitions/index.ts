import { getMarketSnapshotDefinition } from './getMarketSnapshot.js';
import { requestHistoryKlineDefinition } from './requestHistoryKline.js';
import { requestTradingDaysDefinition } from './requestTradingDays.js';
import { calculateMovingAverageDefinition } from './calculateMovingAverage.js';
import { subscriptionManagerDefinition } from './subscriptionManager.js';

// 导出所有工具定义
export const tools = [
  getMarketSnapshotDefinition,
  requestHistoryKlineDefinition,
  requestTradingDaysDefinition,
  calculateMovingAverageDefinition,
  subscriptionManagerDefinition
];
