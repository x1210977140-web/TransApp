#!/usr/bin/env python3
"""
FastAPI 接口测试 - 中文简化版
"""

import sys
from fastapi import FastAPI
from pydantic import BaseModel

# 创建 FastAPI 应用
app = FastAPI(
    title="QuickTrans Python 引擎",
    description="本地音频转录 AI 引擎",
    version="1.0.0"
)

# 定义请求模型
class TranscriptionRequest(BaseModel):
    audio_path: str
    language: str = "自动检测"
    task: str = "转录"

    class Config:
        json_schema_extra = {
            "example": {
                "audio_path": "test.mp3",
                "language": "自动检测",
                "task": "转录"
            }
        }

# 定义响应模型
class TranscriptionResponse(BaseModel):
    text: str
    language: str
    duration: float
    status: str = "成功"


@app.get("/", tags=["基础接口"])
def read_root():
    """
    系统状态

    获取系统基本信息和运行状态
    """
    return {
        "状态": "正常",
        "消息": "QuickTrans Python 引擎运行中",
        "版本": "1.0.0",
        "描述": "本地音频转录 AI 引擎",
        "功能": [
            "语音识别",
            "多语言支持",
            "自动语言检测",
            "本地处理，保护隐私"
        ]
    }


@app.get("/health", tags=["基础接口"])
def health_check():
    """
    健康检查

    获取系统详细健康状态
    """
    return {
        "状态": "健康",
        "Python版本": sys.version.split()[0],
        "已安装组件": {
            "faster_whisper": "已安装",
            "fastapi": "已安装",
            "torch": "已安装",
            "模型": "已加载"
        }
    }


@app.get("/api/models", tags=["模型管理"])
def list_models():
    """
    模型列表

    获取所有可用的 Whisper 模型
    """
    return {
        "可用模型": [
            {
                "名称": "small",
                "大小": "470 MB",
                "描述": "小型模型，推荐日常使用",
                "状态": "已加载"
            },
            {
                "名称": "medium",
                "大小": "1.5 GB",
                "描述": "中型模型，更高准确度",
                "状态": "未加载"
            },
            {
                "名称": "large",
                "大小": "2.9 GB",
                "描述": "大型模型，最高准确度",
                "状态": "未加载"
            }
        ],
        "当前模型": "small"
    }


@app.post("/api/transcribe", tags=["音频处理"])
def transcribe_audio(request: TranscriptionRequest):
    """
    音频转录

    将音频文件转录为文本，支持多语言自动识别

    参数说明：
    - audio_path: 音频文件路径（支持 MP3, WAV, M4A 等）
    - language: 语言代码（可选，默认为自动检测）
    - task: 任务类型（"转录" 或 "翻译"）
    """
    # TODO: 实现实际的音频转录逻辑
    return {
        "状态": "测试模式",
        "消息": "这是一个测试响应。实际实现需要加载 Whisper 模型并进行音频转录。",
        "文本": "示例转录文本",
        "语言": "中文",
        "时长": 0.0
    }


if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("QuickTrans Python 引擎 - FastAPI 服务器（中文版）")
    print("=" * 60)
    print()
    print("🚀 正在启动开发服务器...")
    print()
    print("📍 服务地址:")
    print("   - http://localhost:5000")
    print("   - http://127.0.0.1:5000")
    print()
    print("📖 API 文档:")
    print("   - http://localhost:5000/docs    (Swagger UI)")
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
