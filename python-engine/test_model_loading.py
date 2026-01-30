#!/usr/bin/env python3
"""
Whisper 模型加载测试

目的：验证 faster-whisper 和 PyTorch 是否能正常工作
"""

import sys
from faster_whisper import WhisperModel

def test_model_loading():
    """测试 Whisper 模型是否能正常加载"""

    print("=" * 60)
    print("Whisper 模型加载测试")
    print("=" * 60)
    print()

    # 模型配置
    model_size = "medium"  # 可选: tiny, base, small, medium, large

    print(f"📦 模型大小: {model_size}")
    print(f"🔄 正在加载模型...")
    print()

    try:
        # 加载模型
        # 首次运行会自动下载模型文件（约 1.5 GB）
        model = WhisperModel(
            model_size,
            device="cpu",  # Apple Silicon 上的优化
            compute_type="float32"  # 或 "int8" 以节省内存
        )

        print("✅ 模型加载成功！")
        print()
        print("📊 模型信息:")
        print(f"   - 模型类型: {model_size}")
        print(f"   - 设备: CPU")
        print(f"   - 计算类型: float32")
        print()
        print("🎉 faster-whisper 和 PyTorch 工作正常！")
        print()
        print("下一步：运行 test_transcription.py 测试音频转录")
        print()

        return True

    except Exception as e:
        print("❌ 模型加载失败！")
        print()
        print(f"错误信息: {e}")
        print()
        print("请检查:")
        print("  1. 网络连接（首次需要下载模型）")
        print("  2. 磁盘空间（至少需要 2 GB）")
        print("  3. Python 虚拟环境是否激活")
        print()

        return False


if __name__ == "__main__":
    success = test_model_loading()
    sys.exit(0 if success else 1)
