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

## 1.3 接入飞书机器人（推荐）

OpenClaw 支持连接多个即时通讯平台，国内用户推荐使用**飞书**，可以在聊天中直接指挥 AI 干活。

### 1.3.1 创建飞书机器人

**步骤 1：进入飞书开发者后台**

1. 访问飞书开放平台：https://open.feishu.cn
2. 登录飞书账号（没有账号需要先注册）
3. 点击右上角 **开发者后台**

![飞书开放平台](../images/feishu-open-platform.jpg)

![飞书开发者后台入口](../images/feishu-developer-console.jpg)

**步骤 2：创建应用**

1. 点击 **创建应用**
2. 选择 **自建应用** → **企业自建**
3. 填写应用名称（如：OpenClaw 助手）
4. 点击 **创建**

![创建飞书应用](../images/feishu-create-app.jpg)

**步骤 3：获取应用凭证**

1. 进入 **凭证管理** 页面
2. 记录 **App ID** 和 **App Secret**

> ⚠️ 重要：App Secret 只显示一次，请立即保存！

![获取应用凭证](../images/feishu-credentials.jpg)

**步骤 4：添加机器人**

1. 进入 **添加机器人** 页面
2. 点击 **添加机器人**
3. 填写机器人名称（如：OpenClaw）
4. 点击 **保存**

**步骤 5：配置权限**

进入 **权限管理**，添加以下权限：
- `im:message` - 发送和接收消息
- `im:message:send` - 发送消息
- `im:file` - 访问文件
- `contact:contact` - 获取通讯录信息

![配置权限](../images/feishu-permissions.jpg)

**步骤 6：创建版本并发布**

1. 进入 **版本管理与发布**
2. 点击 **创建版本**
3. 填写版本号（如：1.0.0）
4. 提交审核
5. 审核通过后点击 **发布为在线应用**

**步骤 7：在飞书中审批**

1. 打开飞书客户端
2. 进入 **审批**
3. 找到应用发布审批，点击 **同意**

### 1.3.2 安装飞书插件

打开 PowerShell，执行：

```bash
# 安装飞书插件
openclaw plugins install @m1heng-clawd/feishu
```

### 1.3.3 配置飞书插件

1. 打开新的 PowerShell 窗口
2. 执行配置命令：

```bash
openclaw config
```

3. 按提示选择：
   - 配置项：**Feishu**
   - 输入 **App ID** 和 **App Secret**
   - 域名：**中国**
   - 接受群组聊天：**Yes**
   - 选择 **Open** → **Continue** → **完成**

### 1.3.4 重启服务

```bash
openclaw gateway restart
```

### 1.3.5 测试对话

1. 打开飞书客户端
2. 在联系人中找到刚才创建的机器人
3. 发送消息：`你好`
4. 机器人应该回复问候

---

## 1.4 你的第一个技能

### 1.4.1 查看可用技能

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

### 1.5.1 重要文件说明

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

## 1.6 常用命令

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

## 1.7 故障排查

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

## 1.8 下一步

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
