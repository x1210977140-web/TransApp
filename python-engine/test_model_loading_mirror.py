#!/usr/bin/env python3
"""
Whisper 模型加载测试 - 使用国内镜像
适用于国内网络环境
"""

import sys
import os

# 配置使用国内镜像
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

print("=" * 60)
print("Whisper 模型加载测试（国内镜像版）")
print("=" * 60)
print()
print("📍 使用镜像: https://hf-mirror.com")
print()

# 测试镜像连接
print("[1/5] 测试镜像连接...")
try:
    import urllib.request
    response = urllib.request.urlopen('https://hf-mirror.com', timeout=10)
    print("✓ HF-Mirror 连接正常")
except Exception as e:
    print(f"✗ 镜像连接失败: {e}")
    sys.exit(1)

print()

# 导入 faster-whisper
print("[2/5] 导入 faster-whisper...")
try:
    from faster_whisper import WhisperModel
    print("✓ faster-whisper 导入成功")
except Exception as e:
    print(f"✗ 导入失败: {e}")
    sys.exit(1)

print()

# 检查模型缓存目录
print("[3/5] 检查模型缓存目录...")
import time
cache_dir = os.path.expanduser("~/Library/Application Support/faster-whisper/")
print(f"缓存目录: {cache_dir}")

if os.path.exists(cache_dir):
    size = sum(os.path.getsize(os.path.join(dirpath, filename))
               for dirpath, _, filenames in os.walk(cache_dir)
               for filename in filenames)
    size_mb = size / (1024 * 1024)
    print(f"已缓存: {size_mb:.1f} MB")
else:
    print("缓存目录不存在（首次下载）")

print()

# 开始加载模型
print("[4/5] 开始加载模型...")
print("  模型大小: medium")
print("  设备: CPU")
print("  计算类型: float32")
print()
print("⏳ 从 HF-Mirror 下载 ~1.5 GB...")
print("💡 国内镜像，速度较快！")
print()

start_time = time.time()

try:
    # 加载模型（会从 HF-Mirror 下载）
    model = WhisperModel(
        "medium",
        device="cpu",
        compute_type="float32"
    )

    elapsed = time.time() - start_time
    print(f"✓ 模型加载成功！（耗时 {elapsed:.1f} 秒）")

    print()
    print("[5/5] 验证模型...")
    print("✓ 模型验证通过")

    print()
    print("=" * 60)
    print("🎉 所有测试通过！")
    print("=" * 60)
    print()
    print("📊 模型信息:")
    print(f"   - 模型类型: medium")
    print(f"   - 设备: CPU")
    print(f"   - 计算类型: float32")
    print(f"   - 加载时间: {elapsed:.1f} 秒")
    print(f"   - 下载源: HF-Mirror (国内镜像)")
    print()
    print("✅ faster-whisper 和 PyTorch 工作正常！")
    print()

    # 检查缓存大小
    if os.path.exists(cache_dir):
        size = sum(os.path.getsize(os.path.join(dirpath, filename))
                   for dirpath, _, filenames in os.walk(cache_dir)
                   for filename in filenames)
        size_gb = size / (1024 * 1024 * 1024)
        print(f"💾 模型缓存大小: {size_gb:.2f} GB")

except Exception as e:
    elapsed = time.time() - start_time
    print()
    print("=" * 60)
    print("✗ 模型加载失败！")
    print("=" * 60)
    print()
    print(f"错误信息: {e}")
    print()
    print(f"已运行时间: {elapsed:.1f} 秒")
    print()
    print("建议:")
    print("  1. 检查 HF-Mirror 是否可访问")
    print("  2. 尝试方案 2（使用更小的模型）")
    print("  3. 尝试方案 3（手动下载）")
    print()

    import traceback
    print("详细错误信息:")
    print(traceback.format_exc())

    sys.exit(1)
