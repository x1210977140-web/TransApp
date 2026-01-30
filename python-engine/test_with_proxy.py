#!/usr/bin/env python3
"""
带代理配置的模型加载测试
"""

import sys
import os

# 配置使用国内镜像
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

print("=" * 60)
print("Whisper 模型加载测试")
print("=" * 60)
print()
print("配置:")
print("  镜像: https://hf-mirror.com")
print("  模型: small (~460 MB)")
print()

# 测试镜像连接
print("测试镜像连接...")
try:
    import urllib.request
    response = urllib.request.urlopen('https://hf-mirror.com', timeout=10)
    print("✓ HF-Mirror 连接正常")
except Exception as e:
    print(f"✗ 连接失败: {e}")
    sys.exit(1)

print()

# 导入并测试
from faster_whisper import WhisperModel
import time

try:
    print("⏳ 加载 Whisper small 模型...")
    print("   从 HF-Mirror 下载（~460 MB）...")
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
    print(f"📍 下载源: HF-Mirror (国内镜像)")
    print()
    print("🎉 faster-whisper 工作正常！")
    print()
    print("下一步：")
    print("  1. 运行 FastAPI 测试: python test_api.py")
    print("  2. 或继续初始化 Electron + React 项目")

except Exception as e:
    print()
    print("❌ 加载失败！")
    print(f"错误: {e}")
    print()
    import traceback
    traceback.print_exc()
    sys.exit(1)
