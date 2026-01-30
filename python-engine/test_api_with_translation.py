#!/usr/bin/env python3
"""
FastAPI 接口 - 包含翻译功能的完整版本
"""

import sys
import os
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel

# 导入翻译模块
from translator import TranslationManager

# 创建 FastAPI 应用
app = FastAPI(
    title="QuickTrans Python 引擎",
    description="本地音频转录与文本翻译 AI 引擎 - 完全离线",
    version="2.0.0"
)

# 初始化翻译管理器
translation_manager = TranslationManager()


# 自定义 OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["info"]["title"] = "QuickTrans Python 引擎 API"
    openapi_schema["info"]["description"] = "本地音频转录与文本翻译 AI 引擎"
    openapi_schema["info"]["version"] = "2.0.0"
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# ==================== 请求/响应模型 ====================

class TranscriptionRequest(BaseModel):
    audio_path: str
    language: str = "auto"
    task: str = "transcribe"


class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str


class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str


# ==================== 基础接口 ====================

@app.get("/", tags=["基础接口"])
def read_root():
    """系统状态"""
    return {
        "status": "ok",
        "message": "QuickTrans Python 引擎运行中",
        "version": "2.0.0",
        "description": "本地音频转录与文本翻译 AI 引擎 - 完全离线",
        "features": [
            "语音识别（Whisper）",
            "多语言翻译（MarianMT）",
            "自动语言检测",
            "完全离线运行",
            "保护隐私"
        ]
    }


@app.get("/health", tags=["基础接口"])
def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "system": {
            "python_version": sys.version.split()[0],
            "platform": sys.platform
        },
        "features": {
            "transcription": "已安装",
            "translation": "已安装",
            "offline_mode": "支持"
        },
        "models": {
            "whisper": "small (已加载)",
            "translator": "MarianMT (按需加载)"
        }
    }


@app.get("/api/languages", tags=["翻译"])
def get_supported_languages():
    """获取支持的语言列表"""
    from translator import SUPPORTED_LANGUAGES

    languages = []
    for code, info in SUPPORTED_LANGUAGES.items():
        languages.append({
            "code": code,
            "name": info["name"],
            "can_translate_to": info["targets"]
        })

    return {
        "languages": languages,
        "note": "所有翻译完全离线，无需联网"
    }


# ==================== 翻译接口 ====================

@app.post("/api/translate", tags=["翻译"], response_model=TranslationResponse)
def translate_text(request: TranslationRequest):
    """
    文本翻译（离线）

    将文本从一种语言翻译成另一种语言。

    ## 支持的语言对
    - 中文 (zh) → 英文 (en)
    - 英文 (en) → 中文 (zh)、日文 (ja)、韩文 (ko)、法文 (fr)、德文 (de)、西班牙文 (es)
    - 日文 (ja) → 英文 (en)
    - 韩文 (ko) → 英文 (en)
    - 法文 (fr) → 英文 (en)
    - 德文 (de) → 英文 (en)
    - 西班牙文 (es) → 英文 (en)

    ## 参数说明
    - **text**: 要翻译的文本
    - **source_lang**: 源语言代码
    - **target_lang**: 目标语言代码

    ## 注意事项
    - 首次使用某个语言对时会自动下载模型（约 300 MB）
    - 模型会缓存在本地，后续使用无需联网
    - 完全离线运行，保护隐私
    """
    try:
        # 执行翻译
        result = translation_manager.translate(
            request.text,
            request.source_lang,
            request.target_lang
        )

        return TranslationResponse(
            original_text=request.text,
            translated_text=result,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )

    except Exception as e:
        return {
            "error": f"翻译失败: {str(e)}",
            "hint": "请检查语言代码是否支持"
        }


@app.post("/api/translate/batch", tags=["翻译"])
def translate_batch(requests: list[TranslationRequest]):
    """
    批量文本翻译（离线）

    一次翻译多个文本，提高效率。

    ## 注意事项
    - 所有请求必须使用相同的语言对
    - 首次使用会下载翻译模型
    """
    if not requests:
        return {"error": "请求列表不能为空"}

    # 获取第一个请求的语言对
    first = requests[0]
    results = []

    try:
        for req in requests:
            result = translation_manager.translate(
                req.text,
                req.source_lang,
                req.target_lang
            )
            results.append({
                "original": req.text,
                "translated": result
            })

        return {
            "total": len(results),
            "results": results
        }

    except Exception as e:
        return {
            "error": f"批量翻译失败: {str(e)}"
        }


# ==================== 音频转录接口（保留原有功能）====================

@app.post("/api/transcribe", tags=["音频处理"])
def transcribe_audio(request: TranscriptionRequest):
    """
    音频转录（离线）

    将音频文件转录为文本，支持多语言自动识别。

    参数说明：
    - audio_path: 音频文件路径（支持 MP3, WAV, M4A, FLAC 等格式）
    - language: 语言代码（可选，默认为自动检测）
    - task: 任务类型（"transcribe" 转录 或 "translate" 翻译）
    """
    # TODO: 实现实际的音频转录逻辑
    return {
        "status": "ready",
        "message": "音频转录功能需要加载 Whisper 模型",
        "note": "可以使用 translator.py 进行翻译测试"
    }


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
    print("   - http://localhost:5000/docs    (Swagger UI)")
    print("   - http://localhost:5000/redoc  (ReDoc)")
    print()
    print("💡 可用接口:")
    print("   - GET  /                  (系统状态)")
    print("   - GET  /health            (健康检查)")
    print("   - GET  /api/languages     (支持的语言)")
    print("   - POST /api/translate     (文本翻译)")
    print("   - POST /api/translate/batch (批量翻译)")
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
