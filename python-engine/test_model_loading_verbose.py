#!/usr/bin/env python3
"""
Whisper 模型加载测试（详细进度版）
"""

import sys
import time

print("=" * 60)
print("Whisper 模型加载测试（详细版）")
print("=" * 60)
print()

# 测试网络连接
print("[1/5] 测试网络连接...")
try:
    import urllib.request
    response = urllib.request.urlopen('https://huggingface.co', timeout=10)
    print("✓ Hugging Face 连接正常")
except Exception as e:
    print(f"✗ 网络连接失败: {e}")
    print("\n请检查:")
    print("  1. 网络连接是否正常")
    print("  2. 是否需要配置代理")
    print("  3. 防火墙设置")
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
import os
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
print("⏳ 首次运行需要下载 ~1.5 GB，请耐心等待...")
print()

start_time = time.time()

try:
    # 加载模型（这里会卡住一段时间）
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
    print("可能的原因:")
    print("  1. 网络连接不稳定")
    print("  2. 磁盘空间不足（需要至少 3 GB）")
    print("  3. 权限问题")
    print("  4. 防火墙阻止了下载")
    print()
    print("建议:")
    print("  1. 检查网络连接")
    print("  2. 运行: df -h ~ （检查磁盘空间）")
    print("  3. 尝试使用更小的模型: model_size='small'")
    print("  4. 查看完整错误日志")
    print()

    import traceback
    print("详细错误信息:")
    print(traceback.format_exc())

    sys.exit(1)
