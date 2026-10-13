<a id="installing-superpowers-for-opencode"></a>

# 为 OpenCode 安装 Superpowers

<a id="prerequisites"></a>

## 前提条件

- 已安装 [OpenCode.ai](https://opencode.ai)

<a id="installation"></a>

## 安装

OpenCode V2 要求使用 2.0.4 或更高版本。

### OpenCode V1

使用现有的 V1 插件配置：

```json
{
  "plugin": ["superpowers@git+https://github.com/AreChen/superpowers-zh.git"]
}
```

<a id="opencode-v2-204-or-later"></a>

### OpenCode V2（2.0.4 或更高版本）

使用 V2 插件配置：

```json
{
  "plugins": ["superpowers@git+https://github.com/AreChen/superpowers-zh.git"]
}
```

对于 V2 的本地安装，请配置包含 `index.js` 的仓库目录。
OpenCode 2.0.4 和 2.0.7 不接受在配置中直接指定 JavaScript 文件路径。
仍支持发现的插件符号链接。

重启 OpenCode。V2 使用 `opencode` 命令；`opencode2` 可能作为别名提供。
插件通过 OpenCode 的插件管理器安装，并注册所有技能。

通过提问来验证：“告诉我你的超能力”

OpenCode 使用自己的插件安装机制。如果你还使用 Claude Code、Codex 或
其他运行框架，请为每个运行框架分别安装 Superpowers。

<a id="migrating-from-the-old-symlink-based-install"></a>

## 从旧的基于符号链接的安装方式迁移

如果你之前使用 `git clone` 和符号链接安装了 superpowers，请移除旧配置：

```bash
# 移除旧的符号链接
rm -f ~/.config/opencode/plugins/superpowers.js
rm -rf ~/.config/opencode/skills/superpowers

# 可选：移除克隆的仓库
rm -rf ~/.config/opencode/superpowers

# 如果你曾为 superpowers 添加 skills.paths，请从 opencode.json 中移除它
```

然后按照上面的安装步骤操作。

<a id="usage"></a>

## 使用

使用 OpenCode 的原生 `skill` 工具：

```
使用 skill 工具列出技能
使用 skill 工具加载 brainstorming
```

<a id="updating"></a>

## 更新

OpenCode 通过基于 git 的包规格说明安装 Superpowers。某些 OpenCode 和 Bun
版本会在锁文件或缓存中固定已解析的 git 依赖，因此重启可能不会获取
Superpowers 的最新提交。如果更新没有出现，请清除 OpenCode 的包缓存或重新安装插件。

要固定到特定版本，请在规格说明中添加标签或提交（V1 的 `plugin` 键和
V2 的 `plugins` 键使用相同格式）：

```json
{
  "plugin": ["superpowers@git+https://github.com/AreChen/superpowers-zh.git#v7.0.0-zh.1"]
}
```

上游从 `v6.4.1` 开始支持 V2。本中文分叉在 V2 上请固定到 `v7.0.0-zh.1` 或更高版本；`v6.3.0-zh.1` 及更早的版本只能在 V1 上加载。

<a id="troubleshooting"></a>

## 故障排查

<a id="plugin-not-loading"></a>

### 插件未加载

1. 检查日志。V1：`opencode run --print-logs "hello" 2>&1 | grep -i superpowers`。
   V2 在后台服务器中加载插件，因此需要添加 `--standalone`：
   `opencode run --standalone --print-logs "hello" 2>&1 | grep -i superpowers`，
   或检查 `~/.local/share/opencode/log/opencode.log`，筛选 `role=server`。
2. 核实 `opencode.json` 中的插件配置行
3. 确保你运行的是较新的 OpenCode 版本

<a id="windows-install-issues"></a>

### Windows 安装问题

某些 Windows OpenCode 构建版本的上游安装程序在处理基于 git 的插件规格说明时存在问题，
包括 `git+https` URL 的缓存路径问题，以及即使 `git.exe` 在普通终端中正常工作，
Bun 仍无法找到它的问题。如果 OpenCode 无法安装插件，请尝试使用系统 npm 安装，
并让 OpenCode 指向本地包：

```powershell
npm install superpowers@git+https://github.com/AreChen/superpowers-zh.git --prefix "$HOME\.config\opencode"
```

然后，根据你的 OpenCode 版本，在 `opencode.json` 中使用已安装包的绝对路径。
OpenCode 不会展开 `~`；`~/...` 条目会被视为包名，而不是本地目录。

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

<a id="skills-not-found"></a>

### 找不到技能

1. 使用 `skill` 工具列出已发现的技能
2. 检查插件是否正在加载（见上文）

<a id="tool-mapping"></a>

### 工具映射

技能以动作来描述操作（“创建待办事项”、“派发子 Agent”、“读取文件”）。插件会注入针对不同版本的映射——请确认你的 OpenCode 版本：

**V1（`opencode` 1.x）：**

- “创建待办事项” / “在待办列表中标记为已完成” → `todowrite`
- `Subagent (general-purpose):` 模板 → 使用 `subagent_type: "general"` 的 `task` 工具（探索代码库时使用 `"explore"`）
- “调用技能” → OpenCode 的原生 `skill` 工具
- “读取文件” → `read`
- “创建文件” / “编辑文件” / “删除文件” → `apply_patch`
- “运行 shell 命令” → `bash`
- “搜索文件内容” / “按名称查找文件” → `grep`、`glob`
- “获取 URL” → `webfetch`

**V2（`opencode` 2.0.4 或更高版本；`opencode2` 可能作为别名提供）：**

- “创建待办事项” → V2 没有待办工具；改用 markdown 文件跟踪计划
- `Subagent (general-purpose):` 模板 → 使用 `agent: "general"` 的 `subagent` 工具（或使用 `"explore"`）；传入 `sessionID` 以继续之前的子 Agent
- “调用技能” → OpenCode 的原生 `skill` 工具
- “读取文件” → `read`
- “创建、编辑或删除文件” → 可用时，使用带有 `patchText` 的 `patch`；否则，使用 `write` 创建或覆盖文件，使用 `edit` 进行定点修改，并使用 `shell` 删除文件
- “运行 shell 命令” → `shell`（`command`、`workdir`、`timeout`、`background`）
- “搜索文件内容” / “按名称查找文件” → `grep`、`glob`
- “获取 URL” → `webfetch`
- “搜索网页” → `websearch`

<a id="getting-help"></a>

## 获取帮助

- 报告问题：https://github.com/obra/superpowers/issues
- 完整文档：https://github.com/AreChen/superpowers-zh/blob/main/docs/README.opencode.md
