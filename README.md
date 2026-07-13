# Superpowers 中文版

Superpowers 是一套面向编程 Agent 的完整软件开发方法论。它由一组可组合的技能和启动指令构成，确保 Agent 能在合适的时机主动调用这些技能。

本项目是 [obra/superpowers](https://github.com/obra/superpowers) 的中文分叉版本，主要面向使用 Codex、OpenCode 的中文用户，同时兼容 Windows、Linux 和 macOS。

## 版本对齐

- **当前中文发行版：** `v6.1.1-zh.1`
- **对齐的上游正式版：** [`obra/superpowers v6.1.1`](https://github.com/obra/superpowers/releases/tag/v6.1.1)
- **上游基线提交：** [`d884ae0`](https://github.com/obra/superpowers/commit/d884ae04edebef577e82ff7c4e143debd0bbec99)
- **对齐日期：** 2026-07-13

版本号中的 `zh.1` 表示：功能基线与上游 `v6.1.1` 对齐，这是该基线上的第 1 个中文发行版。后续同步新的上游版本时，会先更新前三段版本号，再从 `zh.1` 重新开始计数。

## 上游正在招聘

Superpowers 上游团队正在招聘一名全职工程师，协助社区运营与代码开发。

职位详情：https://primeradiant.com/jobs/superpowers-community-engineer/

如果你认识合适的人选，欢迎推荐给上游团队。

## 快速开始

为你的编程 Agent 安装 Superpowers 中文版：[Claude Code](#claude-code)、[Antigravity](#antigravity)、[Codex App](#codex-app)、[Codex CLI](#codex-cli)、[Cursor](#cursor)、[Factory Droid](#factory-droid)、[GitHub Copilot CLI](#github-copilot-cli)、[Kimi Code](#kimi-code)、[OpenCode](#opencode)、[Pi](#pi)。

## 工作原理

Superpowers 从你启动编程 Agent 的那一刻开始发挥作用。当 Agent 发现你准备构建某项功能时，它不会立刻埋头写代码，而是先退一步，询问你真正想解决的问题。

Agent 会通过对话逐步梳理出规格，并以便于阅读和确认的小段内容向你展示。

设计获批后，Agent 会编写一份足够清晰的实施计划：即使交给一名缺少项目背景、工程判断欠佳且不喜欢测试的初级工程师，也能据此完成任务。计划强调真正的红灯—绿灯 TDD、YAGNI（你不会需要它）和 DRY。

当你确认“开始”后，Agent 会启动由子 Agent 驱动的开发流程。不同 Agent 会依次完成各项工程任务，检查并审查彼此的工作，然后继续推进。只要计划足够清晰，Agent 连续自主工作数小时而不偏离目标并不罕见。

系统还包含更多细节，但以上就是核心流程。由于技能会自动触发，你不需要记忆特殊命令——安装后，你的编程 Agent 就拥有了 Superpowers。

## 商业服务

如果你在企业环境中使用 Superpowers，并需要商业支持、额外工具或托管式成本管理，可联系上游团队：sales@primeradiant.com。

## 安装

不同编程 Agent 的安装方式不同。如果你同时使用多个 Agent，需要分别安装。

### Claude Code

推荐直接注册本中文仓库提供的插件市场：

```bash
/plugin marketplace add AreChen/superpowers-zh
```

然后安装中文插件：

```bash
/plugin install superpowers@superpowers-dev
```

如果你希望安装上游英文版，也可以使用 [Claude 官方插件市场](https://claude.com/plugins/superpowers)：

```bash
/plugin install superpowers@claude-plugins-official
```

### Antigravity

直接从本仓库安装插件：

```bash
agy plugin install https://github.com/AreChen/superpowers-zh
```

Antigravity 会运行插件的会话启动钩子，因此 Superpowers 会从第一条消息起生效。更新时重新执行同一条命令即可。

### Codex App

先通过 Codex CLI 添加本项目的 Git 插件市场：

```bash
codex plugin marketplace add AreChen/superpowers-zh --ref main
```

然后：

1. 重启 Codex App。
2. 在侧边栏打开“插件”。
3. 选择 `Superpowers 中文版开发版` 市场。
4. 找到 `Superpowers 中文版`，点击旁边的 `+` 并按提示安装。

### Codex CLI

先添加本项目的插件市场：

```bash
codex plugin marketplace add AreChen/superpowers-zh --ref main
```

打开插件界面：

```text
/plugins
```

选择 `Superpowers 中文版开发版` 市场，搜索 `superpowers` 并安装插件。

查看已配置的市场：

```bash
codex plugin marketplace list
```

更新市场：

```bash
codex plugin marketplace upgrade superpowers-dev
```

### Cursor

在 Cursor Agent 对话中从插件市场安装：

```text
/add-plugin superpowers
```

也可以在插件市场中搜索 `superpowers`。请确认安装详情显示的是 `Superpowers 中文版`；如果只看到上游英文版，可改用本仓库的本地插件方式。

### Factory Droid

注册本中文仓库的插件市场：

```bash
droid plugin marketplace add https://github.com/AreChen/superpowers-zh
```

安装插件：

```bash
droid plugin install superpowers@superpowers-dev
```

### GitHub Copilot CLI

注册本中文仓库的插件市场：

```bash
copilot plugin marketplace add AreChen/superpowers-zh
```

安装插件：

```bash
copilot plugin install superpowers@superpowers-dev
```

### Kimi Code

可以直接从本中文仓库安装：

```text
/plugins install https://github.com/AreChen/superpowers-zh
```

也可以打开 Kimi Code 的插件管理器：

```text
/plugins
```

进入 `Marketplace`，搜索并安装 `Superpowers`。请在安装前确认插件描述为中文版本。

详细说明：[docs/README.kimi.md](docs/README.kimi.md)

### OpenCode

OpenCode 使用自己的插件安装机制。即使你已经在其他编程 Agent 中安装了 Superpowers，仍需为 OpenCode 单独安装。

在全局或项目级 `opencode.json` 的 `plugin` 数组中加入：

```json
{
  "plugin": [
    "superpowers@git+https://github.com/AreChen/superpowers-zh.git"
  ]
}
```

重启 OpenCode。插件会自动注册本项目中的全部技能，无需手动为技能目录创建符号链接。

也可以让 OpenCode 获取并遵循仓库内的安装说明：

```text
获取并遵循 https://raw.githubusercontent.com/AreChen/superpowers-zh/refs/heads/main/.opencode/INSTALL.md 中的说明
```

详细说明：[docs/README.opencode.md](docs/README.opencode.md)

### Pi

从本仓库安装为 Pi 软件包：

```bash
pi install git:github.com/AreChen/superpowers-zh
```

本地开发时，可以把当前检出目录作为临时软件包加载：

```bash
pi -e /path/to/superpowers-zh
```

Pi 软件包会加载 Superpowers 技能，并通过一个小型扩展在会话启动和上下文压缩后注入 `using-superpowers` 引导。Pi 原生支持技能，因此不需要兼容性的 `Skill` 工具。子 Agent 和任务列表工具仍可作为可选的 Pi 配套软件包使用。

## 基本工作流

1. **brainstorming** —— 在编写代码前触发。通过提问澄清初步想法、探索替代方案，分段展示设计供用户确认，并保存设计文档。

2. **using-git-worktrees** —— 设计获批后触发。在新分支上创建隔离工作区，完成项目初始化，并验证测试基线干净。

3. **writing-plans** —— 获得批准的设计后触发。把工作拆分为小型任务，每项任务通常需要 2–5 分钟，并包含准确的文件路径、完整代码和验证步骤。

4. **subagent-driven-development** 或 **executing-plans** —— 计划完成后触发。前者为每项任务派遣新的子 Agent，并进行规格符合性和代码质量两阶段审查；后者按批次执行，并在关键节点等待人工确认。

5. **test-driven-development** —— 实施期间触发。强制执行“红灯—绿灯—重构”：先写失败测试并确认失败，再编写最小实现并确认通过，然后提交。测试之前编写的生产代码需要删除并重新按 TDD 实现。

6. **requesting-code-review** —— 在任务之间触发。根据计划审查实现，按严重程度报告问题；严重问题会阻止继续推进。

7. **finishing-a-development-branch** —— 全部任务完成后触发。验证测试并提供合并、创建 PR、保留或丢弃分支等选项，最后清理 worktree。

**Agent 会在执行任何任务前检查是否存在相关技能。** 这些是必须遵循的工作流，而不是可选建议。

## 包含内容

### 技能库

**测试**

- **test-driven-development** —— 红灯—绿灯—重构循环，包含测试反模式参考。

**调试**

- **systematic-debugging** —— 四阶段根因分析流程，包含根因追踪、纵深防御和基于条件的等待技术。
- **verification-before-completion** —— 在声称完成前用证据确认问题确实已经解决。

**协作**

- **brainstorming** —— 通过苏格拉底式提问完善设计。
- **writing-plans** —— 编写详细实施计划。
- **executing-plans** —— 带检查点的分批执行。
- **dispatching-parallel-agents** —— 并行子 Agent 工作流。
- **requesting-code-review** —— 请求审查前的完整流程。
- **receiving-code-review** —— 理解并处理审查反馈。
- **using-git-worktrees** —— 使用隔离分支并行开发。
- **finishing-a-development-branch** —— 合并或创建 PR 的决策流程。
- **subagent-driven-development** —— 通过规格符合性和代码质量两阶段审查快速迭代。

**元技能**

- **writing-skills** —— 按最佳实践创建和测试新技能。
- **using-superpowers** —— 技能系统的入口和使用规则。

## 核心理念

- **测试驱动开发** —— 始终先写测试。
- **系统化优于临时应对** —— 遵循流程，不靠猜测。
- **降低复杂度** —— 把简单作为首要目标。
- **证据优于声明** —— 声称成功之前先验证。

参阅 [Superpowers 最初的发布公告](https://blog.fsck.com/2025/10/09/superpowers/)。

## 参与贡献

本项目跟随上游 Superpowers 的总体贡献原则。通常不接受随意新增技能；任何技能修改都必须能在项目支持的编程 Agent 和主要操作系统上正常工作。

1. Fork [AreChen/superpowers-zh](https://github.com/AreChen/superpowers-zh)。
2. 同步最新的 `main` 分支。
3. 为你的改动创建独立分支。
4. 创建或修改技能时，遵循 `writing-skills` 技能完成编写和测试。
5. 向 `main` 提交 PR，并完整填写 PR 模板。

技能行为测试使用 [superpowers-evals](https://github.com/prime-radiant-inc/superpowers-evals/) 中的 drill 评测框架，将其克隆到 `evals/` 后可按 `evals/README.md` 配置。插件基础设施测试位于 `tests/`，通过对应的 `run-*.sh` 或 `npm test` 运行。

完整指南见 [`skills/writing-skills/SKILL.md`](skills/writing-skills/SKILL.md)。

## 更新

Superpowers 的更新方式取决于你使用的编程 Agent。通过 Git 市场安装时，通常可以使用对应 Agent 的市场更新命令；通过仓库 URL 安装时，可重新执行安装命令或拉取最新的 `main` 分支。

## 许可证

本项目采用 MIT 许可证，详情见 [LICENSE](LICENSE)。

## Visual Companion 遥测

技能和插件通常不会向作者提供任何使用反馈，因此我们无法直接了解有多少人在使用 Superpowers。默认情况下，`brainstorming` 的可选 Visual Companion 会从 Prime Radiant 网站加载品牌图标，并附带当前 Superpowers 版本号。

该请求不包含你的项目、提示词或编程 Agent 的详细信息，也不会记录点击行为或你正在构建的内容。它只用于粗略了解使用人数和版本分布，并且完全可选。

如需关闭，请把环境变量 `SUPERPOWERS_DISABLE_TELEMETRY` 设置为任意真值。Superpowers 也会遵循 Claude Code 的 `DISABLE_TELEMETRY` 和 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 退出设置。

## 社区

Superpowers 由 [Jesse Vincent](https://blog.fsck.com) 和 [Prime Radiant](https://primeradiant.com) 团队创建。本中文分叉由 [AreChen](https://github.com/AreChen) 维护。

- **Discord**：[加入上游社区](https://discord.gg/35wsABTejz)，获取支持、提出问题并分享你使用 Superpowers 构建的项目。
- **问题反馈**：https://github.com/AreChen/superpowers-zh/issues
- **上游版本公告**：[订阅通知](https://primeradiant.com/superpowers/)
