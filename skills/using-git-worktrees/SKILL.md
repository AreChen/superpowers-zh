---
name: using-git-worktrees
description: 在开始需要与当前工作区隔离的功能开发时，或在执行实施计划之前使用——通过原生工具或 git 工作树回退方案确保隔离工作区存在
---

# 使用 Git 工作树

## 概述

确保工作在隔离工作区中进行。优先使用你所在平台的原生工作树工具。只有在没有原生工具可用时，才回退到手动使用 git 工作树。

**核心原则：** 先检测现有隔离。然后使用原生工具。再回退到 git。绝不要对抗运行平台。

**开始时宣布：** “我正在使用 using-git-worktrees 技能来设置一个隔离工作区。”

## 第 0 步：检测现有隔离

**创建任何内容之前，先检查你是否已经位于隔离工作区中。**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

**子模块防护：** 在 git 子模块中，`GIT_DIR != GIT_COMMON` 同样成立。在断定
“已经位于工作树中”之前，请验证你并非位于子模块中：

```bash
# If this returns a path, you're in a submodule, not a worktree — treat as normal repo
git rev-parse --show-superproject-working-tree 2>/dev/null
```

**如果 `GIT_DIR != GIT_COMMON`（且不在子模块中）：** 你已经位于链接工作树中。
跳到第 2 步（项目设置）。绝不要创建另一个工作树。

报告时包含分支状态：
- 位于分支上：“已位于 `<path>` 的隔离工作区中，当前分支为 `<name>`。”
- Detached HEAD：“已位于 `<path>` 的隔离工作区中（detached HEAD，由外部管理）。完成时需要创建分支。”

**如果 `GIT_DIR == GIT_COMMON`（或位于子模块中）：** 你位于普通仓库检出中。

用户是否已经在你的指令中表明了工作树偏好？如果没有，请在创建工作树之前征求同意：

> “你希望我设置一个隔离工作树吗？它可以保护你的当前分支不受更改影响。”

如果已有明确声明的偏好，无需询问，直接遵照执行。如果用户拒绝，则在原位置工作并跳到第 2 步。

## 第 1 步：创建隔离工作区

**你有两种机制。请按以下顺序尝试。**

### 1a. 原生工作树工具（首选）

用户已经要求使用隔离工作区（第 0 步中的同意）。你是否已经有创建工作树的方法？
它可能是名为 `EnterWorktree`、`WorktreeCreate` 的工具、`/worktree` 命令，
或 `--worktree` 标志。如果有，请使用它并跳到第 2 步。

原生工具会自动处理目录放置、分支创建和清理。当你拥有原生工具时，使用
`git worktree add` 会创建运行平台无法看到或管理的幽灵状态。

只有在没有原生工作树工具可用时，才继续执行步骤 1b。

### 1b. Git 工作树回退方案

**仅当步骤 1a 不适用时才使用此方案**——也就是没有可用的原生工作树工具。
使用 git 手动创建工作树。

#### 目录选择

按以下优先级执行。用户的明确偏好始终优先于观察到的文件系统状态。

1. **检查你的指令中是否声明了工作树目录偏好。** 如果用户已经指定目录，无需询问，直接使用。

2. **检查是否存在项目本地工作树目录：**
   ```bash
   ls -d .worktrees 2>/dev/null     # Preferred (hidden)
   ls -d worktrees 2>/dev/null      # Alternative
   ```
   如果找到，就使用它。如果两者都存在，优先使用 `.worktrees`。

3. **如果没有任何其他可用指引，**默认使用项目根目录下的 `.worktrees/`。

#### 安全验证（仅限项目本地目录）

**创建工作树前，必须验证该目录已被忽略：**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**如果未被忽略：** 将其添加到 .gitignore，提交该更改，然后继续。

**为何至关重要：** 防止意外将工作树内容提交到仓库。

#### 创建工作树

```bash
# Determine path based on chosen location
path="$LOCATION/$BRANCH_NAME"

git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

**沙箱回退方案：** 如果 `git worktree add` 因权限错误（沙箱拒绝）而失败，请告诉用户
沙箱阻止了工作树创建，因此你将改为在当前目录中工作。然后就地运行设置和基线测试。

## 第 2 步：项目设置

自动检测并运行相应的设置：

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

## 第 3 步：验证干净基线

运行测试，确保工作区的起始状态干净：

```bash
# Use project-appropriate command
npm test / cargo test / pytest / go test ./...
```

**如果测试失败：** 报告失败情况，并询问是继续还是调查。

**如果测试通过：** 报告已就绪。

### 报告

```
工作树已准备就绪，位于 <full-path>
测试通过（<N> 个测试，0 个失败）
已准备好实现 <feature-name>
```

## 快速参考

| 情况 | 操作 |
|-----------|--------|
| 已在链接工作树中 | 跳过创建（第 0 步） |
| 位于子模块中 | 按普通仓库处理（第 0 步防护） |
| 有原生工作树工具可用 | 使用它（步骤 1a） |
| 没有原生工具 | 使用 Git 工作树回退方案（步骤 1b） |
| `.worktrees/` 存在 | 使用它（验证已被忽略） |
| `worktrees/` 存在 | 使用它（验证已被忽略） |
| 两者都存在 | 使用 `.worktrees/` |
| 两者都不存在 | 检查指令文件，然后默认使用 `.worktrees/` |
| 目录未被忽略 | 添加到 .gitignore 并提交 |
| 创建时出现权限错误 | 使用沙箱回退方案，原地工作 |
| 基线测试失败 | 报告失败情况并询问 |
| 没有 package.json/Cargo.toml | 跳过依赖项安装 |

## 常见合理化借口

| 借口 | 现实 |
|--------|---------|
| “我显然不在工作树中——没必要检查” | 运行第 0 步。运行平台创建的隔离和子模块都可能骗过肉眼判断；检测命令才能给出结论。 |
| “`git worktree add` 比寻找原生工具更快” | 原生工具（例如 `EnterWorktree`）负责目录、分支和清理。绕过它是头号错误——会创建运行平台看不到也无法管理的幽灵状态。 |
| “工作树目录肯定已经被忽略” | 运行 `git check-ignore`。未忽略的工作树目录会把整棵工作树提交进仓库。 |
| “任何目录名都可以” | 明确指令优先于现有项目本地目录，现有目录又优先于 `.worktrees/` 默认值。 |
| “工作区是新的——基线测试可以稍后再跑” | 不干净的基线会让之后的每次失败都无法归因。现在就运行测试；是否带着失败继续应由你的人类伙伴决定。 |
