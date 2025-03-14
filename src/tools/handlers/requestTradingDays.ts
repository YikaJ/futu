import CommandExecutor from "../../utils/CommandExecutor.js";
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export async function handleRequestTradingDays(params: Record<string, unknown> = {}) {
  const command = new CommandExecutor();
  const scriptPath = path.join(__dirname, "../../../scripts/request_trading_days.py");

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
