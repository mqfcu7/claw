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
