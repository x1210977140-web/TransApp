#!/usr/bin/env python3
"""
配置使用系统代理的模型加载测试
"""

import sys
import os

# 配置代理
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'  # 根据你的代理端口修改
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

# 或者使用 SOCKS5 代理
# os.environ['HTTP_PROXY'] = 'socks5://127.0.0.1:7891'
# os.environ['HTTPS_PROXY'] = 'socks5://127.0.0.1:7891'

# 配置镜像（可选，加速下载）
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

print("=" * 60)
print("Whisper 模型加载测试（使用代理）")
print("=" * 60)
print()
print("配置:")
print("  HTTP_PROXY: http://127.0.0.1:7890")
print("  HTTPS_PROXY: http://127.0.0.1:7890")
print("  镜像: https://hf-mirror.com")
print()

# 测试连接
print("测试网络连接...")
try:
    import urllib.request
    # 测试能否访问 Hugging Face 镜像
    response = urllib.request.urlopen('https://hf-mirror.com', timeout=10)
    print("✓ HF-Mirror 连接正常")
except Exception as e:
    print(f"✗ 连接失败: {e}")
    print()
    print("请检查:")
    print("  1. 代理软件是否运行")
    print("  2. 代理端口是否正确（默认 7890）")
    print("  3. 代理是否支持 HTTPS")
    sys.exit(1)

print()

# 导入并测试
from faster_whisper import WhisperModel
import time

try:
    print("⏳ 加载 Whisper small 模型...")
    print("   通过代理下载...")
    print()

    start_time = time.time()

    model = WhisperModel(
        "small",
        device="cpu",
        compute_type="float32"
    )

    elapsed = time.time() - start_time

    print()
    print("=" * 60)
    print("✅ 模型加载成功！")
    print("=" * 60)
    print()
    print(f"⏱️  加载时间: {elapsed:.1f} 秒")
    print(f"📦 模型: small")
    print()

except Exception as e:
    print()
    print("❌ 加载失败！")
    print(f"错误: {e}")
    print()
    print("提示:")
    print("  如果代理连接失败，可能需要检查代理端口")
    print("  常见端口: 7890, 1080, 8080"
    sys.exit(1)
