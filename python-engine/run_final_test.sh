#!/bin/bash
# 最终测试脚本 - 使用国内镜像

echo "========================================"
echo "Whisper 模型测试（HF-Mirror）"
echo "========================================"
echo ""
echo "📍 镜像: https://hf-mirror.com"
echo "📦 模型: small (~460 MB)"
echo ""

cd /Users/Xiang/PersonalProjects/TransApp/python-engine
source .venv/bin/activate

# 配置镜像
export HF_ENDPOINT=https://hf-mirror.com

# 测试镜像连接
echo "测试镜像连接..."
if curl -s --connect-timeout 5 https://hf-mirror.com > /dev/null 2>&1; then
    echo "✓ HF-Mirror 连接正常"
else
    echo "✗ HF-Mirror 连接失败"
    echo ""
    echo "尝试其他方案..."
    exit 1
fi

echo ""
echo "开始加载模型..."
echo ""

python test_small_model.py
