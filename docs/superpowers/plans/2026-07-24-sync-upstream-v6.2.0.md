# Superpowers v6.2.0 中文同步实施计划

> **面向 Agent 型工作者：** 必需的子技能：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 来逐项任务实施此计划。步骤使用复选框（`- [ ]`）语法进行跟踪。

**目标：** 完整合并 `obra/superpowers v6.2.0`，将技能、插件用户界面和 README 同步为简体中文版，并发布与上游提交 `3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9` 对齐的 `v6.2.0-zh.1`。

**架构：** 先生成一个保留上游父提交的合并提交，再以小型提交逐组恢复和审校中文内容。脚本、测试、协议和文件结构直接继承上游；行为塑造文档以英文标签为语义基线，通过结构化翻译审计、行为场景和确定性测试验证中文等价性。

**技术栈：** Git、PowerShell 7、Git for Windows Bash、WSL Debian、Node.js、Shell、GitHub CLI、EAPIL `/v1/responses` 严格 JSON Schema（GPT-5.5，`reasoning.effort=max`）。

## 全局约束

- 只翻译 `skills/**`、插件面向用户或 Agent 的内容、顶层 `README.md` 和新增中文发行说明；普通开发文档保持上游英文。
- 主要用户是 Codex 和 OpenCode 用户，覆盖 Windows、Linux 与 macOS；不得削弱其他已存在的 Harness。
- 上游行为、文件增删、脚本接口、协议字段、命令、路径和测试字面量优先于旧版中文内容。
- EAPIL 结构化调用使用 `/v1/responses`、严格 JSON Schema、`model=gpt-5.5` 和 `reasoning: {"effort":"max"}`；不得把 API Key 写入日志或文件。
- Windows Shell 测试在命令前执行 `$env:PATH = "C:\Program Files\Git\bin;$env:PATH"`，确保调用 Git Bash 而不是 PowerShell 目录内的同名程序。
- 上游合并、技能组、插件与文档、发行准备分别提交；每次提交前运行 `rtk proxy git diff --check` 和该任务的定向测试。
- 不向 `obra/superpowers` 创建 PR；最终只合并并发布到 `AreChen/superpowers-zh`。

---

### 任务 1：获取并验证上游 v6.2.0

**文件：**

- 修改：Git 公共仓库配置中的 `upstream` 远程（没有工作树文件变化）
- 验证：上游带注释标签 `v6.2.0`

**接口：**

- 使用：当前分支 `codex/sync-upstream-v6.2.0`，当前中文基线 `c51f23a`
- 产出：本地标签 `v6.2.0`，剥离后的提交必须为 `3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9`

- [ ] **步骤 1：检查远程和当前工作树**

```powershell
rtk git status --short --branch
rtk git remote -v
rtk git worktree list
```

预期：当前分支为 `codex/sync-upstream-v6.2.0`，规格与计划提交之外没有工作区变化。

- [ ] **步骤 2：添加或校正上游远程**

```powershell
rtk git remote add upstream https://github.com/obra/superpowers.git
```

如果 `upstream` 已存在，则先用 `rtk git remote get-url upstream` 验证 URL；只有 URL 不一致时运行：

```powershell
rtk git remote set-url upstream https://github.com/obra/superpowers.git
```

- [ ] **步骤 3：获取标签并验证对象链**

```powershell
rtk git fetch upstream tag v6.2.0
rtk git rev-parse 'v6.2.0^{}'
rtk git show -s --format='%H %s' 'v6.2.0^{}'
```

预期：完整提交为 `3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9`，主题以 `Release v6.2.0` 开头。

- [ ] **步骤 4：核对增量范围**

```powershell
rtk git rev-list --count d884ae0..'v6.2.0^{}'
rtk git diff --name-status v6.1.1..v6.2.0
```

预期：51 个上游提交；文件清单包含 SDD、TDD、Windows Hook、Codex 打包、Gemini 和 `find-polluter.sh` 变更。

### 任务 2：创建上游合并提交

**文件：**

- 修改：上游 `v6.2.0` 比较清单中的全部文件
- 保留中文版：`README.md`、`RELEASE-NOTES.md`、插件清单的中文描述和 fork 专属插件安装文档
- 测试：`tests/hooks/test-session-start.sh`、`tests/systematic-debugging/test-find-polluter.sh`、`tests/codex/test-package-codex-plugin.sh`

**接口：**

- 使用：任务 1 验证过的 `v6.2.0` 标签
- 产出：双父提交 `chore: merge upstream v6.2.0`；工作树无冲突标记

- [ ] **步骤 1：启动非快进合并并记录冲突**

```powershell
rtk git merge --no-ff --no-commit v6.2.0
rtk git diff --name-only --diff-filter=U
```

预期：合并停在未提交状态；逐行保存冲突清单用于后续核对。

- [ ] **步骤 2：按文件职责解决冲突**

对脚本、测试、普通开发文档和发生结构变化的技能文件选用上游版本；对 `README.md`、`RELEASE-NOTES.md` 和已有中文插件描述保留中文版，再在后续任务补入上游增量。每处理完一个文件，就重新运行全仓库冲突标记扫描和未解决文件查询；所有文件处理完毕后统一暂存：

```powershell
rtk rg -n '^(<<<<<<<|=======|>>>>>>>)' . -g '!RELEASE-NOTES.md'
rtk git diff --name-only --diff-filter=U
rtk git add -A
```

处理 `skills/test-driven-development/` 时删除 `testing-anti-patterns.md` 并保留上游新增的 `writing-good-tests.md`。处理 SDD 时必须保留以下接口：

```text
sdd-workspace PLAN_FILE
task-brief PLAN_FILE TASK_NUMBER [OUTFILE]
review-package PLAN_FILE BASE HEAD [OUTFILE]
```

- [ ] **步骤 3：验证没有遗留冲突或旧文件**

```powershell
rtk git diff --name-only --diff-filter=U
rtk rg -n '^(<<<<<<<|=======|>>>>>>>)' . -g '!RELEASE-NOTES.md'
Test-Path skills\test-driven-development\testing-anti-patterns.md
Test-Path skills\test-driven-development\writing-good-tests.md
Test-Path skills\subagent-driven-development\re-review-prompt.md
```

预期：冲突清单和冲突标记搜索为空；旧测试反模式文件为 `False`，两个新增文件为 `True`。

- [ ] **步骤 4：运行合并层的定向测试**

```powershell
$env:PATH = "C:\Program Files\Git\bin;$env:PATH"
rtk bash tests/hooks/test-session-start.sh
rtk bash tests/systematic-debugging/test-find-polluter.sh
rtk bash tests/codex/test-package-codex-plugin.sh
```

预期：Hook、polluter 和 Codex 打包测试均退出 0。若中文映射测试因旧断言失败，只记录为任务 7 的 RED，不在此任务修改技能文案。

- [ ] **步骤 5：提交合并**

```powershell
rtk proxy git diff --check
rtk git commit -m "chore: merge upstream v6.2.0"
```

预期：提交有两个父提交，其中一个为上游 `3dcbd5c4...`。

### 任务 3：建立翻译审计与 RED 基线

**文件：**

- 创建：`docs/superpowers/evals/2026-07-24-v6.2.0-translation-audit.md`
- 读取：任务 4–7 列出的英文上游文件和待写中文文件
- 测试：EAPIL 严格 JSON 输出与行为场景

**接口：**

- 使用：`OPENAI_API_KEY` 环境变量和已配置的 EAPIL Base URL；上游源文件来自 `git show v6.2.0:<path>`
- 产出：每个行为域的 RED 证据、翻译审计记录和以下严格结果结构：

```json
{
  "file": "skills/example/SKILL.md",
  "semantically_equivalent": false,
  "missing_requirements": ["缺少的上游约束"],
  "weakened_requirements": ["被弱化的约束"],
  "terminology_issues": ["术语问题"],
  "unsafe_literal_changes": ["被错误翻译的命令或协议值"],
  "summary": "不超过 200 个字符的审计结论"
}
```

- [ ] **步骤 1：验证 EAPIL max 请求形状**

```powershell
rtk python "C:\Users\cmx27\.codex\plugins\cache\eapil-skill-market\eapil-llmapi-structured\0.1.0\skills\eapil-llmapi-structured\scripts\smoke_structured_output.py" --base-url $env:OPENAI_BASE_URL --model gpt-5.5 --endpoint responses --reasoning-effort max --api-key-env OPENAI_API_KEY --dry-run
```

预期：请求使用 `/responses`，正文包含 `"reasoning":{"effort":"max"}` 和严格 JSON Schema；输出不包含 API Key。

- [ ] **步骤 2：为四个高风险行为域编写 RED 场景**

在审计文件中写入以下场景及预期失败：

```text
SDD：第二份计划复用了第一份计划的 ledger；旧中文技能没有 plan-scoped workspace 和五轮熔断规则。
TDD：测试只 grep 提示词里的字符串；旧中文参考没有 observable behavior、independent expectation 和 mutation check。
Finishing：已通过的分支完成后显示“丢弃工作”；旧中文菜单仍允许主动提供破坏性选项。
Windows Hook：用户目录含括号且 Claude Code 由 PowerShell 启动；旧 Hook 没有 shell:bash 调度声明。
```

- [ ] **步骤 3：运行无 6.2.0 中文技能的对照**

对每个场景使用旧 `v6.1.1-zh.1` 中文技能运行至少 5 个全新上下文样本，记录选择、遗漏和逐字合理化说辞。若对照没有暴露对应缺口，记录“上游结构变化仍由确定性测试证明”，不得伪造行为失败。

- [ ] **步骤 4：提交 RED 证据**

```powershell
rtk git add docs/superpowers/evals/2026-07-24-v6.2.0-translation-audit.md
rtk proxy git diff --cached --check
rtk git commit -m "test(i18n): record v6.2.0 translation baselines"
```

### 任务 4：同步 SDD 生命周期与提示词中文翻译

**文件：**

- 修改：`skills/subagent-driven-development/SKILL.md`
- 修改：`skills/subagent-driven-development/implementer-prompt.md`
- 修改：`skills/subagent-driven-development/task-reviewer-prompt.md`
- 创建并翻译：`skills/subagent-driven-development/re-review-prompt.md`
- 保持上游实现：`skills/subagent-driven-development/scripts/sdd-workspace`
- 保持上游实现：`skills/subagent-driven-development/scripts/task-brief`
- 保持上游实现：`skills/subagent-driven-development/scripts/review-package`
- 测试：`tests/claude-code/test-sdd-workspace.sh`
- 测试：`tests/claude-code/test-subagent-driven-development.sh`

**接口：**

- 使用：任务 3 的 SDD RED 场景和上游 `v6.2.0` 英文文件
- 产出：中文技能明确 plan-scoped workspace、resume implementer、scoped re-review、五轮熔断和最终清理

- [ ] **步骤 1：翻译上游 SDD 文件**

逐段对照 `git show v6.2.0:<path>`。保留 `PLAN_FILE`、`BASE`、`HEAD`、`task-brief`、`review-package`、`.superpowers/sdd/<plan-basename>/`、模板占位符和代码围栏原样；自然语言翻译为简体中文。

- [ ] **步骤 2：运行结构化语义审计**

以英文源文和中文候选为输入调用 EAPIL `/v1/responses`，使用任务 3 Schema 和 `reasoning.effort=max`。只有 `semantically_equivalent=true` 且四个问题数组均为空时通过。

- [ ] **步骤 3：验证 GREEN 行为和脚本接口**

```powershell
$env:PATH = "C:\Program Files\Git\bin;$env:PATH"
rtk bash tests/claude-code/test-sdd-workspace.sh
rtk bash tests/claude-code/test-subagent-driven-development.sh
```

对任务 3 的 SDD 场景用中文技能运行至少 5 个新样本。预期：不读取其他计划 ledger；修复轮恢复同一实现 Agent；第五轮后控制器裁决；干净终审后删除计划工作区。

- [ ] **步骤 4：提交 SDD 翻译**

```powershell
rtk git add skills/subagent-driven-development tests/claude-code
rtk proxy git diff --cached --check
rtk git commit -m "feat(i18n): sync v6.2.0 SDD workflow"
```

### 任务 5：同步 TDD 与高质量测试指南

**文件：**

- 修改：`skills/test-driven-development/SKILL.md`
- 创建并翻译：`skills/test-driven-development/writing-good-tests.md`
- 删除：`skills/test-driven-development/testing-anti-patterns.md`

**接口：**

- 使用：任务 3 的 TDD RED 场景
- 产出：六条正向测试规则、可证伪性检查、独立期望值和 mutation check 的中文等价表达

- [ ] **步骤 1：翻译 TDD 上游增量和新参考**

保留 GOOD/BAD 标记、代码示例、API 名称和测试命令原样；把 “string-presence trap”“change-detector trap”“observable behavior”“mutation check”统一译为“字符串存在性陷阱”“变更检测器陷阱”“可观察行为”“变异检查”。

- [ ] **步骤 2：运行语义审计和 GREEN 微测试**

使用任务 3 Schema、`reasoning.effort=max` 审计两个文件。对 TDD 场景运行至少 5 个中文技能样本；预期拒绝用 grep/常量断言冒充行为测试，并能指出哪项生产变更会使测试失败。

- [ ] **步骤 3：检查引用和旧文件残留**

```powershell
rtk rg -n "testing-anti-patterns\.md" skills tests README.md
Test-Path skills\test-driven-development\testing-anti-patterns.md
Test-Path skills\test-driven-development\writing-good-tests.md
```

预期：没有死链；旧文件为 `False`，新文件为 `True`。

- [ ] **步骤 4：提交 TDD 翻译**

```powershell
rtk git add -A skills/test-driven-development
rtk proxy git diff --cached --check
rtk git commit -m "feat(i18n): sync v6.2.0 testing guidance"
```

### 任务 6：同步分支完成与工作树技能

**文件：**

- 修改：`skills/finishing-a-development-branch/SKILL.md`
- 修改：`skills/using-git-worktrees/SKILL.md`
- 测试：`tests/claude-code/test-worktree-native-preference.sh`
- 测试：`tests/claude-code/test-worktree-path-policy.sh`

**接口：**

- 使用：任务 3 的 Finishing RED 场景和上游工作树错误修复
- 产出：完成菜单不主动提供丢弃选项；显式丢弃仍要求输入分支名确认；清理前保存原工作树路径

- [ ] **步骤 1：翻译两个技能并保留命令字面量**

保留 `git merge --ff-only`、`git worktree remove`、`git branch -d`、typed confirmation、forge CLI 和 push URL 规则。合理化表格的每一行必须与上游一一对应。

- [ ] **步骤 2：运行语义审计和完成菜单 GREEN 测试**

EAPIL 审计必须返回等价。对任务 3 Finishing 场景运行至少 5 个新样本；预期默认选项中没有 discard，只有用户明确要求时才进入输入分支名确认流程。

- [ ] **步骤 3：运行工作树测试**

```powershell
$env:PATH = "C:\Program Files\Git\bin;$env:PATH"
rtk bash tests/claude-code/test-worktree-native-preference.sh
rtk bash tests/claude-code/test-worktree-path-policy.sh
```

- [ ] **步骤 4：提交分支工作流翻译**

```powershell
rtk git add skills/finishing-a-development-branch skills/using-git-worktrees tests/claude-code
rtk proxy git diff --cached --check
rtk git commit -m "feat(i18n): sync v6.2.0 branch workflows"
```

### 任务 7：逐个同步其余技能与 Harness 映射

**文件：**

- 修改：`skills/brainstorming/SKILL.md`
- 修改：`skills/brainstorming/visual-companion.md`
- 修改：`skills/dispatching-parallel-agents/SKILL.md`
- 修改：`skills/executing-plans/SKILL.md`
- 修改：`skills/receiving-code-review/SKILL.md`
- 修改：`skills/requesting-code-review/SKILL.md`
- 修改：`skills/systematic-debugging/SKILL.md`
- 修改：`skills/verification-before-completion/SKILL.md`
- 修改：`skills/writing-plans/SKILL.md`
- 修改：`skills/writing-skills/SKILL.md`
- 修改：`skills/using-superpowers/references/antigravity-tools.md`
- 修改：`skills/using-superpowers/references/codex-tools.md`
- 创建并翻译：`skills/using-superpowers/references/gemini-tools.md`
- 修改测试：`tests/antigravity/test-antigravity-tools.sh`
- 修改测试：`tests/pi/test-pi-extension.mjs`

**接口：**

- 使用：每个文件的上游 `v6.2.0` 版本
- 产出：压缩后的中文技能不保留上游已删除的总结段落；映射测试断言稳定表格结构和中英文等价操作名

- [ ] **步骤 1：按上方顺序逐个翻译技能**

每完成一个 `SKILL.md`，立即运行 EAPIL 等价审计并检查 YAML；当前文件通过后才进入下一个文件。纯删除总结段落的改动不添加新的中文总结。

- [ ] **步骤 2：翻译参考文件并恢复 Gemini 映射**

保留 Codex 工具名、Gemini 工具名、Antigravity 工具名和 Markdown 表格键不变，只翻译解释文本。`gemini-tools.md` 必须能从 `using-superpowers` 平台映射入口找到。

- [ ] **步骤 3：修复中文版映射测试的既有 RED**

Pi 与 Antigravity 测试断言表格中的稳定工具名和中文版动作，不再要求中文文档出现没有语义用途的英文 `Skill`、`read`、`write`、`edit`、`bash`。不得把英文关键词塞回文档来迁就测试。

- [ ] **步骤 4：逐项运行确定性测试**

```powershell
$env:PATH = "C:\Program Files\Git\bin;$env:PATH"
rtk bash tests/antigravity/run-tests.sh
rtk node tests/pi/test-pi-extension.mjs
rtk bash tests/claude-code/run-skill-tests.sh
```

若 `run-skill-tests.sh` 需要外部 Claude 凭据而当前环境不可用，记录明确的跳过原因，并运行其中所有不依赖外部模型的测试文件；不得报告整套测试通过。

- [ ] **步骤 5：提交剩余技能和映射**

```powershell
rtk git add skills tests/antigravity tests/pi
rtk proxy git diff --cached --check
rtk git commit -m "feat(i18n): sync remaining v6.2.0 skills"
```

### 任务 8：同步插件、README、版本和发行说明

**文件：**

- 修改：`README.md`
- 修改：`RELEASE-NOTES.md`
- 修改：`package.json`
- 修改：`.claude-plugin/plugin.json`
- 修改：`.claude-plugin/marketplace.json`
- 修改：`.codex-plugin/plugin.json`
- 修改：`.cursor-plugin/plugin.json`
- 修改：`.kimi-plugin/plugin.json`
- 修改：`gemini-extension.json`
- 修改：上游发生变化的插件安装说明和运行时用户提示

**接口：**

- 使用：上游 `README.md` 的 `v6.1.1..v6.2.0` 差异和任务 4–7 的最终功能
- 产出：所有发行入口版本 `6.2.0-zh.1`；README 和 Release Notes 写明上游标签与完整提交

- [ ] **步骤 1：把 README 的上游增量翻译并合入现有中文版**

保留中文版安装章节、Codex/OpenCode 优先说明和 Windows/Linux/macOS 命令；加入上游 v6.2.0 新增或恢复的 Gemini、Windows Hook 与相关安装信息。不得用上游英文 README 覆盖整份中文版。

- [ ] **步骤 2：统一七个版本字段**

将所有列出的 JSON 文件版本改为 `6.2.0-zh.1`，保留合法 JSON 和现有中文名称/描述。

- [ ] **步骤 3：新增中文发行说明**

在 `RELEASE-NOTES.md` 顶部加入 `v6.2.0-zh.1（2026-07-24）`，明确：

```text
对齐官方版本：obra/superpowers v6.2.0
上游基线提交：3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9
中文发行序号：zh.1
```

随后保留上游 `v6.2.0` 原始英文发布说明和既有历史。

- [ ] **步骤 4：验证 JSON、版本和插件入口**

```powershell
rtk node -e "for (const f of ['package.json','.claude-plugin/plugin.json','.claude-plugin/marketplace.json','.codex-plugin/plugin.json','.cursor-plugin/plugin.json','.kimi-plugin/plugin.json','gemini-extension.json']) JSON.parse(require('fs').readFileSync(f,'utf8')); console.log('json ok')"
rtk rg -n "6\.1\.1-zh\.1|v6\.1\.1|d884ae0" README.md package.json .claude-plugin .codex-plugin .cursor-plugin .kimi-plugin gemini-extension.json
rtk rg -n "6\.2\.0-zh\.1|3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9" README.md RELEASE-NOTES.md package.json .claude-plugin .codex-plugin .cursor-plugin .kimi-plugin gemini-extension.json
```

预期：JSON 解析成功；README 和当前版本字段没有旧中文版本；新版本和完整上游提交均可找到。

- [ ] **步骤 5：提交插件与发行文档**

```powershell
rtk git add README.md RELEASE-NOTES.md package.json .claude-plugin .codex-plugin .cursor-plugin .kimi-plugin gemini-extension.json .opencode
rtk proxy git diff --cached --check
rtk git commit -m "chore(release): prepare v6.2.0-zh.1"
```

### 任务 9：运行完整的跨平台验证

**文件：**

- 验证：整个工作树
- 不创建发行提交，除非测试适配确实需要修复并按 TDD 单独提交

**接口：**

- 使用：任务 2–8 的所有提交
- 产出：Windows/Git Bash 和 WSL/Linux 验证记录，零未解释失败

- [ ] **步骤 1：Windows / Git Bash 验证**

```powershell
$env:PATH = "C:\Program Files\Git\bin;$env:PATH"
rtk npm test --prefix tests/brainstorm-server
rtk bash tests/opencode/run-tests.sh
rtk bash tests/hooks/test-session-start.sh
rtk bash tests/codex/test-marketplace-manifest.sh
rtk bash tests/codex/test-package-codex-plugin.sh
rtk bash tests/kimi/run-tests.sh
rtk node tests/pi/test-pi-extension.mjs
rtk bash tests/antigravity/run-tests.sh
rtk bash tests/systematic-debugging/test-find-polluter.sh
rtk bash tests/shell-lint/test-lint-shell.sh
```

- [ ] **步骤 2：WSL Debian / GNU tar 验证**

```powershell
rtk wsl.exe -d Debian -- bash -lc "cd /mnt/e/Project/CodeProject/superpowers-zh/.worktrees/sync-upstream-v6.2.0 && bash tests/opencode/run-tests.sh && bash tests/hooks/test-session-start.sh && bash tests/codex/test-package-codex-plugin.sh && bash tests/systematic-debugging/test-find-polluter.sh"
```

预期：全部退出 0，并且 Codex 测试实际走 GNU tar 路径。

- [ ] **步骤 3：结构、翻译和 Git 审计**

```powershell
rtk proxy git diff --check main...HEAD
rtk rg -n '^(<<<<<<<|=======|>>>>>>>)' . -g '!RELEASE-NOTES.md'
rtk git status --short --branch
rtk git log --oneline --decorate main..HEAD
rtk git diff --stat main...HEAD
```

逐项核对设计规格的验收标准；英文扫描结果按“代码/协议字面量、普通上游开发文档、遗漏翻译”三类归档，只有第三类必须修复。

- [ ] **步骤 4：验证上游可追溯性和版本一致性**

```powershell
rtk git merge-base --is-ancestor 3dcbd5c4b48e02263fbf4a3c01e3fe4f81d584d9 HEAD
rtk git rev-list --parents -1 --grep="merge upstream v6.2.0"
rtk rg -n '"version": "6\.2\.0-zh\.1"' package.json .claude-plugin .codex-plugin .cursor-plugin .kimi-plugin gemini-extension.json
```

预期：上游提交是 HEAD 的祖先；合并提交有两个父提交；七个版本入口完全一致。

### 任务 10：完成分支、合并主分支并发布

**文件：**

- 修改：本地 `main` 分支引用、远程 `origin/main`、标签 `v6.2.0-zh.1` 和 GitHub Release
- 验证：任务 9 的最新完整输出

**接口：**

- 使用：通过全部门禁的 `codex/sync-upstream-v6.2.0` HEAD
- 产出：`origin/main`、标签和 Release 指向同一个已验证提交

- [ ] **步骤 1：使用 finishing-a-development-branch 做最终门禁**

重新运行任务 9 的关键测试和 `rtk git status --short --branch`；记录分支 HEAD。不得使用旧测试输出代替。

- [ ] **步骤 2：在主工作区快进合并**

```powershell
rtk git -C E:\Project\CodeProject\superpowers-zh status --short --branch
rtk git -C E:\Project\CodeProject\superpowers-zh merge --ff-only codex/sync-upstream-v6.2.0
```

预期：主工作区原本干净，`main` 快进到已验证 HEAD。

- [ ] **步骤 3：推送主分支并验证远程提交**

```powershell
rtk git -C E:\Project\CodeProject\superpowers-zh push origin main
rtk git -C E:\Project\CodeProject\superpowers-zh rev-parse HEAD
rtk git -C E:\Project\CodeProject\superpowers-zh ls-remote origin refs/heads/main
```

预期：本地与远程主分支 SHA 完全相同。

- [ ] **步骤 4：创建并推送发行标签**

```powershell
rtk git -C E:\Project\CodeProject\superpowers-zh tag -a v6.2.0-zh.1 -m "Superpowers 中文版 v6.2.0-zh.1"
rtk git -C E:\Project\CodeProject\superpowers-zh push origin v6.2.0-zh.1
```

- [ ] **步骤 5：创建 GitHub Release 并验证资源**

```powershell
$lines = Get-Content -LiteralPath E:\Project\CodeProject\superpowers-zh\RELEASE-NOTES.md
$start = [Array]::IndexOf($lines, '## v6.2.0-zh.1（2026-07-24）')
$next = (($start + 1)..($lines.Count - 1) | Where-Object { $lines[$_] -match '^## v' } | Select-Object -First 1)
if ($start -lt 0 -or $null -eq $next) { throw '无法定位 v6.2.0-zh.1 发行说明边界' }
$notes = ($lines[$start..($next - 1)] -join "`n")
rtk gh release create v6.2.0-zh.1 --repo AreChen/superpowers-zh --title "Superpowers 中文版 v6.2.0-zh.1" --notes $notes
rtk gh release view v6.2.0-zh.1 --repo AreChen/superpowers-zh --json tagName,name,url,targetCommitish,isDraft,isPrerelease
```

预期：从 `RELEASE-NOTES.md` 精确提取第一个发行小节，不创建临时文件；Release 非草稿、非预发行，标签名和标题正确。

- [ ] **步骤 6：最终一致性检查**

```powershell
rtk git -C E:\Project\CodeProject\superpowers-zh status --short --branch
rtk gh release view v6.2.0-zh.1 --repo AreChen/superpowers-zh --json url
```

预期：`main...origin/main` 无领先或落后，工作区干净，Release URL 可访问。
