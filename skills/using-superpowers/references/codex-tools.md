## 子 Agent 分派需要多 Agent 支持

添加到你的 Codex 配置（`~/.codex/config.toml`）中：

```toml
[features]
multi_agent = true
```

这将启用 `dispatching-parallel-agents` 和 `subagent-driven-development` 等技能使用的多 Agent 工具。具体能获得哪些工具取决于模型预设选择的多 Agent 版本（当前预设运行 V2，旧预设运行 V1）。当实际工具列表与任何表格（包括本文件）不一致时，以实际工具列表为准。

- **派生：** 使用 `spawn_agent {fork_turns: "none"}` 为子 Agent 提供干净上下文；默认的 `"all"` 会把完整对话复制给子 Agent。在 Codex 0.145+ 中，`~/.codex/agents/` 下的角色文件会通过 `agent_type` 附加到隔离分支。完整历史分支可接受 `model` 和 `reasoning_effort` 覆盖（只有 `agent_type` 会被拒绝）；隔离分支是 SDD 默认方式，目的是保持上下文干净，而不是因为覆盖参数需要它。
- **修复轮次：** 使用 `followup_task` 恢复实现者——它会传递消息、触发一轮执行，并透明地重新加载被运行平台驱逐的子 Agent。不要因为“无法再次给派生 Agent 发消息”就派遣新的实现者；V2 始终支持这种恢复。
- **生命周期：** V2 没有 `close_agent`。需要槽位时，已完成的子 Agent 会自动被驱逐；不关闭它们没有成本。只有 V1 会话拥有 `close_agent`——在 V1 中，审查返回后关闭审查者，每项任务审查通过后关闭实现者。
- **模型名称：** 未检查当前 `spawn_agent` 允许列表前，绝不要从技能、表格或旧会话复制模型名称；V2 只接受兼容 V2 的预设，对其他名称会直接报错。

## 等待子 Agent

`wait_agent` 是事件订阅，不是轮询：长等待会在子 Agent 产生邮箱活动的瞬间唤醒，延迟与短等待相同。短超时轮询没有收益，每次超时都会多消耗一次工具调用和上下文计费；在实测会话中，约三分之二的等待调用都是超时的短轮询。

- 仍有本地工作时不要等待。已完成子 Agent 的最终答复会推送到邮箱，并在你的下一轮中到达。
- 真正空闲且仍有子 Agent 时，用有界时间段等待：`wait_agent` 的 `timeout_ms` 设为 300000-600000（5-10 分钟）。每段等待结束（唤醒或超时）后发布一行状态，运行 `list_agents`，并追查已完成却没有报告的子 Agent。绝不要堆叠短于 5 分钟的轮询；事件订阅会以同样速度唤醒有界等待。
- 完成邮件无法唤醒空闲控制器（它会送达但不会触发新一轮）；覆盖这一空闲窗口是 `wait_agent` 唯一的用途。没有活动而超时，是你重新核对状态的信号，不是缩短下一段等待的理由。

## 派遣时的模型路由

每次调用 `spawn_agent`——包括你自己作为扇出任务中的子 Agent 时——都要根据正在执行的技能的模型选择规则显式设置 `model` 和 `reasoning_effort`。只设置 `model` 是陷阱：子 Agent 的思考强度会悄悄重置为该模型默认值，而不是继承你的设置。

请人类伙伴在 `~/.codex/config.toml` 中增加机器级兜底配置，确保遗漏的派遣仍会路由到明确的档位，而不会静默继承会话中最昂贵的模型：

```toml
[agents]
default_subagent_model = "<允许列表中的中档模型>"
default_subagent_reasoning_effort = "medium"
```

## 环境检测

创建工作树或完成分支收尾的技能应在继续操作之前，使用只读 git 命令检测其环境：

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

- `GIT_DIR != GIT_COMMON` → 已经位于链接工作树中（跳过创建）
- `BRANCH` 为空 → detached HEAD（无法从沙箱创建分支/推送/创建 PR）

有关每个技能如何使用这些信号，请参阅 `using-git-worktrees` 的步骤 0 和 `finishing-a-development-branch` 的步骤 1。

## Codex App 收尾

当沙箱阻止分支/推送操作时（在外部管理的工作树中处于 detached HEAD），Agent 会提交所有工作，并告知用户使用 App 的原生控件：

- **“Create branch”** — 为分支命名，然后通过 App UI 提交/推送/创建 PR
- **“Hand off to local”** — 将工作转移到用户的本地检出目录

Agent 仍然可以运行测试、暂存文件，并输出建议的分支名称、提交消息和 PR 描述，供用户复制。
