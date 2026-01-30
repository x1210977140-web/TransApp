#!/bin/bash
# 使用虚拟环境运行模型加载测试

echo "========================================"
echo "Whisper 模型加载测试（虚拟环境版）"
echo "========================================"
echo ""

# 进入项目目录
cd /Users/Xiang/PersonalProjects/TransApp/python-engine

# 激活虚拟环境
echo "激活虚拟环境..."
source .venv/bin/activate

# 显示 Python 路径
echo "Python 路径: $(which python)"
echo ""

# 验证包已安装
echo "验证依赖包..."
python -c "import faster_whisper; print('✓ faster-whisper OK')" || { echo "✗ faster-whisper 缺失"; exit 1; }
python -c "import torch; print('✓ torch OK')" || { echo "✗ torch 缺失"; exit 1; }
echo ""

# 运行测试（详细版本）
echo "开始模型加载测试..."
echo ""

python test_model_loading_verbose.py

echo ""
echo "测试完成！"
