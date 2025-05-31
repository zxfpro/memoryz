# memoryz/models.py
from datetime import datetime

class MemoryNode:
    """
    表示一个记忆节点，现在包含用户ID。
    """
    def __init__(self, id, user_id, content, timestamp=None):
        self.id = id
        self.user_id = user_id # 添加用户ID
        self.content = content
        # 如果没有提供timestamp，使用当前时间；否则使用提供的时间戳
        if timestamp is None:
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            # 如果传入的是datetime对象，转换为字符串
            if isinstance(timestamp, datetime):
                self.timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            else:
                self.timestamp = timestamp # 假设已经是字符串格式
    
    def __repr__(self):
        return f"MemoryNode(id={self.id}, user_id='{self.user_id}', content='{self.content[:50]}...')"
