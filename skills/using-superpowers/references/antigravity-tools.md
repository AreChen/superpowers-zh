# Antigravity CLI (`agy`) 工具映射

技能以动作来表述（“派遣一个子 Agent”“创建一个待办事项”“读取一个文件”）。在 Antigravity CLI (`agy`) 上，这些动作对应于以下工具。

| 技能所请求的动作 | Antigravity CLI 等效方式 |
|----------------------|----------------------|
| 派遣一个子 Agent（`Subagent (general-purpose):` 模板） | 使用带有内置 `TypeName` 的 `invoke_subagent`——`self` 用于全能力工作，`research` 用于只读工作 |
| 任务跟踪（“创建一个待办事项”“标记为完成”） | 一个**任务产物**——使用 `write_to_file`，并设置 `IsArtifact: true` 和 `ArtifactType: "task"`（参见[任务跟踪](#task-tracking)）。**不是** `manage_task`，后者用于管理后台进程。 |

## 任务跟踪

Antigravity **没有待办工具**（`manage_task` 管理后台
进程——`list`/`kill`/`status`/`send_input`——它*不是*检查清单）。当某项
技能要求创建待办列表或跟踪任务时，请维护一个**任务产物**：一个
使用 `write_to_file`（`IsArtifact: true`、
`ArtifactMetadata.ArtifactType: "task"`）保存的 Markdown 检查清单，并在执行过程中使用 `replace_file_content` /
`multi_replace_file_content` 对其进行编辑。

在开始任何多步骤任务时，创建任务产物，列出计划中的每一个步骤。
完成每个步骤后，编辑该产物以将其标记为完成（`- [x]`）。
如果计划发生变化，请更新检查清单。使其始终保持最新——它是判断尚余事项的
事实依据；一旦对话变长，请在开始
每个步骤之前重新阅读它。
