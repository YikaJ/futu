import CommandExecutor from "../utils/CommandExecutor.js";
import path from 'path';
import { fileURLToPath } from 'url';

// 获取当前文件的目录路径
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 从处理函数索引中导入处理函数映射表
import { handlers } from './handlers/index.js';

export async function runToolsAction(methodName: keyof typeof handlers, params: Record<string, unknown> = {}) {
  // 查找对应的处理函数
  const handler = handlers[methodName];

  if (!handler) {
    throw new Error("Unknown tool");
  }

  // 调用对应的处理函数
  return await handler(params);
}