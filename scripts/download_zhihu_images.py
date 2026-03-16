#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
从知乎文章下载所有图片
用法：python3 download_zhihu_images.py <文章 URL> <保存目录>
"""

import sys
import os
import re
import requests
from bs4 import BeautifulSoup

def download_images(url, save_dir):
    """下载网页中的所有图片"""
    
    # 创建保存目录
    os.makedirs(save_dir, exist_ok=True)
    
    # 获取网页内容
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print(f"正在获取网页：{url}")
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
        
        if not img_url:
            continue
        
        # 跳过小图标和占位图
        if 'icon' in img_url or 'placeholder' in img_url:
            continue
        
        # 只下载知乎的图片
        if 'zhimg.com' not in img_url:
            continue
        
        try:
            # 下载图片
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
        print("示例：python3 download_zhihu_images.py 'https://zhuanlan.zhihu.com/p/2001018648215709469' ./zhihu_images")
        sys.exit(1)
    
    url = sys.argv[1]
    save_dir = sys.argv[2]
    
    download_images(url, save_dir)
