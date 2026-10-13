# Muse 工具映射

技能以动作来表述需求（“派发一个子 Agent”、“创建一个待办事项”、“读取一个文件”）。在 Muse 中，这些动作对应以下工具。

| 技能请求的动作 | Muse 对应工具 |
|----------------------|----------------|
| 读取文件 | `read_file` |
| 读取多个文件 | `read_file`（调用多次）或 `search` |
| 创建新文件 | `write_file` |
| 编辑文件 | `edit_file` |
| 运行 shell 命令 | `bash` |
| 搜索文件内容 | `search` |
| 按名称查找文件 | 使用带有 `glob` 的 `search` |
| 获取 URL | `web_fetch` |
| 搜索网页 | `web_search` |
| 调用技能 | 使用 `read_file` 读取 `skills/<name>/SKILL.md`，或使用原生技能工具 |
| 派发子 Agent（`Subagent (general-purpose):` 模板） | 填好提示词后使用 `subagent_spawn` |
| 任务跟踪（“创建待办事项”、“标记完成”） | `write_todos` 或用 `bash` 管理的任务文件 |
| 向用户提问 | `request_user_input` |

## 指令文件

当技能提到“你的指令文件”时，在 Muse 中，这指的是项目根目录下的 **`CLAUDE.md`** 或 **`AGENTS.md`**。在已配置的情况下，Muse 会按层级加载这些文件。

## 技能调用

Muse 通过 `muse skills` 提供原生技能支持。要调用 Superpowers 技能，请读取其 `SKILL.md` 并遵循其中的指令。引导技能（`using-superpowers`）会通过插件钩子在 `SessionStart` 时自动注入——你已经在遵循它，不要重新加载它。

## 子 Agent 派发

使用 `subagent_spawn` 将工作委派给相互隔离的子 Agent。派发前填写提示词模板（例如 `implementer-prompt.md`、`task-reviewer-prompt.md`）。如果没有可用的子 Agent 工具，就直接在当前上下文中完成工作，而不是编造工具调用。

## 任务跟踪

使用 `write_todos` 跟踪检查清单。为技能检查清单中的每一项创建一个待办事项，并随进展标记为 in_progress/completed。如果 `write_todos` 不可用，通过 `write_file`/`edit_file` 维护一个 Markdown 任务文件。
