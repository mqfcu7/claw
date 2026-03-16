# 第 2 章：技能使用基础

> 学会使用技能，让 AI 助手更强大

---

## 2.1 技能的类型

OpenClaw 技能分为三大类，了解类型有助于你更好地选择和使用技能。

### 2.1.1 内置技能

**定义**：OpenClaw 自带的技能，安装时自动包含。

**特点**：
- ✅ 无需额外安装
- ✅ 稳定性高
- ✅ 文档完善
- ⚠️ 功能相对基础

**常见内置技能**：

| 技能名称 | 功能 | 触发示例 |
|---------|------|---------|
| `read` | 读取文件 | "帮我看看这个文件" |
| `write` | 写入文件 | "创建一个新文件" |
| `edit` | 编辑文件 | "修改这段文字" |
| `exec` | 执行命令 | "运行这个脚本" |
| `browser` | 浏览器控制 | "打开这个网页" |

**使用示例**：

```
你：帮我读取一下 ~/Documents/notes.md 文件
AI：好的，我来读取这个文件...

[读取文件内容]

文件内容如下：
# 我的笔记
...
```

### 2.1.2 社区技能

**定义**：由社区开发者创建并发布的技能。

**特点**：
- ✅ 功能丰富多样
- ✅ 持续更新
- ✅ 可从 ClawHub 安装
- ⚠️ 质量参差不齐

**获取方式**：

```bash
# 搜索技能
openclaw skills search 天气

# 查看技能详情
openclaw skills info weather

# 安装技能
openclaw skills install weather
```

**热门社区技能**：

| 技能 | 功能 | 安装量 |
|------|------|--------|
| `weather` | 天气查询 | 10k+ |
| `tech-news-daily` | 科技新闻 | 5k+ |
| `video-frames` | 视频截图 | 3k+ |
| `article-illustrator` | 文章配图 | 2k+ |

### 2.1.3 自定义技能

**定义**：你自己开发或修改的技能。

**特点**：
- ✅ 完全定制化
- ✅ 满足特定需求
- ✅ 可分享给他人
- ⚠️ 需要开发能力

**开发流程**：

```bash
# 1. 创建技能目录
mkdir -p ~/.openclaw/workspace/skills/my-skill

# 2. 创建 SKILL.md
cat > ~/.openclaw/workspace/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: 我的自定义技能
allowed-tools: read, write, exec
---

# 技能说明
...
EOF

# 3. 测试技能
openclaw skills test my-skill
```

## 2.2 技能的调用方式

### 2.2.1 自然语言触发

**最常用**的方式，直接告诉 AI 你想做什么。

**示例**：

```
你：今天北京天气怎么样？
→ 触发 weather 技能

你：帮我搜一下最新的 AI 新闻
→ 触发 tech-news-daily 技能

你：给这篇文章配几张图
→ 触发 article-illustrator 技能
```

**技巧**：
- 📌 使用明确的动词（查询、搜索、创建、修改）
- 📌 提供具体参数（地点、时间、数量）
- 📌 避免模糊表达

### 2.2.2 命令触发

使用特定命令前缀直接调用技能。

**格式**：

```
/<技能名> [参数]
```

**示例**：

```bash
# 查询天气
/weather 北京

# 搜索新闻
/tech-news-daily --limit 5

# 视频截图
/video-frames ./video.mp4 --count 10
```

**优势**：
- ✅ 精确控制
- ✅ 可传递参数
- ✅ 适合自动化脚本

### 2.2.3 快捷键触发

为常用技能设置快捷键。

**配置方法**：

```json
// ~/.openclaw/config/settings.json
{
  "shortcuts": {
    "weather": "⌘W",
    "search": "⌘S",
    "news": "⌘N"
  }
}
```

**使用**：
- 按下 `⌘W` → 打开天气查询
- 按下 `⌘S` → 打开搜索
- 按下 `⌘N` → 获取新闻

## 2.3 技能配置

### 2.3.1 环境变量

某些技能需要 API 密钥等配置。

**设置方式**：

```bash
# 方式 1：Gateway 配置
openclaw configure --section env

# 方式 2：直接编辑配置文件
cat >> ~/.openclaw/gateway/config.json << 'EOF'
{
  "env": {
    "TAVILY_API_KEY": "your-api-key",
    "WEATHER_API_KEY": "your-weather-key"
  }
}
EOF

# 方式 3：临时设置（当前会话）
export TAVILY_API_KEY=your-api-key
```

**常见需要配置的技能**：

| 技能 | 环境变量 | 获取方式 |
|------|---------|---------|
| `weather` | `WEATHER_API_KEY` | openweathermap.org |
| `tavily-search` | `TAVILY_API_KEY` | tavily.com |
| `github` | `GITHUB_TOKEN` | github.com/settings/tokens |

### 2.3.2 配置文件

技能的个性化设置。

**示例**：`~/.openclaw/workspace/skills/weather/config.json`

```json
{
  "default_city": "北京",
  "unit": "celsius",
  "language": "zh-CN",
  "show_forecast": true,
  "forecast_days": 3
}
```

**配置项说明**：

| 配置项 | 说明 | 默认值 |
|-------|------|-------|
| `default_city` | 默认城市 | 北京 |
| `unit` | 温度单位 | celsius |
| `language` | 语言 | zh-CN |
| `show_forecast` | 显示预报 | true |
| `forecast_days` | 预报天数 | 3 |

### 2.3.3 API 密钥管理

**安全存储**：

```bash
# 使用密钥管理工具
openclaw secrets set WEATHER_API_KEY your-key

# 查看已存储的密钥（隐藏值）
openclaw secrets list

# 删除密钥
openclaw secrets delete WEATHER_API_KEY
```

**最佳实践**：
- 🔒 不要将密钥提交到 Git
- 🔒 使用环境变量或密钥管理工具
- 🔒 定期更换密钥
- 🔒 限制密钥权限

## 2.4 技能管理

### 2.4.1 启用/禁用技能

**查看已安装技能**：

```bash
openclaw skills list
```

**输出示例**：

```
已安装技能 (15 个):

✅ weather          v2.1.0    天气查询
✅ tech-news-daily  v1.5.0    科技新闻
✅ video-frames     v1.2.0    视频截图
❌ article-illustrator v1.0.0  文章配图 (已禁用)
```

**禁用技能**：

```bash
# 禁用单个技能
openclaw skills disable article-illustrator

# 启用技能
openclaw skills enable article-illustrator
```

**批量管理**：

```bash
# 禁用所有新闻类技能
openclaw skills disable --pattern "news-*"

# 启用所有技能
openclaw skills enable --all
```

### 2.4.2 更新技能

**检查更新**：

```bash
openclaw skills check-updates
```

**输出示例**：

```
发现 3 个可更新技能:

weather          v2.1.0 → v2.2.0  [重要更新]
tech-news-daily  v1.5.0 → v1.6.0  [功能增强]
video-frames     v1.2.0 → v1.2.1  [Bug 修复]
```

**更新技能**：

```bash
# 更新单个技能
openclaw skills update weather

# 更新所有技能
openclaw skills update --all

# 更新到特定版本
openclaw skills update weather@2.2.0
```

### 2.4.3 卸载技能

**卸载单个技能**：

```bash
openclaw skills uninstall weather
```

**卸载并清理配置**：

```bash
openclaw skills uninstall weather --purge
```

**批量卸载**：

```bash
# 卸载所有新闻类技能
openclaw skills uninstall --pattern "news-*"
```

**警告**：卸载前请确认：
- ⚠️ 没有正在进行的任务使用该技能
- ⚠️ 已备份相关配置文件
- ⚠️ 了解卸载后无法恢复

## 2.5 技能组合使用

### 2.5.1 链式调用

多个技能按顺序执行。

**示例**：获取新闻 → 生成摘要 → 发送给用户

```
你：获取今天的科技新闻，做个摘要发给我

AI: 好的，我来处理...

1️⃣ 调用 tech-news-daily 获取新闻
2️⃣ 调用 summarize 生成摘要
3️⃣ 调用 message 发送给你

✅ 完成！摘要已发送。
```

### 2.5.2 条件触发

根据条件选择技能。

**示例**：

```
如果提到"天气" → 调用 weather
如果提到"新闻" → 调用 tech-news-daily
如果提到"视频" → 调用 video-frames
```

### 2.5.3 并行执行

同时执行多个技能。

**示例**：

```
你：同时查询北京、上海、广州的天气

AI: 好的，我同时查询三个城市...

[并行调用 weather 技能 3 次]

北京：晴 25°C
上海：多云 23°C
广州：小雨 28°C
```

## 2.6 故障排查

### 2.6.1 技能无法触发

**症状**：说话后技能没有反应。

**排查步骤**：

```bash
# 1. 检查技能是否已安装
openclaw skills list | grep <skill-name>

# 2. 检查技能是否已启用
openclaw skills status <skill-name>

# 3. 查看技能日志
openclaw logs --skill <skill-name>

# 4. 测试技能
openclaw skills test <skill-name>
```

**常见原因**：
- ❌ 技能未安装
- ❌ 技能已禁用
- ❌ 触发词不匹配
- ❌ API 密钥缺失

### 2.6.2 技能执行错误

**症状**：技能执行失败，报错。

**排查步骤**：

```bash
# 查看详细错误
openclaw logs --level error --skill <skill-name>

# 检查依赖
openclaw skills check-deps <skill-name>

# 重新安装
openclaw skills reinstall <skill-name>
```

**常见错误**：

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `API key missing` | 缺少 API 密钥 | 配置环境变量 |
| `Network error` | 网络问题 | 检查网络连接 |
| `Permission denied` | 权限不足 | 检查文件权限 |
| `Timeout` | 超时 | 增加超时时间 |

### 2.6.3 性能问题

**症状**：技能响应慢。

**优化方法**：

```bash
# 1. 清理缓存
openclaw skills cache clear

# 2. 检查资源占用
openclaw status --resource

# 3. 优化配置
# 编辑技能配置文件，调整参数
```

## 2.7 最佳实践

### ✅ 推荐做法

1. **明确表达需求**
   - ❌ "帮我查一下"
   - ✅ "帮我查北京今天的天气"

2. **合理配置技能**
   - 设置默认参数
   - 配置 API 密钥
   - 调整超时时间

3. **定期更新技能**
   - 每周检查更新
   - 及时安装安全补丁

4. **备份配置**
   - 定期备份配置文件
   - 使用版本控制

### ❌ 避免做法

1. **不要硬编码密钥**
   ```javascript
   // ❌ 错误
   const API_KEY = "sk-123456";
   
   // ✅ 正确
   const API_KEY = process.env.API_KEY;
   ```

2. **不要同时启用过多技能**
   - 只启用需要的技能
   - 禁用不常用的技能

3. **不要忽略错误提示**
   - 仔细阅读错误信息
   - 及时排查问题

---

## 2.8 定时任务：让 AI 自动干活

OpenClaw 的定时任务系统让你可以设置 AI 自动执行任务，不需要每次都开口问。

### 2.8.1 两套机制

OpenClaw 有两套定时任务机制：**Heartbeat（心跳）** 和 **Cron（定时调度）**。

**Heartbeat 心跳**：
- 每 30 分钟触发一次（可配置）
- 读取 `HEARTBEAT.md` 检查清单
- 没事就安静，有事就通知
- 适合：定期检查、轻量监控

**Cron 定时调度**：
- 精确时间触发（如每天早上 9 点）
- 支持三种触发方式：`at`、`every`、`cron`
- 适合：准时触发的任务

### 2.8.2 Heartbeat 心跳：AI 的「自觉性」

**心跳是什么？**

想象你有个助理，每 30 分钟自己抬头看看有没有什么需要处理的事。没事就安静坐着，有事就主动找你。这就是 Heartbeat。

**心跳工作流程**：

1. OpenClaw 每 30 分钟触发一次心跳
2. AI 读取 `HEARTBEAT.md` 检查清单
3. 按清单逐项检查
4. 如果什么都不用做，回复 `HEARTBEAT_OK`（你完全无感）
5. 如果发现重要事项，直接发消息通知你

**实战：HEARTBEAT.md 示例**

```markdown
# 每日检查清单

- 检查邮箱有没有紧急邮件
- 看看日历上接下来 2 小时有没有会议
- 如果今天的公众号文章还没生成，开始写
- 如果超过 8 小时没互动，发个轻松的 check-in
```

就这么简单。一个 Markdown 文件，用人话写。AI 每 30 分钟读一遍，自己判断该干什么。

**配置心跳**

在 OpenClaw 配置文件里加几行：

```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "30m",           // 每 30 分钟一次
        "target": "last",         // 发到你最近用的聊天渠道
        "activeHours": {
          "start": "08:00",       // 早 8 点开始
          "end": "22:00"          // 晚 10 点结束（别半夜吵你）
        }
      }
    }
  }
}
```

**关键细节**：`activeHours` 让你设定「工作时间」。凌晨 3 点不会有心跳跳出来问你「需要帮忙吗？」。

**心跳适合什么场景？**

| 场景 | 为什么选心跳 |
|------|-------------|
| 定期检查邮箱 | 和其他检查打包一起做，省 token |
| 日历提醒 | 需要上下文判断是否紧急 |
| 待办跟进 | AI 记得你之前聊过什么 |
| 轻量监控 | 一次心跳搞定多个检查项 |

**核心优势**：一次心跳 = 一次 AI 调用，同时检查 5 件事。比分别设 5 个定时任务便宜得多。

### 2.8.3 Cron 定时调度：精确到分钟的自动化

**心跳不够用的时候**

心跳有个特点——它的时间不是精确的。说好的 30 分钟，实际可能是 28 分钟或 33 分钟。

如果你需要「**每天早上 9 点整**发日报」「**每周一 10 点整**发周报」，就需要 Cron。

**Cron 支持三种触发方式**：

1. **`at`**：在某个精确时间点执行一次（比如「20 分钟后提醒我」）
2. **`every`**：固定间隔重复（比如「每 2 小时」）
3. **`cron`**：标准 cron 表达式（比如「每周一早上 9 点」）

**实战案例 1：每天早上 9 点自动发日报**

```bash
openclaw cron add \
  --name "每日早报" \
  --cron "0 9 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "生成今天的早报：天气、日历安排、重要邮件摘要、AI 行业新闻。" \
  --announce \
  --channel telegram
```

拆解一下：
- `--cron "0 9 * * *"`：每天 9:00 触发
- `--tz "America/Los_Angeles"`：按洛杉矶时间（避免时区坑）
- `--session isolated`：在独立会话中运行（不污染主对话）
- `--announce`：把结果自动发到你的聊天软件

每天早上 9 点，你的 Telegram 自动收到一条定制化的早报。不用开口问。

**实战案例 2：20 分钟后提醒开会**

```bash
openclaw cron add \
  --name "开会提醒" \
  --at "20m" \
  --session main \
  --system-event "提醒：产品评审会 10 分钟后开始。" \
  --wake now \
  --delete-after-run
```

这是一次性提醒。执行完自动删除，干净利落。

**实战案例 3：每周一生成项目周报**

```bash
openclaw cron add \
  --name "周报" \
  --cron "0 10 * * 1" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "回顾本周完成的所有任务，生成一份结构化的项目周报，包含进展、风险和下周计划。" \
  --model opus \
  --announce \
  --channel telegram
```

注意这里用了 `--model opus`——周报需要更深度的思考，可以指定用更强的模型。日常小任务用便宜的模型，重要任务用好模型。**按需调配，精打细算。**

### 2.8.4 Heartbeat vs Cron：怎么选？

**决策树**：

```
需要精确时间？
→ 是 → 用 Cron
→ 否 → 继续...

需要独立于主对话运行？
→ 是 → 用 Cron（isolated）
→ 否 → 继续...

能和其他检查打包一起？
→ 是 → 用 Heartbeat（写进 HEARTBEAT.md）
→ 否 → 用 Cron

需要不同的 AI 模型？
→ 是 → 用 Cron（isolated + --model）
→ 否 → 用 Heartbeat
```

**经验法则**：日常监控用心跳，精确触发用 Cron。**两者组合用效果最好。**

比如作者的配置：
- **Heartbeat**：每 30 分钟检查邮箱、日历、公众号任务状态
- **Cron 每日 7:00**：生成早报（isolated，用 opus 模型）
- **Cron 每周一 10:00**：生成周报

心跳管日常，Cron 管精确。各司其职。

### 2.8.5 进阶玩法

**1. 多渠道分发**

同一个定时任务的结果，可以发到不同渠道：

```bash
# 发到 Telegram
openclaw cron add --name "日报-TG" --cron "0 9 * * *" \
  --session isolated --message "生成日报" \
  --announce --channel telegram

# 发到 WhatsApp 群
openclaw cron add --name "日报-WA" --cron "0 9 * * *" \
  --session isolated --message "生成团队日报" \
  --announce --channel whatsapp --to "+8613800138000"
```

**2. 给不同 Agent 分配不同任务**

如果你跑了多个 Agent，可以用 `--agent` 参数指定：

```bash
openclaw cron add --name "内容日报" \
  --agent content \
  --cron "0 9 * * *" \
  --session isolated \
  --message "检查今天的内容计划并执行"
```

内容 Agent 管写作，运营 Agent 管数据，开发 Agent 管代码检查。**每个 Agent 都有自己的定时任务，互不干扰。**

**3. 一次性提醒的妙用**

别小看 `--at` 这个一次性任务。它是最实用的功能之一：

- 「30 分钟后提醒我回复那封邮件」
- 「明天早上 8 点提醒我给客户打电话」
- 「下周三下午 2 点提醒我续费服务器」

你可以直接在对话中让 AI 帮你设置，不用自己写命令。说一句「20 分钟后提醒我开会」，AI 自己就会调用 Cron 工具。

### 2.8.6 避坑指南

**坑 1：时区问题**

**永远显式设置时区。**不设时区，默认用服务器时区（通常是 UTC）。你以为的「早上 9 点」可能是凌晨 1 点。

```bash
# ✅ 正确：指定时区
--tz "Asia/Shanghai"

# ❌ 危险：不指定时区
--cron "0 9 * * *"  # 这是 UTC 的 9 点！
```

**坑 2：心跳太频繁**

默认 30 分钟一次就够了。如果你设成 5 分钟一次，token 费用会飙升，而且大部分心跳的结果都是「没什么事」。

**坑 3：Main vs Isolated 没选对**

- **Main session**：共享对话上下文，适合需要「记得之前聊过什么」的任务
- **Isolated session**：干净的独立环境，每次从零开始，适合独立任务

周报用 isolated（不需要知道你今天聊了什么），提醒用 main（需要打断当前对话流）。

**坑 4：忘记 `--delete-after-run`**

一次性任务如果不加这个参数，执行完会留在任务列表里（虽然会自动禁用）。虽然不影响功能，但时间长了列表会越来越乱。好消息是 `--at` 类型默认就会自动删除。

---

## 本章小结

通过本章学习，你应该能够：
- ✅ 区分三种技能类型
- ✅ 使用三种方式调用技能
- ✅ 配置技能的环境变量和参数
- ✅ 管理技能的生命周期
- ✅ 排查常见问题

**下一章**：[第 3 章：常用技能详解](./03-common-skills.md)

---

## 练习题

1. 安装一个天气技能并配置 API 密钥
2. 使用三种不同方式调用天气技能
3. 禁用一个技能，然后再启用它
4. 检查并更新所有已安装的技能

---

**本章完成时间**：2026-03-16
**最后更新**：2026-03-16
