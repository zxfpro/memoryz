# memoryz/manager.py

from memoryz.repository import MemoryRepository, get_memory_repository
from memoryz.models import MemoryNode
import json # 用于处理新的输入格式
from memoryz.querys import Querys # 导入 Querys 类
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
        self._querys = Querys(repository=repository) # 实例化 Querys 类，伪：可能需要传递 repository 或其他配置
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

        # 调用 Querys 的 build 方法构建索引
        self._querys.build(user_id, new_content, memory_id=new_memory_id)

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
        # 先更新 Repository
        success = self._repository.update(user_id, memory_id, new_content, add_related, remove_related)

        # 如果内容更新了，调用 Querys 的 build 方法更新索引
        if success and new_content is not None:
             self._querys.build(user_id, new_content, memory_id=memory_id)

        return success

    def query_memory(self, user_id, query_text):
        """
        依据关键点筛选和剔除关联记忆（伪）。
        与底层数据库/Llama Index/Memoryling交互获取相关记忆（伪）。
        处理跨时间轴的相关问题（伪）。
        处理大模型交互时的网络问题和请求报错（伪）。
        """
        print(f"伪：正在查询用户 '{user_id}' 与 '{query_text}' 相关的记忆...")

        # 调用 Querys 的 query 方法获取结果
        query_results = self._querys.query(user_id, query_text)

        # 伪：这里可以根据需要进一步处理 query_results，
        # 例如从 Repository 获取更详细的信息，或者结合图结构进行后处理。
        # 目前，我们直接返回 Querys 的结果。

        print("查询结果：")
        if query_results:
            for res in query_results:
                # 确保结果格式正确，与 CLI 期望的输出一致
                mem_id = res.get('id', 'N/A')
                content = res.get('content', 'N/A')
                related = res.get('related', [])
                print(f"  ID: {mem_id}, 内容: '{content}', 关联记忆ID: {related}")
        else:
            print("  未找到相关记忆。")

        return query_results


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