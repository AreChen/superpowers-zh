## 子 Agent 分派需要多 Agent 支持

添加到你的 Codex 配置（`~/.codex/config.toml`）中：

```toml
[features]
multi_agent = true
```

这将为 `dispatching-parallel-agents` 和 `subagent-driven-development` 等技能启用 `spawn_agent`、`wait_agent` 和 `close_agent`。使用 subagent-driven-development 时，你应始终在实现者和审查者子 Agent 完成其全部工作后将其关闭。

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
