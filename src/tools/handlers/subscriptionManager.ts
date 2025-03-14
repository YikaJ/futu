import CommandExecutor from "../../utils/CommandExecutor.js";
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export async function handleSubscriptionManager(params: Record<string, unknown> = {}) {
  const command = new CommandExecutor();
  const scriptPath = path.join(__dirname, "../../../scripts/subscription_manager.py");

  // 获取必要参数
  const commandType = params?.command as string;

  if (!commandType) {
    return { error: "command 参数不能为空" };
  }

  // 构建命令
  let cmdArgs = `${commandType}`;

  // 根据不同命令类型添加参数
  if (commandType === 'subscribe') {
    // 订阅需要代码列表和订阅类型
    const codeList = params?.code_list as string[];
    const subtypeList = params?.subtype_list as string[];

    if (!codeList || codeList.length === 0) {
      return { error: "订阅时 code_list 参数不能为空" };
    }

    if (!subtypeList || subtypeList.length === 0) {
      return { error: "订阅时 subtype_list 参数不能为空" };
    }

    // 添加代码列表
    const formattedCodeList = codeList.map(code => `"${code}"`);
    cmdArgs += ` --code_list ${formattedCodeList.join(' ')}`;

    // 添加订阅类型
    const formattedSubtypeList = subtypeList.map(subtype => `"${subtype}"`);
    cmdArgs += ` --subtype_list ${formattedSubtypeList.join(' ')}`;

    // 添加可选参数
    if (params.is_first_push === false) cmdArgs += ` --no_first_push`;
    if (params.subscribe_push === false) cmdArgs += ` --no_push`;
    if (params.is_detailed_orderbook === true) cmdArgs += ` --detailed_orderbook`;
    if (params.extended_time === true) cmdArgs += ` --extended_time`;

  } else if (commandType === 'unsubscribe') {
    // 处理取消所有订阅的情况
    if (params.unsubscribe_all === true) {
      cmdArgs += ` --all`;
    } else {
      // 取消特定订阅的情况
      const codeList = params?.code_list as string[];
      const subtypeList = params?.subtype_list as string[];

      // 至少需要一个参数
      if ((!codeList || codeList.length === 0) && (!subtypeList || subtypeList.length === 0)) {
        return { error: "取消订阅时必须提供 code_list 或 subtype_list 参数" };
      }

      // 添加代码列表
      if (codeList && codeList.length > 0) {
        const formattedCodeList = codeList.map(code => `"${code}"`);
        cmdArgs += ` --code_list ${formattedCodeList.join(' ')}`;
      }

      // 添加订阅类型
      if (subtypeList && subtypeList.length > 0) {
        const formattedSubtypeList = subtypeList.map(subtype => `"${subtype}"`);
        cmdArgs += ` --subtype_list ${formattedSubtypeList.join(' ')}`;
      }
    }
  }
  // query 命令不需要额外参数

  const cmd = `python "${scriptPath}" ${cmdArgs}`;

  try {
    // 执行命令并解析JSON结果
    const parsedResult = await command.executeJSONCommand(cmd, { debug: true });

    // 检查结果是否包含错误
    if (parsedResult.error) {
      return {
        content: [{
          type: "text",
          text: `订阅管理操作失败: ${JSON.stringify(parsedResult.error)}`
        }]
      };
    }

    // 根据不同操作类型返回不同提示信息
    let operationText = '';
    switch (commandType) {
      case 'subscribe':
        operationText = '订阅';
        break;
      case 'unsubscribe':
        operationText = '取消订阅';
        break;
      case 'query':
        operationText = '查询订阅状态';
        break;
    }

    return {
      content: [{
        type: "text",
        text: `${operationText}操作结果: ${JSON.stringify(parsedResult, null, 2)}`
      }]
    };
  } catch (error: any) {
    return {
      content: [{
        type: "text",
        text: `订阅管理操作失败: ${error.message}`
      }]
    };
  }
}
