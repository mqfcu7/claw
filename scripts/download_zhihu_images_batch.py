#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
从知乎文章下载所有图片
用法：python3 download_zhihu_images.py
"""

import os
import requests

# 知乎文章的所有图片 URL
IMAGE_URLS = [
    "https://pic3.zhimg.com/v2-73c3016f75eed0dd7a059eb524870934_1440w.jpg",
    "https://pic4.zhimg.com/v2-f4eebfd6c020508d2f1422b65a5e93f1_1440w.jpg",
    "https://pic4.zhimg.com/v2-42f07a74199bb3eae479ef7f6840e127_1440w.jpg",
    "https://pica.zhimg.com/v2-fe5aa4c2a6eaddbc224f7fa47f41a3c8_1440w.jpg",
    "https://picx.zhimg.com/v2-0e0e52d0af37495a368e49cbc8fb779d_1440w.jpg",
    "https://pic1.zhimg.com/v2-9281e8702018b435ee29526b5db42fc6_1440w.jpg",
    "https://pic4.zhimg.com/v2-2399db5ddd6a54cea5aeba923753838b_1440w.jpg",
    "https://pic1.zhimg.com/v2-7ab7b6e357189eb625f5493a3a7670a4_1440w.jpg",
    "https://pic4.zhimg.com/v2-6ad1ba914931d995a7a0f6fdb2473d97_1440w.jpg",
    "https://picx.zhimg.com/v2-6b672b0e89120d7c818ca545dd9abcb3_1440w.jpg",
    "https://pic4.zhimg.com/v2-63e3f90d170c8e120b4b570d02800909_1440w.jpg",
    "https://picx.zhimg.com/v2-da31d9315d418df1b87ae684919192f5_1440w.jpg",
    "https://pic2.zhimg.com/v2-bb70c37140876dfa9c0a6bf009278961_1440w.jpg",
    "https://pic3.zhimg.com/v2-11d16eee17de983c38172a0d77f9df94_1440w.jpg",
    "https://pic1.zhimg.com/v2-9bb8997975fe782731a57628ec25e770_1440w.jpg",
    "https://pic3.zhimg.com/v2-de44804fdd86de04f18f06d65678d8ae_1440w.jpg",
    "https://pica.zhimg.com/v2-7a45f0efc95a47bae5cf3b244f47eb2c_1440w.jpg",
    "https://pica.zhimg.com/v2-28d2d02553bea351e5c00630a09fb5b4_1440w.jpg",
    "https://pic1.zhimg.com/v2-0682c7956f3cbd04b7442d92c46d0368_1440w.jpg",
    "https://pica.zhimg.com/v2-23d6e2d7cf93d5afe6b48920152cd9ea_1440w.jpg",
    "https://pic1.zhimg.com/v2-57c29aeae7ab6239a17288fe2640e0b2_1440w.jpg",
    "https://pic2.zhimg.com/v2-0652cb9315fee66bdf3c3f43beb0a903_1440w.jpg",
    "https://pic3.zhimg.com/v2-43e2ed63473a26fe25ae2c43fcff9b12_1440w.jpg",
    "https://pica.zhimg.com/v2-cbf35b7b2bfe69d8b52c906bc81d6600_1440w.jpg",
    "https://picx.zhimg.com/v2-385f0e6f34f4fdf16c29935e74b9735b_1440w.jpg",
    "https://pic3.zhimg.com/v2-64da73986f6ff4c7b3c3e40417d19a9c_1440w.jpg",
    "https://pic1.zhimg.com/v2-e138a31da7db86d18bfab43bc8f49fe0_1440w.jpg",
    "https://pica.zhimg.com/v2-fc658dbf6709855388624122cd3deff4_1440w.jpg",
    "https://pic1.zhimg.com/v2-cea235b7d3ffc87f1550df61c475d6fc_1440w.jpg",
    "https://pic2.zhimg.com/v2-a51584bac2dfda8bfa9d75095f86f7ff_1440w.jpg",
    "https://pic4.zhimg.com/v2-a7df83f5997787cc8f18d539d7baa8a1_1440w.jpg",
    "https://pic4.zhimg.com/v2-06e88f47cad258f7cc9b74fba33abb79_1440w.jpg",
    "https://pic1.zhimg.com/v2-89ffd64260405a070ea13546c3cd7dcc_1440w.jpg",
    "https://pica.zhimg.com/v2-017221ab6662879a3c429dd7388c8c5c_1440w.jpg",
    "https://pic1.zhimg.com/v2-666fe67b213c2dbcf89745ca66af4cbc_1440w.jpg",
    "https://picx.zhimg.com/v2-85bc023112d7239ceb6fb0c9292a3_1440w.jpg",
    "https://pica.zhimg.com/v2-dedca2dc4a213043d10658e27d4a88da_1440w.jpg",
    "https://pic1.zhimg.com/v2-4ddf9feb38b12513cc4dd953cd0f9d5c_1440w.jpg",
    "https://pic4.zhimg.com/v2-0c42148c773789dcedbba755f8cc8d2d_1440w.jpg",
    "https://pica.zhimg.com/v2-42854db282bf55ac863b7ba0b85c01a2_1440w.jpg",
    "https://pica.zhimg.com/v2-ce2e323f1b7879dbdd52fc0b8f3a3bc4_1440w.jpg",
    "https://pic2.zhimg.com/v2-6db07f0a5e739cc8593be32c308b308f_1440w.jpg",
    "https://pic4.zhimg.com/v2-53c92236f3407eabadecba494d3535cb_1440w.jpg",
    "https://picx.zhimg.com/v2-9606aeee1b7cdcabbe8b54a6ccbf12b9_1440w.jpg",
    "https://pic3.zhimg.com/v2-0bff72ef4c4e6eb1e95aa0e2b67d7672_1440w.jpg",
    "https://pica.zhimg.com/v2-d801807d2b1a55a9c99ce5427e7723e2_1440w.jpg",
    "https://pica.zhimg.com/v2-167cc00192dab03cf9ba7462cee41734_1440w.jpg",
    "https://picx.zhimg.com/v2-3c95271cf5d470ff9ddd201c71fa7f3f_1440w.jpg",
    "https://pica.zhimg.com/v2-55179491a4365f0d4e59fceeef62cda0_1440w.jpg",
    "https://pic1.zhimg.com/v2-a3a4bdf153987c8a58d9102040f0b7c0_1440w.jpg",
    "https://pica.zhimg.com/v2-254a0e4bf084968d3dd9f7294166b2ba_1440w.jpg",
    "https://pic3.zhimg.com/v2-851b7a7c76f57a17c4eb9b6ede9ea38c_1440w.jpg",
    "https://pica.zhimg.com/v2-9a3470dfde7d5438c55eb91b4c68140c_1440w.jpg",
    "https://pica.zhimg.com/v2-91abc6510ffcc285eca1e63a519b0b1e_1440w.jpg",
]

def download_images():
    save_dir = "images/zhihu-screenshots"
    os.makedirs(save_dir, exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
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
