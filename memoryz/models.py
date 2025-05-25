# memoryz/models.py

class MemoryNode:
    """
    表示一个记忆节点，现在包含用户ID。
    """
    def __init__(self, id, user_id, content, timestamp, related_memories=None):
        self.id = id
        self.user_id = user_id # 添加用户ID
        self.content = content
        self.timestamp = timestamp # 伪：记录时间
        self.related_memories = related_memories if related_memories is not None else [] # 表示图的边

    def __repr__(self):
        return f"MemoryNode(id={self.id}, user_id='{self.user_id}', content='{self.content[:50]}...', related={self.related_memories})"

# 伪：可以考虑其他模型来表示更复杂的图结构或用户特定的记忆集合
# class UserMemoryGraph:
#     """
#     表示一个用户的记忆思维导图。
#     """
#     def __init__(self, user_id):
#         self.user_id = user_id
#         self.nodes = {} # { memory_id: MemoryNode }
#         self.edges = {} # { memory_id: [related_memory_ids] }
#     # ... 其他图操作方法 ...