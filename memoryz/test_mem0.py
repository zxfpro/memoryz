"""
!pip install -U "mem0ai[graph]"
!pip install langchain_memgraph==0.1.1
!pip install -U mem0ai
"""

from openai import OpenAI
from mem0 import Memory


from mem0.configs.base import MemoryConfig
from mem0.graphs.configs import GraphStoreConfig
from mem0.graphs.configs import Neo4jConfig
from mem0.graphs.configs import MemgraphConfig



import os

from dotenv import load_dotenv

load_dotenv()


os.environ["OPENAI_API_KEY"] = os.getenv("BIANXIE_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("BIANXIE_BASE")


gsconfig = GraphStoreConfig(
    provider = "memgraph",
    config ={
            "url": "bolt://localhost:7687",
            "username": "memgraph",
            "password": "xxx",
    },
)

mconfig = MemoryConfig(
    # graph_store = gsconfig
)

memory = Memory(config = mconfig)


memory.get_all(user_id = 'default_user')


def test_add():

    user_id = "user_demo"
    chat_history = [{"role":"user","content":"hello"},{"role":"assistant","content":"hello good job"}]
    
    memory.add(chat_history, user_id = user_id)

    memories = memory.get_all(user_id = user_id)

    print(memories,'memories')



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

    user_id = "user_demo"
    chat_history = [{"role":"user","content":"hello"},{"role":"assistant","content":"hello good job"}]
    memory.add(chat_history, user_id = user_id)
    chat_history = [{"role":"user","content":"hello2"},{"role":"assistant","content":"hello good job2"}]
    memory.add(chat_history, user_id = user_id)


    limit = 5
    memories = memory.get_chat_history(user_id, limit)
    assert 1 < len(memories) < 5

def test_query():

        relevant_memories = memory.search(query=message, user_id=user_id, limit=3)
    memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])
    



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


if __name__ == "__main__":
    test_query()



