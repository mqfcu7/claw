# 第 1 章：OpenClaw 入门

> 从零开始，认识 OpenClaw，安装你的第一个技能

---

## 1.1 什么是 OpenClaw？

OpenClaw 是一个强大的 AI 助手框架，它允许你：
- 🤖 **连接多个 AI 模型**：支持多种主流 AI 模型
- 🛠️ **扩展技能**：通过技能系统无限扩展能力
- 📱 **多平台支持**：飞书、微信、Discord 等
- 🔌 **插件生态**：丰富的插件和工具集成

### 1.1.1 核心概念

**技能（Skill）**：
- 是 OpenClaw 的能力扩展单元
- 每个技能完成特定任务
- 可以安装、卸载、更新

**会话（Session）**：
- 你与 AI 助手的对话上下文
- 支持多会话并行

**工作区（Workspace）**：
- 你的技能和配置文件存放位置
- 默认在 `~/.openclaw/workspace`

## 1.2 安装 OpenClaw

### 1.2.1 系统要求

- **操作系统**：macOS、Linux、Windows
- **Node.js**：v18 或更高版本
- **内存**：至少 4GB
- **磁盘**：至少 1GB 可用空间

### 1.2.2 安装步骤

```bash
# 1. 安装 Node.js（如未安装）
# macOS
brew install node

# Linux
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 2. 安装 OpenClaw
npm install -g openclaw@latest

# 3. 验证安装
openclaw --version
```

### 1.2.3 初次配置

```bash
# 运行配置向导
openclaw configure
```

配置过程中需要设置：
1. **API 密钥**：AI 模型的访问密钥
2. **工作区路径**：技能和文件的存放位置
3. **消息平台**：选择要连接的消息平台

## 1.3 你的第一个技能

### 1.3.1 查看可用技能

```bash
# 列出已安装的 skill
openclaw skills list

# 搜索技能
openclaw skills search 天气
```

### 1.3.2 安装技能

```bash
# 从 ClawHub 安装技能
openclaw skills install weather

# 从本地安装
openclaw skills install ./my-skill
```

### 1.3.3 使用技能

安装完成后，技能会自动可用。例如天气技能：

```
你：今天北京天气怎么样？
AI：北京今天晴转多云，最高温度 25°C...
```

## 1.4 工作区结构

OpenClaw 工作区的标准结构：

```
~/.openclaw/workspace/
├── skills/           # 技能目录
├── memory/           # 记忆文件
├── MEMORY.md         # 长期记忆
├── SOUL.md          # AI 人格配置
├── USER.md          # 用户信息
├── HEARTBEAT.md     # 定期任务
└── TOOLS.md         # 工具配置
```

### 1.4.1 重要文件说明

**SOUL.md**：
- 定义 AI 助手的人格和语气
- 设置行为准则和边界

**USER.md**：
- 记录用户信息
- 偏好和习惯

**MEMORY.md**：
- 长期记忆存储
- 重要事件和决策

**HEARTBEAT.md**：
- 定期执行的任务清单
- 提醒和检查项

## 1.5 常用命令

```bash
# 查看状态
openclaw status

# 启动网关
openclaw gateway start

# 停止网关
openclaw gateway stop

# 查看日志
openclaw logs

# 帮助
openclaw help
```

## 1.6 故障排查

### 1.6.1 常见问题

**问题 1：技能无法安装**
```bash
# 检查网络连接
ping clawhub.com

# 清除缓存
openclaw skills cache clear

# 重试安装
openclaw skills install <skill-name>
```

**问题 2：网关无法启动**
```bash
# 检查端口占用
lsof -i :8080

# 查看错误日志
openclaw logs --level error

# 重启网关
openclaw gateway restart
```

**问题 3：API 密钥错误**
```bash
# 重新配置
openclaw configure --section api

# 验证密钥
openclaw api test
```

## 1.7 下一步

完成本章后，你应该能够：
- ✅ 安装和配置 OpenClaw
- ✅ 安装和使用基本技能
- ✅ 理解工作区结构
- ✅ 使用常用命令

**下一章**：[第 2 章：技能使用基础](./chapters/02-skill-usage-basics.md)

---

## 练习题

1. 安装 OpenClaw 并完成初次配置
2. 安装一个天气技能并测试
3. 查看工作区目录，了解各个文件的用途
4. 尝试使用 `openclaw status` 查看系统状态

---

**本章完成时间**：待完成
**最后更新**：2026-03-16
