# 会话诊断：<session-id>

报告路径：~/.superpowers/diagnosing-superpowers/<session-id>/report.md
撰写时间：<ISO 时间戳>

## 1. 问题陈述（REQUIRED）

<从案例文件中复制。>

## 2. 分诊结论（REQUIRED）

<证据显示，在所报告的问题发生前后出现了什么。使用文字叙述，
每项陈述之后附上 `path:line`。注明置信度：high / medium / low，以及
什么会提高置信度。不要陈述 superpowers 应该做什么。>

## 3. 环境（REQUIRED）

- OS：
- 运行框架及版本：
- 观察到的模型：
- Superpowers 安装根目录 / 版本 / git sha：
- 已读取或注入的技能文件（案例文件中的 sha1 表）：
- 其他插件、扩展、MCP 服务器：
- 存在的指令文件（仅路径）：

为每个环境字段和技能观察结果标注 historical evidence、
unverified snapshot、current observation 或 unknown，并记录其
支持证据的位置。

## 4. 已检查的会话（REQUIRED）

| 角色 | 会话 id | 绝对路径 | 行数 | 字节数 |
|---|---|---|---|---|

被排除的候选项：<id — 路径 — 原因>，或 "none"。

## 5. 时间线（REQUIRED）

每条由人类键入的提示占一行。事件列列出调用的技能、
派发的子 Agent、上下文压缩、错误、恢复和中止。

| 轮次 | 行号 | 时间 | 请求（单行） | 事件 |
|---|---|---|---|---|

## 6. 发现（REQUIRED，每个维度一个子节）

每项发现：
```
- finding: <一句话>
  evidence: <path:line> — "<简短引文>"
  turns: <首个轮次>–<末个轮次>
  confidence: high | medium | low
```
没有内容可报告的维度写作 `none found — checked: <检查了什么>`。

### 6.1 技能时间线
### 6.2 计划遵循情况
### 6.3 重复工作
### 6.4 遇到的障碍
### 6.5 质量证据
### 6.6 请求冲突
### 6.7 成本与时间
### 6.8 使用的其他插件与技能

## 7. Superpowers 的参与情况（REQUIRED）

not indicated | possible | likely

证据行：<path:line 列表>。本节仅说明参与情况。
不指认缺陷，也不提出改动。

## 8. 覆盖情况说明（REQUIRED）

- 未读取：<范围、文件及原因>
- 不可用的运行框架功能：<列表或 none>
- 读取时会话仍在进行中：yes/no
- 供你的人类伙伴复核：<列表或 none>

## 9. 类似会话（仅在被要求时）

| 会话 id | 路径 | 日期 | 运行框架 | 匹配之处 | 不匹配之处 |
|---|---|---|---|---|---|
