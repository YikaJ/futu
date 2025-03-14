import CommandExecutor from "../../utils/CommandExecutor.js";
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export async function handleRequestHistoryKline(params: Record<string, unknown> = {}) {
  const command = new CommandExecutor();
  const scriptPath = path.join(__dirname, "../../../scripts/request_history_kline.py");

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
