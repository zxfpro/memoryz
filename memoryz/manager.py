# memoryz/manager.py

from memoryz.repository import MemoryRepository, get_memory_repository
from memoryz.models import MemoryNode
import json # 用于处理新的输入格式
# 导入可能的底层交互库（伪）
# import llama_index_client as li_client
# import memoryling_client as ml_client
# 导入可能的图处理库（伪）
# import networkx as nx # 伪：用于表示思维导图

class MemoryManager:
    """
    记忆管理核心业务逻辑层。
    通过 MemoryRepository 接口与数据层交互。
    处理短期/长期记忆转换、重复检查、跨时间轴、底层交互、错误处理等。
    现在支持用户隔离和记忆融合。
    """
    def __init__(self, repository: MemoryRepository):
        self._repository = repository
        # 伪：初始化底层交互客户端
        # self._li_client = li_client.Client() # 伪
        # self._ml_client = ml_client.Client() # 伪
        # 伪：初始化图结构 (如果需要全局图) 或按用户管理图
        # self._mind_maps = {} # { user_id: nx.DiGraph() } # 伪

    def add_chat_history(self, user_id, chat_history):
        """
        处理新的聊天历史输入格式，并添加/融合记忆。
        chat_history 格式: [{"role": "user", "content": "hello"}, {"role": "assistant", "content": "hello good job"}]
        """
        # TODO f"伪：正在处理用户 '{user_id}' 的聊天历史..."
        if not isinstance(chat_history, list):
            print("错误：聊天历史输入格式不正确，应为列表。")
            return

        processed_contents = []
        for message in chat_history:
            if isinstance(message, dict) and 'role' in message and 'content' in message:
                # 伪：这里可以将 user 和 assistant 的消息合并或分开处理
                processed_contents.append(f"{message['role']}: {message['content']}")
            else:
                print(f"警告：跳过格式不正确的聊天消息: {message}")

        combined_content = "\n".join(processed_contents)

        # 1. 添加原始聊天内容作为记忆节点 (可选，取决于是否保留原始对话)
        # original_memory_id = self._repository.add(user_id, combined_content)
        # print(f"伪：原始聊天内容添加为记忆，ID: {original_memory_id}")

        # 2. 提取关键信息并进行记忆融合
        self._fuse_memory(user_id, combined_content)


    def _fuse_memory(self, user_id, new_content):
        """
        将新的内容融合到用户的思维导图中（伪）。
        这涉及提取关键概念、与现有记忆关联、更新图结构等。
        """
        print(f"伪：正在为用户 '{user_id}' 融合记忆...")

        # 伪：
        # - 使用大模型或NLP技术从 new_content 中提取关键概念/实体。
        # - 查询 Repository 查找与这些概念相关的现有记忆节点。
        # - 分析新内容与现有记忆的关系 (例如，时间顺序、因果关系、主题相似度)。
        # - 创建新的记忆节点 (如果需要)。
        # - 更新现有记忆节点 (例如，增加信息、修改内容)。
        # - 在图结构中建立或更新关联边。

        # 伪：简化处理，直接将新内容添加为记忆，并尝试与最近的记忆关联
        new_memory_id = self._repository.add(user_id, new_content)

        # 伪：尝试与最近的几条记忆建立关联
        recent_memories = self._repository.get_recent(user_id, limit=5) # 伪：获取最近5条
        related_ids = [mem.id for mem in recent_memories if mem.id != new_memory_id]

        if related_ids:
            self._repository.update(user_id, new_memory_id, add_related=related_ids)
            # 伪：也可以反向关联
            # for rel_id in related_ids:
            #     self._repository.update(user_id, rel_id, add_related=[new_memory_id])

        print(f"伪：记忆融合完成，新记忆ID: {new_memory_id}")


    def remove_memory(self, user_id, memory_id):
        """
        移除指定用户的记忆。
        """
        return self._repository.delete(user_id, memory_id)

    def update_memory(self, user_id, memory_id, new_content=None, add_related=None, remove_related=None):
        """
        更新指定用户的记忆。
        """
        return self._repository.update(user_id, memory_id, new_content, add_related, remove_related)

    def query_memory(self, user_id, query_text):
        """
        依据关键点筛选和剔除关联记忆（伪）。
        与底层数据库/Llama Index/Memoryling交互获取相关记忆（伪）。
        处理跨时间轴的相关问题（伪）。
        处理大模型交互时的网络问题和请求报错（伪）。
        """
        print(f"伪：正在查询用户 '{user_id}' 与 '{query_text}' 相关的记忆...")

        # 1. 从 Repository 获取初步匹配的记忆
        repo_results = self._repository.find_by_content(user_id, query_text)
        print(f"伪：Repository 初步查询结果 ({len(repo_results)} 条)")

        # 2. 与底层交互获取更多相关记忆
        external_results = []
        # 伪：与底层交互
        # try:
        #     # 伪：根据配置选择底层
        #     if 'llama_index':
        #         # 伪：调用 Llama Index 查询，可能需要传递用户ID或在底层处理用户隔离
        #         li_results = self._li_client.query(user_id, query_text) # 伪调用
        #         external_results.extend(li_results)
        #     elif 'memoryling':
        #         # 伪：调用 Memoryling 查询
        #         ml_results = self._ml_client.query(user_id, query_text) # 伪调用
        #         external_results.extend(ml_results)
        # except Exception as e:
        #     print(f"伪：底层交互发生错误: {e}")
        #     # 伪：处理网络问题和请求报错，例如重试、记录日志、返回部分结果等
        #     pass # 伪：忽略错误继续

        # 3. 合并并处理结果：筛选、剔除、处理跨时间轴关联
        # 伪：这里需要更复杂的逻辑来处理图结构、关联度、时间轴等进行筛选和排序
        all_results = repo_results + external_results # 伪：简单合并
        final_results = []
        seen_ids = set()

        print("伪：处理结果：筛选、剔除、跨时间轴关联...")
        for res in all_results:
            if isinstance(res, dict): # 伪：处理来自外部库的字典格式结果
                 mem_id = res.get('id')
                 content = res.get('content')
                 related = res.get('related', [])
                 # 伪：确保结果属于当前用户 (如果底层交互没有自动处理)
                 res_user_id = res.get('user_id')
                 if mem_id is not None and mem_id not in seen_ids and (res_user_id is None or res_user_id == user_id):
                      final_results.append({'id': mem_id, 'content': content, 'related': related})
                      seen_ids.add(mem_id)
            elif isinstance(res, MemoryNode): # 处理来自 Repository 的 MemoryNode
                 if res.id not in seen_ids and res.user_id == user_id: # 确保属于当前用户
                      final_results.append({'id': res.id, 'content': res.content, 'related': res.related_memories})
                      seen_ids.add(res.id)


        print("查询结果：")
        if final_results:
            for res in final_results:
                print(f"  ID: {res['id']}, 内容: '{res['content']}', 关联记忆ID: {res['related']}")
        else:
            print("  未找到相关记忆。")

        return final_results


    def get_chat_history(self, user_id, limit=10):
        """
        为用户提供获取聊天历史的接口（伪）。
        这可能涉及查询特定用户相关的记忆节点。
        """
        print(f"伪：正在获取用户 '{user_id}' 的最近 {limit} 条聊天历史...")
        # 伪：模拟获取聊天历史，可能通过 Repository 或直接查询与用户ID关联的记忆
        history = self._repository.get_recent(user_id, limit) # 使用用户ID
        print("伪：聊天历史获取完成。")
        return history

    def list_all_memories(self, user_id):
        """
        列出指定用户当前所有记忆（伪）。
        """
        return self._repository.get_all(user_id)

    # 伪：其他可能的方法，例如：
    # def get_mind_map(self, user_id):
    #     """获取指定用户的思维导图结构（伪）。"""
    #     pass
    #
    # def analyze_memory_relationship(self, user_id, memory_id1, memory_id2):
    #     """分析两个记忆节点之间的关系（伪）。"""
    #     pass