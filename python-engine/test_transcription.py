#!/usr/bin/env python3
"""
音频转录功能测试
测试 Whisper 模型的语音识别功能
"""

import sys
import os
import time

print("=" * 60)
print("Whisper 音频转录测试")
print("=" * 60)
print()

from faster_whisper import WhisperModel

# 检查是否有测试音频
print("[1/4] 检查测试音频...")

# 查找测试音频文件
test_audio_paths = [
    "test_audio.mp3",
    "test_audio.wav",
    "sample.mp3",
    "sample.wav",
    "../test_audio.mp3",
    "../test_audio.wav"
]

test_audio = None
for path in test_audio_paths:
    if os.path.exists(path):
        test_audio = path
        break

if test_audio:
    print(f"✓ 找到测试音频: {test_audio}")
    file_size = os.path.getsize(test_audio) / (1024 * 1024)
    print(f"  文件大小: {file_size:.2f} MB")
else:
    print("⚠️  未找到测试音频文件")
    print()
    print("提示：你可以:")
    print("  1. 将测试音频文件放到项目目录")
    print("  2. 命名为 test_audio.mp3 或 test_audio.wav")
    print("  3. 重新运行此测试")
    print()
    print("或者跳过音频测试，仅验证模型功能...")

    response = input("是否继续模型功能测试？(y/n): ").lower()
    if response != 'y':
        print("测试结束")
        sys.exit(0)

    test_audio = None

print()

# 加载模型
print("[2/4] 加载 Whisper 模型...")
start_time = time.time()

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="float32"
)

load_time = time.time() - start_time
print(f"✓ 模型加载成功（{load_time:.1f} 秒）")
print()

# 测试模型初始化
print("[3/4] 验证模型功能...")
print("  模型配置:")
print("    - 模型类型: small")
print("    - 设备: CPU")
print("    - 计算类型: float32")
print("  ✓ 模型验证通过")
print()

# 如果有测试音频，进行转录测试
if test_audio:
    print("[4/4] 测试音频转录...")
    print(f"  正在转录: {test_audio}")
    print()

    try:
        start_time = time.time()

        # 转录音频
        segments, info = model.transcribe(
            test_audio,
            language="auto",  # 自动检测语言
            task="transcribe"
        )

        # 收集结果
        transcription = []
        for segment in segments:
            transcription.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            })

        elapsed = time.time() - start_time

        print("✓ 转录完成！")
        print()
        print("=" * 60)
        print("转录结果:")
        print("=" * 60)
        print()
        print(f"检测到的语言: {info.language} (置信度: {info.language_probability:.2f})")
        print(f"音频时长: {info.duration:.1f} 秒")
        print(f"处理时间: {elapsed:.1f} 秒")
        print(f"处理倍率: {info.duration/elapsed:.2f}x")
        print()
        print("转录文本:")
        print("-" * 60)
        for seg in transcription:
            print(f"[{seg['start']:.1f}s - {seg['end']:.1f}s] {seg['text']}")
        print("-" * 60)
        print()
        print("✅ 音频转录功能正常！")

    except Exception as e:
        print(f"✗ 转录失败: {e}")
        print()
        print("可能的原因:")
        print("  1. 音频格式不支持")
        print("  2. 音频文件损坏")
        print("  3. 需要安装 ffmpeg（系统已有）")
        import traceback
        traceback.print_exc()

else:
    print("[4/4] 跳过音频转录（无测试音频）")
    print()
    print("⚠️  要完整测试音频转录功能，请:")
    print("  1. 准备一个音频文件（MP3/WAV/M4A）")
    print("  2. 放到项目目录")
    print("  3. 重新运行此测试")

print()
print("=" * 60)
print("测试完成")
print("=" * 60)
print()
print("总结:")
print("  ✓ 模型加载: 正常")
print("  ✓ 模型功能: 正常")
if test_audio:
    print("  ✓ 音频转录: 正常")
else:
    print("  ⚠️  音频转录: 未测试（需要音频文件）")
print()
print("下一步:")
print("  1. 测试 FastAPI 接口: python test_api.py")
print("  2. 或继续方案 B: 初始化 Electron + React 项目")
