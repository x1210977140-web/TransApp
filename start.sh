#!/bin/bash

echo "正在启动 QuickTrans..."
echo ""

# 检查 Python 虚拟环境
if [ ! -d "python-engine/.venv" ]; then
    echo "错误: Python 虚拟环境不存在，请先运行安装脚本"
    exit 1
fi

# 启动 Python API 服务器
cd python-engine
source .venv/bin/activate
echo "正在启动 Python API 服务器 (端口 5000)..."
python api_server.py > /tmp/quicktrans-api.log 2>&1 &
API_PID=$!
echo "Python API 服务器已启动 (PID: $API_PID)"

# 等待 API 服务器启动
sleep 3

# 启动前端
cd ../frontend
echo "正在启动前端应用..."
npm run dev

# 如果前端退出，也关闭 API 服务器
kill $API_PID
