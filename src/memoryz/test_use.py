from memoryz.manager import MemoryManager
from memoryz.repository import get_memory_repository
from memoryz.models import MemoryNode


def test_add():
    repository = get_memory_repository()
    manager = MemoryManager(repository)

    user_id = "user_demo"
    chat_history = [{"role":"user","content":"hello"},{"role":"assistant","content":"hello good job"}]
    manager.add_chat_history(user_id, chat_history)
    memories = manager.list_all_memories(user_id)
    assert type(memories[0])==MemoryNode



def test_remove():
    repository = get_memory_repository()
    manager = MemoryManager(repository)

    user_id = "user_demo"
    chat_history = [{"role":"user","content":"hello"},{"role":"assistant","content":"hello good job"}]
    manager.add_chat_history(user_id, chat_history)

    memory_id = 1
    manager.remove_memory(user_id, memory_id)
    memories = manager.list_all_memories(user_id)
    assert memories == []


def test_get_history():
    repository = get_memory_repository()
    manager = MemoryManager(repository)

    user_id = "user_demo"
    chat_history = [{"role":"user","content":"hello"},{"role":"assistant","content":"hello good job"}]
    manager.add_chat_history(user_id, chat_history)
    chat_history = [{"role":"user","content":"hello2"},{"role":"assistant","content":"hello good job2"}]
    manager.add_chat_history(user_id, chat_history)


    limit = 5
    memories = manager.get_chat_history(user_id, limit)
    assert 1 < len(memories) < 5

def test_query():
    repository = get_memory_repository()
    manager = MemoryManager(repository)

    user_id = "user_demo"
    chat_history = [{"role":"user","content":"hello"},{"role":"assistant","content":"hello good job"}]
    manager.add_chat_history(user_id, chat_history)
    chat_history = [{"role":"user","content":"hello2"},{"role":"assistant","content":"hello good job2"}]
    manager.add_chat_history(user_id, chat_history)

    query_text = "hello"
    memories = manager.query_memory(user_id, query_text)
    print(memories)

def main5():
    """
    add user123 [{"role":"user","content":"这是需要更新的记忆"}]
    add user123 [{"role":"user","content":"这是另一条记忆"}]
    update user123 2 --content "这是更新后的记忆内容" --add-related 3
    -   `--content <new_content>`: 更新记忆内容 (如果包含空格，请用引号括起来)。
    -   `--add-related <id1,id2..>`: 添加关联记忆ID (逗号分隔)。
    -   `--remove-related <id1,id2..>`: 移除关联记忆ID (逗号分隔)。

    """
    repository = get_memory_repository()
    manager = MemoryManager(repository)

    user_id = "你"
    query_text = "你是谁?"

    chat_history = [{"role":"user","content":"hello"},{"role":"assistant","content":"hello good job"}]
    manager.add_chat_history(user_id, chat_history)
    chat_history2 = [{"role":"user","content":"这是另一条记忆"}]
    manager.add_chat_history(user_id, chat_history2)

    memories = manager.query_memory(user_id, query_text)
    print(memories,'vvv')


if __name__ == "__main__":
    test_query()



