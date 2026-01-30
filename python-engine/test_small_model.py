#!/usr/bin/env python3
"""
使用更小的 Whisper 模型进行测试
"""

import sys
import os

# 配置使用国内镜像
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

print("=" * 60)
print("Whisper 模型加载测试（Small 模型）")
print("=" * 60)
print()
print("📍 使用镜像: https://hf-mirror.com")
print("📦 模型大小: small (~460 MB)")
print()

from faster_whisper import WhisperModel
import time

try:
    print("⏳ 加载 small 模型...")
    start_time = time.time()

    model = WhisperModel(
        "small",  # 使用 small 模型
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
    print(f"📦 模型大小: small (~460 MB)")
    print()
    print("🎉 faster-whisper 工作正常！")
    print()
    print("💡 提示:")
    print("  - small 模型适合快速测试")
    print("  - medium 模型准确度更高（~1.5 GB）")
    print("  - 可以根据需要切换模型大小")

except Exception as e:
    print()
    print("❌ 加载失败！")
    print(f"错误: {e}")
    sys.exit(1)
