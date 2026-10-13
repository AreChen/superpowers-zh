# OpenCode 版 Superpowers

在 [OpenCode.ai](https://opencode.ai) 中使用 Superpowers 的完整指南。

## 安装

OpenCode V2 要求使用 2.0.4 或更高版本。

### OpenCode V1

使用现有的 V1 插件配置：

```json
{
  "plugin": ["superpowers@git+https://github.com/AreChen/superpowers-zh.git"]
}
```

### OpenCode V2（2.0.4 或更高版本）

使用 V2 插件配置：

```json
{
  "plugins": ["superpowers@git+https://github.com/AreChen/superpowers-zh.git"]
}
```

本地安装 V2 时，请配置包含 `index.js` 的仓库目录。OpenCode 2.0.4 和
2.0.7 不接受在配置中直接指定 JavaScript 文件路径，但仍支持自动发现的插件符号链接。

重启 OpenCode。V2 使用 `opencode` 命令；也可能提供 `opencode2` 别名。
插件通过 OpenCode 的插件管理器安装，并注册全部技能。

可通过提问验证：“告诉我你的超能力”。

### 从旧的符号链接安装方式迁移（V1）

如果之前通过 `git clone` 和符号链接安装了 Superpowers，请移除旧配置：

```bash
# 移除旧符号链接
rm -f ~/.config/opencode/plugins/superpowers.js
rm -rf ~/.config/opencode/skills/superpowers

# 可选：移除克隆的仓库
rm -rf ~/.config/opencode/superpowers

# 如果曾为 superpowers 添加 skills.paths，请从 opencode.json 中移除它
```

然后按上方安装步骤操作。

## 使用

### 查找技能

使用 OpenCode 原生 `skill` 工具列出全部可用技能：

```
使用 skill 工具列出技能
```

### 加载技能

```
使用 skill 工具加载 brainstorming
```

### 个人技能

在 `~/.config/opencode/skills/` 中创建自己的技能：

```bash
mkdir -p ~/.config/opencode/skills/my-skill
```

创建 `~/.config/opencode/skills/my-skill/SKILL.md`：

```markdown
---
name: my-skill
description: 当[条件]时使用——[作用]
---

# 我的技能

[在此填写技能内容]
```

### 项目技能

在项目内的 `.opencode/skills/` 中创建项目专用技能。

**V2 技能优先级：** 项目技能 > 个人技能 > Superpowers 技能。在已测试的
V1 1.18.31 中，个人或项目技能与随附的 Superpowers 技能同名时，后者优先；
请为个人和项目技能使用不同名称。迁移不会改变这一行为。

## 更新

OpenCode 使用基于 Git 的包声明安装 Superpowers。某些 OpenCode 和 Bun
版本会在锁文件或缓存中固定解析出的 Git 依赖，因此重启不一定会获取最新提交。
如果更新没有生效，请清除 OpenCode 的包缓存或重新安装插件。

要固定特定版本，在包声明中添加标签或提交（V1 的 `plugin` 和 V2 的 `plugins` 使用相同格式）：

```json
{
  "plugin": ["superpowers@git+https://github.com/AreChen/superpowers-zh.git#v7.0.0-zh.1"]
}
```

上游从 `v6.4.1` 开始支持 V2。本中文分叉在 V2 上请固定到 `v7.0.0-zh.1`
或更高版本；`v6.3.0-zh.1` 及之前版本只能在 V1 上加载。

## 工作原理

插件通过各版本对应的 API 完成两件事：

1. **注册技能目录**，让 OpenCode 无需符号链接或手动配置就能发现全部 Superpowers 技能。
   - **V1：** 通过 `config` 钩子注入 `config.skills.paths`。
   - **V2：** 通过 `setup()` 调用 `ctx.skill.transform()`（V2 原生 API，上游已确认在运行时生效）。
2. **注入引导上下文**，使用对应版本的工具映射：V1 会话使用下方 V1 工具名，V2 会话使用 V2 工具名。
   - **V1：** 通过 `experimental.chat.messages.transform` 钩子。
   - **V2：** 通过对应的 `ctx.session.hook("context")`（上游已确认在运行时生效）。

控制器会话在临时模型上下文中接收 using-superpowers 引导。受委派的子会话
仍可访问原生技能，但不接收控制器引导。没有父会话的手动分叉保留控制器行为。
V2 原生上下文压缩保留早期用户消息时（默认的 `compaction.keep.tokens` 预算），
引导会像未压缩会话一样，插入检查点之前的第一条保留用户消息中。
压缩移除了全部用户消息时，插件会在检查点之后追加一条临时引导消息。
两种情况都不会改变已保存的历史记录。

会话查询失败时，插件在当前请求中保留引导，并在下次请求重试。
失败的查询不会被缓存为控制器分类结果。

### 工具映射

技能用动作描述需求，不绑定某个运行时的工具名。引导会将动作映射到当前 OpenCode 版本实际提供的工具。

**V1（`opencode` 1.x）：**

- “创建待办事项” / “标记待办完成” → `todowrite`
- `Subagent (general-purpose):` 模板 → 使用 `subagent_type: "general"` 的 `task` 工具（探索代码库时使用 `"explore"`）
- “调用技能” → OpenCode 原生 `skill` 工具
- “读取文件” → `read`
- “创建文件” / “编辑文件” / “删除文件” → `apply_patch`
- “运行 Shell 命令” → `bash`
- “搜索文件内容” / “按名称查找文件” → `grep`、`glob`
- “获取 URL” → `webfetch`

**V2（`opencode` 2.0.4 或更高版本；可能提供 `opencode2` 别名）：**

- “创建待办事项” → V2 没有待办工具；映射会要求模型改用 Markdown 文件（或运行平台的计划功能）跟踪计划
- `Subagent (general-purpose):` 模板 → 使用 `agent: "general"` 的 `subagent` 工具（或使用 `"explore"`）；传入 `sessionID` 继续已有子 Agent
- “调用技能” → OpenCode 原生 `skill` 工具
- “读取文件” → `read`
- “创建、编辑或删除文件” → 可用时使用带 `patchText` 的 `patch`；否则用 `write` 创建或覆盖文件、用 `edit` 定向修改、用 `shell` 删除
- “运行 Shell 命令” → `shell`（`command`、`workdir`、`timeout`、`background`）
- “搜索文件内容” / “按名称查找文件” → `grep`、`glob`
- “获取 URL” → `webfetch`
- “搜索网页” → `websearch`

简而言之，V2 将 `task` 改名为 `subagent`（Agent 名称从 `subagent_type`
移至 `agent`，再次调用时提供 `sessionID` 可继续），将 `apply_patch` 改为
`patch`、`bash` 改为 `shell`，并完全移除了待办工具。可用的文件修改工具
取决于所选模型：部分 GPT 模型 ID 可使用 `patch`，其他模型使用 `write` 和 `edit`。

（V1 列表由上游对照已安装的 OpenCode 1.18.x CLI 工具清单核实；
V2 列表由上游对照 OpenCode 2.0.4 和 2.0.7 的宿主接口契约核实。）

## 故障排查

### 插件未加载

**V1：** 检查 OpenCode 日志：

```
opencode run --print-logs "hello" 2>&1 | grep -i superpowers
```

**V2：** 插件在后台服务器中加载，`--print-logs` 只有配合 `--standalone` 才显示该服务器的日志：

```
opencode run --standalone --print-logs "hello" 2>&1 | grep -i superpowers
```

也可检查 `~/.local/share/opencode/log/opencode.log`，筛选 `role=server`。

同时确认 `opencode.json` 中的插件路径正确，并使用较新的 OpenCode 版本。

### Windows 安装问题

部分 Windows OpenCode 构建版本的上游安装程序在处理 Git 包声明时存在问题，
例如 `git+https` URL 的缓存路径问题，以及普通终端能运行 `git.exe`、Bun 却找不到它。
如果 OpenCode 无法安装插件，可尝试通过系统 npm 安装，再让 OpenCode 指向本地包：

```powershell
npm install superpowers@git+https://github.com/AreChen/superpowers-zh.git --prefix "$HOME\.config\opencode"
```

随后根据 OpenCode 版本，在 `opencode.json` 中使用已安装包的绝对路径。
OpenCode 不会展开 `~`；`~/...` 会被当作包名，而不是本地目录。

**V1：**

```json
{
  "plugin": ["C:\\Users\\<you>\\.config\\opencode\\node_modules\\superpowers"]
}
```

**V2（2.0.4 或更高版本）：**

```json
{
  "plugins": ["C:\\Users\\<you>\\.config\\opencode\\node_modules\\superpowers"]
}
```

### 找不到技能

1. 用 OpenCode 的 `skill` 工具列出可用技能。
2. 检查插件是否加载（见上文）。
3. 每个技能都必须有包含有效 YAML frontmatter 的 `SKILL.md`。

### 引导没有出现

- **V1：** 确认 OpenCode 版本支持 `experimental.chat.messages.transform` 钩子；修改配置后重启 OpenCode。
- **V2：** 插件使用 `ctx.session.hook("context")` 注入引导。通过 `opencode api get /api/plugin` 确认插件已加载；修改配置后运行 `opencode service restart`。也可能提供 `opencode2` 命令别名。

## 获取帮助

- 报告问题：https://github.com/obra/superpowers/issues
- 主文档：https://github.com/AreChen/superpowers-zh
- OpenCode V2 文档：https://opencode.ai/v2/docs/
- OpenCode V1 文档：https://opencode.ai/docs/
