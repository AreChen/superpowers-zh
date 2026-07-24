---
name: requesting-code-review
description: 在完成任务、实现重大功能或合并前使用，以验证工作是否符合要求
---

# 请求代码审查

派遣一个代码审查子 Agent，在问题产生连锁效应之前将其发现。审查者会收到专为评估而精心构建的准确上下文——绝不会收到你的会话历史记录。

**核心原则：** 及早审查，频繁审查。

## 何时请求审查

**强制：**
- 子 Agent 驱动开发中的每项任务完成后
- 完成重大功能后
- 合并到 main 前

**可选但很有价值：**
- 遇到阻碍时（获得全新视角）
- 重构前（基线检查）
- 修复复杂 bug 后

## 如何请求

**1. 获取 git SHA：**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. 派遣代码审查子 Agent：**

派遣一个 `general-purpose` 子 Agent，并填写 [code-reviewer.md](code-reviewer.md) 中的模板

**占位符：**
- `{DESCRIPTION}` - 你所构建内容的简要摘要
- `{PLAN_OR_REQUIREMENTS}` - 它应该做什么
- `{BASE_SHA}` - 起始提交
- `{HEAD_SHA}` - 结束提交

**3. 根据反馈采取行动：**
- 立即修复“严重”问题
- 继续之前修复“重要”问题
- 记录“次要”问题，留待以后处理
- 如果审查者有误，则提出异议（并说明理由）

## 示例

```
[刚刚完成任务 2：添加验证函数]

你：继续之前，让我请求代码审查。

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[派遣代码审查子 Agent]
  DESCRIPTION: 添加了 verifyIndex() 和 repairIndex()，涵盖 4 种问题类型
  PLAN_OR_REQUIREMENTS: docs/superpowers/plans/deployment-plan.md 中的任务 2
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661

[子 Agent 返回]：
  优点：架构清晰，测试真实有效
  问题：
    重要：缺少进度指示器
    次要：报告间隔使用了魔法数字（100）
  评估：可以继续

你：[修复进度指示器]
[继续执行任务 3]
```

## 常见合理化借口

| 借口 | 现实 |
|--------|---------|
| “我自己审查 diff 就好，不用派遣审查者” | 你是协调者——直接在当前上下文中审查 diff，会消耗你继续推动工作所需的上下文窗口。派遣审查子 Agent：diff 和评估保留在它的上下文中，只有发现项返回给你。 |
| “审查者需要我的完整会话历史才能理解变更” | 只向它提供精心构建的准确上下文，绝不要提供会话历史。这样审查者会专注于工作成果，而不是你的思考过程。 |

## 危险信号

**绝不要：**
- 因为“它很简单”而跳过审查
- 忽略“严重”问题
- 在“重要”问题尚未修复时继续
- 与有效的技术反馈争辩

**如果审查者有误：**
- 用技术理由提出异议
- 展示能够证明其正常工作的代码/测试
- 请求澄清

模板见：[code-reviewer.md](code-reviewer.md)
