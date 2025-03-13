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
},]