#!/bin/bash
# QuickTrans Python 引擎测试脚本
# 用途：自动化测试所有功能

set -e  # 遇到错误立即退出

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目路径
PROJECT_DIR="/Users/Xiang/PersonalProjects/TransApp"
PYTHON_DIR="$PROJECT_DIR/python-engine"
VENV="$PYTHON_DIR/.venv"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}QuickTrans Python 引擎测试${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查虚拟环境
echo -e "${YELLOW}[1/4] 检查虚拟环境...${NC}"
if [ -d "$VENV" ]; then
    echo -e "${GREEN}✓${NC} 虚拟环境存在"
else
    echo -e "${RED}✗${NC} 虚拟环境不存在！"
    echo "请先运行: python3.11 -m venv python-engine/.venv"
    exit 1
fi
echo ""

# 激活虚拟环境
echo -e "${YELLOW}[2/4] 激活虚拟环境...${NC}"
source "$VENV/bin/activate"
echo -e "${GREEN}✓${NC} 虚拟环境已激活"
echo ""

# 测试包导入
echo -e "${YELLOW}[3/4] 测试核心包导入...${NC}"
python -c "import faster_whisper; print('  ✓ faster-whisper')" || echo -e "${RED}  ✗ faster-whisper 导入失败${NC}"
python -c "import torch; print('  ✓ torch')" || echo -e "${RED}  ✗ torch 导入失败${NC}"
python -c "import transformers; print('  ✓ transformers')" || echo -e "${RED}  ✗ transformers 导入失败${NC}"
python -c "import fastapi; print('  ✓ fastapi')" || echo -e "${RED}  ✗ fastapi 导入失败${NC}"
python -c "import uvicorn; print('  ✓ uvicorn')" || echo -e "${RED}  ✗ uvicorn 导入失败${NC}"
python -c "import pydantic; print('  ✓ pydantic')" || echo -e "${RED}  ✗ pydantic 导入失败${NC}"
python -c "import opencc; print('  ✓ opencc')" || echo -e "${RED}  ✗ opencc 导入失败${NC}"
echo ""

# 运行测试脚本
echo -e "${YELLOW}[4/4] 运行模型加载测试...${NC}"
echo -e "${BLUE}注意：首次运行会下载 ~1.5 GB 的模型文件${NC}"
echo -e "${BLUE}可能需要 5-10 分钟，请耐心等待...${NC}"
echo ""

if [ -f "$PYTHON_DIR/test_model_loading.py" ]; then
    python "$PYTHON_DIR/test_model_loading.py"
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}✓ 所有测试通过！${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        echo "下一步："
        echo "  1. 运行 FastAPI 测试: python test_api.py"
        echo "  2. 查看文档: cat README.md"
    else
        echo ""
        echo -e "${RED}========================================${NC}"
        echo -e "${RED}✗ 测试失败${NC}"
        echo -e "${RED}========================================${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} 测试文件不存在: test_model_loading.py"
    exit 1
fi
