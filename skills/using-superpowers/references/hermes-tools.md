# Hermes Agent 工具映射

技能会描述动作（“派遣子 Agent”“创建待办”“读取文件”）。在 Hermes Agent 上，这些动作对应以下工具。

## 工具

| 技能请求的动作 | Hermes 工具 |
|---|---|
| 读取文件 | `read_file` |
| 创建新文件 | `write_file` |
| 编辑文件（定向补丁） | `patch` |
| 运行 shell 命令 | `terminal` |
| 搜索文件内容 | `search_files` |
| 按名称查找文件 | 使用 `find` 的 `terminal` |
| 获取 URL / 读取网页 | `web_extract(urls=[...])` |
| 搜索网页 | `web_search(query=...)` |
| 派遣子 Agent | `delegate_task(goal=..., context=..., toolsets=[...], role="leaf")` |
| 任务跟踪 | `todo` 工具 |
| 调用技能 | `skill_view("skill-name")` |

## 指令文件

技能提到“你的指令文件”时，在 Hermes Agent 上指项目目录中的 **`AGENTS.md`**，或全局的 `~/.hermes/SOUL.md`。

## 调用技能

Hermes Agent 提供包含 `skill_view` 和 `skills_list` 的 `skills` 工具集。调用 Superpowers 技能：

```
skill_view("brainstorming")
skill_view("test-driven-development")
```

如果 `skill_view` 找不到 Superpowers 技能（插件完全注册前，技能可能尚未出现在目录中），则直接读取 SKILL.md：

```
read_file(path="~/.hermes/plugins/superpowers/skills/<skill-name>/SKILL.md")
```

这是其他没有原生技能加载的运行平台所使用的相同回退机制。

## 派遣子 Agent

使用 `delegate_task` 为并行或串行工作流创建隔离的子 Agent：

```
delegate_task(goal="...", context="...", toolsets=[...], role="leaf")
```

如果 `delegate_task` 不可用，就在线完成工作，不要臆造工具调用。

## 任务跟踪

在会话内使用 `todo` 工具进行任务跟踪。对于多 Agent 任务板，如果可用则使用 `hermes kanban` CLI。将旧的 `TodoWrite` 引用视为任务跟踪动作。
