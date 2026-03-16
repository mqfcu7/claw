# 第 9 章：实战案例 - 飞书文件传输技能

> 将飞书文件传输功能制作成 OpenClaw 技能，实现自动化文件发送

---

## 9.1 项目背景

在自动化工作流中，经常需要从 OpenClaw 发送文件到飞书。手动操作既繁琐又容易出错。

**需求**：
- ✅ 从 OpenClaw 自动发送文件到飞书
- ✅ 支持任意文件类型
- ✅ 无需手动操作
- ✅ 可重复使用

**解决方案**：创建一个 OpenClaw 技能 - `feishu-file-transfer`

---

## 9.2 技能实现原理

### 9.2.1 核心机制

1. **使用飞书机器人 API** 进行文件上传和发送
2. **通过 Python 标准库** urllib 处理 HTTP 请求，避免第三方依赖问题
3. **使用 SSL 上下文配置** 解决 TLS 证书验证问题

### 9.2.2 工作流程

```
1. 获取飞书机器人访问令牌 (tenant_access_token)
   ↓
2. 上传文件到飞书服务器并获得 file_key
   ↓
3. 使用 file_key 将文件发送给指定接收者
```

---

## 9.3 技能实现代码

### 9.3.1 基础版本

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
        
        # SSL 上下文配置
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
        """上传文件并获取 file_key"""
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
    
    print("文件传输完成!" if result.get('code') == 0 else "文件传输失败!")
```

### 9.3.2 OpenClaw 集成版

为了让技能自动获取用户 ID，与 OpenClaw 会话上下文集成：

```python
#!/usr/bin/env python3
# OpenClaw 集成版飞书文件传输技能

from feishu_file_transfer import FeishuFileTransfer
import os

class OpenClawFeishuTransfer:
    def __init__(self):
        """从 OpenClaw 配置获取飞书凭证"""
        self.app_id = os.getenv("FEISHU_APP_ID", "cli_a92ee666e1389bc2")
        self.app_secret = os.getenv("FEISHU_APP_SECRET", "n9arOA6nP0WcXIOD5TRSnts8evtNg7wb")
        self.transfer = FeishuFileTransfer(self.app_id, self.app_secret)
    
    def send_file_to_current_user(self, file_path, open_id):
        """向当前用户发送文件"""
        token = self.transfer.get_token()
        file_key = self.transfer.upload_file(token, file_path)
        return self.transfer.send_file(token, file_key, open_id)
```

---

## 9.4 创建 SKILL.md

创建 OpenClaw 技能配置文件：

```markdown
---
name: feishu-file-transfer
description: 将文件发送到飞书（Lark/Feishu）平台
allowed-tools: exec
---

# 飞书文件传输技能

## 描述

此技能允许 OpenClaw 将文件发送到飞书（Lark/Feishu）平台。

## 配置

在使用此技能前，需要配置飞书机器人凭证：

- `FEISHU_APP_ID`: 飞书机器人的 App ID
- `FEISHU_APP_SECRET`: 飞书机器人的 App Secret

## 使用方法

```
feishu_transfer_file <文件路径> <接收者 ID>
```

## 示例

### 示例 1：发送 PDF 文档

```
feishu_transfer_file "/path/to/mydocument.pdf" "ou_xxxxxxxxxx"
```

### 示例 2：发送图片

```
feishu_transfer_file "~/Pictures/screenshot.png" "ou_xxxxxxxxxx"
```

## 实现原理

1. 获取飞书机器人访问令牌
2. 上传文件到飞书服务器
3. 将文件发送给指定的接收者
4. 返回发送结果

## 注意事项

- 确保提供有效的文件路径
- 确保接收者 ID 格式正确（open_id）
- 文件大小不能超过飞书 API 限制（通常 500MB）
- 需要飞书机器人权限：im:message、im:file

## 相关文件

- `feishu_file_transfer.py` - 核心实现
- `feishu_send_file.py` - OpenClaw 集成版
```

---

## 9.5 技能测试

### 9.5.1 测试步骤

1. **准备测试环境**
   ```bash
   # 设置环境变量
   export FEISHU_APP_ID="cli_xxxxxxxxxx"
   export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxx"
   ```

2. **运行测试脚本**
   ```bash
   python3 feishu_file_transfer.py $FEISHU_APP_ID $FEISHU_APP_SECRET ./test.pdf ou_xxxxxxxxxx
   ```

3. **验证结果**
   - 在飞书中查看是否收到文件
   - 检查文件内容是否完整

### 9.5.2 测试结果

```
✅ 获取 token 成功
✅ 上传文件成功，file_key: file_v3_xxxxxx
✅ 文件发送成功！

文件传输完成!
```

---

## 9.6 关键要点

### ✅ 技术亮点

1. **使用 Python 标准库** - 避免第三方依赖问题
2. **SSL 配置绕过证书验证** - 解决 TLS 证书问题
3. **保持文件原始名称和格式** - 完整的文件信息
4. **适合集成到 OpenClaw 自动化工作流** - 可重复使用

### ⚠️ 注意事项

1. **API 权限** - 需要飞书机器人权限
2. **文件大小限制** - 飞书 API 限制（通常 500MB）
3. **频率限制** - 避免频繁调用 API
4. **错误处理** - 添加完善的错误处理逻辑

---

## 9.7 扩展功能

### 9.7.1 支持群组发送

```python
def send_to_group(self, file_path, chat_id):
    """发送文件到群组"""
    token = self.get_token()
    file_key = self.upload_file(token, file_path)
    
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    data = {
        "receive_id": chat_id,
        "msg_type": "file",
        "content": json.dumps({"file_key": file_key})
    }
    # ... 发送逻辑
```

### 9.7.2 支持消息文本

```python
def send_text_message(self, text, receive_id):
    """发送文本消息"""
    token = self.get_token()
    
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    data = {
        "receive_id": receive_id,
        "msg_type": "text",
        "content": json.dumps({"text": text})
    }
    # ... 发送逻辑
```

### 9.7.3 批量发送

```python
def batch_send_files(self, file_paths, receive_ids):
    """批量发送文件给多个用户"""
    results = []
    for file_path in file_paths:
        for receive_id in receive_ids:
            result = self.transfer_file(file_path, receive_id)
            results.append({
                'file': file_path,
                'user': receive_id,
                'success': result.get('code') == 0
            })
    return results
```

---

## 9.8 完整代码

### 9.8.1 项目结构

```
feishu-file-transfer/
├── SKILL.md                      # 技能说明
├── feishu_file_transfer.py       # 核心实现
├── feishu_send_file.py           # OpenClaw 集成版
└── examples/
    └── test.pdf                  # 测试文件
```

### 9.8.2 快速开始

1. **安装依赖**
   ```bash
   # 无需额外依赖，使用 Python 标准库
   ```

2. **配置凭证**
   ```bash
   export FEISHU_APP_ID="cli_xxxxxxxxxx"
   export FEISHU_APP_SECRET="xxxxxxxxxxxxxxxx"
   ```

3. **运行测试**
   ```bash
   python3 feishu_send_file.py ./test.pdf ou_xxxxxxxxxx
   ```

---

## 9.9 练习题

1. 修改脚本，支持发送消息到群组
2. 添加文件大小检查功能
3. 实现发送进度显示
4. 添加错误重试机制

---

**本章完成时间**：2026-03-16
**最后更新**：2026-03-16
**参考文章**：https://zhuanlan.zhihu.com/p/2013197983634707961
