# Superpowers v6.2.0 中文同步设计

**日期：** 2026-07-24

**状态：** 已获用户批准并通过规格说明复核

**中文仓库：** `AreChen/superpowers-zh`

**当前中文基线：** `v6.1.1-zh.1`（上游 `v6.1.1`，提交 `d884ae0`）

**目标上游基线：** `v6.2.0`，提交 `3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9`

## 目标

将 `obra/superpowers v6.2.0` 的全部功能和修复同步到中文分叉，在不改变上游技能行为的前提下更新中文技能、插件用户界面、顶层 README 与发行说明，发布 `v6.2.0-zh.1`。

## 用户与平台

主要用户是 Codex 和 OpenCode 用户，覆盖 Windows、Linux 与 macOS。同步不得削弱 Claude Code、Cursor、Kimi、Pi、Antigravity 和上游恢复的 Gemini CLI 支持；这些入口保持可安装、可解析和与上游功能等价。

## 同步策略

采用保留历史的合并策略：

1. 在隔离分支 `codex/sync-upstream-v6.2.0` 中添加或更新 `upstream` 远程，并获取带注释标签 `v6.2.0`。
2. 将上游标签合并到当前中文基线，而不是重新生成仓库或逐提交复制文件。
3. 冲突解决以“上游行为和结构优先、中文文案继续保留”为原则：脚本、测试接口、文件增删和技能流程采用 `v6.2.0`；用户可见说明重新翻译为简体中文。
4. 保留合并父提交，使后续版本能够继续按标签增量同步。

未采用的方案：

- 不把旧汉化提交重新变基到新标签；该方案会改写已发布历史，并放大 14 个技能的冲突。
- 不逐文件手工搬运上游变更；该方案容易漏掉脚本模式、权限、Hook 清单和测试夹具等非文档改动。

## 上游变更范围

`v6.1.1...v6.2.0` 包含 51 个提交。同步必须完整保留以下类别：

- 子 Agent 驱动开发按计划隔离 `.superpowers/sdd/<plan-basename>/`，计划结束后清理临时工作区。
- 复审修复轮恢复原实现 Agent，新增作用域化 `re-review-prompt.md`，最多五轮后交由控制器裁决。
- `testing-anti-patterns.md` 替换为正向规则文档 `writing-good-tests.md`，并补充可证伪性和 mutation check。
- 多个技能删除重复总结与劝服性段落，把必要约束移动到触发点或合理化表格。
- Windows SessionStart Hook 声明 `shell: "bash"`，由 Claude Code 解析到 Git Bash。
- 恢复 Gemini CLI 安装说明和 `gemini-tools.md` 工具映射。
- 修复 `find-polluter.sh` 的 `./` 前缀、`**/` 折叠和顶层测试匹配。
- Codex 打包脚本同时兼容 bsdtar 与 GNU tar，并固定归档元数据和文件模式。
- 同步相应测试、规格、计划和普通开发文档，普通开发文档保持上游英文原文。

## 中文化边界

### 必须翻译

- `skills/**/SKILL.md` 中新增或改变的自然语言。
- 技能目录内 Agent 会直接读取的参考文档和提示词，包括 `writing-good-tests.md`、`gemini-tools.md`、`re-review-prompt.md` 及发生变化的 SDD 提示词。
- 插件清单、插件安装说明、Hook/运行时引导中面向用户或 Agent 的自然语言。
- 顶层 `README.md`。
- `RELEASE-NOTES.md` 顶部新增的 `v6.2.0-zh.1` 中文发行条目。

### 保持上游原文或实现

- Shell、JavaScript、TypeScript 和 Python 代码的行为、函数名、命令参数与协议字段。
- 上游历史发行说明和普通开发文档；除非文本属于插件安装入口，否则不进行全仓库文档汉化。
- 代码示例、命令、文件名、工具名、固定协议值和测试所依赖的字面量。

### 翻译约束

- 保留 MUST、NEVER、HARD-GATE、红旗和合理化表格的约束强度，不弱化行为塑造。
- “Agent”“Codex”“OpenCode”“Skill/SKILL.md”等产品或协议名称按既有中文版术语处理；不得翻译命令名、工具名和路径。
- 通过 `eapil-llmapi-structured` 辅助翻译或审校时，使用 `reasoning_effort=max`，输出必须经过结构和术语人工复核后才能写入仓库。
- 新增 Gemini 支持是上游功能同步，不改变 Codex/OpenCode 作为中文版重点用户的定位。

## 版本与发行

以下版本字段统一改为 `6.2.0-zh.1`：

- `package.json`
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `.codex-plugin/plugin.json`
- `.cursor-plugin/plugin.json`
- `.kimi-plugin/plugin.json`
- `gemini-extension.json`

README 和发行说明必须同时记录：

- 中文版本：`v6.2.0-zh.1`
- 对齐上游：`obra/superpowers v6.2.0`
- 上游基线提交：`3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9`
- `zh.1` 表示 `v6.2.0` 基线上的第一个中文发行版。

验证通过后，将同步分支合并到 `main`，推送 `main`，创建并推送标签 `v6.2.0-zh.1`，最后发布同名 GitHub Release。不会向 `obra/superpowers` 创建 PR。

## 冲突与错误处理

- 合并冲突逐文件解决；不得批量选择 ours/theirs 后直接提交。
- 删除或改名的上游文件按上游结构处理；旧中文文件不能因翻译内容存在而继续残留。
- 任何脚本接口变化必须同步到调用方和测试，尤其是 SDD 的 plan 参数和 review-package 参数顺序。
- 翻译审计发现英文时，先判断其是否为协议字面量、代码示例或应保留的上游开发文档，再决定是否修改。
- 测试不得用简单 grep 证明技能行为；测试文字映射时，应断言稳定结构或中英文等价词，而不是强迫中文文档残留无意义的英文关键词。
- 当前基线中 Pi 和 Antigravity 映射测试仍断言英文关键词，已在中文版上稳定失败；同步时应吸收上游 `v6.2.0` 的测试范围调整，并使断言兼容中文版实际文案。
- Windows 运行 Shell 测试时显式把 `C:\Program Files\Git\bin` 放到 PATH 首位，避免误调用 PowerShell 安装目录内的同名 `bash.exe`。

## 验证设计

### 结构与版本

- 校验所有插件清单是合法 JSON，版本字段完全一致。
- 校验新增、删除和改名文件与上游 `v6.2.0` 一致，中文版允许的额外发行文档除外。
- 校验工作树无冲突标记、无意外未跟踪文件、无旧 `testing-anti-patterns.md` 残留。
- 扫描本次应翻译文件中的明显未翻译段落，同时维护协议字面量白名单。

### Windows / Git Bash

- Brainstorm server Node 测试。
- OpenCode 插件单元测试。
- SessionStart Hook 测试，包含 `shell: "bash"`。
- Codex marketplace 与打包测试。
- Kimi、Pi、Antigravity、Shell lint 和 `find-polluter.sh` 测试。

### Linux 兼容路径

- 在 WSL Debian 中运行 Shell 测试、Hook 测试、OpenCode 测试和 Codex GNU tar 打包测试。
- 通过上游确定性归档测试验证 GNU tar 与 bsdtar 分支；本地不能直接模拟 macOS 时，不声称运行过 macOS，只报告由上游跨平台测试和不变实现提供的兼容性证据。

### 技能一致性

- 检查所有 `SKILL.md` YAML 前置元数据及技能目录完整性。
- 对 SDD plan-scoped workspace、review-package、task-brief、五轮熔断和复审提示词运行上游确定性测试。
- 对 TDD 新文档运行路径引用检查，确保没有死链到 `testing-anti-patterns.md`。

## 验收标准

- 上游 `v6.2.0` 的 51 个提交在分支历史中可追溯，功能文件与测试变更无遗漏。
- 中文化严格限制在技能、插件用户界面、README 和新增中文发行说明。
- 所有版本入口报告 `6.2.0-zh.1`，README 与 Release Notes 明确写出官方对齐版本和完整基线提交。
- Codex、OpenCode 和 Windows 关键路径全部通过；Linux/WSL Shell 与 GNU tar 路径通过。
- 所有可在本地运行的确定性测试通过；无法本地验证的平台或外部 Agent 行为测试在发行说明中如实标注，不作推断性成功声明。
- 合并、推送、标签和 GitHub Release 均指向已验证的同一提交。
