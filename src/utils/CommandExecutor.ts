import { exec } from 'child_process';
import { promisify } from 'util';

const execPromise = promisify(exec);

/**
 * 命令执行器类，将命令行操作封装成 Promise
 */
export class CommandExecutor {
  /**
   * 执行命令并返回标准输出
   * @param cmd 要执行的命令
   * @param options 执行选项
   * @returns 命令执行的标准输出结果
   */
  async executeCommand(cmd: string, options: { timeout?: number, debug?: boolean } = {}): Promise<string> {
    const debug = options.debug || false;

    if (debug) {
      console.log(`执行命令: ${cmd}`);
    }

    try {
      const { stdout, stderr } = await execPromise(cmd, {
        timeout: options.timeout || 30000, // 默认30秒超时
        maxBuffer: 1024 * 1024 * 10 // 增加缓冲区大小到10MB
      });

      if (debug && stderr) {
        console.warn(`命令标准错误输出: ${stderr}`);
      }

      return stdout.trim();
    } catch (error: any) {
      console.error(`命令执行失败: ${error.message || error}`);
      if (error.stderr) {
        console.error(`标准错误: ${error.stderr}`);
      }
      throw new Error(`命令执行失败: ${error.message || error}`);
    }
  }

  /**
   * 执行可能输出JSON的命令，并解析结果
   * @param cmd 要执行的命令
   * @param options 执行选项
   * @returns 解析后的JSON对象
   */
  async executeJSONCommand(cmd: string, options: { timeout?: number, debug?: boolean } = {}): Promise<any> {
    const output = await this.executeCommand(cmd, options);
    const debug = options.debug || false;

    if (debug) {
      console.log('命令原始输出:', output);
    }

    try {
      // 首先尝试使用明确的分隔符提取JSON
      const jsonRegex = /###JSON_BEGIN###\s*([\s\S]*?)\s*###JSON_END###/m;
      const match = output.match(jsonRegex);

      if (match && match[1]) {
        if (debug) {
          console.log('找到JSON内容:', match[1].trim());
        }
        return JSON.parse(match[1].trim());
      }

      // 尝试使用Markdown格式提取
      const mdJsonRegex = /```json\s*([\s\S]*?)\s*```/m;
      const mdMatch = output.match(mdJsonRegex);

      if (mdMatch && mdMatch[1]) {
        if (debug) {
          console.log('找到Markdown JSON内容:', mdMatch[1].trim());
        }
        return JSON.parse(mdMatch[1].trim());
      }

      // 尝试直接从输出中提取JSON对象
      // 查找可能的JSON字符串（从第一个{到最后一个}）
      const jsonStartIndex = output.indexOf('{');
      const jsonEndIndex = output.lastIndexOf('}');

      if (jsonStartIndex !== -1 && jsonEndIndex !== -1 && jsonStartIndex < jsonEndIndex) {
        const possibleJson = output.substring(jsonStartIndex, jsonEndIndex + 1);
        if (debug) {
          console.log('尝试解析可能的JSON:', possibleJson);
        }
        return JSON.parse(possibleJson);
      }

      // 如果上述方法都失败，尝试直接解析整个输出
      return JSON.parse(output);
    } catch (error: any) {
      if (debug) {
        console.error('JSON解析失败，详细错误:', error);
      }
      throw new Error(`JSON解析失败: ${error.message}, 原始输出: ${output.substring(0, 200)}${output.length > 200 ? '...' : ''}`);
    }
  }
}

export default CommandExecutor;
