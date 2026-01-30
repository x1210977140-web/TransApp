#!/usr/bin/env python3
"""
测试已下载的 Whisper 模型
"""

import sys
import os

print("=" * 60)
print("Whisper 模型加载测试（使用已下载的模型）")
print("=" * 60)
print()

from faster_whisper import WhisperModel
import time

try:
    print("⏳ 加载 Whisper small 模型...")
    print("   使用本地缓存的模型文件")
    print()

    start_time = time.time()

    # 加载模型（会自动使用本地缓存）
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
    print(f"📍 缓存位置: ~/Library/Application Support/faster-whisper/")
    print()
    print("🎉 faster-whisper 工作正常！")
    print()
    print("✅ 模型验证通过！")
    print()
    print("下一步：")
    print("  1. 测试 FastAPI 接口: python test_api.py")
    print("  2. 继续方案 B: 初始化 Electron + React 项目")

except Exception as e:
    print()
    print("❌ 加载失败！")
    print(f"错误: {e}")
    print()
    import traceback
    traceback.print_exc()
    sys.exit(1)
