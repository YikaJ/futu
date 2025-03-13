export const tools = [{
  "name": "get_market_snapshot",
  "description": "获取股票、窝轮、期权等金融产品的实时快照数据，包含价格、成交量、财务指标等详细信息",
  "inputSchema": {
    "type": "object",
    "properties": {
      "code_list": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "需要查询的证券代码列表，支持股票/窝轮/期权等多种类型，最大支持400个代码"
      }
    },
    "required": ["code_list"]
  }
}, {
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
}, {
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
}]