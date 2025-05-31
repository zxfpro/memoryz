# memoryz/repository.py

from abc import ABC, abstractmethod
from memoryz.models import MemoryNode
import time # 伪：用于模拟时间戳
import json # 用于处理新的输入格式

class MemoryRepository(ABC):
    """
    记忆数据存储的抽象接口 (Repository Pattern)。
    现在支持用户隔离。
    """
    @abstractmethod
    def add(self, user_id, content, related_memories=None):
        """为指定用户添加新的记忆节点，返回节点ID。"""
        pass

    @abstractmethod
    def get(self, user_id, memory_id):
        """根据用户ID和记忆ID获取记忆节点。"""
        pass

    @abstractmethod
    def update(self, user_id, memory_id, new_content=None, add_related=None, remove_related=None):
        """更新指定用户的记忆节点。"""
        pass

    @abstractmethod
    def delete(self, user_id, memory_id):
        """删除指定用户的记忆节点。"""
        pass

    @abstractmethod
    def find_by_content(self, user_id, query_text):
        """根据用户ID和内容模糊查询记忆节点。"""
        pass

    @abstractmethod
    def get_recent(self, user_id, limit):
        """获取指定用户最近的记忆节点（伪：按添加顺序）。"""
        pass

    @abstractmethod
    def get_all(self, user_id):
        """获取指定用户所有记忆节点（伪）。"""
        pass


class InMemoryMemoryRepository(MemoryRepository):
    """
    基于内存的记忆数据存储实现 (用于伪代码运行)。
    按用户ID隔离存储。
    """
    def __init__(self):
        # 存储结构: { user_id: { memory_id: MemoryNode, '_next_memory_id': int } }
        self._memory_store = {}

    def _get_user_store(self, user_id):
        """获取或创建指定用户的记忆存储和下一个ID计数器。"""
        if user_id not in self._memory_store:
            self._memory_store[user_id] = {'memories': {}, '_next_memory_id': 1}
        return self._memory_store[user_id]['memories'], self._memory_store[user_id]

    def add(self, user_id, content, related_memories=None):
        user_memories, user_data = self._get_user_store(user_id)
        next_memory_id = user_data['_next_memory_id']

        # Ensure related_memories is a list
        if related_memories is None:
            related_memories = []

        # 伪：检查内容是否重复 (仅在该用户内部检查)
        for node in user_memories.values():
            if node.content == content:
                print(f"伪：用户 '{user_id}' 的记忆内容 '{content}' 已存在，ID: {node.id}")
                return node.id # 返回现有记忆ID

        memory_id = next_memory_id
        timestamp = int(time.time()) # 伪：使用当前时间戳
        node = MemoryNode(memory_id, user_id, content, timestamp)
        user_memories[memory_id] = node
        user_data['_next_memory_id'] += 1
        print(f"伪：用户 '{user_id}' 记忆添加成功，ID: {memory_id}")
        return memory_id

    def get(self, user_id, memory_id):
        user_memories, _ = self._get_user_store(user_id)
        return user_memories.get(memory_id)

    def update(self, user_id, memory_id, new_content=None, add_related=None, remove_related=None):
        user_memories, _ = self._get_user_store(user_id)
        node = user_memories.get(memory_id)
        if not node:
            print(f"伪：错误：用户 '{user_id}' 的记忆 ID: {memory_id} 不存在")
            return False

        if new_content:
            node.content = new_content
            print(f"伪：用户 '{user_id}' 的记忆 ID: {memory_id} 内容更新成功")

        return True

    def delete(self, user_id, memory_id):
        user_memories, _ = self._get_user_store(user_id)
        if memory_id in user_memories:
            del user_memories[memory_id]
            # 伪：更新该用户下其他记忆的关联关系
            for node in user_memories.values():
                if memory_id in node.related_memories:
                    node.related_memories.remove(memory_id)
            print(f"伪：用户 '{user_id}' 的记忆 ID: {memory_id} 移除成功")
            return True
        else:
            print(f"伪：错误：用户 '{user_id}' 的记忆 ID: {memory_id} 不存在")
            return False

    def find_by_content(self, user_id, query_text):
        user_memories, _ = self._get_user_store(user_id)
        results = []
        for node in user_memories.values():
            if query_text.lower() in node.content.lower():
                results.append(node)
        return results

    def get_recent(self, user_id, limit):
        user_memories, _ = self._get_user_store(user_id)
        # 伪：简单地返回该用户下最后添加的 limit 个
        all_memories = sorted(user_memories.values(), key=lambda x: x.timestamp)
        return all_memories[-limit:] if len(all_memories) > limit else all_memories

    def get_all(self, user_id):
        user_memories, _ = self._get_user_store(user_id)
        return list(user_memories.values())


    def get_all(self, user_id):
        user_memories, _ = self._get_user_store(user_id)
        return list(user_memories.values())

# 伪：Repository Factory (用于演示如何切换底层实现)
def get_memory_repository(config=None):
    """
    简单工厂方法，根据配置返回不同的 Repository 实现。
    在实际代码中，这里会根据 config 初始化图数据库客户端等。
    """
    # 伪：目前只返回内存实现
    print("伪：使用内存存储 Repository。")
    return InMemoryMemoryRepository()