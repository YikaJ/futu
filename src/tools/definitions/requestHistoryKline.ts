export const requestHistoryKlineDefinition = {
  "name": "request_history_kline",
  "description": "获取指定股票的历史K线数据，包含开盘价、收盘价、最高价、最低价、成交量等信息",
  "inputSchema": {
    "type": "object",
    "properties": {
      "code": {
        "type": "string",
        "description": "股票代码，例如：HK.00700",
      },
      "start": {
        "type": "string",
        "description": "开始时间，格式：yyyy-MM-dd，可选",
      },
      "end": {
        "type": "string",
        "description": "结束时间，格式：yyyy-MM-dd，可选",
      },
      "ktype": {
        "type": "string",
        "description": "K线类型：K_DAY=日K线, K_WEEK=周K线, K_MON=月K线, K_YEAR=年K线, K_1M=1分钟, K_5M=5分钟, K_15M=15分钟, K_30M=30分钟, K_60M=60分钟, K_3M=3分钟, K_QUARTER=季K线，默认K_DAY",
      },
      "autype": {
        "type": "number",
        "description": "复权类型：0=不复权(NONE), 1=前复权(QFQ), 2=后复权(HFQ)，默认1",
      },
      "fields": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "需返回的字段列表，可选值：ALL(所有), DATE_TIME(时间), HIGH(最高价), OPEN(开盘价), LOW(最低价), CLOSE(收盘价), LAST_CLOSE(昨收价), TRADE_VOL(成交量), TRADE_VAL(成交额), TURNOVER_RATE(换手率), PE_RATIO(市盈率), CHANGE_RATE(涨跌幅)，默认ALL",
      },
      "max_count": {
        "type": "number",
        "description": "本次请求最大返回的K线根数，默认1000",
      },
      "extended_time": {
        "type": "boolean",
        "description": "是否允许美股盘前盘后数据，默认false",
      },
    },
    "required": ["code"],
  }
};
