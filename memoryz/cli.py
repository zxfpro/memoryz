# memoryz/cli.py

import sys
import os
from memoryz.manager import MemoryManager
from memoryz.repository import get_memory_repository # 导入工厂方法

def display_help():
    """
    显示CLI命令帮助信息。
    """
    print("Memoryz CLI 伪代码用法:")
    print("  add <content>                - 添加记忆")
    print("  remove <memory_id>           - 移除记忆")
    print("  update <memory_id> [options] - 更新记忆")
    print("    Options:")
    print("      --content <new_content>  - 更新内容")
    print("      --add-related <id1,id2..> - 添加关联记忆ID (逗号分隔)")
    print("      --remove-related <id1,id2..> - 移除关联记忆ID (逗号分隔)")
    print("  query <query_text>           - 查询记忆")
    print("  history <user_id> [limit]    - 获取聊天历史 (伪)")
    print("  list                         - 列出所有记忆 (伪)")
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
            command = input("> ").strip().split()
            if not command:
                continue

            action = command[0].lower()

            if action == 'exit':
                break
            elif action == 'help':
                display_help()
            elif action == 'add':
                if len(command) < 2:
                    print("用法: add <content>")
                    continue
                content = " ".join(command[1:])
                # 伪：这里简化处理，不解析 related_ids
                manager.add_memory(content)
            elif action == 'remove':
                if len(command) != 2:
                    print("用法: remove <memory_id>")
                    continue
                try:
                    memory_id = int(command[1])
                    manager.remove_memory(memory_id)
                except ValueError:
                    print("错误：记忆ID必须是数字。")
            elif action == 'update':
                if len(command) < 3:
                    print("用法: update <memory_id> [options]")
                    display_help()
                    continue
                try:
                    memory_id = int(command[1])
                except ValueError:
                    print("错误：记忆ID必须是数字。")
                    continue

                new_content = None
                add_related = None
                remove_related = None

                i = 2
                while i < len(command):
                    if command[i] == '--content':
                        if i + 1 < len(command):
                            new_content = command[i+1]
                            i += 2
                        else:
                            print("错误：--content 选项需要提供内容。")
                            break
                    elif command[i] == '--add-related':
                        if i + 1 < len(command):
                            add_related_str = command[i+1]
                            add_related = parse_related_ids(add_related_str)
                            if add_related is None: break # 解析失败
                            i += 2
                        else:
                            print("错误：--add-related 选项需要提供关联记忆ID列表。")
                            break
                    elif command[i] == '--remove-related':
                         if i + 1 < len(command):
                            remove_related_str = command[i+1]
                            remove_related = parse_related_ids(remove_related_str)
                            if remove_related is None: break # 解析失败
                            i += 2
                         else:
                            print("错误：--remove-related 选项需要提供关联记忆ID列表。")
                            break
                    else:
                        print(f"未知选项: {command[i]}")
                        display_help()
                        break
                else: # 如果循环没有因为break中断
                     manager.update_memory(memory_id, new_content, add_related, remove_related)


            elif action == 'query':
                if len(command) < 2:
                    print("用法: query <query_text>")
                    continue
                query_text = " ".join(command[1:])
                manager.query_memory(query_text)
            elif action == 'history':
                 if len(command) < 2:
                    print("用法: history <user_id> [limit]")
                    continue
                 user_id = command[1]
                 limit = 10
                 if len(command) > 2:
                     try:
                         limit = int(command[2])
                     except ValueError:
                         print("错误：limit 必须是数字。")
                         continue
                 manager.get_chat_history(user_id, limit)
            elif action == 'list':
                memories = manager.list_all_memories()
                print("当前所有记忆：")
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