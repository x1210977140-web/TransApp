#!/usr/bin/env python3
"""
FastAPI 接口测试 - 中文版
"""

import sys
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel

# 创建 FastAPI 应用（中文配置）
app = FastAPI(
    title="QuickTrans Python 引擎",
    description="""
    本地音频转录 AI 引擎，基于 faster-whisper。

    ## 功能特点
    * 支持多种音频格式（MP3, WAV, M4A 等）
    * 自动语言识别
    * 高精度语音识别
    * 本地处理，保护隐私
    """,
    version="1.0.0",
    terms_of_service="",
    contact={
        "name": "QuickTrans 团队",
        "url": "https://github.com/quicktrans",
    },
    license_info={
        "name": "MIT License",
    },
)

# 自定义 OpenAPI 架构
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # 中文标签
    openapi_schema["info"]["title"] = "QuickTrans Python 引擎 API"
    openapi_schema["info"]["description"] = "本地音频转录 AI 引擎 - 基于 faster-whisper"
    openapi_schema["info"]["version"] = "1.0.0"

    # 为路径添加中文标签
    if "paths" in openapi_schema:
        for path in openapi_schema["paths"]:
            for method in openapi_schema["paths"][path]:
                if "summary" not in openapi_schema["paths"][path][method]:
                    openapi_schema["paths"][path][method]["summary"] = f"{method.upper()} {path}"
                    openapi_schema["paths"][path][method]["description"] = f"{method.upper()} 请求 {path}"

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# 定义请求模型
class TranscriptionRequest(BaseModel):
    audio_path: str
    language: str = "auto"
    task: str = "transcribe"

    class Config:
        json_schema_extra = {
            "example": {
                "audio_path": "/path/to/audio.mp3",
                "language": "auto",
                "task": "transcribe"
            }
        }

# 定义响应模型
class TranscriptionResponse(BaseModel):
    text: str
    language: str
    duration: float
    confidence: float = 0.95

    class Config:
        json_schema_extra = {
            "example": {
                "text": "这是转录的文本内容",
                "language": "zh",
                "duration": 10.5,
                "confidence": 0.95
            }
        }

# 基础路由
@app.get("/",
    summary="系统状态",
    description="获取系统基本信息和运行状态",
    tags=["基础接口"])
def read_root():
    """根路径 - 系统状态检查"""
    return {
        "status": "ok",
        "status_text": "运行正常",
        "message": "QuickTrans Python 引擎运行中",
        "version": "1.0.0",
        "description": "本地音频转录 AI 引擎",
        "features": [
            "语音识别",
            "多语言支持",
            "自动语言检测",
            "本地处理，保护隐私"
        ]
    }


@app.get("/health",
    summary="健康检查",
    description="获取系统详细健康状态",
    response_description="系统健康状态信息",
    tags=["基础接口"])
def health_check():
    """健康检查端点 - 获取系统详细信息"""
    return {
        "status": "healthy",
        "status_text": "运行正常",
        "system": {
            "python_version": sys.version.split()[0],
            "platform": sys.platform,
        },
        "dependencies": {
            "faster_whisper": "已安装",
            "fastapi": "已安装",
            "uvicorn": "已安装",
            "torch": "已安装"
        },
        "model": {
            "name": "Whisper Small",
            "status": "已加载",
            "size": "473 MB"
        }
    }


@app.get("/api/models",
    summary="可用模型列表",
    description="获取所有可用的 Whisper 模型",
    tags=["模型管理"])
def list_models():
    """获取可用模型列表"""
    return {
        "models": [
            {
                "name": "tiny",
                "size": "40 MB",
                "description": "最小最快，适合快速测试",
                "available": False
            },
            {
                "name": "base",
                "size": "140 MB",
                "description": "基础模型，速度和准确度平衡",
                "available": False
            },
            {
                "name": "small",
                "size": "470 MB",
                "description": "小型模型，推荐日常使用",
                "available": True,
                "loaded": True
            },
            {
                "name": "medium",
                "size": "1.5 GB",
                "description": "中型模型，更高准确度",
                "available": False
            },
            {
                "name": "large",
                "size": "2.9 GB",
                "description": "大型模型，最高准确度",
                "available": False
            }
        ],
        "current_model": "small"
    }


@app.post("/api/transcribe",
    summary="音频转录",
    description="将音频文件转录为文本，支持多语言自动识别",
    response_description="转录结果，包含文本、语言和时长信息",
    tags=["音频处理"])
def transcribe_audio(request: TranscriptionRequest):
    """
    音频转录端点

    ## 功能说明
    将音频文件转录为文本，支持多种音频格式和多语言识别。

    ## 参数说明
    - **audio_path**: 音频文件路径（支持 MP3, WAV, M4A, FLAC 等格式）
    - **language**: 语言代码（可选）
      - 默认为 'auto' 自动检测
      - 可选值：'zh' 中文, 'en' 英文, 'ja' 日文, 'ko' 韩文等
    - **task**: 任务类型（可选）
      - 'transcribe': 转录（默认）
      - 'translate': 翻译成英文

    ## 返回说明
    - **text**: 转录的文本内容
    - **language**: 检测到的语言
    - **duration**: 音频时长（秒）
    - **confidence**: 置信度（0-1）

    ## 注意事项
    - 音频文件必须是有效路径
    - 支持的格式：MP3, WAV, M4A, FLAC, OGG
    - 首次使用可能需要几秒钟加载模型
    """
    # TODO: 实现实际的音频转录逻辑
    return TranscriptionResponse(
        text="这是一个测试响应。实际实现需要加载 Whisper 模型并进行音频转录。",
        language="zh",
        duration=0.0,
        confidence=0.95
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
    print("   - http://localhost:5000/docs    (Swagger UI 中文)")
    print("   - http://localhost:5000/redoc  (ReDoc)")
    print()
    print("💡 可用接口:")
    print("   - GET  /                  (系统状态)")
    print("   - GET  /health            (健康检查)")
    print("   - GET  /api/models        (模型列表)")
    print("   - POST /api/transcribe    (音频转录)")
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
