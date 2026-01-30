#!/bin/bash
# QuickTrans API 服务器启动脚本

echo "============================================================"
echo "  QuickTrans API 服务器"
echo "============================================================"
echo ""

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "❌ 错误: 虚拟环境不存在"
    echo "   请先运行: python3 -m venv .venv"
    exit 1
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source .venv/bin/activate

# 检查依赖
echo "✓ 虚拟环境已激活"
echo ""

# 显示信息
echo "📋 服务信息:"
echo "   - 地址: http://127.0.0.1:5000"
echo "   - 文档: http://127.0.0.1:5000/docs"
echo ""
echo "💡 主要功能:"
echo "   - POST /api/transcribe              (音频转录)"
echo "   - POST /api/translate               (文本翻译)"
echo "   - POST /api/translate/batch         (批量翻译)"
echo "   - POST /api/transcribe-and-translate (转录+翻译)"
echo ""
echo "⚠️  按 Ctrl+C 停止服务器"
echo ""
echo "============================================================"
echo ""

# 启动服务器
python api_server.py
