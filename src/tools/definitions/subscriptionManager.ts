export const subscriptionManagerDefinition = {
  "name": "subscription_manager",
  "description": "管理股票行情订阅，支持订阅、取消订阅和查询订阅状态",
  "inputSchema": {
    "type": "object",
    "properties": {
      "command": {
        "type": "string",
        "enum": ["subscribe", "unsubscribe", "query"],
        "description": "操作命令：subscribe(订阅)、unsubscribe(取消订阅)、query(查询订阅状态)"
      },
      "code_list": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "股票代码列表，订阅或取消订阅时需要"
      },
      "subtype_list": {
        "type": "array",
        "items": {
          "type": "string",
          "enum": ["QUOTE", "ORDER_BOOK", "TICKER", "K_1M", "K_3M", "K_5M", "K_15M", "K_30M", "K_60M", "K_DAY", "K_WEEK", "K_MON", "K_QUARTER", "K_YEAR", "RT_DATA", "BROKER", "ORDER_DETAIL"],
          "enumDescriptions": [
            "QUOTE - 基础报价",
            "ORDER_BOOK - 摆盘",
            "TICKER - 逐笔",
            "K_1M - 1分钟K线",
            "K_3M - 3分钟K线",
            "K_5M - 5分钟K线",
            "K_15M - 15分钟K线",
            "K_30M - 30分钟K线",
            "K_60M - 60分钟K线",
            "K_DAY - 日K线",
            "K_WEEK - 周K线",
            "K_MON - 月K线",
            "K_QUARTER - 季K线",
            "K_YEAR - 年K线",
            "RT_DATA - 分时",
            "BROKER - 经纪队列",
            "ORDER_DETAIL - 委托明细"
          ]
        },
        "description": "订阅类型列表，包括：基础报价(QUOTE)、摆盘(ORDER_BOOK)、逐笔(TICKER)、K线(K_1M等)、分时(RT_DATA)、经纪队列(BROKER)、委托明细(ORDER_DETAIL)"
      },
      "is_first_push": {
        "type": "boolean",
        "description": "订阅成功后是否立即推送一次数据，默认true"
      },
      "subscribe_push": {
        "type": "boolean",
        "description": "订阅后是否持续推送数据，默认true"
      },
      "is_detailed_orderbook": {
        "type": "boolean",
        "description": "是否订阅详细摆盘，默认false"
      },
      "extended_time": {
        "type": "boolean",
        "description": "是否允许美股盘前盘后数据，默认false"
      },
      "unsubscribe_all": {
        "type": "boolean",
        "description": "是否取消所有订阅，仅在取消订阅时使用，默认false"
      }
    },
    "required": ["command"]
  }
};
