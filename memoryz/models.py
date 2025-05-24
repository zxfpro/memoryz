# memoryz/models.py

class MemoryNode:
    """
    表示一个记忆节点。
    """
    def __init__(self, id, content, timestamp, related_memories=None):
        self.id = id
        self.content = content
        self.timestamp = timestamp # 伪：记录时间
        self.related_memories = related_memories if related_memories is not None else []

    def __repr__(self):
        return f"MemoryNode(id={self.id}, content='{self.content[:50]}...', related={self.related_memories})"