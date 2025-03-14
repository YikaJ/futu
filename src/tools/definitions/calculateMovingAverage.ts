export const calculateMovingAverageDefinition = {
  "name": "calculate_moving_average",
  "description": "计算指定股票的多种周期移动平均线(MA)，支持5日、10日、20日等自定义周期",
  "inputSchema": {
    "type": "object",
    "properties": {
      "code_list": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "需要计算移动平均线的股票代码列表，例如：[\"HK.00700\", \"US.AAPL\"]"
      },
      "ma_periods": {
        "type": "array",
        "items": {
          "type": "number"
        },
        "description": "移动平均线周期列表，例如：[5, 10, 20, 60]，默认为[5, 10, 20]"
      }
    },
    "required": ["code_list"]
  }
};
