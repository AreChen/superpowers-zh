# Gemini CLI 工具映射

技能以动作来表述（“派遣一个子 Agent”“创建一个待办事项”“读取一个文件”）。在 Gemini CLI 上，这些动作对应于以下工具。

| 技能所请求的动作 | Gemini CLI 等效方式 |
|----------------------|----------------------|
| 读取文件 | `read_file` |
| 一次读取多个文件 | `read_many_files` |
| 创建新文件 | `write_file` |
| 编辑文件 | `replace` |
| 运行 Shell 命令 | `run_shell_command` |
| 搜索文件内容 | `grep_search` |
| 按名称查找文件 | `glob` |
| 列出文件和子目录 | `list_directory` |
| 获取 URL | `web_fetch` |
| 搜索网络 | `google_web_search` |
| 调用技能 | `activate_skill` |
| 派遣子 Agent（`Subagent (general-purpose):` 模板） | 调用 `invoke_agent` 并设置 `agent_name: "generalist"`（也可使用 `@generalist` 聊天语法调用——参见[子 Agent 支持](#子-agent-支持)） |
| 多次并行派遣 | 在同一次响应中进行多个 `invoke_agent` 调用 |
| 任务跟踪（“创建待办事项”“标记为完成”） | `write_todos`（状态：pending、in_progress、completed、cancelled、blocked） |

## 指令文件

技能提到“你的指令文件”时，在 Gemini CLI 中指的是 **`GEMINI.md`**。Gemini CLI 会分层加载 `GEMINI.md`：全局文件位于 `~/.gemini/GEMINI.md`；项目级文件位于工作区目录及其祖先目录；工具访问子目录中的文件时，还会加载该子目录下的 `GEMINI.md`。

## 个人技能目录

用户级技能位于 **`~/.gemini/skills/`**，**`~/.agents/skills/`** 则是跨运行时别名（与 Codex 和 Copilot CLI 共享）。同一作用域同时存在两个目录时，`.agents/skills/` 优先。每个技能都是一个包含 `SKILL.md` 的子目录（其 frontmatter 含 `name` 和 `description`）。

## 子 Agent 支持

Gemini CLI 通过 `invoke_agent` 工具派遣子 Agent；该工具接受 `agent_name` 和 `prompt` 参数。同一派遣能力也提供聊天语法快捷方式：输入 `@generalist <prompt>`，等同于调用 `invoke_agent` 并设置 `agent_name: "generalist"`。内置 Agent 名称包括 `generalist`、`cli_help`、`codebase_investigator`，以及启用浏览器工具后可用的 `browser_agent`。

技能使用 `Subagent (general-purpose):` 进行派遣，并且要么引用提示模板文件（例如 `superpowers:subagent-driven-development` 的 `./implementer-prompt.md`），要么直接提供内联提示。在 Gemini CLI 中：

| 技能派遣形式 | Gemini CLI 等效方式 |
|---------------------|----------------------|
| 引用 `*-prompt.md` 模板（实现者、任务审查者、代码审查者等） | 填充模板，然后调用 `invoke_agent`，设置 `agent_name: "generalist"` 并传入填充后的提示 |
| 引用 `superpowers:requesting-code-review` 的 `./code-reviewer.md` | 调用 `invoke_agent`，设置 `agent_name: "generalist"` 并传入填充后的审查模板 |
| 内联提示（未引用模板） | 调用 `invoke_agent`，设置 `agent_name: "generalist"` 并传入内联提示 |

### 填充提示

技能提供的提示模板会包含 `{WHAT_WAS_IMPLEMENTED}` 或 `[FULL TEXT of task]` 等占位符。将完整提示传给 `invoke_agent` 之前，必须填充所有占位符。提示模板本身已经包含 Agent 角色、审查标准和预期输出格式——子 Agent 会遵循这些内容。

### 并行派遣

Gemini CLI 支持并行派遣子 Agent。在同一次响应中发出多个 `invoke_agent` 调用（或在一个提示中进行多次 `@generalist` 调用），即可并行运行彼此独立的子 Agent 工作。保持依赖任务顺序执行，但不要仅为了让历史记录更简单而把独立的子 Agent 任务串行化。

## 其他 Gemini CLI 工具

以下工具为 Gemini CLI 特有：

| 工具 | 用途 |
|------|---------|
| `save_memory`（旧版） | 当 `experimental.memoryV2 = false` 时跨会话保存事实 |
| `get_internal_docs` | 查阅 Gemini CLI 内置文档 |
| `ask_user` | 向用户提出结构化问题（文本/单选/多选） |
| `enter_plan_mode` / `exit_plan_mode` | 进入或退出只读计划模式 |
| `update_topic` | 更新当前对话的主题/战略意图元数据 |
| `complete_task` | 表示 Gemini 子 Agent 已完成，并将结果返回给父 Agent |
| `tracker_create_task`、`tracker_update_task`、`tracker_get_task`、`tracker_list_tasks`、`tracker_add_dependency`、`tracker_visualize` | 支持依赖关系与可视化的丰富任务跟踪器 |
| `read_mcp_resource`、`list_mcp_resources` | 访问 MCP 资源 |
