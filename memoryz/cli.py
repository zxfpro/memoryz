# memoryz/cli.py

import sys
import os
import json # 导入 json 模块
from memoryz.manager import MemoryManager
from memoryz.repository import get_memory_repository # 导入工厂方法

def display_help():
    """
    显示CLI命令帮助信息。
    """
    print("Memoryz CLI 伪代码用法:")
    # 更新 add 命令的用法
    print("  add <user_id> <chat_history_json> - 添加聊天历史 (JSON格式)")
    # 更新其他命令的用法以包含 user_id
    print("  remove <user_id> <memory_id>           - 移除记忆")
    print("  update <user_id> <memory_id> [options] - 更新记忆")
    print("    Options:")
    print("      --content <new_content>  - 更新内容 (如果包含空格，请用引号括起来)") # 添加引号提示
    print("      --add-related <id1,id2..> - 添加关联记忆ID (逗号分隔)")
    print("      --remove-related <id1,id2..> - 移除关联记忆ID (逗号分隔)")
    print("  query <user_id> <query_text>           - 查询记忆")
    print("  history <user_id> [limit]    - 获取聊天历史 (伪)")
    print("  list <user_id>               - 列出指定用户所有记忆 (伪)")
    print("  help                         - 显示帮助信息")
    print("  exit                         - 退出")

def parse_related_ids(ids_str):
    """解析关联记忆ID字符串为列表"""
    if not ids_str:
        return []
    try:
        return [int(id_str.strip()) for id_str in ids_str.split(',') if id_str.strip()]
    except ValueError:
        print("错误：关联记忆ID必须是数字，多个ID用逗号分隔。")
        return None

def main():
    """
    CLI交互主循环。
    """
    # 伪：初始化 Repository 和 Manager
    # 在实际应用中，这里会读取配置并使用工厂方法创建 Repository
    repository = get_memory_repository()
    manager = MemoryManager(repository)

    print("欢迎使用 Memoryz CLI 伪代码。输入 'help' 查看命令。")

    while True:
        try:
            # 调整输入处理，允许包含空格的 JSON 字符串
            command_line = input("> ").strip()
            if not command_line:
                continue

            # 尝试解析命令和参数
            # 使用 split(maxsplit=2) 将命令、user_id 和其余部分分开
            parts = command_line.split(maxsplit=2)
            action = parts[0].lower()
            user_id = None
            rest_of_line = ""

            if len(parts) > 1:
                user_id = parts[1]
            if len(parts) > 2:
                rest_of_line = parts[2].strip() # 获取 user_id 之后的所有内容

            if action == 'exit':
                break
            elif action == 'help':
                display_help()
            elif action == 'add':
                # add 命令需要 user_id 和 chat_history_json
                if len(parts) != 3:
                    print("用法: add <user_id> <chat_history_json>")
                    continue
                # user_id 已经在上面获取
                chat_history_json_str = rest_of_line # 聊天历史是 user_id 之后的所有内容

                try:
                    chat_history = json.loads(chat_history_json_str)
                    manager.add_chat_history(user_id, chat_history)
                except json.JSONDecodeError as e:
                    print(f"错误：聊天历史 JSON 格式不正确: {e}")
                except Exception as e:
                    print(f"添加记忆时发生错误: {e}")

            elif action == 'remove':
                # remove 命令需要 user_id 和 memory_id
                # parts: [action, user_id, memory_id]
                if len(parts) != 3:
                    print("用法: remove <user_id> <memory_id>")
                    continue
                # user_id 已经在上面获取
                try:
                    memory_id = int(rest_of_line) # memory_id 是 user_id 之后的所有内容
                    manager.remove_memory(user_id, memory_id)
                except ValueError:
                    print("错误：记忆ID必须是数字。")
                except Exception as e:
                    print(f"移除记忆时发生错误: {e}")

            elif action == 'update':
                # update 命令需要 user_id, memory_id 和 options
                # parts: [action, user_id, "memory_id options..."]
                if len(parts) < 3:
                    print("用法: update <user_id> <memory_id> [options]")
                    display_help()
                    continue
                # user_id 已经在上面获取

                # 从 rest_of_line 中解析 memory_id 和 options
                rest_parts = rest_of_line.split(maxsplit=1) # 分割 "memory_id options..." 为 ["memory_id", "options..."]

                if not rest_parts:
                    print("用法: update <user_id> <memory_id> [options]")
                    display_help()
                    continue

                memory_id_str = rest_parts[0]
                options_str = rest_parts[1] if len(rest_parts) > 1 else ""

                try:
                    memory_id = int(memory_id_str)
                except ValueError:
                    print("错误：记忆ID必须是数字。")
                    continue

                # 现在解析 options_str。简单的 split() 对于包含空格的内容（如 --content "..."）有问题。
                # 对于伪代码，我们假设 --content 选项后面跟着的内容直到下一个选项或行尾都是内容。
                # 其他选项（--add-related, --remove-related）后面跟着的是单个参数。
                update_options = options_str.split()

                new_content = None
                add_related = None
                remove_related = None

                i = 0
                while i < len(update_options):
                    if update_options[i] == '--content':
                        # 假设 --content 后面跟着的内容直到下一个选项或行尾都是内容
                        content_parts = update_options[i+1:]
                        # 查找下一个选项的索引
                        next_option_index = len(content_parts)
                        for j in range(len(content_parts)):
                            if content_parts[j].startswith('--'):
                                next_option_index = j
                                break
                        new_content = " ".join(content_parts[:next_option_index])
                        i += next_option_index + 1 # 跳过内容和选项本身
                    elif update_options[i] == '--add-related':
                        if i + 1 < len(update_options):
                            add_related_str = update_options[i+1]
                            add_related = parse_related_ids(add_related_str)
                            if add_related is None: break # 解析失败
                            i += 2
                        else:
                            print("错误：--add-related 选项需要提供关联记忆ID列表。")
                            break
                    elif update_options[i] == '--remove-related':
                         if i + 1 < len(update_options):
                            remove_related_str = update_options[i+1]
                            remove_related = parse_related_ids(remove_related_str)
                            if remove_related is None: break # 解析失败
                            i += 2
                         else:
                            print("错误：--remove-related 选项需要提供关联记忆ID列表。")
                            break
                    else:
                        print(f"未知选项: {update_options[i]}")
                        display_help()
                        break
                else: # 如果循环没有因为break中断
                     manager.update_memory(user_id, memory_id, new_content, add_related, remove_related)


            elif action == 'query':
                # query 命令需要 user_id 和 query_text
                # parts: [action, user_id, "query_text..."]
                if len(parts) < 3:
                    print("用法: query <user_id> <query_text>")
                    continue
                # user_id 已经在上面获取
                query_text = rest_of_line # query_text 是 user_id 之后的所有内容
                manager.query_memory(user_id, query_text)

            elif action == 'history':
                 # history 命令需要 user_id 和可选的 limit
                 # parts: [action, user_id, optional limit]
                 if len(parts) < 2:
                    print("用法: history <user_id> [limit]")
                    continue
                 # user_id 已经在上面获取
                 limit = 10
                 if len(parts) > 2: # 检查是否有 limit 参数
                     try:
                         limit = int(rest_of_line) # limit 是 user_id 之后的所有内容
                     except ValueError:
                         print("错误：limit 必须是数字。")
                         continue
                 manager.get_chat_history(user_id, limit)

            elif action == 'list':
                # list 命令需要 user_id
                # parts: [action, user_id]
                if len(parts) < 2:
                    print("用法: list <user_id>")
                    continue
                # user_id 已经在上面获取
                memories = manager.list_all_memories(user_id)
                print(f"用户 '{user_id}' 的当前所有记忆：")
                if memories:
                    for mem in memories:
                        print(f"  ID: {mem.id}, 内容: '{mem.content}', 关联记忆ID: {mem.related_memories}")
                else:
                    print("  记忆库为空。")
            else:
                print(f"未知命令: {action}. 输入 'help' 查看命令。")
        except Exception as e:
            print(f"发生未处理的错误: {e}")
            # 伪：在这里可以添加更详细的错误日志记录

if __name__ == "__main__":
    # 伪：为了让伪代码可运行，需要将这些文件放在同一个目录下
    # 或者创建一个简单的 setup.py 或 pyproject.toml 来构建包
    # 这里假设文件结构为 memoryz/models.py, memoryz/repository.py, memoryz/manager.py, memoryz/cli.py
    # 并在 memoryz 目录外运行 python -m memoryz.cli
    # 或者在 memoryz 目录下运行 python cli.py (需要调整导入)
    # 为了简单起见，我们假设在 memoryz 目录外运行，且 memoryz 目录在 PYTHONPATH 中
    # 或者直接将所有伪代码放在一个文件中运行，但这样不利于展示架构
    # 最简单的运行方式是将所有伪代码复制到一个文件中，然后运行该文件。
    # 为了演示模块化，我将保持文件分离，并提供运行建议。
    main()