export const requestTradingDaysDefinition = {
  "name": "request_trading_days",
  "description": "获取指定市场或股票的交易日历，包含交易日期和交易类型信息",
  "inputSchema": {
    "type": "object",
    "properties": {
      "market": {
        "type": "string",
        "description": "市场类型: HK=香港市场, US=美国市场, CN=A股市场, NT=深(沪)股通, ST=港股通(深、沪), JP_FUTURE=日本期货, SG_FUTURE=新加坡期货",
      },
      "start": {
        "type": "string",
        "description": "起始日期, 格式: yyyy-MM-dd，可选。若不提供而提供end，则为end往前365天",
      },
      "end": {
        "type": "string",
        "description": "结束日期, 格式: yyyy-MM-dd，可选。若不提供而提供start，则为start往后365天",
      },
      "code": {
        "type": "string",
        "description": "股票代码，例如：HK.00700，可选。当code参数存在时会忽略market参数",
      }
    },
    "required": [],
  }
};
