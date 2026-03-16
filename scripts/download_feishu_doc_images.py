#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
下载知乎文章"OpenClaw 自动创建飞书文档"的截图
"""

import os
import requests

IMAGE_URLS = [
    "https://pica.zhimg.com/v2-443345788053370db37bc3ae12274e5b_1440w.image",
    "https://pica.zhimg.com/v2-29d948caa4dc35b98b303701f1211b96_1440w.jpg",
    "https://picx.zhimg.com/v2-1f2643b4f9661f2096a063b579e1fac3_1440w.jpg",
    "https://pic1.zhimg.com/v2-164b7508699bf0c9807c5552df6200a6_1440w.jpg",
    "https://pic4.zhimg.com/v2-e0bc5a80814b1380deb9fd6727d463d1_1440w.jpg",
    "https://picx.zhimg.com/v2-a414663f1a97dd430a51fbe94ecd4249_1440w.jpg",
    "https://pic3.zhimg.com/v2-b5ac8ca2b7e5c453961c30a7ad6bb0b8_1440w.jpg",
    "https://pica.zhimg.com/v2-68a32195780812a554f81c2312090f40_1440w.jpg",
    "https://pic2.zhimg.com/v2-b187f11ba31cd2cb7b32778efa4842f5_1440w.jpg",
    "https://pic3.zhimg.com/v2-f238b53cab0adad490bb9ef0cdaa245e_1440w.jpg",
    "https://pic4.zhimg.com/v2-174970702e86d801d0b29a91c15ae83d_1440w.jpg",
    "https://picx.zhimg.com/v2-99782590d6aef28dfbc0448a303eaa85_1440w.jpg",
    "https://picx.zhimg.com/v2-4760080a860a25fd0f4377598d3d6343_1440w.jpg",
    "https://pic2.zhimg.com/v2-0d8a51c3f51c6cc443ea9e7c71b60889_1440w.jpg",
    "https://picx.zhimg.com/v2-2baaf7d6efe3d8693a103f8b6c7f16df_1440w.jpg",
    "https://pic1.zhimg.com/v2-200052da6e9946b92ee310872bff7c8c_1440w.jpg",
]

def download_images():
    save_dir = "images/zhihu-feishu-doc"
    os.makedirs(save_dir, exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
    }
    
    for i, url in enumerate(IMAGE_URLS, 1):
        try:
            print(f"下载第 {i}/{len(IMAGE_URLS)} 张：{url}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            filename = f"feishu_doc_{i:02d}.jpg"
            filepath = os.path.join(save_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ 已保存：{filepath}")
            
        except Exception as e:
            print(f"❌ 下载失败：{e}")
    
    print(f"\n完成！共下载 {len(IMAGE_URLS)} 张图片到：{save_dir}")

if __name__ == "__main__":
    download_images()
