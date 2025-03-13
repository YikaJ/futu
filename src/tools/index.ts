import CommandExecutor from "../utils/CommandExecutor.js";

export async function runToolsAction(methodName: string, params: Record<string, unknown> = {}) {
  switch (methodName) {
    case "get_market_snapshot": {
      const command = new CommandExecutor()
      // 从参数中获取股票代码列表
      const codeList = params?.code_list as string[];

      if (!codeList || codeList.length === 0) {
        return { error: "code_list 参数不能为空" };
      }

      // 正确处理多个股票代码，将每个股票代码作为单独的参数传递
      // 这里每个代码需要作为单独的命令行参数
      const formattedCodeList = codeList.map(code => `"${code}"`);
      const cmd = `python /Users/yikazhu/code/mcp/futu/scripts/main.py --code_list ${formattedCodeList.join(' ')}`;

      try {
        // 使用新增的 executeJSONCommand 方法，自动解析 JSON 结果
        // 打开调试模式查看详细输出
        const parsedResult = await command.executeJSONCommand(cmd, { debug: true });

        // 检查结果是否包含错误
        if (parsedResult.error) {
          return {
            content: [{
              type: "text",
              text: `获取市场快照数据失败: ${JSON.stringify(parsedResult.error)}`
            }]
          };
        }

        return {
          content: [{
            type: "text",
            text: `获取到市场快照数据: ${JSON.stringify(parsedResult, null, 2)}`
          }]
        };
      } catch (error: any) {
        return {
          content: [{
            type: "text",
            text: `获取市场快照数据失败: ${error.message}`
          }]
        };
      }
    }
    default:
      throw new Error("Unknown tool");
  }
}