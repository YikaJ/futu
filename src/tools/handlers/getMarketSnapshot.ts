import CommandExecutor from "../../utils/CommandExecutor.js";
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export async function handleGetMarketSnapshot(params: Record<string, unknown> = {}) {
  const command = new CommandExecutor();
  const scriptPath = path.join(__dirname, "../../../scripts/get_market_snapshot.py");

  // 从参数中获取股票代码列表
  const codeList = params?.code_list as string[];

  if (!codeList || codeList.length === 0) {
    return { error: "code_list 参数不能为空" };
  }

  // 正确处理多个股票代码，将每个股票代码作为单独的参数传递
  const formattedCodeList = codeList.map(code => `"${code}"`);

  const cmd = `python "${scriptPath}" --code_list ${formattedCodeList.join(' ')}`;

  try {
    // 使用executeJSONCommand方法执行命令并解析JSON结果
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
