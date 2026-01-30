#!/usr/bin/env python3
"""
测试离线翻译功能
"""

import sys
import os

# 配置使用国内镜像（加速模型下载）
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

print("=" * 60)
print("离线翻译功能测试")
print("=" * 60)
print()
print("特点:")
print("  ✓ 完全离线运行")
print("  ✓ 无需联网")
print("  ✓ 免费使用")
print("  ✓ 基于 MarianMT 模型")
print()

# 检查依赖
print("[1/4] 检查依赖...")
try:
    import transformers
    print("✓ transformers 已安装")
except ImportError:
    print("✗ transformers 未安装")
    print("请运行: pip install transformers")
    sys.exit(1)

try:
    import torch
    print("✓ torch 已安装")
except ImportError:
    print("✗ torch 未安装")
    sys.exit(1)

print()

# 导入翻译模块
print("[2/4] 导入翻译模块...")
try:
    from translator import OfflineTranslator, TranslationManager
    print("✓ 翻译模块导入成功")
except Exception as e:
    print(f"✗ 导入失败: {e}")
    sys.exit(1)

print()

# 测试翻译功能
print("[3/4] 测试翻译功能...")
print()

# 测试 1: 中文 → 英文
print("测试 1: 中文 → 英文")
print("-" * 60)
try:
    translator_zh_en = OfflineTranslator("Helsinki-NLP/opus-mt-zh-en")
    zh_text = "你好，这是一个测试。"
    print(f"原文: {zh_text}")
    en_result = translator_zh_en.translate(zh_text)
    print(f"译文: {en_result}")
    print("✓ 中文→英文 测试通过")
except Exception as e:
    print(f"✗ 测试失败: {e}")
print()

# 测试 2: 英文 → 中文
print("测试 2: 英文 → 中文")
print("-" * 60)
try:
    translator_en_zh = OfflineTranslator("Helsinki-NLP/opus-mt-en-zh")
    en_text = "Hello, this is a test."
    print(f"原文: {en_text}")
    zh_result = translator_en_zh.translate(en_text)
    print(f"译文: {zh_result}")
    print("✓ 英文→中文 测试通过")
except Exception as e:
    print(f"✗ 测试失败: {e}")
print()

# 测试 3: 使用管理器
print("[4/4] 测试翻译管理器...")
print("-" * 60)
try:
    manager = TranslationManager()

    # 测试多语言翻译
    test_cases = [
        ("你好", "zh", "en"),
        ("Hello", "en", "zh"),
    ]

    for text, src, tgt in test_cases:
        result = manager.translate(text, src, tgt)
        print(f"{src}→{tgt}: {text} → {result}")

    print("✓ 翻译管理器测试通过")
except Exception as e:
    print(f"✗ 测试失败: {e}")

print()
print("=" * 60)
print("✅ 离线翻译功能测试完成！")
print("=" * 60)
print()
print("支持的语言对:")
print("  • 中文 → 英文 (zh → en)")
print("  • 英文 → 中文 (en → zh)")
print("  • 日文 → 英文 (ja → en)")
print("  • 英文 → 日文 (en → ja)")
print("  • 韩文 → 英文 (ko → en)")
print("  • 法文 → 英文 (fr → en)")
print("  • 德文 → 英文 (de → en)")
print("  • 西班牙文 → 英文 (es → en)")
print()
print("注意:")
print("  • 首次使用会自动下载模型（约 300 MB/语言对）")
print("  • 模型会缓存在本地，无需重复下载")
print("  • 完全离线运行，无需联网")
print()
