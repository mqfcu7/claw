# 第 3 章：常用技能详解

> 掌握核心技能，让 AI 助手发挥最大价值

---

## 3.1 搜索类技能

### 3.1.1 网络搜索技能

**技能名称**：`openclaw-tavily-search` / `web_search`

**功能**：使用 Tavily API 进行网络搜索，获取实时信息。

**使用场景**：
- 🔍 查找最新资讯
- 🔍 验证事实
- 🔍 收集研究资料
- 🔍 竞品分析

**基本用法**：

```
你：帮我搜索一下最新的 AI 大模型动态

AI：好的，我来搜索...

[调用 Tavily Search]

找到以下结果：

1. **OpenAI 发布 GPT-5**
   来源：TechCrunch
   摘要：OpenAI 今天发布了新一代大模型...
   链接：https://...

2. **Google DeepMind 新突破**
   来源：The Verge
   摘要：DeepMind 团队在...
   链接：https://...
```

**高级用法**：

```bash
# 限制结果数量
/search "AI 大模型" --count 3

# 限定时间范围
/search "AI 大模型" --freshness week

# 指定语言
/search "AI 大模型" --language zh-CN

# 指定地区
/search "AI 大模型" --country CN
```

**配置参数**：

| 参数 | 说明 | 默认值 |
|------|------|-------|
| `count` | 返回结果数量 | 5 |
| `freshness` | 时间范围 (day/week/month) | - |
| `language` | 语言代码 | zh-CN |
| `country` | 国家代码 | CN |

**配置 API 密钥**：

```bash
# 设置环境变量
export TAVILY_API_KEY=your-api-key

# 或在 Gateway 配置中添加
cat >> ~/.openclaw/gateway/config.json << 'EOF'
{
  "env": {
    "TAVILY_API_KEY": "your-api-key"
  }
}
EOF
```

**最佳实践**：

✅ **好的搜索词**：
- "2026 年 AI 大模型最新进展"
- "OpenAI GPT-5 发布 评测"
- "Kimi 融资 10 亿美元 详情"

❌ **避免的搜索词**：
- "AI"（太宽泛）
- "那个什么模型"（不明确）
- "最新的新闻"（缺少关键词）

---

### 3.1.2 本地文件搜索

**技能名称**：`search-files`

**功能**：在工作区中搜索文件。

**使用场景**：
- 📁 查找文档
- 📁 定位配置文件
- 📁 搜索代码文件

**基本用法**：

```
你：帮我找一下工作区里的新闻视频模板

AI：好的，我来搜索...

[搜索文件]

找到以下结果：

1. **news-video-template/**
   路径：~/workspace/templates/news-video-template/
   类型：目录
   修改时间：2026-03-16

2. **NewsVideoToday.tsx**
   路径：~/workspace/templates/news-video-template/src/
   类型：TypeScript 文件
   大小：20KB
```

**搜索技巧**：

```bash
# 按名称搜索
find ~/.openclaw/workspace -name "*news*"

# 按类型搜索
find ~/.openclaw/workspace -name "*.tsx"

# 按时间搜索（7 天内修改）
find ~/.openclaw/workspace -mtime -7
```

---

## 3.2 创作类技能

### 3.2.1 文章写作技能

**技能名称**：`blog-writer`

**功能**：帮助撰写博客文章、技术文档等。

**使用场景**：
- ✍️ 技术博客
- ✍️ 产品文档
- ✍️ 教程指南
- ✍️ 演讲稿

**基本用法**：

```
你：帮我写一篇关于 OpenClaw 技能开发的博客

AI：好的，我来帮你写...

[调用 blog-writer 技能]

# OpenClaw 技能开发入门

## 什么是 OpenClaw 技能？

OpenClaw 技能是扩展 AI 助手能力的模块...

## 第一个技能

创建一个简单的技能...

## 总结

通过本文，你学会了...
```

**文章结构模板**：

```markdown
# 标题

> 副标题或简介

## 引言
- 背景介绍
- 问题描述
- 解决方案

## 正文
### 第一部分
- 概念讲解
- 代码示例
- 图解说明

### 第二部分
- 实践步骤
- 注意事项
- 常见问题

## 总结
- 要点回顾
- 下一步行动
- 参考资料
```

**写作技巧**：

✅ **好的文章结构**：
- 清晰的标题层级
- 每段一个主题
- 代码示例配说明
- 图表辅助理解

❌ **避免的问题**：
- 大段文字无分段
- 缺少代码示例
- 没有实际案例

---

### 3.2.2 视频制作技能

**技能名称**：`modern-short-video`

**功能**：使用 Remotion 制作短视频。

**使用场景**：
- 🎬 产品宣传视频
- 🎬 新闻摘要视频
- 🎬 教程演示视频
- 🎬 社交媒体视频

**完整案例**：今天的 AI 新闻视频

**项目结构**：

```
news-daily-2026-03-16/
├── src/
│   ├── NewsVideoToday.tsx  # 视频组件
│   ├── Root.tsx            # 配置
│   └── index.tsx           # 入口
├── public/images/          # 素材图片
├── out/                    # 输出视频
└── package.json
```

**制作流程**：

```bash
# 1. 准备素材
# 收集新闻配图到 public/images/

# 2. 编写脚本
# 编辑 NewsVideoToday.tsx 中的 NEWS_ITEMS

# 3. 安装依赖
npm install

# 4. 渲染视频
npx remotion render src/index.tsx NewsVideo out/video.mp4 --codec=h264 --crf=18

# 5. 输出
# 视频保存到 out/video.mp4
```

**视频配置**：

```typescript
const NEWS_ITEMS = [
  {
    id: 1,
    tag: "标签",
    title: "主标题",
    subtitle: "副标题",
    highlight: "亮点",
    detail: "详细内容",
    highlights: ["关键词 1", "关键词 2"],
    color: "#E74C3C",
    image: staticFile('images/news1.jpg'),
    duration: 8, // 秒
  },
];
```

**渲染参数**：

| 参数 | 说明 | 推荐值 |
|------|------|-------|
| `--codec` | 视频编码 | h264 |
| `--crf` | 质量 (0-51) | 18 |
| `--fps` | 帧率 | 30 |
| `--resolution` | 分辨率 | 1080x1920 |

**优化技巧**：

✅ **提高质量**：
- 使用 CRF 15-18
- 图片素材用高清
- 文字大小适中

✅ **减小体积**：
- 使用 CRF 20-23
- 压缩图片素材
- 控制视频时长

---

### 3.2.3 文章配图技能

**技能名称**：`article-illustrator`

**功能**：为文章自动生成配图。

**使用场景**：
- 🎨 博客配图
- 🎨 社交媒体图片
- 🎨 演示文稿插图

**使用方法**：

```
你：给这篇文章配几张图：[文章内容]

AI：好的，我来分析文章结构...

[调用 article-illustrator]

已生成以下配图：

1. **封面图**
   主题：AI 科技
   风格：现代简约
   尺寸：1200x630

2. **插图 1**
   主题：技能开发
   风格：扁平化
   尺寸：800x600

3. **插图 2**
   主题：代码示例
   风格：深色主题
   尺寸：800x600
```

**配图原则**：

✅ **好的配图**：
- 与内容相关
- 风格统一
- 尺寸合适
- 版权清晰

❌ **避免的问题**：
- 图片与内容无关
- 风格杂乱
- 尺寸不匹配
- 版权不明

---

## 3.3 工具类技能

### 3.3.1 文件处理技能

**技能名称**：`read` / `write` / `edit`

**功能**：读取、写入、编辑文件。

**read - 读取文件**：

```
你：帮我读取一下 ~/Documents/notes.md

AI：好的...

[读取文件]

文件内容：
# 我的笔记

## 待办事项
- [ ] 完成第 3 章写作
- [ ] 更新技能文档
```

**write - 写入文件**：

```
你：创建一个新文件，内容是今天的会议纪要

AI：好的，我来创建...

[写入文件]

✅ 已创建：~/Documents/meeting-notes-2026-03-16.md
```

**edit - 编辑文件**：

```
你：把刚才那个文件的第一行改成"# 会议纪要"

AI：好的，我来修改...

[编辑文件]

✅ 已修改第 1 行
```

**最佳实践**：

✅ **安全操作**：
- 编辑前先备份
- 使用相对路径
- 确认文件内容

❌ **避免操作**：
- 直接修改系统文件
- 覆盖重要文件
- 使用绝对路径

---

### 3.3.2 命令执行技能

**技能名称**：`exec`

**功能**：执行 shell 命令。

**使用场景**：
- 💻 运行脚本
- 💻 文件操作
- 💻 系统管理
- 💻 自动化任务

**基本用法**：

```
你：帮我列出当前目录的文件

AI：好的...

[执行命令：ls -la]

total 48
drwxr-xr-x  7 user  staff   224 Mar 16 14:22 .
drwxr-xr-x 49 user  staff  1568 Mar 16 14:21 ..
-rw-r--r--  1 user  staff  2788 Mar 16 14:22 README.md
```

**常用命令**：

```bash
# 文件操作
ls -la          # 列出文件
cp file1 file2  # 复制文件
mv file1 dir/   # 移动文件
rm file         # 删除文件

# 目录操作
mkdir dir       # 创建目录
cd dir          # 进入目录
pwd             # 显示路径

# 系统信息
df -h           # 磁盘空间
top             # 进程信息
ps aux          # 进程列表
```

**安全警告**：

⚠️ **危险命令（不要执行）**：
```bash
rm -rf /        # 删除所有文件
sudo rm -rf /   # 超级用户删除
chmod 777 /     # 开放所有权限
```

✅ **安全做法**：
- 使用 `trash` 代替 `rm`
- 重要操作前确认
- 备份重要文件

---

### 3.3.3 数据分析技能

**技能名称**：`data-analysis`

**功能**：分析 CSV、Excel 等数据文件。

**使用场景**：
- 📊 销售数据分析
- 📊 用户行为分析
- 📊 财务报表
- 📊 调查结果

**基本用法**：

```
你：帮我分析一下这个销售数据

AI：好的，我来分析...

[读取并分析数据]

## 分析结果

### 总体情况
- 总销售额：¥1,234,567
- 订单数量：3,456
- 平均客单价：¥357

### 趋势分析
- 环比增长：+15.3%
- 同比增长：+28.7%

### Top 产品
1. 产品 A：¥234,567 (19%)
2. 产品 B：¥198,765 (16%)
3. 产品 C：¥156,789 (13%)
```

**可视化**：

```
你：把这些数据做成图表

AI：好的，我来生成...

[生成图表]

📊 销售趋势图
📈 产品占比饼图
📉 月度对比柱状图
```

---

## 3.4 生活类技能

### 3.4.1 天气查询技能

**技能名称**：`weather`

**功能**：查询天气信息。

**配置**：

```bash
# 设置 API 密钥
export WEATHER_API_KEY=your-key

# 或在配置文件中添加
{
  "env": {
    "WEATHER_API_KEY": "your-key"
  }
}
```

**基本用法**：

```
你：北京今天天气怎么样？

AI：好的，我来查询...

[查询天气]

## 北京天气 - 2026-03-16

🌤️ 天气：晴转多云
🌡️ 温度：15°C ~ 25°C
💨 风力：东北风 2-3 级
💧 湿度：45%
🌅 日出：06:32
🌇 日落：18:45

## 未来 3 天预报
- 明天：多云 16°C ~ 24°C
- 后天：小雨 14°C ~ 20°C
- 大后天：晴 15°C ~ 23°C
```

**配置选项**：

```json
{
  "default_city": "北京",
  "unit": "celsius",
  "show_forecast": true,
  "forecast_days": 3
}
```

---

### 3.4.2 提醒事项技能

**技能名称**：`apple-reminders` / `todo`

**功能**：管理待办事项。

**基本用法**：

```
你：提醒我明天上午 10 点开会

AI：好的，已创建提醒...

✅ 已添加：
📅 时间：2026-03-17 10:00
📝 事项：开会
🔔 提醒：提前 15 分钟
```

**常用命令**：

```bash
# 添加待办
remindctl add "买牛奶" --due tomorrow

# 查看待办
remindctl list

# 完成待办
remindctl complete "买牛奶"

# 删除待办
remindctl delete "买牛奶"
```

---

### 3.4.3 新闻推送技能

**技能名称**：`tech-news-daily`

**功能**：获取每日科技新闻。

**配置**：

```bash
# 设置 API 密钥
export TAVILY_API_KEY=your-key
```

**基本用法**：

```
你：今天的科技新闻

AI：好的，我来获取...

[调用 tech-news-daily]

## 今日科技资讯 Top 10

1. **OpenAI 发布 GPT-5**
   摘要：OpenAI 今天发布了新一代大模型...
   
2. **Google DeepMind 新突破**
   摘要：DeepMind 团队在...
   
...
```

**定时推送**：

```bash
# 在 HEARTBEAT.md 中添加
- 每天早上 8 点获取科技新闻
```

---

## 3.5 技能组合案例

### 案例 1：新闻视频自动化

**流程**：

```
1. tech-news-daily 获取新闻
   ↓
2. blog-writer 生成脚本
   ↓
3. modern-short-video 制作视频
   ↓
4. message 发送给用户
```

**实现**：

```typescript
// 伪代码
async function createNewsVideo() {
  // 1. 获取新闻
  const news = await techNewsDaily();
  
  // 2. 生成脚本
  const script = await blogWriter({
    topic: "AI 新闻",
    items: news
  });
  
  // 3. 制作视频
  const video = await modernShortVideo({
    script: script,
    images: news.images
  });
  
  // 4. 发送
  await message.send({
    to: user,
    video: video
  });
}
```

### 案例 2：数据分析报告

**流程**：

```
1. read 读取数据文件
   ↓
2. data-analysis 分析数据
   ↓
3. article-illustrator 生成图表
   ↓
4. blog-writer 撰写报告
   ↓
5. write 保存报告
```

---

## 3.6 技能选择指南

### 根据需求选择技能

| 需求 | 推荐技能 |
|------|---------|
| 查资料 | `web_search` |
| 写文章 | `blog-writer` |
| 做视频 | `modern-short-video` |
| 配图片 | `article-illustrator` |
| 查天气 | `weather` |
| 管文件 | `read`/`write`/`edit` |
| 跑脚本 | `exec` |
| 看新闻 | `tech-news-daily` |

### 技能组合建议

✅ **推荐组合**：
- `web_search` + `blog-writer` = 研究报告
- `tech-news-daily` + `modern-short-video` = 新闻视频
- `read` + `data-analysis` + `blog-writer` = 数据分析报告

❌ **避免组合**：
- 同时调用过多技能（响应慢）
- 循环调用技能（死循环）
- 技能间依赖混乱

---

## 本章小结

通过本章学习，你应该能够：
- ✅ 使用搜索类技能获取信息
- ✅ 使用创作类技能生成内容
- ✅ 使用工具类技能处理任务
- ✅ 使用生活类技能辅助日常
- ✅ 组合多个技能完成复杂任务

**下一章**：[第 4 章：技能开发基础](./04-skill-development-basics.md)

---

## 练习题

1. 使用 `web_search` 搜索今天的 AI 新闻
2. 使用 `blog-writer` 写一篇简短的技术文章
3. 使用 `weather` 查询你所在城市的天气
4. 组合使用 `read` + `edit` + `write` 修改一个文件

---

**本章完成时间**：2026-03-16
**最后更新**：2026-03-16
