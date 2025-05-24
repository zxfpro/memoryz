# memoryz/repository.py

from abc import ABC, abstractmethod
from memoryz.models import MemoryNode
import time # 伪：用于模拟时间戳

class MemoryRepository(ABC):
    """
    记忆数据存储的抽象接口 (Repository Pattern)。
    """
    @abstractmethod
    def add(self, content, related_memories=None):
        """添加新的记忆节点，返回节点ID。"""
        pass

    @abstractmethod
    def get(self, memory_id):
        """根据ID获取记忆节点。"""
        pass

    @abstractmethod
    def update(self, memory_id, new_content=None, add_related=None, remove_related=None):
        """更新记忆节点。"""
        pass

    @abstractmethod
    def delete(self, memory_id):
        """删除记忆节点。"""
        pass

    @abstractmethod
    def find_by_content(self, query_text):
        """根据内容模糊查询记忆节点。"""
        pass

    @abstractmethod
    def get_recent(self, limit):
        """获取最近的记忆节点（伪：按添加顺序）。"""
        pass

    @abstractmethod
    def get_all(self):
        """获取所有记忆节点（伪）。"""
        pass


class InMemoryMemoryRepository(MemoryRepository):
    """
    基于内存的记忆数据存储实现 (用于伪代码运行)。
    """
    def __init__(self):
        self._memory_store = {} # { memory_id: MemoryNode }
        self._next_memory_id = 1

    def add(self, content, related_memories=None):
        # 伪：检查内容是否重复
        for node in self._memory_store.values():
            if node.content == content:
                print(f"伪：记忆内容 '{content}' 已存在，ID: {node.id}")
                return node.id # 返回现有记忆ID

        memory_id = self._next_memory_id
        timestamp = int(time.time()) # 伪：使用当前时间戳
        node = MemoryNode(memory_id, content, timestamp, related_memories)
        self._memory_store[memory_id] = node
        self._next_memory_id += 1
        print(f"伪：记忆添加成功，ID: {memory_id}")
        return memory_id

    def get(self, memory_id):
        return self._memory_store.get(memory_id)

    def update(self, memory_id, new_content=None, add_related=None, remove_related=None):
        node = self.get(memory_id)
        if not node:
            print(f"伪：错误：记忆 ID: {memory_id} 不存在")
            return False

        if new_content:
            node.content = new_content
            print(f"伪：记忆 ID: {memory_id} 内容更新成功")

        if add_related:
            for rel_id in add_related:
                if rel_id in self._memory_store and rel_id not in node.related_memories:
                    node.related_memories.append(rel_id)
                    print(f"伪：记忆 ID: {memory_id} 添加关联记忆 ID: {rel_id}")
                elif rel_id not in self._memory_store:
                     print(f"伪：警告：关联记忆 ID: {rel_id} 不存在")


        if remove_related:
            for rel_id in remove_related:
                if rel_id in node.related_memories:
                    node.related_memories.remove(rel_id)
                    print(f"伪：记忆 ID: {memory_id} 移除关联记忆 ID: {rel_id}")
                else:
                     print(f"伪：警告：关联记忆 ID: {rel_id} 未与记忆 ID: {memory_id} 关联")
        return True

    def delete(self, memory_id):
        if memory_id in self._memory_store:
            del self._memory_store[memory_id]
            # 伪：更新其他记忆的关联关系
            for node in self._memory_store.values():
                if memory_id in node.related_memories:
                    node.related_memories.remove(memory_id)
            print(f"伪：记忆 ID: {memory_id} 移除成功")
            return True
        else:
            print(f"伪：错误：记忆 ID: {memory_id} 不存在")
            return False

    def find_by_content(self, query_text):
        results = []
        for node in self._memory_store.values():
            if query_text.lower() in node.content.lower():
                results.append(node)
        return results

    def get_recent(self, limit):
        # 伪：简单地返回最后添加的 limit 个
        all_memories = sorted(self._memory_store.values(), key=lambda x: x.timestamp)
        return all_memories[-limit:] if len(all_memories) > limit else all_memories

    def get_all(self):
        return list(self._memory_store.values())

# 伪：Repository Factory (用于演示如何切换底层实现)
def get_memory_repository(config=None):
    """
    简单工厂方法，根据配置返回不同的 Repository 实现。
    在实际代码中，这里会根据 config 初始化图数据库客户端等。
    """
    # 伪：目前只返回内存实现
    print("伪：使用内存存储 Repository。")
    return InMemoryMemoryRepository()