# 第 7 章：最佳实践

> 学习技能开发的最佳实践，编写高质量、可维护的技能

---

## 7.1 代码组织

### 7.1.1 模块化设计

**将技能拆分为模块**：

```
my-skill/
├── SKILL.md
├── src/
│   ├── __init__.py
│   ├── main.py          # 主逻辑
│   ├── utils.py         # 工具函数
│   ├── api.py           # API 调用
│   └── config.py        # 配置管理
├── scripts/
│   └── run.py
└── tests/
    └── test_skill.py
```

**模块示例**：

```python
# src/utils.py
def format_date(date):
    """格式化日期"""
    return date.strftime("%Y-%m-%d")

def validate_input(data):
    """验证输入"""
    if not data:
        raise ValueError("输入不能为空")
    return True

# src/api.py
def fetch_data(endpoint):
    """API 调用"""
    response = requests.get(endpoint)
    return response.json()

# src/main.py
from .utils import format_date, validate_input
from .api import fetch_data

def process(data):
    """主处理函数"""
    validate_input(data)
    result = fetch_data(data['endpoint'])
    return format_date(result['date'])
```

### 7.1.2 代码复用

**提取公共函数**：

```python
# ❌ 重复代码
def get_weather_beijing():
    response = requests.get(f"{BASE_URL}/beijing?key={API_KEY}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_weather_shanghai():
    response = requests.get(f"{BASE_URL}/shanghai?key={API_KEY}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# ✅ 复用代码
def get_weather(city):
    """获取城市天气"""
    response = requests.get(f"{BASE_URL}/{city}?key={API_KEY}")
    if response.status_code == 200:
        return response.json()
    else:
        return None
```

**使用装饰器**：

```python
from functools import wraps

def cache_result(ttl=3600):
    """缓存结果装饰器"""
    def decorator(func):
        cache = {}
        
        @wraps(func)
        def wrapper(*args):
            import time
            key = str(args)
            
            if key in cache:
                result, timestamp = cache[key]
                if time.time() - timestamp < ttl:
                    return result
            
            result = func(*args)
            cache[key] = (result, time.time())
            return result
        
        return wrapper
    return decorator

@cache_result(ttl=3600)
def get_weather(city):
    return api_call(city)
```

### 7.1.3 版本控制

**Git 提交规范**：

```bash
# 功能开发
git commit -m "feat: 添加天气查询功能"

# Bug 修复
git commit -m "fix: 修复 API 超时问题"

# 文档更新
git commit -m "docs: 更新使用说明"

# 代码重构
git commit -m "refactor: 优化代码结构"

# 性能优化
git commit -m "perf: 提高响应速度"
```

**分支管理**：

```bash
# 主分支
main

# 开发分支
develop

# 功能分支
feature/weather-skill
feature/news-skill

# 修复分支
fix/api-timeout
fix/error-handling
```

---

## 7.2 用户体验

### 7.2.1 清晰的提示

**好的响应格式**：

```markdown
✅ **成功响应**

已完成：文件备份

详情：
- 源文件：~/Documents/notes.md
- 备份位置：~/.openclaw/workspace/backups/
- 备份时间：2026-03-16 14:30:22
- 文件大小：2.5KB
```

**错误响应**：

```markdown
⚠️ **操作失败**

无法备份文件

原因：文件不存在

建议：
1. 检查文件路径是否正确
2. 确认文件是否被删除
3. 使用绝对路径重试

示例：
```
备份 ~/Documents/notes.md
```
```

### 7.2.2 友好的错误信息

**对比**：

```
❌ 技术错误：
Error: ConnectionError: Failed to connect to api.weather.com:443

✅ 用户友好：
⚠️ 无法获取天气信息

网络连接失败，请检查：
1. 网络是否正常
2. 防火墙设置
3. 稍后重试
```

### 7.2.3 进度反馈

**长时间任务的反馈**：

```markdown
📊 处理进度

[████████░░] 80%

步骤：
✅ 获取新闻数据
✅ 生成脚本
✅ 准备素材
🔄 渲染视频...
⏳ 上传文件
```

**在脚本中实现**：

```python
import sys

def process_with_progress(items):
    total = len(items)
    
    for i, item in enumerate(items):
        process(item)
        
        # 更新进度
        progress = (i + 1) / total * 100
        bar = '█' * int(progress / 10) + '░' * (10 - int(progress / 10))
        print(f"\r[{bar}] {progress:.0f}%", end='')
        sys.stdout.flush()
    
    print("\n✅ 完成！")
```

---

## 7.3 安全性

### 7.3.1 敏感信息保护

**不要硬编码密钥**：

```python
# ❌ 错误
API_KEY = "sk-1234567890abcdef"

# ✅ 正确
import os
API_KEY = os.getenv('API_KEY')
```

**使用环境变量**：

```bash
# 设置环境变量
export API_KEY="your-secret-key"
export DATABASE_URL="postgresql://user:pass@localhost/db"

# 在脚本中读取
import os
api_key = os.getenv('API_KEY')
```

**配置文件加密**：

```python
from cryptography.fernet import Fernet

# 生成密钥
key = Fernet.generate_key()
cipher = Fernet(key)

# 加密
encrypted = cipher.encrypt(b"secret_token")

# 解密
decrypted = cipher.decrypt(encrypted)
```

### 7.3.2 权限控制

**最小权限原则**：

```markdown
---
name: file-reader
description: 只读文件
allowed-tools: read  # 只允许读
---
```

**不要给不必要的权限**：

```markdown
# ❌ 权限过大
allowed-tools: read, write, exec, browser

# ✅ 最小权限
allowed-tools: read
```

### 7.3.3 输入验证

**验证用户输入**：

```python
def safe_process(user_input):
    # 验证类型
    if not isinstance(user_input, str):
        raise ValueError("输入必须是字符串")
    
    # 验证长度
    if len(user_input) > 1000:
        raise ValueError("输入过长")
    
    # 验证内容
    dangerous_chars = [';', '|', '&', '$']
    for char in dangerous_chars:
        if char in user_input:
            raise ValueError("包含非法字符")
    
    # 安全处理
    return process(user_input)
```

**防止命令注入**：

```python
# ❌ 危险
import os
os.system(f"echo {user_input}")

# ✅ 安全
import subprocess
subprocess.run(['echo', user_input], check=True)
```

---

## 7.4 文档规范

### 7.4.1 SKILL.md 规范

**完整结构**：

```markdown
---
name: skill-name
description: 简短描述（50 字内）
allowed-tools: read, write
version: 1.0.0
author: Your Name
---

# 技能名称

## 简介

1-2 句话介绍技能功能。

## 触发条件

列出所有触发关键词。

## 使用方式

### 基本用法

```
示例输入
```

### 高级用法

```
示例输入 --param value
```

## 示例

### 示例 1

用户：输入
AI：输出

### 示例 2

用户：输入
AI：输出

## 配置

说明需要的配置项。

## 注意事项

列出使用注意事项。
```

### 7.4.2 代码注释

**好的注释**：

```python
def calculate_distance(lat1, lon1, lat2, lon2):
    """
    计算两点之间的距离（Haversine 公式）
    
    参数:
        lat1: 第一个点的纬度
        lon1: 第一个点的经度
        lat2: 第二个点的纬度
        lon2: 第二个点的经度
    
    返回:
        距离（公里）
    """
    # 将角度转换为弧度
    lat1_rad = math.radians(lat1)
    # ... 计算逻辑
```

**避免的注释**：

```python
# ❌ 无意义注释
i = i + 1  # i 加 1

# ✅ 有意义的注释
# 重试次数加 1，最多重试 3 次
retry_count += 1
```

### 7.4.3 README 规范

**技能 README**：

```markdown
# 技能名称

> 一句话描述

## 安装

```bash
openclaw skills install skill-name
```

## 使用

```
示例用法
```

## 配置

| 配置项 | 说明 | 默认值 |
|-------|------|-------|
| API_KEY | API 密钥 | - |

## 示例

更多示例见 [examples/](examples/)

## 开发

```bash
git clone ...
cd skill-name
pip install -r requirements.txt
```

## 许可

MIT
```

---

## 7.5 性能最佳实践

### 7.5.1 响应时间

**目标**：
- ✅ 简单查询：<1 秒
- ✅ 中等任务：<5 秒
- ✅ 复杂任务：<30 秒

**优化方法**：

```python
# 1. 使用缓存
@cache(ttl=3600)
def get_data(key):
    return api_call(key)

# 2. 批量处理
results = api_batch_call(items)

# 3. 异步执行
async def fetch_all():
    await asyncio.gather(task1, task2, task3)
```

### 7.5.2 资源使用

**内存管理**：

```python
# ❌ 占用大量内存
data = []
for i in range(1000000):
    data.append(process(i))

# ✅ 生成器
def generate():
    for i in range(1000000):
        yield process(i)
```

**清理临时文件**：

```python
import tempfile
import os

def process_with_temp():
    # 创建临时文件
    temp = tempfile.NamedTemporaryFile(delete=False)
    
    try:
        # 处理
        write_data(temp)
        result = process(temp.name)
        return result
    
    finally:
        # 清理
        temp.close()
        os.unlink(temp.name)
```

---

## 本章小结

通过本章学习，你应该能够：
- ✅ 组织模块化代码
- ✅ 提供良好的用户体验
- ✅ 保护敏感信息和权限
- ✅ 编写规范的文档
- ✅ 优化技能性能

**下一章**：[第 8 章：实战案例 - 新闻视频制作](./08-case-study-news-video.md)

---

## 练习题

1. 重构一个技能，使用模块化设计
2. 为技能添加完整的文档
3. 实现输入验证和错误处理
4. 优化技能的性能

---

**本章完成时间**：2026-03-16
**最后更新**：2026-03-16
