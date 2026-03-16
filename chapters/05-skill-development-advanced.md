# 第 5 章：技能开发进阶

> 掌握高级技能开发技巧，创建强大的自定义技能

---

## 5.1 使用外部工具

### 5.1.1 exec 命令执行

**在技能中执行 shell 命令**：

```markdown
---
name: file-processor
description: 处理文件
allowed-tools: exec
---

## 使用 exec 执行命令

在技能响应中，可以使用 exec 工具：

```bash
# 列出文件
ls -la ~/Documents/

# 运行脚本
python3 scripts/process.py

# 文件操作
cp file1.txt file2.txt
```
```

**实际案例**：

```typescript
// 在技能响应中
exec({
  command: "python3 scripts/fetch_data.py",
  workdir: "~/.openclaw/workspace/skills/my-skill"
});
```

### 5.1.2 文件读写

**读取文件**：

```typescript
read({
  path: "~/.openclaw/workspace/config.json"
});
```

**写入文件**：

```typescript
write({
  path: "~/.openclaw/workspace/output.md",
  content: "# 输出内容\n\n这是生成的内容..."
});
```

**编辑文件**：

```typescript
edit({
  path: "~/.openclaw/workspace/config.json",
  oldText: '"debug": false',
  newText: '"debug": true'
});
```

### 5.1.3 网络请求

**使用 Python 脚本**：

```python
# scripts/fetch_data.py
import requests
import json

def fetch_weather(city):
    api_key = os.getenv('WEATHER_API_KEY')
    url = f"https://api.weather.com/{city}?key={api_key}"
    
    response = requests.get(url)
    data = response.json()
    
    return data

if __name__ == "__main__":
    city = sys.argv[1]
    result = fetch_weather(city)
    print(json.dumps(result))
```

**在技能中调用**：

```markdown
## 执行脚本

```bash
python3 scripts/fetch_data.py 北京
```
```

---

## 5.2 脚本编写

### 5.2.1 Python 脚本

**基本结构**：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
技能脚本：数据处理
"""

import sys
import json
import os

def main():
    # 获取参数
    if len(sys.argv) < 2:
        print("用法：python3 script.py <参数>")
        sys.exit(1)
    
    param = sys.argv[1]
    
    # 处理逻辑
    result = process(param)
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False))

def process(param):
    # 处理逻辑
    return {"status": "success", "data": param}

if __name__ == "__main__":
    main()
```

**实际案例：新闻获取**：

```python
#!/usr/bin/env python3
# scripts/fetch_news.py

import requests
import os
from datetime import datetime

def fetch_tech_news(limit=10):
    """获取科技新闻"""
    
    api_key = os.getenv('TAVILY_API_KEY')
    
    query = "AI 大模型 科技新闻 今日热点"
    
    url = "https://api.tavily.com/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "query": query,
        "max_results": limit,
        "search_depth": "advanced"
    }
    
    response = requests.post(url, json=data, headers=headers)
    results = response.json()
    
    # 格式化输出
    news_list = []
    for item in results['results']:
        news_list.append({
            "title": item['title'],
            "url": item['url'],
            "summary": item['content']
        })
    
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "count": len(news_list),
        "news": news_list
    }

if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    result = fetch_tech_news(limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

### 5.2.2 Bash 脚本

**基本结构**：

```bash
#!/bin/bash

# 技能脚本：文件备份

set -e  # 出错立即退出

# 配置
BACKUP_DIR="$HOME/.openclaw/workspace/backups"
SOURCE_FILE="$1"

# 检查参数
if [ -z "$SOURCE_FILE" ]; then
    echo "错误：请指定要备份的文件"
    exit 1
fi

# 检查文件是否存在
if [ ! -f "$SOURCE_FILE" ]; then
    echo "错误：文件不存在：$SOURCE_FILE"
    exit 1
fi

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 生成备份文件名
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME=$(basename "$SOURCE_FILE")
BACKUP_FILE="$BACKUP_DIR/${FILENAME%.*}_$TIMESTAMP.${FILENAME##*.}"

# 复制文件
cp "$SOURCE_FILE" "$BACKUP_FILE"

echo "✅ 备份成功：$BACKUP_FILE"
```

### 5.2.3 Node.js 脚本

**基本结构**：

```javascript
#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

async function main() {
    const args = process.argv.slice(2);
    
    if (args.length < 1) {
        console.log('用法：node script.js <参数>');
        process.exit(1);
    }
    
    const param = args[0];
    const result = await process(param);
    
    console.log(JSON.stringify(result, null, 2));
}

async function process(param) {
    // 处理逻辑
    return { status: 'success', data: param };
}

main().catch(console.error);
```

---

## 5.3 资源管理

### 5.3.1 图片资源

**目录结构**：

```
my-skill/
├── SKILL.md
├── images/
│   ├── logo.png
│   ├── icon.jpg
│   └── template/
│       └── background.png
└── scripts/
```

**在技能中使用**：

```markdown
## 使用图片

图片路径：`images/logo.png`

在响应中可以引用：
MEDIA:./images/logo.png
```

**最佳实践**：

✅ **图片优化**：
- 使用合适的格式（PNG/JPG）
- 压缩图片大小
- 使用相对路径

❌ **避免**：
- 过大的图片（>1MB）
- 绝对路径
- 版权不明的图片

### 5.3.2 模板文件

**创建模板**：

```markdown
# templates/report.md

# {{title}}

> {{subtitle}}

## 概述
{{overview}}

## 详细内容
{{content}}

## 总结
{{summary}}
```

**在脚本中使用**：

```python
def generate_report(data):
    # 读取模板
    with open('templates/report.md', 'r') as f:
        template = f.read()
    
    # 替换变量
    report = template.replace('{{title}}', data['title'])
    report = report.replace('{{subtitle}}', data['subtitle'])
    report = report.replace('{{overview}}', data['overview'])
    report = report.replace('{{content}}', data['content'])
    report = report.replace('{{summary}}', data['summary'])
    
    return report
```

### 5.3.3 配置文件

**JSON 配置**：

```json
{
  "api": {
    "timeout": 30,
    "retry": 3
  },
  "output": {
    "format": "markdown",
    "include_images": true
  },
  "cache": {
    "enabled": true,
    "ttl": 3600
  }
}
```

**YAML 配置**：

```yaml
api:
  timeout: 30
  retry: 3

output:
  format: markdown
  include_images: true

cache:
  enabled: true
  ttl: 3600
```

**读取配置**：

```python
import json

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

config = load_config()
timeout = config['api']['timeout']
```

---

## 5.4 错误处理

### 5.4.1 异常捕获

**Python 示例**：

```python
def fetch_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.Timeout:
        return {"error": "请求超时", "code": "TIMEOUT"}
    
    except requests.exceptions.ConnectionError:
        return {"error": "网络连接失败", "code": "CONNECTION_ERROR"}
    
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP 错误：{e}", "code": "HTTP_ERROR"}
    
    except Exception as e:
        return {"error": f"未知错误：{e}", "code": "UNKNOWN"}
```

### 5.4.2 用户提示

**友好的错误信息**：

```markdown
## 错误处理

### 错误场景 1：API 密钥缺失

❌ 错误输出：
```
Error: WEATHER_API_KEY not set
```

✅ 友好输出：
```
⚠️ 缺少 API 密钥

要使用天气查询功能，需要配置 API 密钥：

1. 访问 openweathermap.org 获取密钥
2. 运行命令：export WEATHER_API_KEY=your-key
3. 重试查询
```

### 错误场景 2：网络错误

❌ 错误输出：
```
ConnectionError: Failed to connect
```

✅ 友好输出：
```
⚠️ 网络连接失败

请检查：
1. 网络连接是否正常
2. 防火墙设置
3. 代理配置

然后重试。
```
```

### 5.4.3 日志记录

**Python 日志**：

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('skill.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('my-skill')

def process_data(data):
    logger.info(f"开始处理数据：{data}")
    
    try:
        result = heavy_computation(data)
        logger.info(f"处理成功：{result}")
        return result
    
    except Exception as e:
        logger.error(f"处理失败：{e}", exc_info=True)
        raise
```

**日志级别**：

| 级别 | 用途 | 示例 |
|------|------|------|
| `DEBUG` | 调试信息 | 变量值、流程跟踪 |
| `INFO` | 一般信息 | 操作开始/结束 |
| `WARNING` | 警告 | 非致命问题 |
| `ERROR` | 错误 | 操作失败 |
| `CRITICAL` | 严重错误 | 系统崩溃 |

---

## 5.5 性能优化

### 5.5.1 缓存策略

**简单缓存实现**：

```python
import json
import hashlib
from datetime import datetime, timedelta

class Cache:
    def __init__(self, ttl=3600):
        self.ttl = ttl  # 缓存时间（秒）
        self.cache_file = 'cache.json'
        self.data = self._load()
    
    def _load(self):
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.data, f)
    
    def get(self, key):
        if key in self.data:
            cached = self.data[key]
            if datetime.now() < datetime.fromisoformat(cached['expires']):
                return cached['value']
        return None
    
    def set(self, key, value):
        self.data[key] = {
            'value': value,
            'expires': (datetime.now() + timedelta(seconds=self.ttl)).isoformat()
        }
        self._save()

# 使用
cache = Cache(ttl=3600)

def fetch_weather(city):
    cache_key = f"weather_{city}"
    
    # 尝试从缓存获取
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    # 从 API 获取
    data = api_call(city)
    
    # 保存到缓存
    cache.set(cache_key, data)
    
    return data
```

### 5.5.2 异步处理

**Python 异步**：

```python
import asyncio
import aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.json()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

# 使用
urls = ['url1', 'url2', 'url3']
results = asyncio.run(fetch_all(urls))
```

### 5.5.3 批量处理

**批量 API 调用**：

```python
def batch_process(items, batch_size=10):
    results = []
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        batch_results = process_batch(batch)
        results.extend(batch_results)
        
        # 避免频率限制
        time.sleep(0.1)
    
    return results
```

---

## 本章小结

通过本章学习，你应该能够：
- ✅ 使用外部工具（exec、文件读写、网络请求）
- ✅ 编写 Python/Bash/Node.js 脚本
- ✅ 管理技能资源（图片、模板、配置）
- ✅ 处理错误和异常
- ✅ 优化技能性能

**下一章**：[第 6 章：调试与测试](./06-debugging-and-testing.md)

---

## 练习题

1. 创建一个使用 Python 脚本的技能
2. 为技能添加错误处理
3. 实现简单的缓存机制
4. 添加日志记录功能

---

**本章完成时间**：2026-03-16
**最后更新**：2026-03-16
