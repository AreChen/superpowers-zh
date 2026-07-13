# 纵深防御验证

## 概述

当你修复由无效数据导致的错误时，在一个地方添加验证似乎就足够了。但不同的代码路径、重构或模拟都可能绕过这项单一检查。

**核心原则：** 在数据经过的每一层都进行验证。让该错误从结构上不可能发生。

## 为什么需要多层验证

单层验证：“我们修复了这个错误”
多层验证：“我们让这个错误不可能发生”

不同的层会捕获不同的情况：
- 入口验证会捕获大多数错误
- 业务逻辑会捕获边界情况
- 环境防护会防止特定上下文中的危险
- 当其他层失效时，调试日志会提供帮助

## 四层验证

### 第 1 层：入口点验证
**目的：** 在 API 边界拒绝明显无效的输入

```typescript
function createProject(name: string, workingDirectory: string) {
  if (!workingDirectory || workingDirectory.trim() === '') {
    throw new Error('workingDirectory 不能为空');
  }
  if (!existsSync(workingDirectory)) {
    throw new Error(`workingDirectory 不存在：${workingDirectory}`);
  }
  if (!statSync(workingDirectory).isDirectory()) {
    throw new Error(`workingDirectory 不是目录：${workingDirectory}`);
  }
  // ... 继续执行
}
```

### 第 2 层：业务逻辑验证
**目的：** 确保数据对于此操作是合理的

```typescript
function initializeWorkspace(projectDir: string, sessionId: string) {
  if (!projectDir) {
    throw new Error('工作区初始化需要 projectDir');
  }
  // ... 继续执行
}
```

### 第 3 层：环境防护
**目的：** 防止在特定上下文中执行危险操作

```typescript
async function gitInit(directory: string) {
  // 在测试中，拒绝在临时目录之外执行 git init
  if (process.env.NODE_ENV === 'test') {
    const normalized = normalize(resolve(directory));
    const tmpDir = normalize(resolve(tmpdir()));

    if (!normalized.startsWith(tmpDir)) {
      throw new Error(
        `测试期间拒绝在临时目录之外执行 git init：${directory}`
      );
    }
  }
  // ... 继续执行
}
```

### 第 4 层：调试检测
**目的：** 捕获上下文以供事后取证

```typescript
async function gitInit(directory: string) {
  const stack = new Error().stack;
  logger.debug('即将执行 git init', {
    directory,
    cwd: process.cwd(),
    stack,
  });
  // ... 继续执行
}
```

## 应用此模式
当你发现 bug 时：

1. **追踪数据流** - 错误值源自何处？在何处被使用？
2. **绘制所有检查点** - 列出数据经过的每一个点
3. **在每一层添加验证** - 入口、业务、环境、调试
4. **测试每一层** - 尝试绕过第 1 层，验证第 2 层能将其捕获

## 会话中的示例

Bug：空的 `projectDir` 导致在源代码目录中运行 `git init`

**数据流：**
1. 测试设置 → 空字符串
2. `Project.create(name, '')`
3. `WorkspaceManager.createWorkspace('')`
4. `git init` 在 `process.cwd()` 中运行

**添加的四层防护：**
- 第 1 层：`Project.create()` 验证其非空/存在/可写
- 第 2 层：`WorkspaceManager` 验证 projectDir 非空
- 第 3 层：`WorktreeManager` 在测试中拒绝在 tmpdir 之外执行 git init
- 第 4 层：在 git init 之前记录堆栈跟踪

**结果：**全部 1847 个测试均通过，bug 无法复现

## 关键洞见

所有四层都是必要的。在测试过程中，每一层都捕获了其他层遗漏的 bug：
- 不同的代码路径绕过了入口验证
- 模拟对象绕过了业务逻辑检查
- 不同平台上的边缘情况需要环境防护
- 调试日志识别出了结构性误用

**不要止步于一个验证点。** 在每一层都添加检查。
