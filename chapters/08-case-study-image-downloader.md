# 第 8 章：实战案例 - 网页图片批量下载技能

> 从零开始，创建一个实用的网页图片下载技能

---

## 8.1 项目背景

在编写技术书籍或教程时，经常需要下载网页中的截图。手动一张张保存既耗时又容易遗漏。

**需求**：
- ✅ 批量下载网页中的所有图片
- ✅ 自动按顺序编号
- ✅ 保存高清版本
- ✅ 支持知乎、CSDN 等技术网站

**解决方案**：创建一个 OpenClaw 技能 - `web-image-downloader`

---

## 8.2 技能设计

### 8.2.1 功能分析

**核心功能**：
1. 从网页提取所有图片 URL
2. 批量下载图片
3. 保存到指定目录
4. 自动命名（img_01.jpg, img_02.jpg...）

**扩展功能**：
- 支持多个网站（知乎、CSDN、掘金等）
- 并发下载提高速度
- 显示下载进度

### 8.2.2 技术选型

**方案对比**：

| 方案 | 优点 | 缺点 |
|------|------|------|
| 浏览器插件 | 可视化，易用 | 需要手动操作 |
| Python 脚本 | 灵活，可定制 | 需要编程 |
| OpenClaw 技能 | 自然语言触发 | 需要配置 |

**选择**：OpenClaw 技能 + Python 脚本

---

## 8.3 实现过程

### 8.3.1 获取图片 URL

**方法 1：浏览器控制台**

打开知乎文章，在控制台执行：

```javascript
// 提取所有图片 URL
const imgs = document.querySelectorAll('figure img, .RichText img');
const imageUrls = Array.from(imgs)
    .map(img => img.src || img.dataset.src)
    .filter(src => src && src.includes('zhimg.com'));

console.log(JSON.stringify(imageUrls, null, 2));
```

**输出示例**：

```json
[
  "https://pic3.zhimg.com/v2-73c3016f75eed0dd7a059eb524870934_1440w.jpg",
  "https://pic4.zhimg.com/v2-f4eebfd6c020508d2f1422b65a5e93f1_1440w.jpg",
  ...
]
```

**方法 2：使用 browser 工具**

```typescript
// 在 OpenClaw 技能中
browser.act({
  kind: "evaluate",
  fn: "() => { const imgs = document.querySelectorAll('img'); return Array.from(imgs).map(img => img.src); }"
});
```

### 8.3.2 编写下载脚本

**基础版本** (`download_zhihu_images.py`)：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
从知乎文章下载所有图片
用法：python3 download_zhihu_images.py <文章 URL> <保存目录>
"""

import sys
import os
import requests
from bs4 import BeautifulSoup

def download_images(url, save_dir):
    """下载网页中的所有图片"""
    
    # 创建保存目录
    os.makedirs(save_dir, exist_ok=True)
    
    # 获取网页内容
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 查找所有图片
    img_tags = soup.find_all('img')
    
    print(f"找到 {len(img_tags)} 张图片")
    
    # 下载图片
    downloaded = 0
    for i, img in enumerate(img_tags):
        img_url = img.get('src') or img.get('data-src')
        
        if not img_url or 'zhimg.com' not in img_url:
            continue
        
        try:
            print(f"下载第 {i+1} 张：{img_url}")
            img_response = requests.get(img_url, headers=headers)
            img_response.raise_for_status()
            
            # 生成文件名
            img_name = f"zhihu_img_{downloaded+1}.jpg"
            img_path = os.path.join(save_dir, img_name)
            
            # 保存图片
            with open(img_path, 'wb') as f:
                f.write(img_response.content)
            
            downloaded += 1
            print(f"✅ 已保存：{img_path}")
            
        except Exception as e:
            print(f"❌ 下载失败：{e}")
    
    print(f"\n完成！共下载 {downloaded} 张图片到：{save_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：python3 download_zhihu_images.py <文章 URL> <保存目录>")
        sys.exit(1)
    
    url = sys.argv[1]
    save_dir = sys.argv[2]
    
    download_images(url, save_dir)
```

**批量版本** (`download_zhihu_images_batch.py`)：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
批量下载知乎文章图片（预设 URL 列表）
"""

import os
import requests

# 知乎文章的所有图片 URL
IMAGE_URLS = [
    "https://pic3.zhimg.com/v2-73c3016f75eed0dd7a059eb524870934_1440w.jpg",
    "https://pic4.zhimg.com/v2-f4eebfd6c020508d2f1422b65a5e93f1_1440w.jpg",
    # ... 更多 URL
]

def download_images():
    save_dir = "images/zhihu-screenshots"
    os.makedirs(save_dir, exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
    }
    
    for i, url in enumerate(IMAGE_URLS, 1):
        try:
            print(f"下载第 {i}/{len(IMAGE_URLS)} 张：{url}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            filename = f"zhihu_img_{i:02d}.jpg"
            filepath = os.path.join(save_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ 已保存：{filepath}")
            
        except Exception as e:
            print(f"❌ 下载失败：{e}")
    
    print(f"\n完成！共下载 {len(IMAGE_URLS)} 张图片到：{save_dir}")

if __name__ == "__main__":
    download_images()
```

### 8.3.3 创建 SKILL.md

```markdown
---
name: web-image-downloader
description: 从网页批量下载图片，支持知乎等网站
allowed-tools: exec, write
---

# 网页图片下载技能

批量下载网页中的所有图片，保存到本地目录。

## 使用场景

- 📸 下载教程文章的所有截图
- 📸 保存网页中的图片素材
- 📸 批量获取图片资源

## 使用方法

### 基本用法

```
你：帮我下载这个网页的所有图片：https://zhuanlan.zhihu.com/p/2001018648215709469
```

### 指定保存目录

```
你：下载知乎文章图片到 images/zhihu-screenshots 目录
```

## 示例

### 示例 1：下载知乎文章图片

用户：帮我下载知乎文章的所有截图
AI：好的，我来下载...

[执行下载脚本]

✅ 已下载 54 张图片到：images/zhihu-screenshots/
```

---

## 8.4 技能测试

### 8.4.1 测试步骤

1. **准备测试环境**
   ```bash
   cd /Users/jiangmeilan/.openclaw/workspace/claw-book
   mkdir -p images/test-download
   ```

2. **运行下载脚本**
   ```bash
   python3 scripts/download_zhihu_images_batch.py
   ```

3. **验证结果**
   ```bash
   ls -la images/zhihu-screenshots/
   # 应该看到 54 张图片
   ```

### 8.4.2 测试结果

```
下载第 1/54 张：https://pic3.zhimg.com/v2-73c3016f75eed0dd7a059eb524870934_1440w.jpg
✅ 已保存：images/zhihu-screenshots/zhihu_img_01.jpg

下载第 2/54 张：https://pic4.zhimg.com/v2-f4eebfd6c020508d2f1422b65a5e93f1_1440w.jpg
✅ 已保存：images/zhihu-screenshots/zhihu_img_02.jpg

...

完成！共下载 54 张图片到：images/zhihu-screenshots
```

**验证**：
```bash
ls images/zhihu-screenshots/ | wc -l
# 输出：54
```

---

## 8.5 技能优化

### 8.5.1 添加下载进度

```python
from tqdm import tqdm

for i, url in enumerate(tqdm(IMAGE_URLS), 1):
    response = requests.get(url, headers=headers)
    # ... 保存逻辑
```

**效果**：
```
100%|████████████████████| 54/54 [00:23<00:00, 2.34it/s]
```

### 8.5.2 并发下载

```python
from concurrent.futures import ThreadPoolExecutor

def download_single(url, filename):
    response = requests.get(url, headers=headers)
    with open(filename, 'wb') as f:
        f.write(response.content)

with ThreadPoolExecutor(max_workers=5) as executor:
    filenames = [f"img_{i:02d}.jpg" for i in range(1, len(IMAGE_URLS)+1)]
    executor.map(download_single, IMAGE_URLS, filenames)
```

**速度提升**：从 23 秒 → 5 秒

### 8.5.3 支持更多网站

```python
def get_image_urls(url):
    """根据网站类型提取图片 URL"""
    
    if 'zhuanlan.zhihu.com' in url:
        return get_zhihu_images(url)
    elif 'blog.csdn.net' in url:
        return get_csdn_images(url)
    elif 'juejin.cn' in url:
        return get_juejin_images(url)
    else:
        return get_generic_images(url)
```

---

## 8.6 经验总结

### ✅ 成功之处

1. **实用性强** - 解决了实际问题
2. **易于使用** - 自然语言触发
3. **可扩展** - 支持添加新网站
4. **高效** - 批量下载，节省时间

### ⚠️ 注意事项

1. **版权问题** - 仅用于个人学习，不要商用
2. **网络限速** - 批量下载时添加延时
3. **存储空间** - 高清图片占用空间大
4. **网站政策** - 遵守 robots.txt

### 🔧 改进方向

1. **GUI 界面** - 让非技术人员也能使用
2. **浏览器扩展** - 一键下载当前页面图片
3. **云存储** - 直接保存到云盘
4. **图片处理** - 自动压缩、裁剪

---

## 8.7 完整代码

### 8.7.1 项目结构

```
web-image-downloader/
├── SKILL.md                      # 技能说明
├── download_zhihu_images.py      # 基础版本
├── download_zhihu_images_batch.py # 批量版本
└── images/
    └── zhihu-screenshots/        # 下载的图片
        ├── zhihu_img_01.jpg
        ├── zhihu_img_02.jpg
        └── ...
```

### 8.7.2 关键代码片段

**提取图片 URL**：
```javascript
// 浏览器控制台
const imgs = document.querySelectorAll('figure img, .RichText img');
const urls = Array.from(imgs).map(img => img.src || img.dataset.src);
```

**下载图片**：
```python
response = requests.get(url, headers=headers)
with open(filepath, 'wb') as f:
    f.write(response.content)
```

**批量处理**：
```python
for i, url in enumerate(IMAGE_URLS, 1):
    filename = f"img_{i:02d}.jpg"
    download(url, filename)
```

---

## 8.8 练习题

1. 修改脚本，支持下载 CSDN 博客的配图
2. 添加下载进度条显示
3. 实现并发下载，提高速度
4. 添加图片压缩功能

---

**本章完成时间**：2026-03-16
**最后更新**：2026-03-16
