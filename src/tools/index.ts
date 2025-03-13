import CommandExecutor from "../utils/CommandExecutor.js";
import path from 'path';
import { fileURLToPath } from 'url';

// 获取当前文件的目录路径
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export async function runToolsAction(methodName: string, params: Record<string, unknown> = {}) {
  const scriptPath = path.join(__dirname, `../../scripts/${methodName}.py`);
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

      // 使用path.join构建脚本的绝对路径
      const cmd = `python "${scriptPath}" --code_list ${formattedCodeList.join(' ')}`;

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
    case "request_history_kline": {
      const command = new CommandExecutor()

      // 获取必要参数
      const code = params?.code as string;

      if (!code) {
        return { error: "code 参数不能为空" };
      }

      // 构建命令参数
      let cmdArgs = `--code "${code}"`;

      // 添加可选参数
      if (params.start) cmdArgs += ` --start "${params.start}"`;
      if (params.end) cmdArgs += ` --end "${params.end}"`;
      if (params.ktype !== undefined) cmdArgs += ` --ktype "${params.ktype}"`;
      if (params.autype !== undefined) cmdArgs += ` --autype ${params.autype}`;
      if (params.max_count !== undefined) cmdArgs += ` --max_count ${params.max_count}`;
      if (params.extended_time !== undefined) cmdArgs += ` --extended_time ${params.extended_time}`;

      // 处理fields参数，如果是数组则添加所有项
      if (params.fields && Array.isArray(params.fields)) {
        const fields = params.fields.map((field: string) => `"${field}"`).join(' ');
        cmdArgs += ` --fields ${fields}`;
      }

      const cmd = `python "${scriptPath}" ${cmdArgs}`;

      try {
        // 使用executeJSONCommand方法执行命令并解析JSON结果
        const parsedResult = await command.executeJSONCommand(cmd, { debug: true });

        // 检查结果是否包含错误
        if (parsedResult.error) {
          return {
            content: [{
              type: "text",
              text: `获取历史K线数据失败: ${JSON.stringify(parsedResult.error)}`
            }]
          };
        }

        return {
          content: [{
            type: "text",
            text: `获取到历史K线数据: ${JSON.stringify(parsedResult, null, 2)}`
          }]
        };
      } catch (error: any) {
        return {
          content: [{
            type: "text",
            text: `获取历史K线数据失败: ${error.message}`
          }]
        };
      }
    }
    case "request_trading_days": {
      const command = new CommandExecutor()

      // 构建命令参数
      let cmdArgs = "";

      // 添加可选参数
      if (params.market) cmdArgs += ` --market "${params.market}"`;
      if (params.start) cmdArgs += ` --start "${params.start}"`;
      if (params.end) cmdArgs += ` --end "${params.end}"`;
      if (params.code) cmdArgs += ` --code "${params.code}"`;

      const cmd = `python "${scriptPath}"${cmdArgs}`;

      try {
        // 使用executeJSONCommand方法执行命令并解析JSON结果
        const parsedResult = await command.executeJSONCommand(cmd, { debug: true });

        // 检查结果是否包含错误
        if (parsedResult.error) {
          return {
            content: [{
              type: "text",
              text: `获取交易日历失败: ${JSON.stringify(parsedResult.error)}`
            }]
          };
        }

        return {
          content: [{
            type: "text",
            text: `获取到交易日历数据: ${JSON.stringify(parsedResult, null, 2)}`
          }]
        };
      } catch (error: any) {
        return {
          content: [{
            type: "text",
            text: `获取交易日历失败: ${error.message}`
          }]
        };
      }
    }
    default:
      throw new Error("Unknown tool");
  }
}