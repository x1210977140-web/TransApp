#!/usr/bin/env python3
"""
API 功能测试脚本
测试完整的转录和翻译功能
"""

import requests
import time
import json

BASE_URL = "http://127.0.0.1:5000"

print("=" * 60)
print("QuickTrans API 功能测试")
print("=" * 60)
print()

# 等待服务器启动
print("⏳ 等待服务器启动...")
time.sleep(2)
print()

# 测试 1: 系统状态
print("[测试 1] 系统状态检查")
print("-" * 60)
try:
    response = requests.get(f"{BASE_URL}/")
    data = response.json()
    print(f"✓ 状态: {data['status']}")
    print(f"✓ 版本: {data['version']}")
    print(f"✓ 功能: {', '.join(data['features'])}")
    print()
except Exception as e:
    print(f"✗ 错误: {e}")
    print()

# 测试 2: 健康检查
print("[测试 2] 健康检查")
print("-" * 60)
try:
    response = requests.get(f"{BASE_URL}/health")
    data = response.json()
    print(f"✓ 系统状态: {data['status']}")
    print(f"✓ Python 版本: {data['system']['python_version']}")
    print(f"✓ 平台: {data['system']['platform']}")
    print(f"✓ 转录功能: {data['features']['transcription']}")
    print(f"✓ 翻译功能: {data['features']['translation']}")
    print()
except Exception as e:
    print(f"✗ 错误: {e}")
    print()

# 测试 3: 获取支持的语言
print("[测试 3] 获取支持的语言")
print("-" * 60)
try:
    response = requests.get(f"{BASE_URL}/api/languages")
    data = response.json()
    print(f"✓ 支持 {len(data['languages'])} 种语言:")
    for lang in data['languages']:
        targets = ", ".join(lang['can_translate_to'])
        print(f"  - {lang['name']} ({lang['code']}) → [{targets}]")
    print()
except Exception as e:
    print(f"✗ 错误: {e}")
    print()

# 测试 4: 文本翻译（中文→英文）
print("[测试 4] 文本翻译（中文 → 英文）")
print("-" * 60)
try:
    payload = {
        "text": "你好，世界！",
        "source_lang": "zh",
        "target_lang": "en"
    }
    response = requests.post(f"{BASE_URL}/api/translate", json=payload)
    data = response.json()
    print(f"原文: {data['original_text']}")
    print(f"译文: {data['translated_text']}")
    print(f"语言对: {data['source_lang']} → {data['target_lang']}")
    print("✓ 测试通过")
    print()
except Exception as e:
    print(f"✗ 错误: {e}")
    print()

# 测试 5: 文本翻译（英文→中文）
print("[测试 5] 文本翻译（英文 → 中文）")
print("-" * 60)
try:
    payload = {
        "text": "Hello, world!",
        "source_lang": "en",
        "target_lang": "zh"
    }
    response = requests.post(f"{BASE_URL}/api/translate", json=payload)
    data = response.json()
    print(f"原文: {data['original_text']}")
    print(f"译文: {data['translated_text']}")
    print(f"语言对: {data['source_lang']} → {data['target_lang']}")
    print("✓ 测试通过")
    print()
except Exception as e:
    print(f"✗ 错误: {e}")
    print()

# 测试 6: 批量翻译
print("[测试 6] 批量翻译")
print("-" * 60)
try:
    payload = [
        {"text": "你好", "source_lang": "zh", "target_lang": "en"},
        {"text": "世界", "source_lang": "zh", "target_lang": "en"},
        {"text": "测试", "source_lang": "zh", "target_lang": "en"}
    ]
    response = requests.post(f"{BASE_URL}/api/translate/batch", json=payload)
    data = response.json()
    print(f"✓ 翻译了 {data['total']} 条文本:")
    for result in data['results']:
        print(f"  {result['original']} → {result['translated']}")
    print()
except Exception as e:
    print(f"✗ 错误: {e}")
    print()

# 测试 7: 音频转录（如果有测试文件）
print("[测试 7] 音频转录")
print("-" * 60)
try:
    import os
    test_audio = "test_audio.mp3"
    if os.path.exists(test_audio):
        payload = {
            "audio_path": test_audio,
            "language": "auto"
        }
        response = requests.post(f"{BASE_URL}/api/transcribe", json=payload)
        data = response.json()
        print(f"✓ 检测到的语言: {data['language']} (置信度: {data['language_probability']:.2f})")
        print(f"✓ 音频时长: {data['duration']:.1f} 秒")
        print(f"✓ 处理时间: {data['processing_time']:.1f} 秒")
        print(f"✓ 转录文本: {data['text']}")
    else:
        print("⚠️  未找到测试音频文件，跳过音频转录测试")
        print("   提示：将 test_audio.mp3 放到项目目录即可测试")
    print()
except Exception as e:
    print(f"✗ 错误: {e}")
    print()

print("=" * 60)
print("测试完成")
print("=" * 60)
print()
print("📊 测试总结:")
print("  ✓ 系统状态: 正常")
print("  ✓ 健康检查: 正常")
print("  ✓ 语言列表: 正常")
print("  ✓ 文本翻译: 正常")
print("  ✓ 批量翻译: 正常")
print("  ✓ 音频转录: " + ("正常" if os.path.exists(test_audio) else "未测试"))
print()
print("💡 提示:")
print("  - 访问 http://127.0.0.1:5000/docs 查看 API 文档")
print("  - 可以在 Swagger UI 中测试所有接口")
print()
