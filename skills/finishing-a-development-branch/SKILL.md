---
name: finishing-a-development-branch
description: 在实现完成、所有测试均通过，并且你需要决定如何集成这些工作时使用
---

# 完成开发分支

## 概述

**核心原则：** 验证测试 → 检测环境 → 呈现选项 → 执行选择 → 清理。

**开始时宣布：** “我正在使用 finishing-a-development-branch 技能来完成这项工作。”

## 第 1 步：验证测试

运行项目的完整测试套件（`npm test` / `cargo test` / `pytest` / `go test ./...`）。

**如果测试失败，**报告失败并停止——只有测试套件全绿后才能显示菜单：

```
测试失败（<N> 个失败）。必须先修复才能完成：

[显示失败信息]
```

**如果测试通过：** 继续执行第 2 步。

## 第 2 步：检测环境

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
# Capture now, while still inside the workspace — Step 5 changes directory
# before cleanup (Step 6) needs this value
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

这决定了要显示哪个菜单以及如何清理：

| 状态 | 菜单 | 清理 |
|-------|------|------|
| `GIT_DIR == GIT_COMMON`（普通仓库） | 标准 3 个选项 | 没有要清理的工作树 |
| `GIT_DIR != GIT_COMMON`，命名分支 | 标准 3 个选项 | 按来源清理（见第 6 步） |
| `GIT_DIR != GIT_COMMON`，detached HEAD | 精简 2 个选项（无合并） | 由外部管理——保留原位 |

## 第 3 步：确定基础分支

基础分支就是当前工作从中分出的分支——通常在计划、对话或该分支的 upstream 中
已经指明。如果还不知道，请询问：“这个分支是从 <你最合理的猜测> 分出来的——
对吗？”合并前必须确认；合并到错误基础分支的撤销成本很高。

## 第 4 步：呈现选项

**普通仓库和命名分支工作树——必须原样呈现以下 3 个选项：**

```
实现已完成。你想怎么处理？

1. 在本地合并回 <base-branch>
2. 推送并创建 Pull Request
3. 保持分支原样（我稍后处理）

请选择哪个选项？
```

**Detached HEAD——必须原样呈现以下 2 个选项：**

```
实现已完成。你当前处于 detached HEAD（由外部管理的工作区）。

1. 作为新分支推送并创建 Pull Request
2. 保持原样（我稍后处理）

请选择哪个选项？
```

严格按上述形式呈现菜单——保持简洁，每个选项都必须来自上面的列表。只有当你的人类
伙伴明确要求丢弃工作时，才进入丢弃流程（见下文“如果你的人类伙伴要求丢弃工作”）。
等待对方回答；集成决定属于他们。

## 第 5 步：执行选择

### 选项 1：在本地合并

```bash
# Get main repo root for CWD safety
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

# Merge first — verify success before removing anything
git checkout <base-branch>
git pull
git merge <feature-branch>

# Verify tests on merged result
<test command>
```

如果合并结果上的测试失败：停止，保留工作树和分支并调查——尚未推送任何内容，
因此本地合并仍可恢复。

合并结果全绿后：清理工作树（第 6 步），再删除分支：

```bash
git branch -d <feature-branch>
```

### 选项 2：推送并创建 PR

```bash
git push -u origin <feature-branch>
# From a detached HEAD, name the new branch on the remote:
# git push origin HEAD:refs/heads/<new-branch>
```

然后使用代码托管平台的工具，以 <base-branch> 为目标创建 Pull/Merge Request——
如果有 CLI 就使用 CLI，否则使用多数平台在推送时打印的创建 URL；若仓库存在 PR
模板和约定，则遵循它们，并将 URL 报告给你的人类伙伴。

保留工作树——你的人类伙伴会在其中处理 PR 反馈。

### 选项 3：保持原样

报告：“保留分支 <name>。工作树保留在 <path>。”

### 如果你的人类伙伴要求丢弃工作

此路径仅在对方明确要求丢弃工作时存在。请先确认：

```
这将永久删除：
- 分支 <name>
- 所有提交：<commit-list>
- 位于 <path> 的工作树

输入 'discard' 以确认。
```

等待完全一致的确认。收到后：

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
```

然后清理工作树（第 6 步），并强制删除分支：

```bash
git branch -D <feature-branch>
```

## 第 6 步：清理工作区

**仅对选项 1 和已确认的丢弃操作运行。** 选项 2 和 3 始终保留工作树。两个调用方
都已经切换到主仓库根目录——移除工作树必须在工作树外部运行——并且必须使用第 2 步
中切换目录前捕获的 `GIT_DIR`/`GIT_COMMON`/`WORKTREE_PATH` 值。

**如果 `GIT_DIR == GIT_COMMON`：** 普通仓库，没有要清理的工作树。完成。

**如果 `WORKTREE_PATH` 位于 `.worktrees/` 或 `worktrees/` 下：** 此工作树由
Superpowers 创建——清理由我们负责：

```bash
git worktree remove "$WORKTREE_PATH"
git worktree prune  # Self-healing: clean up any stale registrations
```

**否则：** 此工作区属于宿主环境——保留原位。如果你的平台提供 workspace-exit
工具，请使用它。

## 快速参考

| 选项 | 合并 | 推送 | 保留工作树 | 清理分支 |
|--------|-------|------|---------------|----------------|
| 1. 本地合并 | 是 | - | - | 是 |
| 2. 创建 PR | - | 是 | 是 | - |
| 3. 保持原样 | - | - | 是 | - |
| 丢弃（仅限明确请求） | - | - | - | 是（强制） |

## 常见合理化借口

| 借口 | 现实 |
|--------|---------|
| “测试在本次会话早些时候通过了” | 在即将集成的代码树上运行完整套件。一次全绿只证明运行它的那棵代码树。 |
| “他们显然想要合并” | 集成决定属于你的人类伙伴。呈现菜单并等待。 |
| “他们看起来已经不需要这个功能了——我来提供丢弃选项” | 菜单按原样就已经完整。只有当你的人类伙伴明确说出要丢弃时，才能进入丢弃流程。 |
| “‘嗯，把它删掉吧’也算确认” | 只有精确输入 `discard` 才授权删除。 |
| “PR 已经创建，所以工作树现在只是累赘” | PR 反馈需要在该工作树中修复。工作合入之前，它必须保留。 |
| “另一个工作树看起来陈旧——我顺便清理” | 只清理 `.worktrees/` 或 `worktrees/` 下的工作树。其他一切都属于宿主环境。 |
| “合并结果失败可能只是偶发问题” | 合并结果一旦失败就停止一切。调查期间保留分支和工作树。 |
| “基础分支显然是 main” | 确认分叉点或询问。合并到错误基础分支的撤销成本很高。 |
| “推送被拒绝——强制推送就能解决” | 推送被拒绝说明远端已变化。先调查；只有你的人类伙伴明确要求时才强制推送。 |
