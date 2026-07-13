# 技能编写最佳实践

> 了解如何编写高效的技能，让 Agent 能够发现并成功使用它们。

优秀的技能简洁、结构清晰，并经过真实使用场景的测试。本指南提供实用的编写决策建议，帮助你编写 Agent 能够发现并有效使用的技能。

有关技能工作原理的概念背景，请参阅[技能概述](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)。

## 核心原则

### 简洁是关键

[上下文窗口](https://platform.claude.com/docs/en/build-with-claude/context-windows)是一种公共资源。你的技能与 Agent 需要了解的其他所有内容共享上下文窗口，包括：

* 系统提示词
* 对话历史
* 其他技能的元数据
* 你的实际请求

技能中的每个 token 并不都会立即产生开销。启动时，只会预加载所有技能的元数据（name 和 description）。只有当技能变得相关时，Agent 才会读取 SKILL.md，并且仅在需要时读取其他文件。不过，保持 SKILL.md 简洁仍然很重要：一旦 Agent 加载它，其中的每个 token 都会与对话历史及其他上下文争夺空间。

**默认假设**：Agent 已经非常聪明

只添加 Agent 尚不了解的上下文。审视每一条信息：

* “Agent 真的需要这段解释吗？”
* “我可以假设 Agent 已经知道这一点吗？”
* “这段内容值得占用这些 token 吗？”

**好的示例：简洁**（约 50 个 token）：

````markdown  theme={null}
## 提取 PDF 文本

使用 pdfplumber 提取文本：

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

**不好的示例：过于冗长**（约 150 个 token）：

```markdown  theme={null}
## 提取 PDF 文本

PDF（便携式文档格式）文件是一种常见的文件格式，其中包含
文本、图像和其他内容。要从 PDF 中提取文本，你需要使用一个库。
有许多可用于处理 PDF 的库，但我们推荐 pdfplumber，
因为它易于使用，并且能很好地处理大多数情况。
首先，你需要使用 pip 安装它。然后，可以使用下面的代码...
```

简洁版本假设 Agent 知道 PDF 是什么，也知道库如何工作。

### 设置适当的自由度
具体程度应与任务的脆弱性和可变性相匹配。

**高自由度**（基于文本的指令）：

适用于：

* 存在多种有效方法
* 决策取决于上下文
* 使用启发式方法来指导处理方式

示例：

```markdown  theme={null}
## 代码审查流程

1. 分析代码的结构和组织方式
2. 检查潜在的错误或边界情况
3. 提出可读性和可维护性方面的改进建议
4. 验证是否遵循项目约定
```

**中等自由度**（伪代码或带参数的脚本）：

适用于：

* 存在首选模式
* 可以接受一定程度的变化
* 配置会影响行为

示例：

````markdown  theme={null}
## 生成报告

使用此模板，并根据需要进行自定义：

```python
def generate_report(data, format="markdown", include_charts=True):
    # 处理数据
    # 以指定格式生成输出
    # 可选择包含可视化内容
```
````

**低自由度**（具体脚本，参数很少或没有参数）：

适用于：

* 操作较为脆弱且容易出错
* 一致性至关重要
* 必须遵循特定顺序

示例：

````markdown  theme={null}
## 数据库迁移

严格运行此脚本：

```bash
python scripts/migrate.py --verify --backup
```

不要修改该命令，也不要添加其他标志。
````

**类比**：将 Agent 想象成一个正在探索路径的机器人：

* **两侧都是悬崖的狭窄桥梁**：只有一种安全的前进方式。提供具体的约束措施和精确的指令（低自由度）。示例：必须严格按指定顺序运行的数据库迁移。
* **没有危险的开阔地带**：多条路径都能通向成功。给出总体方向，并相信 Agent 能找到最佳路线（高自由度）。示例：由上下文决定最佳方法的代码审查。

### 使用你计划采用的所有模型进行测试
技能是对模型能力的扩展，因此其有效性取决于底层模型。请使用你计划与该技能搭配使用的所有模型来测试它。

**针对不同模型的测试注意事项**：

* **Claude Haiku**（快速、经济实惠）：技能是否提供了足够的指导？
* **Claude Sonnet**（均衡）：技能是否清晰且高效？
* **Claude Opus**（推理能力强大）：技能是否避免了过度解释？

对 Opus 完美适用的内容，可能需要为 Haiku 提供更多细节。如果你计划跨多个模型使用技能，应以编写能在所有这些模型上良好运作的指令为目标。

## 技能结构

<Note>
  **YAML 前置元数据**：SKILL.md 的前置元数据需要包含两个字段：

  * `name` - 技能的易读名称（最多 64 个字符）
  * `description` - 用一行描述技能的作用以及何时使用它（最多 1024 个字符）

  有关技能结构的完整详情，请参阅[技能概览](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#skill-structure)。
</Note>

### 命名约定

使用一致的命名模式，让技能更易于引用和讨论。我们建议技能名称采用**动名词形式**（动词 + -ing），因为这种形式能够清楚地描述技能提供的活动或能力。

**良好的命名示例（动名词形式）**：

* "处理 PDF"
* "分析电子表格"
* "管理数据库"
* "测试代码"
* "编写文档"

**可接受的替代形式**：

* 名词短语："PDF 处理"、"电子表格分析"
* 动作导向型："处理 PDF"、"分析电子表格"

**避免**：

* 含义模糊的名称："助手"、"实用工具"、"工具"
* 过于宽泛的名称："文档"、"数据"、"文件"
* 技能集合中的命名模式不一致

一致的命名有助于：

* 在文档和对话中引用技能
* 一目了然地了解技能的作用
* 组织和搜索多个技能
* 维护专业且风格统一的技能库

### 编写有效的描述
`description` 字段支持技能发现，应同时包含技能的作用及其适用时机。

<Warning>
  **始终使用第三人称编写**。描述会被注入系统提示词，而不一致的叙述视角可能会导致发现问题。

  * **推荐：**“处理 Excel 文件并生成报告”
  * **避免：**“我可以帮助你处理 Excel 文件”
  * **避免：**“你可以使用此技能处理 Excel 文件”
</Warning>

**应具体明确，并包含关键术语**。既要说明技能的作用，也要包含应在何时使用该技能的具体触发条件或上下文。

每个技能都只有一个 description 字段。描述对于技能选择至关重要：Agent 会使用它从可能多达 100+ 个可用技能中选择正确的技能。你的描述必须提供足够的细节，让 Agent 知道何时应选择此技能，而 SKILL.md 的其余部分则提供实现细节。

有效示例：

**PDF 处理技能：**

```yaml  theme={null}
description: 从 PDF 文件中提取文本和表格、填写表单、合并文档。在处理 PDF 文件时，或当用户提到 PDF、表单或文档提取时使用。
```

**Excel 分析技能：**

```yaml  theme={null}
description: 分析 Excel 电子表格、创建数据透视表、生成图表。在分析 Excel 文件、电子表格、表格数据或 .xlsx 文件时使用。
```

**Git 提交辅助技能：**

```yaml  theme={null}
description: 通过分析 git diff 生成描述性提交消息。当用户请求帮助编写提交消息或审查已暂存的更改时使用。
```

避免使用如下含糊的描述：

```yaml  theme={null}
description: 帮助处理文档
```

```yaml  theme={null}
description: 处理数据
```

```yaml  theme={null}
description: 对文件做些事情
```

### 渐进式披露模式
SKILL.md 作为概览，像入门指南中的目录一样，根据需要将 Agent 引导至详细资料。有关渐进式披露工作原理的说明，请参阅概览中的[技能如何工作](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work)。

**实用指南：**

* 为获得最佳性能，请将 SKILL.md 正文控制在 500 行以内
* 接近此限制时，将内容拆分到单独文件中
* 使用下列模式有效组织说明、代码和资源

#### 可视化概览：从简单到复杂

一个基础技能起初只包含一个由元数据和说明组成的 SKILL.md 文件：

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=87782ff239b297d9a9e8e1b72ed72db9" alt="显示 YAML 前置元数据和 Markdown 正文的简单 SKILL.md 文件" data-og-width="2048" width="2048" data-og-height="1153" height="1153" data-path="images/agent-skills-simple-file.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=c61cc33b6f5855809907f7fda94cd80e 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=90d2c0c1c76b36e8d485f49e0810dbfd 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=ad17d231ac7b0bea7e5b4d58fb4aeabb 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=f5d0a7a3c668435bb0aee9a3a8f8c329 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=0e927c1af9de5799cfe557d12249f6e6 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=46bbb1a51dd4c8202a470ac8c80a893d 2500w" />

随着你的技能不断扩展，你可以将其他内容一并打包，Agent 仅在需要时加载这些内容：

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=a5e0aa41e3d53985a7e3e43668a33ea3" alt="将 reference.md 和 forms.md 等其他参考文件打包在一起。" data-og-width="2048" width="2048" data-og-height="1327" height="1327" data-path="images/agent-skills-bundling-content.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=f8a0e73783e99b4a643d79eac86b70a2 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=dc510a2a9d3f14359416b706f067904a 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=82cd6286c966303f7dd914c28170e385 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=56f3be36c77e4fe4b523df209a6824c6 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=d22b5161b2075656417d56f41a74f3dd 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=3dd4bdd6850ffcc96c6c45fcb0acd6eb 2500w" />

完整的技能目录结构可能如下：

```
pdf/
├── SKILL.md              # 主要说明（触发时加载）
├── FORMS.md              # 表单填写指南（按需加载）
├── reference.md          # API 参考（按需加载）
├── examples.md           # 使用示例（按需加载）
└── scripts/
    ├── analyze_form.py   # 实用工具脚本（执行，而非加载）
    ├── fill_form.py      # 表单填写脚本
    └── validate.py       # 验证脚本
```

#### 模式 1：带参考资料的高层指南

````markdown  theme={null}
---
name: PDF 处理
description: 从 PDF 文件中提取文本和表格、填写表单并合并文档。在处理 PDF 文件时，或当用户提及 PDF、表单或文档提取时使用。
---

# PDF 处理

## 快速开始

使用 pdfplumber 提取文本：
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## 高级功能

**表单填写**：完整指南请参阅 [FORMS.md](FORMS.md)
**API 参考**：所有方法请参阅 [REFERENCE.md](REFERENCE.md)
**示例**：常见模式请参阅 [EXAMPLES.md](EXAMPLES.md)
````

Agent 仅在需要时加载 FORMS.md、REFERENCE.md 或 EXAMPLES.md。

#### 模式 2：针对特定领域进行组织
对于涵盖多个领域的技能，应按领域组织内容，以免加载无关上下文。当用户询问销售指标时，Agent 只需读取与销售相关的 schema，而不需要读取财务或营销数据。这样可以降低 token 使用量，并让上下文保持聚焦。

```
bigquery-skill/
├── SKILL.md（概览和导航）
└── reference/
    ├── finance.md（收入、计费指标）
    ├── sales.md（销售机会、销售管道）
    ├── product.md（API 使用情况、功能）
    └── marketing.md（营销活动、归因）
```

````markdown SKILL.md theme={null}
# BigQuery 数据分析

## 可用数据集

**财务**：收入、ARR、计费 → 参见 [reference/finance.md](reference/finance.md)
**销售**：销售机会、销售管道、账户 → 参见 [reference/sales.md](reference/sales.md)
**产品**：API 使用情况、功能、采用情况 → 参见 [reference/product.md](reference/product.md)
**营销**：营销活动、归因、电子邮件 → 参见 [reference/marketing.md](reference/marketing.md)

## 快速搜索

使用 grep 查找特定指标：

```bash
grep -i "revenue" reference/finance.md
grep -i "pipeline" reference/sales.md
grep -i "api usage" reference/product.md
```
````

#### 模式 3：条件式详细信息

展示基础内容，并链接到高级内容：

```markdown  theme={null}
# DOCX 处理

## 创建文档

使用 docx-js 创建新文档。参见 [DOCX-JS.md](DOCX-JS.md)。

## 编辑文档

对于简单编辑，直接修改 XML。

**对于跟踪更改**：参见 [REDLINING.md](REDLINING.md)
**有关 OOXML 的详细信息**：参见 [OOXML.md](OOXML.md)
```

仅当用户需要这些功能时，Agent 才会读取 REDLINING.md 或 OOXML.md。

### 避免引用层级嵌套过深
当某个文件由另一个已被引用的文件引用时，Agent 可能只会读取该文件的一部分。遇到嵌套引用时，Agent 可能会使用 `head -100` 等命令预览内容，而不是读取整个文件，从而导致获取的信息不完整。

**确保引用与 SKILL.md 之间仅有一层**。SKILL.md 应直接链接到所有参考文件，以确保 Agent 在需要时读取完整文件。

**反例：层级过深**：

```markdown  theme={null}
# SKILL.md
请参阅 [advanced.md](advanced.md)...

# advanced.md
请参阅 [details.md](details.md)...

# details.md
实际信息如下...
```

**正例：仅一层**：

```markdown  theme={null}
# SKILL.md

**基本用法**：[SKILL.md 中的说明]
**高级功能**：请参阅 [advanced.md](advanced.md)
**API 参考文档**：请参阅 [reference.md](reference.md)
**示例**：请参阅 [examples.md](examples.md)
```

### 使用目录组织较长的参考文件

对于超过 100 行的参考文件，请在顶部加入目录。这样即使 Agent 只预览部分内容，也能看到可用信息的完整范围。

**示例**：

```markdown  theme={null}
# API 参考文档

## 目录
- 身份验证与设置
- 核心方法（创建、读取、更新、删除）
- 高级功能（批量操作、webhook）
- 错误处理模式
- 代码示例

## 身份验证与设置
...

## 核心方法
...
```

这样，Agent 就可以根据需要读取完整文件或跳转到特定章节。

有关这种基于文件系统的架构如何实现渐进式披露的详细信息，请参阅下方“高级”部分中的[运行时环境](#runtime-environment)一节。

## 工作流与反馈循环
### 对复杂任务使用工作流

将复杂操作拆解为清晰、按顺序执行的步骤。对于特别复杂的工作流，提供一份清单，Agent 可以将其复制到回复中，并随着进展逐项勾选。

**示例 1：研究综合工作流**（适用于不含代码的技能）：

````markdown  theme={null}
## 研究综合工作流

复制此清单并跟踪你的进度：

```
研究进度：
- [ ] 步骤 1：阅读所有源文档
- [ ] 步骤 2：识别关键主题
- [ ] 步骤 3：交叉核对各项主张
- [ ] 步骤 4：创建结构化摘要
- [ ] 步骤 5：核实引用
```

**步骤 1：阅读所有源文档**

查看 `sources/` 目录中的每份文档。记录主要论点和支撑证据。

**步骤 2：识别关键主题**

寻找各来源之间的模式。哪些主题反复出现？各来源在哪些方面意见一致或存在分歧？

**步骤 3：交叉核对各项主张**

对于每项主要主张，核实其是否出现在源材料中。记录每个要点由哪个来源支持。

**步骤 4：创建结构化摘要**

按主题组织研究发现。包括：
- 主要主张
- 来源中的支撑证据
- 相互冲突的观点（如有）

**步骤 5：核实引用**

检查每项主张是否引用了正确的源文档。如果引用不完整，请返回步骤 3。
````

此示例展示了如何将工作流应用于不需要代码的分析任务。清单模式适用于任何复杂的多步骤流程。

**示例 2：PDF 表单填写工作流**（适用于包含代码的技能）：

````markdown  theme={null}
## PDF 表单填写工作流

复制以下清单，并在完成每项后勾选：

```
任务进度：
- [ ] 第 1 步：分析表单（运行 analyze_form.py）
- [ ] 第 2 步：创建字段映射（编辑 fields.json）
- [ ] 第 3 步：验证映射（运行 validate_fields.py）
- [ ] 第 4 步：填写表单（运行 fill_form.py）
- [ ] 第 5 步：验证输出（运行 verify_output.py）
```

**第 1 步：分析表单**

运行：`python scripts/analyze_form.py input.pdf`

这会提取表单字段及其位置，并将其保存到 `fields.json`。

**第 2 步：创建字段映射**

编辑 `fields.json`，为每个字段添加值。

**第 3 步：验证映射**

运行：`python scripts/validate_fields.py fields.json`

继续之前，修复所有验证错误。

**第 4 步：填写表单**

运行：`python scripts/fill_form.py input.pdf fields.json output.pdf`

**第 5 步：验证输出**

运行：`python scripts/verify_output.py output.pdf`

如果验证失败，返回第 2 步。
````

清晰的步骤可防止 Agent 跳过关键验证。该清单可帮助你和 Agent 跟踪多步骤工作流的进度。

### 实现反馈循环
**常见模式**：运行验证器 → 修复错误 → 重复

此模式可大幅提高输出质量。

**示例 1：遵循风格指南**（适用于不含代码的技能）：

```markdown  theme={null}
## 内容审查流程

1. 按照 STYLE_GUIDE.md 中的指南起草内容
2. 对照清单进行审查：
   - 检查术语一致性
   - 验证示例是否遵循标准格式
   - 确认所有必需章节均已包含
3. 如果发现问题：
   - 记录每个问题，并注明具体章节位置
   - 修改内容
   - 再次对照清单进行审查
4. 仅在满足所有要求后才继续
5. 完成文档定稿并保存
```

这展示了使用参考文档而非脚本的验证循环模式。“验证器”是 STYLE\_GUIDE.md，Agent 通过阅读和对比来执行检查。

**示例 2：文档编辑流程**（适用于包含代码的技能）：

```markdown  theme={null}
## 文档编辑流程

1. 对 `word/document.xml` 进行编辑
2. **立即验证**：`python ooxml/scripts/validate.py unpacked_dir/`
3. 如果验证失败：
   - 仔细查看错误消息
   - 修复 XML 中的问题
   - 再次运行验证
4. **仅在验证通过后才继续**
5. 重新构建：`python ooxml/scripts/pack.py unpacked_dir/ output.docx`
6. 测试输出文档
```

验证循环可以及早发现错误。

## 内容指南
### 避免具有时效性的信息

不要包含会过时的信息：

**反例：具有时效性**（会变得不再正确）：

```markdown  theme={null}
如果你在 2025 年 8 月之前执行此操作，请使用旧 API。
2025 年 8 月之后，请使用新 API。
```

**正例**（使用“旧模式”部分）：

```markdown  theme={null}
## 当前方法

使用 v2 API 端点：`api.example.com/v2/messages`

## 旧模式

<details>
<summary>旧版 v1 API（已于 2025-08 弃用）</summary>

v1 API 使用的是：`api.example.com/v1/messages`

此端点已不再受支持。
</details>
```

“旧模式”部分提供了历史背景，同时不会让主要内容变得杂乱。

### 使用一致的术语

选择一个术语，并在整个技能中始终使用它：

**正例——一致**：

* 始终使用“API 端点”
* 始终使用“字段”
* 始终使用“提取”

**反例——不一致**：

* 混用“API 端点”、“URL”、“API 路由”和“路径”
* 混用“字段”、“框”、“元素”和“控件”
* 混用“提取”、“拉取”、“获取”和“检索”

一致性有助于 Agent 理解并遵循指令。

## 常见模式
### 模板模式

提供输出格式模板。让严格程度与你的需求相匹配。

**对于严格要求**（例如 API 响应或数据格式）：

````markdown  theme={null}
## 报告结构

始终使用以下完全一致的模板结构：

```markdown
# [Analysis Title]

## 执行摘要
[用一段话概述关键发现]

## 关键发现
- 发现 1，并附支持数据
- 发现 2，并附支持数据
- 发现 3，并附支持数据

## 建议
1. 具体且可执行的建议
2. 具体且可执行的建议
```
````

**对于灵活指导**（适合需要调整的情况）：

````markdown  theme={null}
## 报告结构

以下是一个合理的默认格式，但请根据分析自行作出最佳判断：

```markdown
# [Analysis Title]

## 执行摘要
[Overview]

## 关键发现
[根据发现调整章节]

## 建议
[根据具体上下文定制]
```

根据具体分析类型按需调整各部分。
````

### 示例模式
对于输出质量依赖于查看示例的技能，请像在常规提示中一样提供输入/输出对：

````markdown  theme={null}
## 提交消息格式

按照以下示例生成提交消息：

**示例 1：**
输入：使用 JWT 令牌添加了用户身份验证
输出：
```
feat(auth): 实现基于 JWT 的身份验证

添加登录端点和令牌验证中间件
```

**示例 2：**
输入：修复了报告中日期显示不正确的 bug
输出：
```
fix(reports): 修正时区转换中的日期格式

在整个报告生成过程中统一使用 UTC 时间戳
```

**示例 3：**
输入：更新了依赖项并重构了错误处理
输出：
```
chore: 更新依赖项并重构错误处理

- 将 lodash 升级到 4.17.21
- 统一各端点的错误响应格式
```

遵循此样式：type(scope): 简短描述，然后给出详细说明。
````

与单纯的描述相比，示例能帮助 Agent 更清楚地理解所需的风格和详细程度。

### 条件工作流模式
引导 Agent 处理各个决策点：

```markdown  theme={null}
## 文档修改工作流

1. 确定修改类型：

   **要创建新内容？** → 按照下方的“创建工作流”操作
   **要编辑现有内容？** → 按照下方的“编辑工作流”操作

2. 创建工作流：
   - 使用 docx-js 库
   - 从头构建文档
   - 导出为 .docx 格式

3. 编辑工作流：
   - 解包现有文档
   - 直接修改 XML
   - 每次更改后进行验证
   - 完成后重新打包
```

<Tip>
  如果工作流变得庞大，或因步骤众多而变得复杂，请考虑将其拆分到单独的文件中，并告诉 Agent 根据当前任务读取相应的文件。
</Tip>

## 评估与迭代
### 先构建评估

**务必在编写大量文档之前创建评估。** 这可以确保你的技能解决的是真实问题，而不是为臆想的问题编写文档。

**评估驱动开发：**

1. **识别缺口**：在没有技能的情况下，让你的 Agent 执行有代表性的任务。记录具体的失败情况或缺失的上下文
2. **创建评估**：构建三个用于测试这些缺口的场景
3. **建立基线**：衡量 Agent 在没有技能时的表现
4. **编写最少量的指令**：只创建足以弥补这些缺口并通过评估的内容
5. **迭代**：执行评估，与基线进行比较，并持续完善

这种方法可以确保你解决的是真实问题，而不是预判那些可能永远不会出现的需求。

**评估结构**：

```json  theme={null}
{
  "skills": ["pdf-processing"],
  "query": "从这个 PDF 文件中提取所有文本，并将其保存到 output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "使用适当的 PDF 处理库或命令行工具成功读取 PDF 文件",
    "从文档的所有页面中提取文本内容，不遗漏任何页面",
    "将提取的文本以清晰、易读的格式保存到名为 output.txt 的文件中"
  ]
}
```

<Note>
  此示例展示了使用简单测试评分标准的数据驱动评估。目前，我们尚未提供运行这些评估的内置方式。用户可以创建自己的评估系统。评估是衡量技能有效性的事实依据。
</Note>

### 与 Agent 一起迭代开发技能
最高效的技能开发流程会让 Agent 本身参与其中。与一个实例（“Agent A”）协作，创建一个供其他实例（“Agent B”）使用的技能。Agent A 帮助你设计和完善指令，Agent B 则在真实任务中测试这些指令。之所以有效，是因为底层模型既了解如何编写有效的 Agent 指令，也了解 Agent 需要哪些信息。

**创建新技能：**

1. **在不使用技能的情况下完成任务**：使用常规提示，与 Agent A 一起解决问题。在此过程中，你自然会提供上下文、说明偏好并分享流程性知识。留意哪些信息是你反复提供的。

2. **识别可复用的模式**：完成任务后，找出你提供的哪些上下文对今后的类似任务有用。

   **示例**：如果你完成了一次 BigQuery 分析，可能提供了表名、字段定义、筛选规则（例如“始终排除测试账号”）以及常见的查询模式。

3. **让 Agent A 创建技能**：“创建一个技能，记录我们刚才使用的这种 BigQuery 分析模式。包括表架构、命名约定，以及过滤测试账号的规则。”

   <Tip>
     现代 Agent 原生理解技能的格式和结构。你不需要使用特殊的系统提示词，也不需要借助一个“编写技能”的技能来帮助创建技能。只需让 Agent 创建一个技能，它就会生成结构正确的 SKILL.md 内容，其中包含适当的 frontmatter 和正文内容。
   </Tip>

4. **检查是否简洁**：检查 Agent A 是否添加了不必要的解释。可以这样要求：“删除关于胜率含义的解释——Agent 已经知道这一点。”

5. **改进信息架构**：让 Agent A 更有效地组织内容。例如：“重新组织这些内容，把表架构放在单独的参考文件中。以后我们可能会添加更多表。”

6. **在类似任务中测试**：让 Agent B（已加载该技能的全新实例）使用该技能处理相关用例。观察 Agent B 是否能找到正确的信息、正确应用规则并成功完成任务。

7. **根据观察结果进行迭代**：如果 Agent B 遇到困难或遗漏了某些内容，请带着具体情况回到 Agent A：“当 Agent 使用这个技能时，它忘记针对 Q4 按日期进行筛选。我们是否应该添加一个关于日期筛选模式的章节？”

**迭代现有技能：**

改进技能时，同样的分层模式仍然适用。你需要在以下几项之间交替进行：

* **与 Agent A 协作**（帮助完善技能的专家）
* **使用 Agent B 进行测试**（使用技能执行实际工作的 Agent）
* **观察 Agent B 的行为**，并将获得的洞见反馈给 Agent A

1. **在真实工作流中使用技能**：给 Agent B（已加载该技能）分配真实任务，而不是测试场景

2. **观察 Agent B 的行为**：记录它在哪些方面遇到困难、取得成功或做出意外选择

   **观察示例**：“当我让 Agent B 生成区域销售报告时，它编写了查询，却忘记排除测试账号，尽管技能中提到了这条规则。”

3. **回到 Agent A 进行改进**：分享当前的 SKILL.md，并描述你观察到的情况。可以这样询问：“我注意到，当我要求 Agent B 生成区域报告时，它忘记过滤测试账号。技能中提到了筛选，但也许这条规则不够醒目？”

4. **审查 Agent A 的建议**：Agent A 可能会建议重新组织内容，让规则更醒目；使用“必须过滤”而不是“始终过滤”这类约束力更强的措辞；或者重构工作流部分。

5. **应用并测试更改**：根据 Agent A 的完善建议更新技能，然后让 Agent B 再次处理类似请求以进行测试

6. **根据使用情况重复上述过程**：随着你遇到新场景，继续进行“观察—完善—测试”循环。每轮迭代都根据实际观察到的 Agent 行为而非假设来改进技能。

**收集团队反馈：**

1. 与团队成员共享技能，并观察他们如何使用
2. 询问：技能是否会按预期激活？指令是否清晰？还缺少什么？
3. 吸收反馈，以解决你自身使用模式中的盲点

**这种方法为何有效**：Agent A 了解 Agent 的需求，你提供领域专业知识，Agent B 通过真实使用暴露缺口，而迭代完善会根据观察到的行为而非假设改进技能。

### 观察 Agent 如何浏览技能

在迭代技能时，请留意 Agent 在实践中究竟如何使用它们。重点观察：

* **意外的探索路径**：Agent 是否以你没有预料到的顺序读取文件？这可能表明你的结构并不像你认为的那样直观
* **遗漏的关联**：Agent 是否没有顺着引用找到重要文件？你的链接可能需要更加明确或醒目
* **过度依赖某些部分**：如果 Agent 反复读取同一个文件，请考虑其中的内容是否应该放入主 SKILL.md
* **被忽略的内容**：如果 Agent 从不访问某个随技能打包的文件，该文件可能没有必要，或者主指令中对它的提示不够清晰

请根据这些观察结果而非假设进行迭代。技能元数据中的 'name' 和 'description' 尤其关键。Agent 会依据这些字段决定是否针对当前任务触发该技能。请确保它们清楚描述技能的作用以及应在何时使用。

## 应避免的反模式
### 避免使用 Windows 风格的路径

即使在 Windows 上，也始终在文件路径中使用正斜杠：

* ✓ **推荐**：`scripts/helper.py`、`reference/guide.md`
* ✗ **避免**：`scripts\helper.py`、`reference\guide.md`

Unix 风格的路径可跨所有平台使用，而 Windows 风格的路径会在 Unix 系统上导致错误。

### 避免提供过多选项

除非必要，否则不要提供多种方法：

````markdown  theme={null}
**反面示例：选项过多**（令人困惑）：
"你可以使用 pypdf、pdfplumber、PyMuPDF、pdf2image，或者……"

**正面示例：提供默认方案**（同时留有变通余地）：
"使用 pdfplumber 提取文本：
```python
import pdfplumber
```

对于需要 OCR 的扫描版 PDF，改用 pdf2image 和 pytesseract。"
````

## 高级：包含可执行代码的技能
以下各节重点介绍包含可执行脚本的技能。如果你的技能仅使用 markdown 指令，请跳至[有效技能检查清单](#checklist-for-effective-skills)。

### 解决问题，不要推诿

为技能编写脚本时，应处理错误情况，而不是把问题甩给 Agent。

**好的示例：显式处理错误**：

```python  theme={null}
def process_file(path):
    """处理文件；如果文件不存在，则创建该文件。"""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        # 创建包含默认内容的文件，而不是让操作失败
        print(f"未找到文件 {path}，正在创建默认文件")
        with open(path, 'w') as f:
            f.write('')
        return ''
    except PermissionError:
        # 提供替代方案，而不是让操作失败
        print(f"无法访问 {path}，使用默认值")
        return ''
```

**不好的示例：把问题推给 Agent**：

```python  theme={null}
def process_file(path):
    # 直接让操作失败，再让 Agent 自己想办法
    return open(path).read()
```

配置参数也应有合理依据并记录说明，以避免出现“巫术常量”（Ousterhout 定律）。如果你不知道正确的值，Agent 又该如何确定？

**好的示例：自说明**：

```python  theme={null}
# HTTP 请求通常会在 30 秒内完成
# 更长的超时时间可应对速度较慢的连接
REQUEST_TIMEOUT = 30

# 三次重试在可靠性与速度之间取得平衡
# 大多数间歇性故障会在第二次重试前解决
MAX_RETRIES = 3
```

**不好的示例：魔法数字**：

```python  theme={null}
TIMEOUT = 47  # 为什么是 47？
RETRIES = 5   # 为什么是 5？
```

### 提供实用工具脚本
即使你的 Agent 能够编写脚本，预制脚本仍具有以下优势：

**实用脚本的优势**：

* 比生成的代码更可靠
* 节省 token（无需将代码包含在上下文中）
* 节省时间（无需生成代码）
* 确保每次使用时都保持一致

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=4bbc45f2c2e0bee9f2f0d5da669bad00" alt="将可执行脚本与指令文件一起打包" data-og-width="2048" width="2048" data-og-height="1154" height="1154" data-path="images/agent-skills-executable-scripts.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=9a04e6535a8467bfeea492e517de389f 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=e49333ad90141af17c0d7651cca7216b 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=954265a5df52223d6572b6214168c428 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=2ff7a2d8f2a83ee8af132b29f10150fd 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=48ab96245e04077f4d15e9170e081cfb 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=0301a6c8b3ee879497cc5b5483177c90 2500w" />

上图展示了可执行脚本如何与指令文件协同工作。指令文件（forms.md）引用该脚本，Agent 无需将脚本内容加载到上下文中即可执行它。

**重要区别**：在指令中明确说明 Agent 应该：

* **执行脚本**（最常见）："运行 `analyze_form.py` 以提取字段"
* **将其作为参考资料阅读**（适用于复杂逻辑）："请参阅 `analyze_form.py` 中的字段提取算法"

对于大多数实用脚本，首选执行脚本，因为这种方式更加可靠且高效。有关脚本执行工作方式的详细信息，请参阅下方的[运行时环境](#runtime-environment)部分。

**示例**：

````markdown  theme={null}
## 实用脚本

**analyze_form.py**：从 PDF 中提取所有表单字段

```bash
python scripts/analyze_form.py input.pdf > fields.json
```

输出格式：
```json
{
  "field_name": {"type": "text", "x": 100, "y": 200},
  "signature": {"type": "sig", "x": 150, "y": 500}
}
```

**validate_boxes.py**：检查边界框是否重叠

```bash
python scripts/validate_boxes.py fields.json
# 返回："OK" 或列出冲突
```

**fill_form.py**：将字段值应用到 PDF

```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
```
````

### 使用视觉分析
当输入可以渲染为图像时，让 Agent 对其进行分析：

````markdown  theme={null}
## 表单布局分析

1. 将 PDF 转换为图像：
   ```bash
   python scripts/pdf_to_images.py form.pdf
   ```

2. 分析每一页图像，以识别表单字段
3. Agent 可以通过视觉识别字段的位置和类型
````

<Note>
  在此示例中，你需要编写 `pdf_to_images.py` 脚本。
</Note>

Agent 的视觉能力有助于理解布局和结构。

### 创建可验证的中间输出

当 Agent 执行复杂的开放式任务时，可能会出错。“规划-验证-执行”模式会让 Agent 先以结构化格式创建计划，再使用脚本验证该计划，然后再执行，从而及早发现错误。

**示例**：假设你要求 Agent 根据电子表格更新 PDF 中的 50 个表单字段。如果不进行验证，它可能会引用不存在的字段、创建相互冲突的值、遗漏必填字段，或错误地应用更新。

**解决方案**：使用上面展示的工作流模式（填写 PDF 表单），但添加一个中间 `changes.json` 文件，并在应用更改之前对其进行验证。工作流变为：分析 → **创建计划文件** → **验证计划** → 执行 → 核验。

**此模式有效的原因：**

* **及早发现错误**：验证会在应用更改之前发现问题
* **可由机器验证**：脚本可提供客观的验证结果
* **规划可逆**：Agent 可以在不触碰原始文件的情况下反复修改计划
* **调试清晰**：错误消息会指向具体问题

**何时使用**：批量操作、破坏性更改、复杂的验证规则、高风险操作。

**实现提示**：让验证脚本输出详细信息，并提供具体的错误消息，例如“未找到字段 'signature\_date'。可用字段：customer\_name, order\_total, signature\_date\_signed”，以帮助 Agent 修复问题。

### 软件包依赖项
技能在代码执行环境中运行，并受到特定于平台的限制：

* **claude.ai**：可以从 npm 和 PyPI 安装软件包，并从 GitHub 仓库拉取内容
* **Anthropic API**：无法访问网络，也无法在运行时安装软件包

请在 SKILL.md 中列出所需软件包，并在[代码执行工具文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)中确认这些软件包可用。

### 运行时环境

技能在代码执行环境中运行，可以访问文件系统、运行 bash 命令并执行代码。有关此架构的概念性说明，请参阅概述中的[技能架构](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#the-skills-architecture)。

**这会如何影响您的编写方式：**

**Agent 如何访问技能：**

1. **预加载元数据**：启动时，会将所有技能的 YAML 前置元数据中的 name 和 description 加载到系统提示词中
2. **按需读取文件**：Agent 会在需要时使用文件读取工具，从文件系统访问 SKILL.md 和其他文件
3. **高效执行脚本**：实用工具脚本可通过 bash 执行，无需将其完整内容加载到上下文中。只有脚本的输出会消耗 token
4. **大文件不会带来上下文开销**：参考文件、数据或文档在实际读取前不会消耗上下文 token

* **文件路径很重要**：Agent 会像浏览文件系统一样浏览您的技能目录。请使用正斜杠（`reference/guide.md`），不要使用反斜杠
* **使用描述性文件名**：使用能表明内容的名称：`form_validation_rules.md`，而不是 `doc2.md`
* **按便于发现的方式组织**：按领域或功能组织目录结构
  * 好：`reference/finance.md`、`reference/sales.md`
  * 不好：`docs/file1.md`、`docs/file2.md`
* **打包全面的资源**：包含完整的 API 文档、丰富的示例和大型数据集；在被访问前不会产生上下文开销
* **确定性操作优先使用脚本**：编写 `validate_form.py`，而不是要求 Agent 生成验证代码
* **明确执行意图**：
  * "运行 `analyze_form.py` 以提取字段"（执行）
  * "查看 `analyze_form.py` 以了解提取算法"（作为参考读取）
* **测试文件访问模式**：通过真实请求进行测试，验证 Agent 能否浏览您的目录结构

**示例：**

```
bigquery-skill/
├── SKILL.md (概述，指向参考文件)
└── reference/
    ├── finance.md (收入指标)
    ├── sales.md (销售管道数据)
    └── product.md (使用情况分析)
```

当用户询问收入时，Agent 会读取 SKILL.md，看到对 `reference/finance.md` 的引用，然后调用 bash 只读取该文件。sales.md 和 product.md 文件仍保留在文件系统中，在需要之前消耗的上下文 token 为零。正是这种基于文件系统的模型实现了渐进式披露。Agent 可以浏览并有选择地加载每项任务恰好需要的内容。

有关技术架构的完整详情，请参阅技能概述中的[技能如何工作](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work)。

### MCP 工具引用
如果你的技能使用 MCP (Model Context Protocol) 工具，请始终使用完全限定的工具名称，以避免出现 "tool not found" 错误。

**格式**：`ServerName:tool_name`

**示例**：

```markdown  theme={null}
使用 BigQuery:bigquery_schema 工具检索表架构。
使用 GitHub:create_issue 工具创建议题。
```

其中：

* `BigQuery` 和 `GitHub` 是 MCP 服务器名称
* `bigquery_schema` 和 `create_issue` 是这些服务器中的工具名称

如果没有服务器前缀，Agent 可能无法找到该工具，尤其是在有多个 MCP 服务器可用时。

### 避免假定工具已安装

不要假定软件包已经可用：

````markdown  theme={null}
**反面示例：假定已安装**：
"使用 pdf 库处理该文件。"

**正面示例：明确说明依赖项**：
"安装所需的软件包：`pip install pypdf`

然后使用它：
```python
from pypdf import PdfReader
reader = PdfReader("file.pdf")
```"
````

## 技术说明
### YAML 前置元数据要求

SKILL.md 的前置元数据必须包含 `name`（最多 64 个字符）和 `description`（最多 1024 个字符）字段。有关完整结构的详细信息，请参阅[技能概览](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#skill-structure)。

### Token 预算

为获得最佳性能，请将 SKILL.md 正文控制在 500 行以内。如果内容超过此限制，请使用前文所述的渐进式披露模式，将其拆分到单独的文件中。有关架构的详细信息，请参阅[技能概览](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview#how-skills-work)。

## 有效技能检查清单

分享技能前，请确认：

### 核心质量

* [ ] 描述具体，并包含关键术语
* [ ] 描述既说明技能的作用，也说明何时使用该技能
* [ ] SKILL.md 正文少于 500 行
* [ ] 其他详细信息位于单独的文件中（如有需要）
* [ ] 不含时效性信息（或将其置于“旧模式”部分）
* [ ] 全文术语一致
* [ ] 示例具体，而非抽象
* [ ] 文件引用深度为一层
* [ ] 恰当地使用渐进式披露
* [ ] 工作流包含清晰的步骤

### 代码和脚本

* [ ] 脚本解决问题，而不是将问题推给 Agent 处理
* [ ] 错误处理明确且有帮助
* [ ] 不存在“巫术常量”（所有值都有合理依据）
* [ ] 在说明中列出所需软件包，并已验证这些软件包可用
* [ ] 脚本具有清晰的文档
* [ ] 不使用 Windows 风格的路径（全部使用正斜杠）
* [ ] 关键操作包含验证/核验步骤
* [ ] 对质量至关重要的任务包含反馈循环

### 测试

* [ ] 至少创建了三个评估
* [ ] 已使用 Haiku、Sonnet 和 Opus 进行测试
* [ ] 已使用真实使用场景进行测试
* [ ] 已纳入团队反馈（如适用）

## 后续步骤

<CardGroup cols={2}>
  <Card title="Agent 技能入门" icon="rocket" href="https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart">
    创建你的第一个技能
  </Card>

  <Card title="在 Claude Code 中使用技能" icon="terminal" href="https://code.claude.com/docs/en/skills">
    在 Claude Code 中创建和管理技能
  </Card>

  <Card title="通过 API 使用技能" icon="code" href="https://platform.claude.com/docs/en/build-with-claude/skills-guide">
    以编程方式上传和使用技能
  </Card>
</CardGroup>
