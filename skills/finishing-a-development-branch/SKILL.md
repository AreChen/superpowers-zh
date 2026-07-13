---
name: finishing-a-development-branch
description: 在实现完成、所有测试均通过，并且你需要决定如何集成这些工作时使用——通过提供合并、PR 或清理的结构化选项，引导完成开发工作
---

# 完成开发分支

## 概述

通过提供清晰的选项并处理所选择的工作流，引导完成开发工作。

**核心原则：** 验证测试 → 检测环境 → 提供选项 → 执行选择 → 清理。

**开始时宣布：** “我正在使用 finishing-a-development-branch 技能来完成这项工作。”

## 流程

### 第 1 步：验证测试

**在提供选项之前，验证测试是否通过：**

```bash
# 运行项目的测试套件
npm test / cargo test / pytest / go test ./...
```

**如果测试失败：**
```
测试失败（<N> 个失败）。必须先修复才能完成：
[显示失败信息]

在测试通过之前，无法继续合并/PR。
```

停止。不要继续执行步骤 2。

**如果测试通过：** 继续执行步骤 2。

### 步骤 2：检测环境

**在展示选项之前确定工作区状态：**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

这决定了要显示哪个菜单以及如何进行清理：

| 状态 | 菜单 | 清理 |
|-------|------|---------|
| `GIT_DIR == GIT_COMMON`（普通仓库） | 标准的 4 个选项 | 没有要清理的工作树 |
| `GIT_DIR != GIT_COMMON`，命名分支 | 标准的 4 个选项 | 基于来源（见步骤 6） |
| `GIT_DIR != GIT_COMMON`，分离 HEAD | 精简的 3 个选项（无合并） | 不清理（由外部管理） |

### 步骤 3：确定基础分支

```bash
# 尝试常见的基础分支
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

或者询问：“这个分支是从 main 分出来的——对吗？”

### 步骤 4：呈现选项

**普通仓库和命名分支工作树——必须原样呈现以下 4 个选项：**

```
实现已完成。您想怎么做？

1. 在本地合并回 <base-branch>
2. 推送并创建拉取请求
3. 保持分支原样（我稍后会处理）
4. 丢弃此工作

请选择哪个选项？
```

**detached HEAD——必须原样呈现以下 3 个选项：**

```
实现已完成。您当前处于 detached HEAD（外部管理的工作区）。

1. 作为新分支推送并创建拉取请求
2. 保持原样（我稍后会处理）
3. 丢弃此工作

请选择哪个选项？
```

**不要添加解释**——保持选项简洁。

### 步骤 5：执行选择

#### 选项 1：在本地合并

```bash
# 获取主仓库根目录，以确保 CWD 安全
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

# 先合并——在移除任何内容之前验证是否成功
git checkout <base-branch>
git pull
git merge <feature-branch>

# 验证合并结果上的测试
<test command>

# 仅在合并成功后：清理工作树（步骤 6），然后删除分支
```

然后：清理工作树（步骤 6），然后删除分支：

```bash
git branch -d <feature-branch>
```
#### 选项 2：推送并创建 PR

```bash
# 推送分支
git push -u origin <feature-branch>
```

**不要清理工作树**——用户需要保留它，以便根据 PR 反馈进行迭代。

#### 选项 3：保持原样

报告："保留分支 <name>。工作树保留在 <path>。"

**不要清理工作树。**

#### 选项 4：丢弃

**请先确认：**
```
这将永久删除：
- 分支 <name>
- 所有提交：<commit-list>
- 位于 <path> 的工作树

输入 'discard' 以确认。
```

等待完全一致的确认。

如果已确认：
```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
```

然后：清理工作树（步骤 6），再强制删除分支：
```bash
git branch -D <feature-branch>
```

### 步骤 6：清理工作区

**仅针对选项 1 和 4 运行。** 选项 2 和 3 始终保留工作树。

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

**如果 `GIT_DIR == GIT_COMMON`：** 普通仓库，没有需要清理的工作树。完成。

**如果工作树路径位于 `.worktrees/` 或 `worktrees/` 下：** Superpowers 创建了此工作树——清理由我们负责。

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git worktree remove "$WORKTREE_PATH"
git worktree prune  # 自修复：清理所有陈旧的注册记录
```
**否则：** 主机环境（运行平台）拥有此工作区。切勿移除它。如果你的平台提供 workspace-exit 工具，请使用它。否则，将工作区保留在原处。

## 快速参考

| 选项 | 合并 | 推送 | 保留工作树 | 清理分支 |
|--------|-------|------|---------------|----------------|
| 1. 本地合并 | 是 | - | - | 是 |
| 2. 创建 PR | - | 是 | 是 | - |
| 3. 保持原样 | - | - | 是 | - |
| 4. 丢弃 | - | - | - | 是（强制） |

## 常见错误

**跳过测试验证**
- **问题：** 合并有问题的代码，创建会失败的 PR
- **修复：** 在提供选项之前始终验证测试

**开放式问题**
- **问题：** “接下来我该怎么做？”含义不明确
- **修复：** 恰好提供 4 个结构化选项（对于 detached HEAD 则提供 3 个）

**为选项 2 清理工作树**
- **问题：** 移除用户进行 PR 迭代所需的工作树
- **修复：** 仅对选项 1 和 4 执行清理

**在移除工作树之前删除分支**
- **问题：** `git branch -d` 失败，因为工作树仍在引用该分支
- **修复：** 先合并，再移除工作树，然后删除分支
**在工作树内部运行 git worktree remove**
- **问题：** 当 CWD 位于正被移除的工作树内时，命令会静默失败
- **修复：** 在执行 `git worktree remove` 前，始终先 `cd` 到主仓库根目录

**清理运行平台拥有的工作树**
- **问题：** 移除由运行平台创建的工作树会导致幽灵状态
- **修复：** 仅清理 `.worktrees/` 或 `worktrees/` 下的工作树

**丢弃操作没有确认**
- **问题：** 意外删除工作成果
- **修复：** 要求输入 "discard" 进行确认

## 红旗项

**绝不：**
- 在测试失败时继续
- 未验证合并结果上的测试就进行合并
- 未经确认就删除工作成果
- 未经明确请求就强制推送
- 在确认合并成功之前移除工作树
- 清理并非由你创建的工作树（来源检查）
- 从工作树内部运行 `git worktree remove`

**始终：**
- 在提供选项前验证测试
- 在显示菜单前检测环境
- 恰好提供 4 个选项（分离 HEAD 时提供 3 个）
- 对选项 4 获取输入式确认
- 仅为选项 1 和 4 清理工作树
- 在移除工作树前，先 `cd` 到主仓库根目录
- 移除后运行 `git worktree prune`
