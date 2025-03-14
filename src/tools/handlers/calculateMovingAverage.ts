import CommandExecutor from "../../utils/CommandExecutor.js";
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export async function handleCalculateMovingAverage(params: Record<string, unknown> = {}) {
  const command = new CommandExecutor();
  const scriptPath = path.join(__dirname, "../../../scripts/calculate_moving_average.py");

  // 从参数中获取股票代码列表
  const codeList = params?.code_list as string[];

  if (!codeList || codeList.length === 0) {
    return { error: "code_list 参数不能为空" };
  }

  // 正确处理多个股票代码，将每个股票代码作为单独的参数传递
  const formattedCodeList = codeList.map(code => `"${code}"`);

  // 构建基础命令
  let cmdArgs = `--code_list ${formattedCodeList.join(' ')}`;

  // 添加移动平均线周期参数（如果提供）
  if (params.ma_periods && Array.isArray(params.ma_periods)) {
    cmdArgs += ` --ma_periods ${params.ma_periods.join(' ')}`;
  }

  const cmd = `python "${scriptPath}" ${cmdArgs}`;

  try {
    // 执行命令并解析JSON结果
    const parsedResult = await command.executeJSONCommand(cmd, { debug: true });

    // 检查结果是否包含错误
    if (parsedResult.error) {
      return {
        content: [{
          type: "text",
          text: `计算移动平均线失败: ${JSON.stringify(parsedResult.error)}`
        }]
      };
    }

    return {
      content: [{
        type: "text",
        text: `计算移动平均线结果: ${JSON.stringify(parsedResult, null, 2)}`
      }]
    };
  } catch (error: any) {
    return {
      content: [{
        type: "text",
        text: `计算移动平均线失败: ${error.message}`
      }]
    };
  }
}
