# 第 4 章：OpenClaw 原理解读

> 深入理解 OpenClaw 的工作原理和架构设计

---

## 4.1 OpenClaw 是什么？

OpenClaw（曾用名 Clawdbot、MoltBot）是一个**开源的个人 AI 助手框架**。

### 4.1.1 核心价值

**传统 AI 助手**（如 ChatGPT）：
- ❌ 你不问，它就不动
- ❌ 只能回答问题，不能实际操作
- ❌ 没有记忆，每次对话从零开始
- ❌ 无法连接外部系统

**OpenClaw AI 助手**：
- ✅ 可以设置定时任务，自动执行
- ✅ 能操作电脑、发送消息、调用 API
- ✅ 有长期记忆，记得你的偏好和历史
- ✅ 可连接飞书、Telegram、WhatsApp 等平台

**一句话总结**：OpenClaw 让 AI 从「聊天机器人」进化为「执行助手」。

### 4.1.2 核心特性

| 特性 | 说明 | 示例 |
|------|------|------|
| **技能系统** | 通过技能扩展能力 | 天气查询、文件传输、新闻推送 |
| **定时任务** | Heartbeat + Cron 双机制 | 每日早报、会议提醒、周报生成 |
| **多平台支持** | 连接多个聊天平台 | 飞书、Telegram、WhatsApp、Discord |
| **记忆系统** | 短期 + 长期记忆 | 记得用户偏好、历史记录 |
| **多 Agent 协作** | 可运行多个独立 Agent | 内容 Agent、运营 Agent、开发 Agent |

---

## 4.2 系统架构

### 4.2.1 整体架构

OpenClaw 是一个通过 Gateway 连接即时通讯平台（如 Telegram、Discord、Slack、飞书等）与本地 AI Agent 的 24×7 运行的个人助手系统。

```
┌─────────────────────────────────────────────────────────┐
│                    用户界面层                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │  飞书   │  │Telegram │  │WhatsApp │  │ Discord │   │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │
└───────┼───────────┼───────────┼───────────┼───────────┘
        │           │           │           │
┌───────┴───────────┴───────────┴───────────┴───────────┐
│                   Gateway 网关层                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  - 消息路由    - 会话管理    - 插件系统          │  │
│  │  - 认证授权    - 限流控制    - 日志记录          │  │
│  └──────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────┐
│                    Agent 核心层                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │  - 意图识别    - 技能调度    - 上下文管理        │  │
│  │  - 记忆系统    - 定时任务    - 工具调用          │  │
│  └──────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────┐
│                    技能/工具层                            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │  技能   │  │  工具   │  │  脚本   │  │  插件   │   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
└─────────────────────────────────────────────────────────┘
```

**个人评价**：OpenClaw 的完成度非常高，尽管因为各种安全问题被质疑，但其产品思想和围绕这个核心思想设计的各种代码组件和交互，值得开发者反复学习。

### 4.2.2 四层架构详解

**第一层：用户界面层**
- 用户通过聊天平台与 AI 交互
- 支持多个平台同时连接
- 消息格式统一转换

**第二层：Gateway 网关层**

Gateway 是 OpenClaw 的控制平面，负责 24×7 持久运行。

**核心职责**：
- 保持与所有消息渠道的长连接
- 管理会话状态
- 响应客户端请求
- 处理定时任务

**Gateway 启动流程**：

```typescript
// src/gateway/server.impl.ts - 简化版
export async function startGatewayServer(port = 18789) {
  // 1. 设置端口环境变量
  process.env.OPENCLAW_GATEWAY_PORT = String(port);
  
  // 2. 加载并验证配置
  let configSnapshot = await readConfigFileSnapshot();
  
  // 3. 创建 WebSocket 服务器
  const wsServer = new WebSocket.Server({ port, host });
  
  // 4. 注册核心处理器
  const channelManager = createChannelManager(configSnapshot.config);
  const agentEventHandler = createAgentEventHandler(configSnapshot.config);
  const cronService = buildGatewayCronService(configSnapshot.config);
  
  // 5. 启动通道连接（WhatsApp、Telegram 等）
  await channelManager.startAll();
  
  // 6. 返回 close 方法用于优雅关闭
  return { close: (opts) => shutdownGateway(opts) };
}
```

**Gateway 通过系统服务管理保持 24×7 运行**：

```bash
# macOS 启动 Gateway
launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# Linux 启动 Gateway
systemctl --user enable --now openclaw-gateway.service
```

**消息接入与分发**（以 Telegram 为例）：

```typescript
// 使用 grammY 作为机器人框架
import { Bot, webhookCallback } from "grammy";

const bot = new Bot(opts.token);
const processMessage = createTelegramMessageProcessor({bot, ...});
registerTelegramHandlers({ cfg, accountId, bot, processMessage, ...});

// 核心分发函数
export const dispatchTelegramMessage = async ({ context, bot, cfg, runtime }) => {
  const { msg, chatId, isGroup, historyKey, route } = context;
  
  // 1. 分发消息
  const { queuedFinal } = await dispatchReplyWithBufferedBlockDispatcher({
    ctx: ctxPayload,
    cfg,
    dispatcherOptions: {
      // 2. 回复消息回调
      deliver: async (payload, info) => {
        const result = await deliverReplies({
          replies: [payload],
          chatId: String(chatId),
          token: opts.token,
          runtime,
          bot,
        });
      },
      onError: (err, info) => {
        runtime.error?.(`telegram reply failed: ${String(err)}`);
      },
    },
  });
};
```

一些特殊消息能力，需要通过 message 工具来发送，而非直接通过 deliverReplies 来发送消息。

**第三层：Agent 核心层**

OpenClaw 支持调用已有的 CLI Agent（如 Claude Code 等），但默认情况下嵌入了基于 **Pi-Agent 框架** 执行 Agent 运行时。

**Pi-Agent 框架特点**：
- 极高的扩展性
- 满足 OpenClaw 定制化需求
- 大模型供应商支持
- Session 管理
- 工具定制化
- 流式输出
- 消息订阅

**Agent Loop 执行流程**：

消息进入 AgentSession 后，通过 **ReAct 范式** 执行 Agent Loop（包括工具调用），通过注册 reply 回调（监听 message_end 事件）将 AI 回复的消息通过机器人发送给 Telegram。

**故障转移机制**：

为了能 24×7 持续运行，不能因为一些异常就停止。OpenClaw 实现了完整的故障转移机制：

1. **Auth Profile 轮换**: 当一个 API Key 遇到速率限制或认证失败时，自动切换到下一个可用的 Profile
2. **上下文溢出自动压缩**: 当会话过长时，自动压缩历史消息
3. **思考级别降级**: 当模型不支持扩展思考模式时，自动降级到基本模式

```typescript
// src/agents/pi-embedded-runner/run.ts - 简化版
export async function runEmbeddedPiAgent(params) {
  // 会话级别并发控制（串行处理）
  const sessionLane = resolveSessionLane(params.sessionKey);
  
  // 全局并发控制（默认并发度 4）
  const globalLane = resolveGlobalLane(params.lane);
  
  return enqueueSession(() => enqueueGlobal(async () => {
    const started = Date.now();
    
    // 模型解析和上下文窗口验证
    const { model, error, authStorage, modelRegistry } = resolveModel(...);
    
    // 认证配置管理和故障转移
    const profileOrder = resolveAuthProfileOrder({
      cfg: params.config,
      store: authStore,
      provider,
      preferredProfile: preferredProfileId,
    });
    
    // 主执行循环，支持故障转移
    while (true) {
      const attempt = await runEmbeddedAttempt({...});
      
      // 处理上下文溢出，自动压缩
      if (isContextOverflowError(errorText)) {
        if (!overflowCompactionAttempted) {
          const compactResult = await compactEmbeddedPiSessionDirect({...});
          if (compactResult.compacted) {
            continue; // 使用压缩后的会话重试
          }
        }
      }
      
      // 处理认证/速率限制故障转移
      if (shouldRotate) {
        const rotated = await advanceAuthProfile();
        if (rotated) continue;
      }
      
      return {...};
    }
  }));
}
```

**第四层：技能/工具层**
- 技能：预定义的功能模块（如天气查询）
- 工具：底层能力（如文件读写、网络请求）
- 脚本：自定义 Python/Bash 脚本
- 插件：第三方扩展

---

## 4.3 核心机制

### 4.3.1 消息处理流程

当用户发送消息时，系统内部发生了什么？

```
用户发送消息
    ↓
Gateway 接收消息
    ↓
验证身份和权限
    ↓
创建/更新会话
    ↓
Agent 分析意图
    ↓
选择合适的技能
    ↓
执行技能（可能调用工具/脚本）
    ↓
生成响应
    ↓
通过 Gateway 发送回用户
```

**示例**：

```
用户：「帮我查一下北京今天的天气」

1. 飞书接收消息
2. Gateway 验证用户身份
3. 找到对应的会话
4. Agent 分析意图：天气查询
5. 选择 weather 技能
6. 调用天气 API
7. 生成响应：「北京今天晴，25°C...」
8. 通过飞书发送给用户
```

### 4.3.2 Session Key 机制

**SessionKey 是 OpenClaw 中用于标识和路由会话的核心概念。**

由于 OpenClaw 支持非常多的 Channel 账号、以及私聊、群组、Thread 等各种会话形式，需要一种命名方式来唯一识别不同的会话。

**SessionKey 格式示例**：

```typescript
// src/routing/session-key.ts
// 主会话
agent:main:main

// Telegram DM（私聊）
agent:main:telegram:default:dm:123456789

// Telegram 群组
agent:main:telegram:group:1001234567890
```

**SessionKey 构建函数**：

```typescript
// 构建主会话 Key
export function buildAgentMainSessionKey(params: {
  agentId: string;
  mainKey?: string | undefined;
}): string {
  const agentId = normalizeAgentId(params.agentId);
  const mainKey = normalizeMainKey(params.mainKey);
  return `agent:${agentId}:${mainKey}`;
}

// 构建对等会话 Key（DM、群组等）
export function buildAgentPeerSessionKey(params: {
  agentId: string;
  mainKey?: string | undefined;
  channel: string;
  accountId?: string | null;
  peerKind?: "dm" | "group" | "channel" | null;
  peerId?: string | null;
}): string {
  // 对于 DM: agent:main:channel:account:dm:peerId
  // 对于群组：agent:main:channel:group:groupId
  // ...
}
```

### 4.3.3 消息处理流程

技能如何被触发？

**方式 1：自然语言触发**

```
用户：「今天天气怎么样？」
→ 意图识别：weather.query
→ 触发技能：weather
```

**方式 2：命令触发**

```
用户：/weather 北京
→ 命令匹配：weather
→ 触发技能：weather
```

**方式 3：定时触发**

```
Heartbeat 每 30 分钟触发
→ 读取 HEARTBEAT.md
→ 检查是否需要执行任务
→ 触发相应技能
```

**方式 4：事件触发**

```
收到新邮件
→ 事件监听器捕获
→ 触发邮件处理技能
```

### 4.3.3 记忆系统

OpenClaw 如何记住事情？

**短期记忆**（会话上下文）：
- 存储当前对话的历史
- 每次对话自动更新
- 会话结束后保留（可配置）

**长期记忆**（MEMORY.md）：
- 存储在 `memory/` 目录
- 按日期分文件（`2026-03-16.md`）
- 手动或自动写入
- 跨会话共享

**记忆检索**：
```
用户：「我昨天说的那个项目怎么样了？」

1. 搜索短期记忆（最近对话）
2. 搜索长期记忆（MEMORY.md）
3. 找到相关记录
4. 生成响应
```

### 4.3.4 队列与并发控制

为了解决群组聊天或高频交互中的"消息竞争"问题，OpenClaw 设计了一套精密的 Queue 系统。

**队列模式（Queue mode）**：

| 模式 | 说明 |
|------|------|
| `collect` | 收集模式（默认）：将所有排队的消息合并成单个后续回复 |
| `steer` | 转向模式：立即注入到当前 agent 回合中 |
| `followup` | 跟进模式：当前运行结束后，为下一个 agent 回合排队 |
| `steer-backlog` | 转向 + 积压模式：现在转向当前回合，然后保留消息用于后续回合 |

**队列配置**：

```typescript
// src/auto-reply/reply/queue/types.ts
export type QueueMode = "steer" | "followup" | "collect" | "steer-backlog" | "interrupt" | "queue";

export type QueueSettings = {
  mode: QueueMode;
  debounceMs?: number;  // 防抖延迟（毫秒），默认 1000ms
  cap?: number;         // 队列容量上限，默认 20
  dropPolicy?: "old" | "new" | "summarize";  // 默认 summarize
};
```

**Collect 模式示例**（消息合并）：

```json
{
  "id": "e1c9d464",
  "message": {
    "content": [{
      "text": "[Queued messages while agent was busy]\n\n---\nQueued #1\n[Slack x +1s] 算了\n\n---\nQueued #2\n[Slack x +4s] 查一下天津的天气",
      "type": "text"
    }],
    "role": "user",
    "timestamp": 1770627650797
  },
  "parentId": "7588527b",
  "type": "message"
}
```

**并发控制**：

OpenClaw 使用两层并发控制：

1. **会话级别**: 同一会话内的消息串行处理，避免状态混乱
2. **全局级别**: 默认并发度为 4，允许最多 4 个会话同时处理

```typescript
// src/agents/pi-embedded-runner/run/lanes.ts
export function resolveSessionLane(sessionId: string): string {
  return `session:${sessionId}`;
}

export function resolveGlobalLane(lane?: string): string {
  return lane || `global:default`;
}

// 全局并发度 4：即保障 active 的会话，不超过 4 个
return enqueueSession(() => enqueueGlobal(async () => {...}));
```

Telegram 还专门使用 `bot.use(sequentialize(getTelegramSequentialKey))` 序列化所有消息。

**Heartbeat 心跳**：

```
每 30 分钟触发
    ↓
读取 HEARTBEAT.md
    ↓
逐项检查
    ↓
如果无事 → 回复 HEARTBEAT_OK（用户无感）
如果有关 → 执行任务并通知用户
```

**Cron 定时调度**：

```
到达指定时间
    ↓
创建独立会话（isolated）
    ↓
执行指定任务
    ↓
发送结果到指定渠道
    ↓
如果是一次性任务 → 自动删除
```

---

## 4.4 技能系统

### 4.4.1 技能是什么？

技能是 OpenClaw 的**能力扩展单元**。

**类比**：
- 手机 App → 扩展手机功能
- 浏览器插件 → 扩展浏览器功能
- OpenClaw 技能 → 扩展 AI 功能

### 4.4.2 技能结构

```
my-skill/
├── SKILL.md          # 技能描述（必需）
├── scripts/          # 脚本（可选）
│   └── process.py
├── references/       # 参考资料（可选）
└── templates/        # 模板（可选）
```

**SKILL.md 核心内容**：

```markdown
---
name: skill-name
description: 技能描述
allowed-tools: read, write, exec
---

# 技能说明

## 触发条件
当用户提到以下关键词时触发：
- 关键词 1
- 关键词 2

## 使用方式
```
示例命令
```

## 示例
用户：示例输入
AI：示例输出
```

### 4.4.3 技能类型

**内置技能**：
- OpenClaw 自带
- 无需安装
- 如：`read`、`write`、`exec`

**社区技能**：
- 开发者创建
- 从 ClawHub 安装
- 如：`weather`、`tech-news-daily`

**自定义技能**：
- 自己开发
- 满足特定需求
- 可分享给他人

---

## 4.5 会话管理：Session

一般 session 的对话数据也被称为**短期记忆**。

与 Agent 的多轮交互需要维持一次会话中历史所有消息（UserMessage, AI Message，Tool Result Message 等）。OpenClaw 作为本地 Agent，采用**本地文件系统**作为 Session 存储工具，解决会话数据的持久化问题。

### 4.5.1 存储结构

**物理存储路径**: `~/.openclaw/agents/<agentId>/sessions/`

**文件组织**：
- `session.json`: 记录所有 Session 的元数据映射
- `<sessionId>.jsonl`: 存储具体的对话日志（JSON Lines 格式，便于追加写入）

### 4.5.2 生命周期管理

Agent Session 并不会一直共享同一个上下文，否则上下文窗口很容易超长。OpenClaw 实现了自动化的会话生命周期管理：

- **每日重置**: 每天自动生成新的 SessionId（通过检测日期变化）
- **空闲归档**: 默认 60 分钟无交互后归档当前 Session
- **子 Agent 管理**: 子 Agent 的 Session 同样遵循 60 分钟自动归档策略

因此一个 SessionKey，可能存在多个 SessionId。比如同样在 Telegram 私聊机器人，今天对话使用的上下文和昨天是完全不同的。

### 4.5.3 Session 加载和管理

**获取 Session 的所有配置**：

```typescript
// src/config/sessions/store.ts
export function loadSessionStore(storePath: string) {
  let store: Record<string, SessionEntry> = {};
  try {
    const raw = fs.readFileSync(storePath, "utf-8");
    const parsed = JSON5.parse(raw);
    if (isSessionStoreRecord(parsed)) {
      store = parsed;
    }
  } catch {
    // 忽略缺失/无效的 store；我们会重新创建
  }
  return structuredClone(store);
}
```

**根据 SessionKey 和对应的 SessionId，获取当前会话的历史文件**：

```typescript
// 构造 Session Manager，创建 AgentSession
sessionManager = guardSessionManager(
  // 获取当前会话的历史文件 sessionFile: <sessionId>.jsonl
  SessionManager.open(params.sessionFile),
  { agentId: sessionAgentId, sessionKey: params.sessionKey, ... }
);

({ session } = await createAgentSession({
  cwd: resolvedWorkspace,
  agentDir,
  authStorage: params.authStorage,
  modelRegistry: params.modelRegistry,
  model: params.model,
  thinkingLevel: mapThinkingLevel(params.thinkLevel),
  tools: builtInTools,
  customTools: allCustomTools,
  sessionManager,
  ...
}));
```

**会话新增消息，加锁后存入文件**：

```typescript
export async function updateSessionStore<T>(
  storePath: string,
  mutator: (store: Record<string, SessionEntry>) => Promise<T> | T,
): Promise<T> {
  return await withSessionStoreLock(storePath, async () => {
    // 在锁内重新读取以避免覆盖并发写入
    const store = loadSessionStore(storePath, { skipCache: true });
    const result = await mutator(store);
    await saveSessionStoreUnlocked(storePath, store);
    return result;
  });
}
```

---

## 4.6 记忆系统：Memory

OpenClaw 拥有一个完善的记忆系统，通过对记忆相关的 Markdown 文件的实时索引和混合检索来实现长期记忆。

### 4.6.1 记忆存储

除了 Agent 固定加载的一些相关文件（比如 AGENTS.md，USER.md, IDENTITY.md 等）之外，记忆存储在 `~/.openclaw/workspace` 下：

- `MEMORY.md` 或 `memory.md`: 全局长期记忆
- `memory/*.md`: 目录中的所有 Markdown 文件
- 额外路径：通过 `memorySearch.extraPaths` 配置

**记忆文件列表**：

```typescript
// src/memory/internal.ts
export async function listMemoryFiles(workspaceDir: string, extraPaths?: string[]) {
  const result: string[] = [];
  
  const memoryFile = path.join(workspaceDir, "MEMORY.md");
  const altMemoryFile = path.join(workspaceDir, "memory.md");
  const memoryDir = path.join(workspaceDir, "memory");
  
  // 添加主记忆文件
  await addMarkdownFile(memoryFile);
  await addMarkdownFile(altMemoryFile);
  
  // 递归遍历 memory 目录
  try {
    const dirStat = await fs.lstat(memoryDir);
    if (!dirStat.isSymbolicLink() && dirStat.isDirectory()) {
      await walkDir(memoryDir, result);
    }
  } catch {}
  
  // 处理额外路径
  const normalizedExtraPaths = normalizeExtraMemoryPaths(workspaceDir, extraPaths);
  for (const inputPath of normalizedExtraPaths) {
    const stat = await fs.lstat(inputPath);
    if (stat.isDirectory()) {
      await walkDir(inputPath, result);
    } else if (stat.isFile() && inputPath.endsWith(".md")) {
      result.push(inputPath);
    }
  }
  
  return deduped;
}
```

**Memory 写入机制**：

- `memoryFlush`（session 自动压缩）：只在 context tokens 快满的情况下执行
- `prompt`：使用类似"记住我"、"记住这个"、"今天"等，agent 会保存记忆到本地文件
- `sessionFlush`：`/new` 新 session 保存旧 session 到 `memory/<YYYY-MM-DD>-slug.md`

配置使用 `sources: ["memory", "sessions"]` 后也会将 session 文件纳入到记忆检索范围中。

### 4.6.2 混合检索

通过给 Agent 提供 `memory_search` 和 `memory_get` 工具，允许其在合适的时候通过 query 检索历史记忆中相关的文本片段（RAG 范式）。

OpenClaw 使用了典型的混合检索方案，即同时通过**关键词精确搜索** + **向量语义检索**，对候选结果计算加权得分，给 agent 展示最相关的几条。

基于本地个人 Agent 的定位，OpenClaw 的精确检索和向量检索都默认使用 **Sqlite** 作为数据库存储（结果是一个 `agents.sqlite` 文件）。

**Memory 检索工具**：

```typescript
// src/agents/tools/memory-tool.ts
export function createMemorySearchTool(options): AnyAgentTool | null {
  return {
    label: "Memory Search",
    name: "memory_search",
    description: "Mandatory recall step: semantically search MEMORY.md + memory/*.md",
    parameters: MemorySearchSchema,
    execute: async (_toolCallId, params) => {
      const query = readStringParam(params, "query", { required: true });
      const maxResults = readNumberParam(params, "maxResults");
      const minScore = readNumberParam(params, "minScore");
      
      const { manager, error } = await getMemorySearchManager({ cfg, agentId });
      if (!manager) {
        return jsonResult({ results: [], disabled: true, error });
      }
      
      const results = await manager.search(query, { maxResults, minScore, sessionKey: options.agentSessionKey });
      return jsonResult({ results, provider: status.provider, model: status.model });
    },
  };
}
```

**MemoryManager 执行混合检索**：

```typescript
// src/memory/manager.ts
export class MemoryIndexManager {
  async search(query: string, opts?: { maxResults?: number; minScore?: number }) {
    // 关键词搜索
    const keywordResults = hybrid.enabled 
      ? await this.searchKeyword(cleaned, candidates).catch(() => []) 
      : [];
    
    // 向量搜索
    const queryVec = await this.embedQueryWithTimeout(cleaned);
    const vectorResults = hasVector 
      ? await this.searchVector(queryVec, candidates).catch(() => []) 
      : [];
    
    // 合并结果
    if (!hybrid.enabled) {
      return vectorResults.filter((entry) => entry.score >= minScore).slice(0, maxResults);
    }
    
    const merged = this.mergeHybridResults({
      vector: vectorResults,
      keyword: keywordResults,
      vectorWeight: hybrid.vectorWeight,
      textWeight: hybrid.textWeight,
    });
    
    return merged.filter((entry) => entry.score >= minScore).slice(0, maxResults);
  }
}
```

**Sqlite-vec 执行 KNN 向量检索示例**：

```sql
-- 创建向量表
CREATE VIRTUAL TABLE vec_items USING vec0(embedding float[4]);

-- 插入向量
INSERT INTO vec_items(rowid, embedding) VALUES (?, ?);

-- KNN 搜索
SELECT rowid, distance 
FROM vec_items 
WHERE embedding MATCH ? 
ORDER BY distance 
LIMIT 3;
```

### 4.6.3 索引写入

记忆检索依赖的本地 sqlite 数据库，是在特定时机触发索引写入的。比如，在监听到 Memory 文件变更后，会将其同步索引到本地数据库中，方便后续进行记忆检索。如果开启了 session 来源，也会在 session 更新文件后，执行索引写入。

**单个文件的索引写入分为三个部分**：

1. **文件分块**：先将文件根据 chunkTokens 配置分为固定大小的块，为了增强前后文的感知，允许一定 token 的分块重叠
2. **Embedding 计算和缓存**：利用配置的远程或本地 embedding 模型计算 chunk 的语义向量。同时由于经常多次索引，因此可以利用 embedding 缓存来避免重复计算
3. **写入本地数据库**：写入索引检索依赖 `chunks_vec` 和 `chunks_fts` 两种表

### 4.5.1 什么是会话？

会话是**一次完整的对话上下文**。

**特点**：
- 每个会话独立
- 有自己的历史记录
- 可以并行运行多个会话

### 4.5.2 会话类型

**主会话（main）**：
- 默认会话
- 共享上下文
- 适合日常对话

**独立会话（isolated）**：
- 干净的独立环境
- 每次从零开始
- 适合定时任务

**示例**：

```bash
# 主会话（默认）
openclaw cron add --name "日报" --cron "0 9 * * *" \
  --session main \  # 会打断当前对话
  --message "生成日报"

# 独立会话（推荐）
openclaw cron add --name "日报" --cron "0 9 * * *" \
  --session isolated \  # 不影响主对话
  --message "生成日报"
```

### 4.5.3 会话生命周期

```
创建会话
    ↓
用户发送消息
    ↓
AI 回复
    ↓
...（多次交互）
    ↓
用户离开/超时
    ↓
会话保留（可配置）
```

---

## 4.6 工具系统

### 4.6.1 工具是什么？

工具是 OpenClaw 的**底层能力**。

**常见工具**：

| 工具 | 功能 | 示例 |
|------|------|------|
| `read` | 读取文件 | 读取配置文件 |
| `write` | 写入文件 | 保存数据 |
| `edit` | 编辑文件 | 修改配置 |
| `exec` | 执行命令 | 运行脚本 |
| `browser` | 浏览器控制 | 抓取网页 |
| `web_search` | 网络搜索 | 搜索信息 |

### 4.6.2 技能使用工具

技能通过 `allowed-tools` 声明需要的工具：

```markdown
---
name: weather
description: 天气查询
allowed-tools: exec, web_search
---
```

**安全机制**：
- 技能只能使用声明的工具
- 不能越权访问
- 用户可配置权限

---

## 4.7 工具技能 (Tools & Skills)

OpenClaw 提供了极其丰富且开箱即用的工具技能，这也是其能大火的原因之一。除了通用 CLI Agent 都有的文件系统访问、Shell 命令执行、webSearch 工具外，还有获取 Gateway、Session 等运行状态的自感知能力，以及内置的多个实用的插件工具（比如 bird，message，browser，天气等）。

### 4.7.1 工具示例：message

工具集成本身是 agent 的通用能力，但 OpenClaw 的 message 工具比较独特。与特定 Channel 集成，能够达到丝滑的交互效果：

- **发送多条消息**：AI 可以在最终回复用户之前或之后，先发送一张图片、一个文件或者另一条补充消息（主动式 Agent 的基础）
- **富文本与复杂交互**：显式设置 buttons（内联按钮）、card（卡片）、poll（投票）等高级功能
- **引用与回复**：精准控制 replyTo（回复特定消息 ID），而不仅仅是回复当前最后一条

**message 工具调用示例**：

```json
{
  "action": "send",
  "buttons": "[[{\"text\":\"A. 下午好\", \"callback_data\":\"n5_quiz_wrong\"}, {\"text\":\"B. 再见\", \"callback_data\":\"n5_quiz_correct\"}], [{\"text\":\"C. 谢谢\", \"callback_data\":\"n5_quiz_wrong\"}, {\"text\":\"D. 早上好\", \"callback_data\":\"n5_quiz_wrong\"}]]",
  "channel": "telegram",
  "message": "📚 **日语 N5 练习题**\n\n**さようなら** 的中文意思是什么？",
  "target": "123456"
}
```

### 4.7.2 Skills 示例：bird

Skills 通过文件系统 + 渐进式披露，标准化和模块化技能提示词。

**Skills 加载位置**：

1. **内置 Skills**：随安装包一起发布（npm 包或 OpenClaw.app），比如 bird，github 等
2. **托管/本地 Skills**：`~/.openclaw/skills`
3. **工作区 Skills**：`<workspace>/skills`

bird skills 可以搜索和总结 Twitter（X）上的内容。

### 4.7.3 自定义工具和技能

OpenClaw 允许用户自定义加入工具和技能。官方推荐使用 clawhub 命令安装 https://clawhub.ai/ 里的技能或通过 plugin 命令安装插件。

```bash
# 技能安装，以 artifacts-builder 为例
npm i -g clawhub
clawhub install artifacts-builder

# 插件安装
openclaw plugins list
openclaw plugins install @openclaw/voice-call
```

也可以直接将 skills 添加到目录 `.openclaw/workspace/skills/`。

### 4.7.4 工具策略

OpenClaw 支持多个层级的工具配置策略，即特定的场景可以配置不同的工具组合可见性：

- **全局策略**: `config.tools`
- **全局按提供商策略**: `config.tools.byProvider[providerOrModelId]`
- **Agent 策略**: `config.agents.[agentId].tools`
- **Agent 按提供商策略**: `config.agents.[agentId].tools.byProvider[providerOrModelId]`
- **群组策略**: `config.groups.[groupId].tools` (针对特定群组)

### 4.7.1 配置文件位置

```
~/.openclaw/
├── config.json         # 主配置
├── gateway/
│   └── config.json     # Gateway 配置
└── workspace/
    └── config.json     # 工作区配置
```

### 4.7.2 核心配置项

```json
{
  "agents": {
    "defaults": {
      "model": "qwen3.5-plus",      // 默认模型
      "heartbeat": {
        "every": "30m",             // 心跳间隔
        "activeHours": {
          "start": "08:00",         // 工作时间
          "end": "22:00"
        }
      }
    }
  },
  "channels": {
    "feishu": {
      "enabled": true,              // 启用飞书
      "appId": "cli_xxx",
      "appSecret": "xxx"
    }
  },
  "env": {
    "WEATHER_API_KEY": "xxx"        // 环境变量
  }
}
```

### 4.7.3 配置优先级

```
会话配置 > 技能配置 > 工作区配置 > 全局配置
```

---

## 4.8 安全机制

### 4.8.1 权限控制

**技能权限**：
- 只能使用声明的工具
- 不能访问未授权的文件
- 不能执行危险命令

**用户权限**：
- 认证后才能使用
- 可配置访问级别
- 支持多用户

### 4.8.2 敏感信息保护

**API 密钥**：
- 存储在配置文件
- 不显示在日志
- 不传递给模型

**最佳实践**：

```json
// ✅ 正确：使用环境变量
{
  "env": {
    "API_KEY": "${API_KEY}"
  }
}

// ❌ 错误：硬编码密钥
{
  "env": {
    "API_KEY": "sk-123456"
  }
}
```

---

## 4.9 性能优化

### 4.9.1 Token 优化

**心跳 vs Cron**：
- 一次心跳检查 5 件事 = 1 次 AI 调用
- 5 个独立 Cron = 5 次 AI 调用
- **心跳更省 token**

**模型选择**：
- 日常任务用便宜模型
- 重要任务用好模型
- **按需调配**

### 4.9.2 缓存策略

**记忆缓存**：
- 频繁访问的记忆缓存
- 减少重复检索
- 提高响应速度

**技能缓存**：
- 技能执行结果可缓存
- 避免重复执行
- 节省时间和 token

---

## 4.10 扩展机制

### 4.10.1 插件系统

OpenClaw 通过插件扩展平台支持：

```bash
# 安装飞书插件
openclaw plugins install @m1heng-clawd/feishu

# 安装 Telegram 插件
openclaw plugins install telegram
```

### 4.10.2 技能市场

**ClawHub**：
- 官方技能市场
- 搜索和安装技能
- 分享自己的技能

```bash
# 搜索技能
openclaw skills search 天气

# 安装技能
openclaw skills install weather
```

---

## 4.12 本章小结

通过本章学习，你应该理解：

- ✅ OpenClaw 的核心价值和特性
- ✅ 四层架构（界面层、网关层、核心层、技能层）
- ✅ Gateway 网关层的核心机制
- ✅ Session Key 机制和会话路由
- ✅ 消息处理流程
- ✅ Agent Loop 和故障转移机制
- ✅ 队列与并发控制（4 种模式）
- ✅ 会话管理（存储结构、生命周期）
- ✅ 记忆系统（存储、混合检索、索引写入）
- ✅ 工具技能系统（message、bird、自定义）
- ✅ 技能触发机制（4 种方式）
- ✅ 配置系统
- ✅ 安全机制
- ✅ 性能优化
- ✅ 扩展机制

**总结**：OpenClaw 在 Agent 核心层面没有特别多新颖的地方，但作为一个完成度特别高的产品（24×7 运行的本地个人助手），其架构设计思想和扩展集成值得我们反复学习。

本文从核心交互流程出发，了解消息接入和分发链路，以及 SessionKey 的机制，一步一步深入 Agent 核心设计。了解到 Queue 如何解决复杂的并发消息问题，以及 OpenClaw 如何管理 session 文件解决短期记忆的持久化问题，如何通过记忆文件保存和检索长期记忆。

**下一章**：[第 5 章：技能开发进阶](./chapters/05-skill-development-advanced.md)

---

**参考资料**：
- 深度解析：一张图拆解 OpenClaw 的 Agent 核心设计 - 知乎
- OpenClaw 官方文档：https://docs.openclaw.ai

**本章完成时间**：2026-03-16
**最后更新**：2026-03-16
