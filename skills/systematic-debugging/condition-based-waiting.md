# 基于条件的等待

## 概述

不稳定的测试经常使用任意延迟来猜测时序。这会造成竞态条件，使测试在速度快的机器上能够通过，但在高负载或 CI 环境中失败。

**核心原则：** 等待你真正关心的条件，而不是猜测它需要多长时间。

## 何时使用

```dot
digraph when_to_use {
    "Test uses setTimeout/sleep?" [shape=diamond, label="测试是否使用 setTimeout/sleep？"];
    "Testing timing behavior?" [shape=diamond, label="是否在测试时序行为？"];
    "Document WHY timeout needed" [shape=box, label="记录为何需要超时"];
    "Use condition-based waiting" [shape=box, label="使用基于条件的等待"];

    "Test uses setTimeout/sleep?" -> "Testing timing behavior?" [label="是"];
    "Testing timing behavior?" -> "Document WHY timeout needed" [label="是"];
    "Testing timing behavior?" -> "Use condition-based waiting" [label="否"];
}
```

**适用情形：**
- 测试中存在任意延迟（`setTimeout`、`sleep`、`time.sleep()`）
- 测试不稳定（有时通过，但在高负载下失败）
- 并行运行时测试超时
- 等待异步操作完成

**不适用情形：**
- 测试实际的时序行为（防抖、节流间隔）
- 如果使用任意超时，务必记录为什么需要它

## 核心模式
```typescript
// ❌ 之前：凭猜测设定等待时间
await new Promise(r => setTimeout(r, 50));
const result = getResult();
expect(result).toBeDefined();

// ✅ 之后：等待条件满足
await waitFor(() => getResult() !== undefined);
const result = getResult();
expect(result).toBeDefined();
```

## 常用模式

| 场景 | 模式 |
|----------|---------|
| 等待事件 | `waitFor(() => events.find(e => e.type === 'DONE'))` |
| 等待状态 | `waitFor(() => machine.state === 'ready')` |
| 等待数量 | `waitFor(() => items.length >= 5)` |
| 等待文件 | `waitFor(() => fs.existsSync(path))` |
| 复杂条件 | `waitFor(() => obj.ready && obj.value > 10)` |

## 实现

通用轮询函数：
```typescript
async function waitFor<T>(
  condition: () => T | undefined | null | false,
  description: string,
  timeoutMs = 5000
): Promise<T> {
  const startTime = Date.now();

  while (true) {
    const result = condition();
    if (result) return result;

    if (Date.now() - startTime > timeoutMs) {
      throw new Error(`等待 ${description} 超时，已等待 ${timeoutMs}ms`);
    }

    await new Promise(r => setTimeout(r, 10)); // 每 10ms 轮询一次
  }
}
```

有关来自实际调试会话、包含领域特定辅助函数（`waitForEvent`、`waitForEventCount`、`waitForEventMatch`）的完整实现，请参阅此目录中的 `condition-based-waiting-example.ts`。

## 常见错误
**❌ 轮询过快：** `setTimeout(check, 1)` - 浪费 CPU
**✅ 修复：** 每 10ms 轮询一次

**❌ 无超时：** 如果条件始终未满足，则会无限循环
**✅ 修复：** 始终包含超时，并提供清晰的错误信息

**❌ 过期数据：** 在循环前缓存状态
**✅ 修复：** 在循环内调用 getter 以获取最新数据

## 何时使用任意超时才是正确的

```typescript
// 工具每 100ms 进行一次 tick——需要 2 个 tick 来验证部分输出
await waitForEvent(manager, 'TOOL_STARTED'); // 首先：等待条件
await new Promise(r => setTimeout(r, 200));   // 然后：等待定时行为
// 200ms = 以 100ms 为间隔的 2 个 tick——已有文档说明且理由充分
```

**要求：**
1. 首先等待触发条件
2. 基于已知时序（而非猜测）
3. 用注释说明为什么

## 实际影响

来自调试会话（2025-10-03）：
- 修复了 3 个文件中的 15 个不稳定测试
- 通过率：60% → 100%
- 执行速度：提升 40%
- 不再有竞态条件
