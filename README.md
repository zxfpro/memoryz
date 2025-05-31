# Memoryz 记忆管理包 (伪代码)

这是一个用于大模型聊天应用的记忆管理包的伪代码实现。它展示了核心功能、分层架构以及CLI交互模式。

**请注意：** 这只是一个伪代码框架，用于演示设计思路和运行逻辑。其中的底层数据库交互、与 Llama Index/Memoryling 的集成、详细的重复检查、跨时间轴处理、图节点关系的复杂管理以及错误处理等都需要在实际开发中进行详细实现和填充。**特别是记忆融合功能，在伪代码中仅为概念性实现，需要复杂的NLP和图算法支持。**

## 架构概述

伪代码采用了以下设计模式：

-   **Repository Pattern:** 抽象数据存储层，现在支持按用户ID隔离记忆。
-   **Manager/Service Layer:** 包含核心业务逻辑，处理短期/长期记忆转换、记忆融合、底层交互和错误处理。
-   **Simple Factory:** (暗示) 用于创建 Repository 实现。

代码被组织在 `memoryz` 目录下的以下文件中：

-   [`memoryz/models.py`](memoryz/models.py): 定义数据模型 `MemoryNode`，包含 `user_id` 字段。
-   [`memoryz/repository.py`](memoryz/repository.py): 定义 `MemoryRepository` 接口和 `InMemoryMemoryRepository` 内存实现，支持用户隔离存储。
-   [`memoryz/manager.py`](memoryz/manager.py): 定义 `MemoryManager` 类，包含业务逻辑，处理新的输入格式和记忆融合（概念性）。
-   [`memoryz/cli.py`](memoryz/cli.py): CLI交互入口，适配新的命令格式，修复了参数解析问题。

## 核心功能优化 (伪代码版本)

-   **输入格式调整:** `add` 命令现在接受 JSON 格式的聊天历史列表。
-   **用户隔离:** 记忆存储和操作现在与用户ID关联，确保不同用户记忆的隔离。
-   **记忆融合:** 引入记忆融合的伪代码逻辑，模拟将聊天历史融入用户思维导图的过程。**请注意，这部分在伪代码中仅为框架，不包含实际的融合算法。**

## 如何运行伪代码

1.  确保您已经在项目根目录 (`/Users/zhaoxuefeng/GitHub/memoryz`) 下创建了一个名为 `memoryz` 的文件夹。
2.  将伪代码文件 (`models.py`, `repository.py`, `manager.py`, `cli.py`) 保存到 `memoryz` 文件夹内。
3.  打开终端，切换到项目根目录 (`/Users/zhaoxuefeng/GitHub/memoryz`)。
4.  运行以下命令启动CLI：

    ```bash
    python -m memoryz.cli
    ```

## CLI 命令使用说明

启动CLI后，您将看到 `欢迎使用 Memoryz CLI 伪代码。输入 'help' 查看命令。` 的提示符。请注意，大多数命令现在需要指定 `user_id`。您可以输入以下命令进行交互：

-   **`help`**: 显示所有可用命令的帮助信息。

    ```
    > help
    ```

-   **`add <user_id> <chat_history_json>`**: 为指定用户添加聊天历史 (JSON格式)。

    ```
    > add user123 [{"role":"user","content":"hello"},{"role":"assistant","content":"hello good job"}]
    伪：正在处理用户 'user123' 的聊天历史...
    伪：正在为用户 'user123' 融合记忆...
    伪：使用内存存储 Repository。
    伪：用户 'user123' 记忆添加成功，ID: 1
    伪：用户 'user123' 记忆融合完成，新记忆ID: 1
    ```
    请注意，JSON 字符串需要是有效的，并且可能需要根据您的终端环境进行适当的引用或转义。

-   **`remove <user_id> <memory_id>`**: 移除指定用户的记忆。

    ```
    > remove user123 1
    伪：用户 'user123' 的记忆 ID: 1 移除成功
    ```

-   **`update <user_id> <memory_id> [options]`**: 更新指定用户的记忆。
    -   `--content <new_content>`: 更新记忆内容 (如果包含空格，请用引号括起来)。
    -   `--add-related <id1,id2..>`: 添加关联记忆ID (逗号分隔)。
    -   `--remove-related <id1,id2..>`: 移除关联记忆ID (逗号分隔)。

    ```
    > add user123 [{"role":"user","content":"这是需要更新的记忆"}]
    add user124 [{"role":"user","content":"这是需要更新的记忆"}]
    伪：正在处理用户 'user123' 的聊天历史...
    伪：正在为用户 'user123' 融合记忆...
    伪：使用内存存储 Repository。
    伪：用户 'user123' 记忆添加成功，ID: 2
    伪：用户 'user123' 记忆融合完成，新记忆ID: 2
    > add user123 [{"role":"user","content":"这是另一条记忆"}]
    伪：正在处理用户 'user123' 的聊天历史...
    伪：正在为用户 'user123' 融合记忆...
    伪：使用内存存储 Repository。
    伪：用户 'user123' 记忆添加成功，ID: 3
    伪：用户 'user123' 记忆融合完成，新记忆ID: 3
    > update user123 2 --content "这是更新后的记忆内容" --add-related 3
    伪：用户 'user123' 的记忆 ID: 2 内容更新成功
    伪：用户 'user123' 的记忆 ID: 2 添加关联记忆 ID: 3
    ```
    请注意 `--content` 选项后面带有空格的内容需要用引号括起来。

-   **`query <user_id> <query_text>`**: 根据文本查询指定用户的相关记忆 (通过 Querys 能力层)。

    ```
    > query user123 更新后的记忆
    伪：正在查询用户 'user123' 与 '更新后的记忆' 相关的记忆...
    伪：Querys 正在为用户 'user123' 查询记忆...
    伪：查询执行完成。
    伪：Querys 返回模拟结果 (2 条)
    查询结果：
      ID: 101, 内容: '伪：与 '更新后的记忆' 相关的记忆 A', 关联记忆ID: [102]
      ID: 102, 内容: '伪：与 '更新后的记忆' 相关的记忆 B', 关联记忆ID: []
    ```

-   **`history <user_id> [limit]`**: 获取指定用户的聊天历史 (伪实现)。

    ```
    > history user123 5
    伪：正在获取用户 'user123' 的最近 5 条聊天历史...
    伪：使用内存存储 Repository。
    伪：聊天历史获取完成。
    ```

-   **`list <user_id>`**: 列出指定用户当前所有记忆 (伪实现)。

    ```
    > list user123
    用户 'user123' 的当前所有记忆：
      ID: 2, 内容: '这是更新后的记忆内容', 关联记忆ID: [3]
      ID: 3, 内容: '这是另一条记忆', 关联记忆ID: []
    ```

-   **`exit`**: 退出CLI。

    ```
    > exit
    ```

## 后续开发

在实际开发中，您需要：

-   替换 `InMemoryMemoryRepository` 为实际的数据库实现 (例如，使用图数据库客户端)，确保高效的用户隔离和图结构存储。
-   实现与 Llama Index 或 Memoryling 的具体交互逻辑，并考虑如何将用户ID传递给这些库或在结果中处理用户关联。
-   完善短期记忆到长期记忆的转换策略。
-   **实现基于图结构的记忆关联、筛选和剔除逻辑，以及更复杂的记忆融合算法 (例如，使用大模型进行概念提取和关系分析)。这是将聊天历史融入思维导图的关键部分。**
-   处理大模型交互中的网络问题、请求超时和错误重试等。
-   编写详细的单元测试，达到98%的测试覆盖率目标。
-   考虑性能优化，尤其是在处理大量记忆和复杂图结构时。