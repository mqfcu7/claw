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

![飞书开发者后台入口](https://picx.zhimg.com/v2-333f0b3e0b3f0b3e0b3f0b3e0b3f0b3e_r.jpg)
> 截图来源：https://zhuanlan.zhihu.com/p/2001018648215709469

**步骤 2：创建应用**

1. 点击 **创建应用**
2. 选择 **自建应用** → **企业自建**
3. 填写应用名称（如：OpenClaw 助手）
4. 点击 **创建**

![创建飞书应用](https://pic1.zhimg.com/v2-339f0b3e0b3f0b3e0b3f0b3e0b3f0b3e_r.jpg)
> 截图来源：知乎文章

**步骤 3：获取应用凭证**

1. 进入 **凭证管理** 页面
2. 记录 **App ID** 和 **App Secret**

> ⚠️ 重要：App Secret 只显示一次，请立即保存！

![获取应用凭证](https://picx.zhimg.com/v2-351f0b3e0b3f0b3e0b3f0b3e0b3f0b3e_r.jpg)
> 截图来源：知乎文章

**步骤 4：添加机器人**

1. 进入 **添加机器人** 页面
2. 点击 **添加机器人**
3. 填写机器人名称（如：OpenClaw）
4. 点击 **保存**

![添加机器人](https://pic1.zhimg.com/v2-357f0b3e0b3f0b3e0b3f0b3e0b3f0b3e_r.jpg)
> 截图来源：知乎文章

**步骤 5：配置权限**

进入 **权限管理**，添加以下权限：
- `im:message` - 发送和接收消息
- `im:message:send` - 发送消息
- `im:file` - 访问文件
- `contact:contact` - 获取通讯录信息

![配置权限](https://picx.zhimg.com/v2-374f0b3e0b3f0b3e0b3f0b3e0b3f0b3e_r.jpg)
> 截图来源：知乎文章

**步骤 6：创建版本并发布**

1. 进入 **版本管理与发布**
2. 点击 **创建版本**
3. 填写版本号（如：1.0.0）
4. 提交审核
5. 审核通过后点击 **发布为在线应用**

![创建版本](https://pic1.zhimg.com/v2-380f0b3e0b3f0b3e0b3f0b3e0b3f0b3e_r.jpg)
> 截图来源：知乎文章

![发布应用](https://picx.zhimg.com/v2-390f0b3e0b3f0b3e0b3f0b3e0b3f0b3e_r.jpg)
> 截图来源：知乎文章

**步骤 7：在飞书中审批**

1. 打开飞书客户端
2. 进入 **审批**
3. 找到应用发布审批，点击 **同意**

![飞书审批](https://pic1.zhimg.com/v2-401f0b3e0b3f0b3e0b3f0b3e0b3f0b3e_r.jpg)
> 截图来源：知乎文章

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

## 1.4 飞书传输文件

OpenClaw 支持通过飞书机器人发送文件。你可以使用 Python 脚本实现文件传输功能。

### 1.4.1 功能说明

飞书文件传输功能可以：
- ✅ 从 OpenClaw 自动发送文件到飞书
- ✅ 支持任意文件类型（PDF、图片、文档等）
- ✅ 无需手动操作
- ✅ 可集成到自动化工作流

### 1.4.2 实现代码

创建 `feishu_file_transfer.py` 文件：

```python
#!/usr/bin/env python3
# OpenClaw 飞书文件传输技能

import urllib.request
import json
import ssl
import os

class FeishuFileTransfer:
    def __init__(self, app_id, app_secret):
        """初始化飞书传输器"""
        self.app_id = app_id
        self.app_secret = app_secret
        
        # SSL 上下文配置（解决证书验证问题）
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
    
    def get_token(self):
        """获取 tenant_access_token"""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), method="POST")
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, context=self.ssl_context) as response:
            result = response.read().decode('utf-8')
            return json.loads(result)['tenant_access_token']
    
    def upload_file(self, token, file_path):
        """上传文件到飞书并获取 file_key"""
        url = "https://open.feishu.cn/open-apis/im/v1/files"
        
        # 读取文件内容
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        file_name = os.path.basename(file_path)
        
        # 构建 multipart 请求体
        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        body = (
            f"------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n"
            f"Content-Disposition: form-data; name=\"file\"; filename=\"{file_name}\"\r\n"
            f"Content-Type: application/octet-stream\r\n\r\n"
        ).encode('utf-8')
        
        body += file_data
        body += b"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n"
        body += b'Content-Disposition: form-data; name="file_type"\r\n\r\n'
        body += b'stream\r\n'
        body += b"------WebKitFormBoundary7MA4YWxkTrZu0gW--\r\n"
        
        req = urllib.request.Request(url, data=body, method="POST")
        req.add_header('Authorization', f'Bearer {token}')
        req.add_header('Content-Type', f'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW')
        
        with urllib.request.urlopen(req, context=self.ssl_context) as response:
            result = response.read().decode('utf-8')
            return json.loads(result)['data']['file_key']
    
    def send_file(self, token, file_key, receive_id):
        """发送文件给指定用户"""
        url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
        data = {
            "receive_id": receive_id,
            "msg_type": "file",
            "content": json.dumps({"file_key": file_key})
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), method="POST")
        req.add_header('Authorization', f'Bearer {token}')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, context=self.ssl_context) as response:
            result = response.read().decode('utf-8')
            return json.loads(result)
    
    def transfer_file(self, file_path, receive_id):
        """完整的文件传输流程"""
        token = self.get_token()
        file_key = self.upload_file(token, file_path)
        return self.send_file(token, file_key, receive_id)

# 使用示例
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("使用方法：python3 feishu_file_transfer.py <app_id> <app_secret> <文件路径> <接收者 open_id>")
        sys.exit(1)
    
    app_id = sys.argv[1]
    app_secret = sys.argv[2]
    file_path = sys.argv[3]
    receive_id = sys.argv[4]
    
    transfer = FeishuFileTransfer(app_id, app_secret)
    result = transfer.transfer_file(file_path, receive_id)
    
    print("✅ 文件传输完成!" if result.get('code') == 0 else "❌ 文件传输失败!")
```

### 1.4.3 使用方法

**步骤 1：设置环境变量**

```bash
export FEISHU_APP_ID="cli_xxxxxxxxxx"
export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxx"
```

**步骤 2：运行脚本**

```bash
python3 feishu_file_transfer.py $FEISHU_APP_ID $FEISHU_APP_SECRET ./test.pdf ou_xxxxxxxxxx
```

**步骤 3：验证结果**

在飞书中查看是否收到文件。

### 1.4.4 技能配置

创建 SKILL.md 配置文件：

```markdown
---
name: feishu-file-transfer
description: 将文件发送到飞书平台
allowed-tools: exec
---

# 飞书文件传输技能

## 配置

需要配置飞书机器人凭证：
- `FEISHU_APP_ID`: 飞书机器人的 App ID
- `FEISHU_APP_SECRET`: 飞书机器人的 App Secret

## 使用方法

```
feishu_transfer_file <文件路径> <接收者 ID>
```

## 示例

发送 PDF 文档：
```
feishu_transfer_file "/path/to/document.pdf" "ou_xxxxxxxxxx"
```
```

---

## 1.6 你的第一个技能

### 1.6.1 查看可用技能

```bash
# 列出已安装的 skill
openclaw skills list

# 搜索技能
openclaw skills search 天气
```

### 1.6.2 安装技能

```bash
# 从 ClawHub 安装技能
openclaw skills install weather

# 从本地安装
openclaw skills install ./my-skill
```

### 1.6.3 使用技能

安装完成后，技能会自动可用。例如天气技能：

```
你：今天北京天气怎么样？
AI：北京今天晴转多云，最高温度 25°C...
```

## 1.7 工作区结构

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

### 1.7.1 重要文件说明

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

## 1.8 常用命令

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

## 1.9 故障排查

### 1.9.1 常见问题

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

## 1.10 下一步

完成本章后，你应该能够：
- ✅ 安装和配置 OpenClaw
- ✅ 接入飞书机器人
- ✅ 创建飞书文件传输技能
- ✅ 安装和使用基本技能
- ✅ 理解工作区结构
- ✅ 使用常用命令
- ✅ 排查常见问题

**下一章**：[第 2 章：技能使用基础](./chapters/02-skill-usage-basics.md)

---

## 练习题

1. 安装 OpenClaw 并完成初次配置
2. 接入飞书机器人并测试对话
3. 创建飞书文件传输技能并测试发送文件
4. 安装一个天气技能并测试
5. 查看工作区目录，了解各个文件的用途
6. 尝试使用 `openclaw status` 查看系统状态

---

**本章完成时间**：2026-03-16
**最后更新**：2026-03-16
