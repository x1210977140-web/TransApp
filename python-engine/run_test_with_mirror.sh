#!/bin/bash
# 使用国内镜像运行模型加载测试

echo "========================================"
echo "Whisper 模型测试（HF-Mirror 镜像）"
echo "========================================"
echo ""
echo "📍 镜像地址: https://hf-mirror.com"
echo ""

# 进入项目目录
cd /Users/Xiang/PersonalProjects/TransApp/python-engine

# 激活虚拟环境
source .venv/bin/activate

# 配置环境变量使用国内镜像
export HF_ENDPOINT=https://hf-mirror.com

echo "✓ 已配置使用 HF-Mirror 镜像"
echo ""

# 运行测试
python test_model_loading_mirror.py

echo ""
echo "测试完成！"
