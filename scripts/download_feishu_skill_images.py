#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
下载知乎文章"OpenClaw 飞书传输文件技能"的截图
"""

import os
import requests

IMAGE_URLS = [
    "https://picx.zhimg.com/v2-6bbd3a463539be7533addd468b730e50_l.jpg",
    "https://picx.zhimg.com/70/v2-4c87fe470b2b2c95068b3b8310a585bc_1440w.image",
    "https://pic1.zhimg.com/v2-c0726cd893f6e9f39fba23b618ea5d35.jpg",
    "https://pic1.zhimg.com/v2-6971fa3bddd9dcddd98b6303d00aa43c_1440w.jpg",
    "https://pic4.zhimg.com/v2-a8ff74abdc23e404855af9002d931566.webp",
    "https://pic1.zhimg.com/fde7bd037ef3fb4eddf73dd13b45ddb3_l.jpg",
    "https://pic1.zhimg.com/v2-bca9a3520c86c81ed16abe1a4968cd18_l.jpg",
    "https://pic4.zhimg.com/v2-52f8c87376792e927b6cf0896b726f06.png",
    "https://pic1.zhimg.com/v2-6bbd3a463539be7533addd468b730e50_l.jpg",
    "https://pic2.zhimg.com/v2-419a1a3ed02b7cfadc20af558aabc897.png",
    "https://pica.zhimg.com/v2-59c2e43275eff2d3c503f6c97433d654_720w.webp",
]

def download_images():
    save_dir = "images/zhihu-feishu-skill"
    os.makedirs(save_dir, exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
    }
    
    for i, url in enumerate(IMAGE_URLS, 1):
        try:
            print(f"下载第 {i}/{len(IMAGE_URLS)} 张：{url}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # 确定文件扩展名
            ext = '.jpg'
            if 'png' in url:
                ext = '.png'
            elif 'webp' in url:
                ext = '.webp'
            
            filename = f"feishu_skill_{i:02d}{ext}"
            filepath = os.path.join(save_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ 已保存：{filepath}")
            
        except Exception as e:
            print(f"❌ 下载失败：{e}")
    
    print(f"\n完成！共下载 {len(IMAGE_URLS)} 张图片到：{save_dir}")

if __name__ == "__main__":
    download_images()
