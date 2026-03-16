# 第 4 章：技能开发基础

> 从零开始，创建你的第一个 OpenClaw 技能

---

## 4.1 技能结构详解

### 4.1.1 技能目录结构

一个标准的 OpenClaw 技能目录结构：

```
my-skill/
├── SKILL.md              # 技能描述文件（必需）
├── scripts/              # 脚本目录（可选）
│   ├── fetch_data.py     # Python 脚本
│   └── process.sh        # Bash 脚本
├── references/           # 参考资料（可选）
│   └── api-docs.md       # API 文档
├── templates/            # 模板文件（可选）
│   └── output.md         # 输出模板
└── _meta.json            # 元数据（可选）
```

**必需文件**：
- ✅ `SKILL.md` - 技能的唯一必需文件

**可选目录**：
- `scripts/` - 存放 Python、Bash 等脚本
- `references/` - 存放参考文档
- `templates/` - 存放输出模板

### 4.1.2 实际案例：天气技能

```
weather/
├── SKILL.md
├── scripts/
│   └── fetch_weather.py
└── _meta.json
```

---

## 4.2 SKILL.md 详解

### 4.2.1 基本结构

```markdown
---
name: skill-name
description: 技能的简短描述
allowed-tools: read, write, exec
---

# 技能说明

## 触发条件

## 使用方式

## 示例
```

### 4.2.2 元数据字段

**YAML Front Matter**（文件顶部）：

| 字段 | 说明 | 必填 | 示例 |
|------|------|------|------|
| `name` | 技能名称 | ✅ | `weather` |
| `description` | 技能描述 | ✅ | `查询天气信息` |
| `allowed-tools` | 允许使用的工具 | ✅ | `read, write, exec` |
| `version` | 版本号 | ❌ | `1.0.0` |
| `author` | 作者 | ❌ | `Your Name` |

**完整示例**：

```markdown
---
name: weather
description: 查询实时天气和未来预报
allowed-tools: exec, read
version: 1.0.0
author: Your Name
---

# 天气查询技能

查询指定城市的实时天气和未来 3 天预报。

## 触发条件

当用户提到以下关键词时触发：
- 天气
- 气温
- 下雨
- 晴天
- 天气预报

## 使用方式

### 基本用法
```
你：北京今天天气怎么样？
```

### 带参数
```
你：查询上海未来 3 天的天气
```

## 示例

### 示例 1：查询当天天气
用户：北京今天天气怎么样？
AI：好的，我来查询...

### 示例 2：查询预报
用户：上海明天会下雨吗？
AI：让我查一下...
```

### 4.2.3 allowed-tools 说明

**常用工具**：

| 工具 | 用途 | 示例 |
|------|------|------|
| `read` | 读取文件 | 读取配置文件 |
| `write` | 写入文件 | 保存数据 |
| `edit` | 编辑文件 | 修改配置 |
| `exec` | 执行命令 | 运行脚本 |
| `web_search` | 网络搜索 | 搜索信息 |
| `browser` | 浏览器控制 | 抓取网页 |

**选择原则**：
- ✅ 只声明需要的工具
- ✅ 最小权限原则
- ❌ 不要声明不用的工具

---

## 4.3 触发机制

### 4.3.1 关键词触发

**在 SKILL.md 中定义**：

```markdown
## 触发条件

当用户提到以下关键词时触发：
- 天气
- 气温
- 下雨
- 晴天
- 天气预报
- 几度
- 温度
```

**最佳实践**：

✅ **好的关键词**：
- 具体明确（"天气"、"气温"）
- 覆盖常用表达（"下雨"、"晴天"）
- 包含同义词（"温度"、"几度"）

❌ **避免的关键词**：
- 太宽泛（"查"、"看"）
- 容易误触发（"了"、"吗"）
- 与其他技能冲突

### 4.3.2 意图识别

OpenClaw 会自动识别用户意图。

**示例**：

```
用户表达              识别意图
"北京天气怎么样"   →   weather.query
"明天会下雨吗"     →   weather.forecast
"气温多少度"       →   weather.temperature
```

### 4.3.3 上下文匹配

技能会考虑对话上下文。

**示例**：

```
用户：北京天气怎么样？
AI：北京今天晴，25°C。

用户：那上海呢？  ← 上下文：查询天气
AI：上海今天多云，23°C。
```

---

## 4.4 你的第一个技能

### 4.4.1 Hello World 技能

**创建目录**：

```bash
mkdir -p ~/.openclaw/workspace/skills/hello-world
cd ~/.openclaw/workspace/skills/hello-world
```

**创建 SKILL.md**：

```bash
cat > SKILL.md << 'EOF'
---
name: hello-world
description: 一个简单的问候技能
allowed-tools: read
---

# Hello World 技能

这是一个简单的问候技能，用于学习 OpenClaw 技能开发。

## 触发条件

当用户提到以下关键词时触发：
- 你好
- hello
- 嗨
- 早上好
- 下午好
- 晚上好

## 使用方式

```
你：你好
AI：你好！我是你的 AI 助手，有什么可以帮你的吗？
```

## 示例

### 示例 1：基本问候
用户：你好
AI：你好！很高兴见到你！

### 示例 2：时间相关
用户：早上好
AI：早上好！祝你今天愉快！
EOF
```

**测试技能**：

```bash
# 重新加载技能
openclaw skills reload

# 测试
你：你好
AI：你好！很高兴见到你！
```

### 4.4.2 实用技能：文件备份

**创建目录**：

```bash
mkdir -p ~/.openclaw/workspace/skills/file-backup
cd ~/.openclaw/workspace/skills/file-backup
```

**创建 SKILL.md**：

```bash
cat > SKILL.md << 'EOF'
---
name: file-backup
description: 备份指定文件到备份目录
allowed-tools: exec, read, write
---

# 文件备份技能

自动备份指定文件到备份目录，带时间戳。

## 触发条件

当用户提到以下关键词时触发：
- 备份
- backup
- 保存副本
- 复制文件

## 使用方式

### 基本用法
```
你：帮我备份这个文件
```

### 指定目录
```
你：把文件备份到~/backups/
```

## 备份规则

1. 备份文件名格式：`原文件名_时间戳.扩展名`
2. 备份位置：`~/.openclaw/workspace/backups/`
3. 保留最近 10 个版本

## 示例

### 示例 1：备份当前文件
用户：帮我备份这个文件
AI：好的，已备份到 ~/.openclaw/workspace/backups/file_20260316_143022.txt
EOF
```

**创建备份脚本**：

```bash
mkdir scripts
cat > scripts/backup.sh << 'EOF'
#!/bin/bash

# 文件备份脚本

SOURCE_FILE="$1"
BACKUP_DIR="$HOME/.openclaw/workspace/backups"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 生成备份文件名
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME=$(basename "$SOURCE_FILE")
BACKUP_FILE="$BACKUP_DIR/${FILENAME%.*}_$TIMESTAMP.${FILENAME##*.}"

# 复制文件
cp "$SOURCE_FILE" "$BACKUP_FILE"

echo "✅ 已备份：$BACKUP_FILE"
EOF

chmod +x scripts/backup.sh
```

**测试**：

```bash
# 测试备份
你：帮我备份 ~/Documents/notes.md
AI：好的，我来备份...

[执行备份脚本]

✅ 已备份：~/.openclaw/workspace/backups/notes_20260316_143022.md
```

---

## 4.5 技能测试

### 4.5.1 手动测试

**步骤**：

1. **加载技能**
   ```bash
   openclaw skills reload
   ```

2. **触发技能**
   ```
   你：你好
   ```

3. **检查响应**
   - 是否正确触发
   - 响应是否符合预期
   - 是否有错误

### 4.5.2 自动化测试

**创建测试脚本**：

```bash
cat > test.sh << 'EOF'
#!/bin/bash

echo "测试 Hello World 技能..."

# 测试 1：基本问候
echo "测试 1: 你好"
# 预期输出：包含"你好"

# 测试 2：英文问候
echo "测试 2: Hello"
# 预期输出：包含"Hello"或"你好"

# 测试 3：时间问候
echo "测试 3: 早上好"
# 预期输出：包含"早上好"

echo "所有测试完成！"
EOF

chmod +x test.sh
```

### 4.5.3 常见问题排查

**问题 1：技能不触发**

```bash
# 检查 SKILL.md 语法
cat SKILL.md

# 检查关键词
grep "触发条件" SKILL.md

# 重新加载
openclaw skills reload
```

**问题 2：工具权限不足**

```bash
# 检查 allowed-tools
grep "allowed-tools" SKILL.md

# 添加需要的工具
# 编辑 SKILL.md，添加工具
```

**问题 3：脚本执行失败**

```bash
# 检查脚本权限
ls -la scripts/

# 添加执行权限
chmod +x scripts/*.sh

# 检查脚本内容
cat scripts/backup.sh
```

---

## 4.6 技能模板

### 4.6.1 基础模板

```markdown
---
name: skill-name
description: 技能描述
allowed-tools: read, write
---

# 技能名称

技能简介。

## 触发条件

当用户提到以下关键词时触发：
- 关键词 1
- 关键词 2

## 使用方式

### 基本用法
```
你：[示例输入]
```

## 示例

### 示例 1
用户：[输入]
AI：[输出]
```

### 4.6.2 脚本技能模板

```markdown
---
name: script-skill
description: 使用脚本的技能
allowed-tools: exec
---

# 脚本技能

## 触发条件

## 脚本说明

脚本位置：`scripts/process.py`

## 使用方式

## 示例
```

---

## 本章小结

通过本章学习，你应该能够：
- ✅ 理解技能目录结构
- ✅ 编写 SKILL.md 文件
- ✅ 定义触发条件
- ✅ 创建简单的技能
- ✅ 测试和调试技能

**下一章**：[第 5 章：技能开发进阶](./05-skill-development-advanced.md)

---

## 练习题

1. 创建一个 Hello World 技能并测试
2. 创建一个文件备份技能
3. 为技能编写完整的 SKILL.md
4. 测试技能的触发条件

---

**本章完成时间**：2026-03-16
**最后更新**：2026-03-16
