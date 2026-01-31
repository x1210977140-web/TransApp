#!/usr/bin/env python3
"""
QuickTrans API 服务器 - 完整版本
包含音频转录和文本翻译功能
"""

import sys
import os
import time
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 导入功能模块
from faster_whisper import WhisperModel
from translator import TranslationManager, SUPPORTED_LANGUAGES

# 创建 FastAPI 应用
app = FastAPI(
    title="QuickTrans API",
    description="本地音频转录与文本翻译 AI 引擎 - 完全离线",
    version="2.0.0"
)

# 配置 CORS（允许所有来源，因为这是本地应用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
    expose_headers=["*"],  # 暴露所有响应头
)


# ==================== 请求日志中间件 ====================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录所有请求"""
    print(f"[HTTP] {request.method} {request.url.path}")
    print(f"[HTTP] Headers: {dict(request.headers)}")
    if request.method in ["POST", "PUT", "PATCH"]:
        print(f"[HTTP] Body: {request.url.path}")
    response = await call_next(request)
    print(f"[HTTP] Response status: {response.status_code}")
    return response

# 全局模型实例（懒加载）
whisper_model = None
translation_manager = TranslationManager()


# ==================== 请求/响应模型 ====================

class TranscriptionRequest(BaseModel):
    audio_path: str
    language: str = "auto"
    task: str = "transcribe"


class TranscriptionResponse(BaseModel):
    text: str
    language: str
    language_probability: float
    duration: float
    processing_time: float
    segments: list


class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str


class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str


class TranscribeAndTranslateRequest(BaseModel):
    audio_path: str
    source_lang: str = "auto"
    target_lang: str = "en"


# ==================== 辅助函数 ====================

def get_whisper_model():
    """懒加载 Whisper 模型"""
    global whisper_model
    if whisper_model is None:
        print("正在加载 Whisper 模型...")
        whisper_model = WhisperModel(
            "small",
            device="cpu",
            compute_type="float32"
        )
        print("✓ Whisper 模型加载完成")
    return whisper_model


def validate_language(lang_code: str) -> bool:
    """验证语言代码是否支持"""
    return lang_code in SUPPORTED_LANGUAGES


# ==================== 自定义 OpenAPI ====================

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="QuickTrans API",
        version="2.0.0",
        description="本地音频转录与文本翻译 AI 引擎 - 完全离线",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# ==================== 基础接口 ====================

@app.get("/", tags=["基础接口"])
def read_root():
    """系统状态"""
    return {
        "status": "ok",
        "message": "QuickTrans API 运行中",
        "version": "2.0.0",
        "description": "本地音频转录与文本翻译 AI 引擎 - 完全离线",
        "features": [
            "语音识别（Whisper）",
            "多语言翻译（OPUS-MT）",
            "自动语言检测",
            "转录后翻译",
            "完全离线运行"
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
        }
    }


@app.get("/api/languages", tags=["信息"])
def get_supported_languages():
    """获取支持的语言列表"""
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


# ==================== 音频转录接口 ====================

@app.post("/api/transcribe", tags=["音频处理"], response_model=TranscriptionResponse)
def transcribe_audio(request: TranscriptionRequest):
    """
    音频转录（离线）

    将音频文件转录为文本，支持多语言自动识别。

    ## 支持的格式
    - MP3, WAV, M4A, FLAC, OGG

    ## 参数说明
    - **audio_path**: 音频文件路径（绝对或相对路径）
    - **language**: 语言代码（可选，默认 "auto" 自动检测）
    - **task**: 任务类型（"transcribe" 转录 或 "translate" 翻译成英文）

    ## 返回信息
    - 检测到的语言及置信度
    - 音频时长
    - 处理时间
    - 分段转录结果
    """
    # 检查文件是否存在
    audio_path = Path(request.audio_path)
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail=f"文件不存在: {request.audio_path}")

    # 获取模型
    model = get_whisper_model()

    try:
        start_time = time.time()

        # 执行转录
        segments, info = model.transcribe(
            str(audio_path),
            language=request.language if request.language != "auto" else None,
            task=request.task
        )

        # 收集结果
        transcription_segments = []
        full_text = []
        for segment in segments:
            transcription_segments.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            })
            full_text.append(segment.text.strip())

        processing_time = time.time() - start_time

        return TranscriptionResponse(
            text=" ".join(full_text),
            language=info.language,
            language_probability=info.language_probability,
            duration=info.duration,
            processing_time=processing_time,
            segments=transcription_segments
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"转录失败: {str(e)}")


# ==================== 文本翻译接口 ====================

@app.post("/api/translate", tags=["翻译"], response_model=TranslationResponse)
def translate_text(request: TranslationRequest):
    """
    文本翻译（离线）

    将文本从一种语言翻译成另一种语言。

    ## 支持的语言对
    - 中文 (zh) ↔ 英文 (en)
    - 英文 (en) ↔ 日文 (ja)、韩文 (ko)、法文 (fr)、德文 (de)、西班牙文 (es)
    - 其他语言 → 英文

    ## 参数说明
    - **text**: 要翻译的文本
    - **source_lang**: 源语言代码
    - **target_lang**: 目标语言代码

    ## 注意事项
    - 首次使用某个语言对时会自动下载模型（约 300 MB）
    - 模型会缓存在本地，后续使用无需联网
    """
    # 记录请求详情
    print(f"[DEBUG] 收到翻译请求: source={request.source_lang}, target={request.target_lang}, text={request.text[:50]}...")

    # 验证语言代码
    if not validate_language(request.source_lang):
        print(f"[ERROR] 不支持的源语言: {request.source_lang}")
        raise HTTPException(status_code=400, detail=f"不支持的源语言: {request.source_lang}")

    if not validate_language(request.target_lang):
        print(f"[ERROR] 不支持的目标语言: {request.target_lang}")
        raise HTTPException(status_code=400, detail=f"不支持的目标语言: {request.target_lang}")

    try:
        # 执行翻译
        print(f"[DEBUG] 开始翻译...")
        result = translation_manager.translate(
            request.text,
            request.source_lang,
            request.target_lang
        )
        print(f"[DEBUG] 翻译成功: {result[:50]}...")

        return TranslationResponse(
            original_text=request.text,
            translated_text=result,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )

    except ValueError as e:
        print(f"[ERROR] 翻译值错误: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[ERROR] 翻译失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"翻译失败: {str(e)}")


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
        raise HTTPException(status_code=400, detail="请求列表不能为空")

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
        raise HTTPException(status_code=500, detail=f"批量翻译失败: {str(e)}")


# ==================== 组合功能接口 ====================

@app.post("/api/transcribe-and-translate", tags=["组合功能"])
def transcribe_and_translate(request: TranscribeAndTranslateRequest):
    """
    音频转录 + 翻译（一步完成）

    将音频转录为文本，然后翻译成目标语言。

    ## 使用场景
    - 录音转文字并翻译
    - 会议记录翻译
    - 教学视频字幕翻译

    ## 参数说明
    - **audio_path**: 音频文件路径
    - **source_lang**: 转录语言（可选，默认 "auto"）
    - **target_lang**: 翻译目标语言（默认 "en" 英文）

    ## 返回信息
    - 原始转录文本
    - 翻译后的文本
    - 检测到的语言
    - 处理时间统计
    """
    # 检查文件
    audio_path = Path(request.audio_path)
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail=f"文件不存在: {request.audio_path}")

    # 验证目标语言
    if not validate_language(request.target_lang):
        raise HTTPException(status_code=400, detail=f"不支持的目标语言: {request.target_lang}")

    try:
        start_time = time.time()

        # 步骤 1: 转录
        model = get_whisper_model()
        segments, info = model.transcribe(
            str(audio_path),
            language=request.source_lang if request.source_lang != "auto" else None
        )

        # 收集转录文本
        transcription_text = []
        for segment in segments:
            transcription_text.append(segment.text.strip())

        original_text = " ".join(transcription_text)

        # 步骤 2: 翻译
        translated_text = translation_manager.translate(
            original_text,
            info.language,
            request.target_lang
        )

        total_time = time.time() - start_time

        return {
            "original_text": original_text,
            "translated_text": translated_text,
            "detected_language": info.language,
            "target_language": request.target_lang,
            "language_probability": info.language_probability,
            "audio_duration": info.duration,
            "processing_time": total_time
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


# ==================== 服务器启动 ====================

if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("QuickTrans API 服务器")
    print("=" * 60)
    print()
    print("🚀 正在启动服务器...")
    print()
    print("📍 服务地址:")
    print("   - http://localhost:5000")
    print("   - http://127.0.0.1:5000")
    print()
    print("📖 API 文档:")
    print("   - http://localhost:5000/docs    (Swagger UI)")
    print("   - http://localhost:5000/redoc  (ReDoc)")
    print()
    print("💡 主要功能:")
    print("   - POST /api/transcribe              (音频转录)")
    print("   - POST /api/translate               (文本翻译)")
    print("   - POST /api/translate/batch         (批量翻译)")
    print("   - POST /api/transcribe-and-translate (转录+翻译)")
    print()
    print("⚠️  按 Ctrl+C 停止服务器")
    print()

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=5000,
        log_level="info"
    )
