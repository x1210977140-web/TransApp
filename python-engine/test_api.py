#!/usr/bin/env python3
"""
FastAPI 接口测试

目的：验证 FastAPI 和 Uvicorn 是否能正常工作
"""

import sys
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

# 创建 FastAPI 应用
app = FastAPI(
    title="QuickTrans Python 引擎",
    description="本地音频转录 AI 引擎 - 基于 faster-whisper",
    version="1.0.0",
    docs_language="zh"  # 设置文档语言为中文
)


# 定义请求模型
class TranscriptionRequest(BaseModel):
    audio_path: str
    language: str = "auto"
    task: str = "transcribe"


# 定义响应模型
class TranscriptionResponse(BaseModel):
    text: str
    language: str
    duration: float
    status: str = "success"


# 基础路由
@app.get("/")
def read_root():
    """根路径 - 健康检查"""
    return {
        "status": "ok",
        "message": "QuickTrans Python 引擎运行中",
        "version": "1.0.0",
        "description": "本地音频转录 AI 引擎"
    }


@app.get("/health")
def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "status_text": "运行正常",
        "python_version": sys.version.split()[0],
        "faster_whisper": "已安装",
        "fastapi": "已安装",
        "model": "已加载"
    }


@app.post("/api/transcribe", response_model=TranscriptionResponse)
def transcribe_audio(request: TranscriptionRequest):
    """
    音频转录端点

    注意：这是一个简化的示例，实际实现需要加载 Whisper 模型
    """
    # TODO: 实现实际的音频转录逻辑
    return TranscriptionResponse(
        text="这是一个测试响应。实际实现需要 Whisper 模型。",
        language="zh",
        duration=0.0
    )


if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("QuickTrans Python 引擎 - FastAPI 服务器")
    print("=" * 60)
    print()
    print("🚀 正在启动开发服务器...")
    print()
    print("📍 服务地址:")
    print("   - http://localhost:5000")
    print("   - http://127.0.0.1:5000")
    print()
    print("📖 API 文档:")
    print("   - http://localhost:5000/docs (Swagger UI)")
    print("   - http://localhost:5000/redoc (ReDoc)")
    print()
    print("💡 可用接口:")
    print("   - GET  /               (健康检查)")
    print("   - GET  /health         (系统状态)")
    print("   - POST /api/transcribe (音频转录)")
    print()
    print("⚠️  按 Ctrl+C 停止服务器")
    print()

    # 启动服务器
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=5000,
        log_level="info"
    )
