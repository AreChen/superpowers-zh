# 可视化伴侣指南

基于浏览器的可视化头脑风暴伴侣，用于展示模型稿、图示和选项。

## 何时使用

针对每个问题而非每个会话进行决定。判断标准是：**用户通过看它而不是阅读它，是否能理解得更好？**

当内容本身是可视化内容时，**使用浏览器**：

- **UI 模型稿**——线框图、布局、导航结构、组件设计
- **架构图**——系统组件、数据流、关系图
- **并排视觉比较**——比较两种布局、两套配色方案、两个设计方向
- **设计润色**——当问题涉及观感、间距、视觉层级时
- **空间关系**——以图示形式呈现的状态机、流程图、实体关系

当内容是文本或表格时，**使用终端**：

- **需求和范围问题**——“X 是什么意思？”、“哪些功能在范围内？”
- **概念性 A/B/C 选择**——在用文字描述的方案之间进行选择
- **权衡清单**——优缺点、比较表
- **技术决策**——API 设计、数据建模、架构方案选择
- **澄清问题**——任何答案是文字而非视觉偏好的问题

一个*关于* UI 主题的问题并不自动等同于视觉问题。“你想要哪种向导？”是概念性问题——使用终端。“这些向导布局中，哪一种感觉合适？”是视觉问题——使用浏览器。

## 工作原理

服务器会监视一个目录中的 HTML 文件，并将最新的文件提供给浏览器。你将 HTML 内容写入 `screen_dir`，用户会在其浏览器中看到内容，并可通过点击选择选项。选择结果会记录到 `state_dir/events`，供你在下一轮读取。

**内容片段与完整文档：**如果你的 HTML 文件以 `<!DOCTYPE` 或 `<html` 开头，服务器会按原样提供该文件（仅注入辅助脚本）。否则，服务器会自动将你的内容包装在框架模板中——添加页眉、CSS 主题、连接状态以及所有交互基础设施。**默认编写内容片段。**仅在需要完全控制页面时编写完整文档。

## 启动会话

```bash
# 请在用户批准使用伴侣之后再启动。--open 会在显示首个屏幕时自动打开用户的浏览器；
# --project-dir 会持久保存模型稿，并支持使用同一端口重启。
scripts/start-server.sh --project-dir /path/to/project --open

# 返回：{"type":"server-started","port":52341,
#           "url":"http://localhost:52341/?key=ab12…",
#           "screen_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/content",
#           "state_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/state"}
```

保存响应中的 `screen_dir` 和 `state_dir`。使用 `--open` 时，当你推送首个屏幕，浏览器会自动打开——你不需要让用户手动打开，但仍应分享该 URL 作为备用方案（无头/远程环境不会自动打开）。

**该 URL 包含会话密钥（`?key=…`）。**服务器会拒绝任何不含该密钥的请求，因此始终向用户提供 `url` 字段中的**完整** URL——绝不要移除查询字符串，也绝不要提供不带查询字符串的 `http://host:port`。该密钥控制 HTTP 和 WebSocket 访问，因此意外打开的浏览器标签页或网络上的其他机器无法读取屏幕或注入事件。首次加载后，浏览器会通过 cookie 记住该密钥，因此重新加载以及访问 `/files/*` 资源时无需再次提供它。

**查找连接信息：**服务器会将其启动 JSON 写入 `$STATE_DIR/server-info`。如果你在后台启动了服务器但没有捕获 stdout，请读取该文件以获取 URL 和端口。使用 `--project-dir` 时，请在 `<project>/.superpowers/brainstorm/` 中查找会话目录。

**注意：**将项目根目录作为 `--project-dir` 传入，以便模型稿持久保存在 `.superpowers/brainstorm/` 中，并在服务器重启后继续保留。如果不这样做，文件会写入 `/tmp` 并被清理。如果 `.superpowers/` 尚未加入 `.gitignore`，请提醒用户添加它。

**按平台启动服务器：**

**Claude Code：**
```bash
# 默认模式即可——脚本会自行将服务器置于后台运行。
scripts/start-server.sh --project-dir /path/to/project --open
```

在 Windows 上，脚本会自动检测并切换到前台模式（这会阻塞工具调用）。在 Bash 工具调用中使用 `run_in_background: true`，使服务器能够跨对话轮次持续运行，然后在下一轮读取 `$STATE_DIR/server-info` 以获取 URL 和端口。

**Codex：**
```bash
# Codex 会清理后台进程。脚本会自动检测 CODEX_CI 并
# 切换到前台模式。正常运行即可——无需额外标志。
scripts/start-server.sh --project-dir /path/to/project --open
```

**Gemini CLI：**
```bash
# 使用 --foreground，并在 shell 工具调用中设置 is_background: true，
# 使进程能够跨轮次持续运行
scripts/start-server.sh --project-dir /path/to/project --open --foreground
```

**Copilot CLI：**
```bash
# 使用 --foreground，并通过 bash 工具以 mode: "async" 启动服务器，
# 使进程能够跨轮次持续运行。保存返回的 shellId，以便之后需要与其交互时
# 用于 read_bash / stop_bash。
scripts/start-server.sh --project-dir /path/to/project --open --foreground
```

**其他环境：**服务器必须在后台跨对话轮次持续运行。如果你的环境会清理已分离的进程，请使用 `--foreground`，并通过你所在平台的后台执行机制启动该命令。

如果你的浏览器无法访问该 URL（这在远程/容器化环境中很常见），请绑定非环回主机：

```bash
scripts/start-server.sh \
  --project-dir /path/to/project \
  --host 0.0.0.0 \
  --url-host localhost
```

使用 `--url-host` 控制返回的 URL JSON 中输出的主机名。

## 循环
1. **检查服务器是否仍在运行**，然后**将 HTML 写入** `screen_dir` 中的新文件：
   - **必需：在提及 URL 或推送界面之前，确认服务器仍在运行。** 检查 `$STATE_DIR/server-info` 是否存在，并且 `$STATE_DIR/server-stopped` 不存在。如果服务器已关闭，请使用**相同的 `--project-dir`** 通过 `start-server.sh` 重新启动它——它会复用相同的端口，因此用户已打开的标签页会自行重新连接（服务器停机期间会显示“已暂停”遮罩层），你无需发送新的 URL。服务器空闲 4 小时后会自动退出（可通过 `--idle-timeout-minutes` 配置）。
   - 使用语义化文件名：`platform.html`、`visual-style.html`、`layout.html`
   - **绝不要重复使用文件名**——每个界面都使用一个全新的文件
   - 使用你的文件创建工具——**绝不要使用 cat/heredoc**（会向终端倾倒大量杂乱信息）
   - 服务器会自动提供最新的文件

2. **告诉用户会看到什么，然后结束你的回合：**
   - 每一步都提醒他们 URL（而不只是第一步）
   - 简要概括界面上显示的内容（例如，“正在展示主页的 3 种布局选项”）
   - 请他们在终端中回复：“看一下，然后告诉我你的想法。如果愿意，请点击选择一个选项。”

3. **在你的下一个回合中**——用户在终端中回复后：
   - 如果 `$STATE_DIR/events` 存在，则读取它——其中以 JSON 行的形式包含用户的浏览器交互
   - 将其与用户的终端文本合并，以了解完整情况
   - 终端消息是主要反馈；`state_dir/events` 提供结构化交互数据

4. **迭代或推进**——如果反馈会改变当前界面，则写入一个新文件（例如 `layout-v2.html`）。只有当前步骤得到验证后，才能进入下一个问题。

5. **返回终端时卸载内容**——当下一步不需要浏览器时（例如，提出澄清问题、讨论权衡取舍），推送一个等待界面以清除过时内容：

   ```html
   <!-- 文件名：waiting.html（或 waiting-2.html 等） -->
   <div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
     <p class="subtitle">继续在终端中...</p>
   </div>
   ```

   这样可避免在对话已经继续推进后，用户仍盯着一个已经解决的选择。当下一个可视化问题出现时，像往常一样推送一个新的内容文件。

6. 重复上述步骤，直到完成。

## 编写内容片段

只编写放入页面内部的内容。服务器会自动使用框架模板将其包装起来（页眉、主题 CSS、连接状态以及所有交互基础设施）。

**最小示例：**

```html
<h2>哪种布局更合适？</h2>
<p class="subtitle">请考虑可读性和视觉层级</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>单栏</h3>
      <p>简洁、专注的阅读体验</p>
    </div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div>
    <div class="content">
      <h3>双栏</h3>
      <p>侧边栏导航搭配主内容区</p>
    </div>
  </div>
</div>
```

就这些。不需要 `<html>`、CSS，也不需要 `<script>` 标签。服务器会提供所有这些内容。

## 可用的 CSS 类
框架模板为你的内容提供以下 CSS 类：

### 选项（A/B/C 选择）

```html
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>标题</h3>
      <p>描述</p>
    </div>
  </div>
</div>
```

**多选：**向容器添加 `data-multiselect`，以允许用户选择多个选项。每次点击都会切换该项目的选中样式。

```html
<div class="options" data-multiselect>
  <!-- 相同的选项标记——用户可以选择/取消选择多个选项 -->
</div>
```

### 卡片（视觉设计）

```html
<div class="cards">
  <div class="card" data-choice="design1" onclick="toggleSelect(this)">
    <div class="card-image"><!-- 模型内容 --></div>
    <div class="card-body">
      <h3>名称</h3>
      <p>描述</p>
    </div>
  </div>
</div>
```

### 模型容器
```html
<div class="mockup">
  <div class="mockup-header">预览：仪表板布局</div>
  <div class="mockup-body"><!-- 你的样稿 HTML --></div>
</div>
```

### 拆分视图（并排）

```html
<div class="split">
  <div class="mockup"><!-- 左侧 --></div>
  <div class="mockup"><!-- 右侧 --></div>
</div>
```

### 优点/缺点

```html
<div class="pros-cons">
  <div class="pros"><h4>优点</h4><ul><li>益处</li></ul></div>
  <div class="cons"><h4>缺点</h4><ul><li>弊端</li></ul></div>
</div>
```

### 样稿元素（线框图构建块）

```html
<div class="mock-nav">徽标 | 首页 | 关于 | 联系</div>
<div style="display: flex;">
  <div class="mock-sidebar">导航</div>
  <div class="mock-content">主要内容区域</div>
</div>
<button class="mock-button">操作按钮</button>
<input class="mock-input" placeholder="输入字段">
<div class="placeholder">占位区域</div>
```

### 排版与分区
- `h2` — 页面标题
- `h3` — 小节标题
- `.subtitle` — 标题下方的次要文本
- `.section` — 带底部外边距的内容块
- `.label` — 小号全大写标签文本

## 浏览器事件格式

当用户在浏览器中点击选项时，其交互会被记录到 `$STATE_DIR/events`（每行一个 JSON 对象）。当你推送新屏幕时，该文件会自动清空。

```jsonl
{"type":"click","choice":"a","text":"选项 A - 简单布局","timestamp":1706000101}
{"type":"click","choice":"c","text":"选项 C - 复杂网格","timestamp":1706000108}
{"type":"click","choice":"b","text":"选项 B - 混合布局","timestamp":1706000115}
```

完整的事件流会显示用户的探索路径——他们可能会先点击多个选项，再最终确定。最后一个 `choice` 事件通常是最终选择，但点击模式可能会体现出犹豫或偏好，值得进一步询问。

如果 `$STATE_DIR/events` 不存在，则说明用户没有与浏览器交互——仅使用他们在终端中输入的文本。

## 设计技巧

- **根据问题调整保真度**——布局问题使用线框图，细节打磨问题使用精细设计
- **在每个页面上说明问题**——使用“哪个布局感觉更专业？”，而不只是“选择一个”
- **先迭代，再继续推进**——如果反馈会改变当前屏幕，请编写一个新版本
- 每个屏幕最多提供 **2-4 个选项**
- **在真实内容很重要时使用真实内容**——对于摄影作品集，应使用真实图片（Unsplash）。占位内容会掩盖设计问题。
- **保持模型简单**——专注于布局和结构，而不是像素级完美的设计

## 文件命名

- 使用语义化名称：`platform.html`、`visual-style.html`、`layout.html`
- 切勿重复使用文件名——每个屏幕都必须是一个新文件
- 对于迭代版本：附加版本后缀，例如 `layout-v2.html`、`layout-v3.html`
- 服务器按修改时间提供最新的文件

## 清理

```bash
scripts/stop-server.sh $SESSION_DIR
```

如果会话使用了 `--project-dir`，模型文件会保留在 `.superpowers/brainstorm/` 中，以供后续参考。只有 `/tmp` 中的会话会在停止时被删除。

## 参考

- 框架模板（CSS 参考）：`scripts/frame-template.html`
- 辅助脚本（客户端）：`scripts/helper.js`
