# 第 6 章：调试与测试

> 掌握技能调试技巧，确保技能稳定可靠

---

## 6.1 调试技巧

### 6.1.1 日志输出

**在脚本中添加调试日志**：

```python
import logging

# 配置调试日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def process_data(data):
    logger.debug(f"输入数据：{data}")
    
    result = transform(data)
    logger.debug(f"转换结果：{result}")
    
    return result
```

**日志级别使用**：

```python
logger.debug("详细调试信息")      # 变量值、中间状态
logger.info("一般信息")           # 操作开始/结束
logger.warning("警告信息")        # 非致命问题
logger.error("错误信息")          # 操作失败
logger.critical("严重错误")       # 系统崩溃
```

### 6.1.2 断点调试

**使用 pdb 调试 Python**：

```python
import pdb

def complex_function(data):
    # 设置断点
    pdb.set_trace()
    
    # 执行到这里会暂停
    result = process(data)
    
    # 可以检查变量
    print(f"data = {data}")
    print(f"result = {result}")
    
    return result
```

**常用调试命令**：

```bash
n          # 执行下一行
c          # 继续执行
q          # 退出调试
p variable # 打印变量
l          # 列出代码
```

### 6.1.3 变量检查

**打印关键变量**：

```python
def debug_function(data):
    print("=" * 50)
    print("调试信息")
    print("=" * 50)
    print(f"输入：{data}")
    print(f"类型：{type(data)}")
    print(f"长度：{len(data) if hasattr(data, '__len__') else 'N/A'}")
    print("=" * 50)
    
    # 处理逻辑
    result = process(data)
    
    print(f"输出：{result}")
    print("=" * 50)
    
    return result
```

---

## 6.2 单元测试

### 6.2.1 测试框架

**使用 pytest**：

```python
# test_skill.py
import pytest
from scripts.process import process_data

def test_process_normal():
    """测试正常情况"""
    data = {"key": "value"}
    result = process_data(data)
    assert result["status"] == "success"

def test_process_empty():
    """测试空数据"""
    data = {}
    result = process_data(data)
    assert result["status"] == "error"

def test_process_invalid():
    """测试无效数据"""
    data = None
    result = process_data(data)
    assert result["status"] == "error"
```

**运行测试**：

```bash
# 安装 pytest
pip install pytest

# 运行所有测试
pytest

# 运行特定测试
pytest test_skill.py::test_process_normal

# 显示详细信息
pytest -v
```

### 6.2.2 测试用例编写

**测试结构**：

```python
import pytest

class TestSkill:
    """技能测试类"""
    
    def setup_method(self):
        """每个测试前执行"""
        self.test_data = {"key": "value"}
    
    def teardown_method(self):
        """每个测试后执行"""
        pass
    
    def test_case_1(self):
        """测试用例 1"""
        result = process(self.test_data)
        assert result is not None
    
    def test_case_2(self):
        """测试用例 2"""
        with pytest.raises(Exception):
            process(None)
```

**测试覆盖**：

```bash
# 安装 coverage
pip install coverage

# 运行测试并统计覆盖率
coverage run -m pytest
coverage report

# 生成 HTML 报告
coverage html
```

### 6.2.3 集成测试

**端到端测试**：

```python
def test_full_workflow():
    """测试完整工作流程"""
    
    # 1. 准备输入
    input_data = load_test_data()
    
    # 2. 执行技能
    result = run_skill(input_data)
    
    # 3. 验证输出
    assert result["status"] == "success"
    assert len(result["data"]) > 0
    
    # 4. 清理
    cleanup()
```

---

## 6.3 性能优化

### 6.3.1 响应时间优化

**性能分析**：

```python
import time

def profile_function(func, *args):
    start = time.time()
    result = func(*args)
    end = time.time()
    
    print(f"执行时间：{end - start:.3f}秒")
    return result

# 使用
profile_function(process_data, test_data)
```

**优化技巧**：

✅ **减少 API 调用**：
```python
# ❌ 慢：多次 API 调用
for item in items:
    result = api_call(item)

# ✅ 快：批量 API 调用
results = api_call_batch(items)
```

✅ **使用缓存**：
```python
# ❌ 每次都查询
def get_weather(city):
    return api_call(city)

# ✅ 使用缓存
@cache(ttl=3600)
def get_weather(city):
    return api_call(city)
```

### 6.3.2 资源占用优化

**内存优化**：

```python
# ❌ 占用大量内存
def process_large_file():
    with open('large.txt', 'r') as f:
        data = f.read()  # 全部读入内存
    return process(data)

# ✅ 流式处理
def process_large_file():
    with open('large.txt', 'r') as f:
        for line in f:  # 逐行处理
            yield process(line)
```

**CPU 优化**：

```python
# ❌ 单线程
results = [process(item) for item in items]

# ✅ 多线程
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as executor:
    results = list(executor.map(process, items))
```

---

## 6.4 常见问题

### 6.4.1 技能不触发

**排查步骤**：

```bash
# 1. 检查 SKILL.md
cat SKILL.md | grep "触发条件"

# 2. 检查关键词
cat SKILL.md | grep "- 关键词"

# 3. 重新加载技能
openclaw skills reload

# 4. 查看日志
openclaw logs --skill skill-name
```

### 6.4.2 脚本执行失败

**排查步骤**：

```bash
# 1. 检查脚本权限
ls -la scripts/

# 2. 添加执行权限
chmod +x scripts/*.py

# 3. 手动运行脚本
python3 scripts/process.py test

# 4. 查看错误输出
python3 scripts/process.py 2>&1
```

### 6.4.3 API 调用失败

**排查步骤**：

```bash
# 1. 检查 API 密钥
echo $API_KEY

# 2. 测试 API 连接
curl -H "Authorization: Bearer $API_KEY" https://api.example.com/test

# 3. 检查网络
ping api.example.com

# 4. 查看超时设置
cat config.json | grep timeout
```

---

## 本章小结

通过本章学习，你应该能够：
- ✅ 使用日志进行调试
- ✅ 编写单元测试
- ✅ 进行性能分析和优化
- ✅ 排查常见问题

**下一章**：[第 7 章：最佳实践](./07-best-practices.md)

---

## 练习题

1. 为第 4 章的技能编写单元测试
2. 添加调试日志到技能脚本
3. 使用 pytest 运行测试
4. 分析并优化技能性能

---

**本章完成时间**：2026-03-16
**最后更新**：2026-03-16
