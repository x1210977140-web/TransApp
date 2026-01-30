# QuickTrans API 使用指南

**版本：** 2.0.0
**状态：** ✅ 完成并测试通过

---

## 🚀 快速启动

### 方法 1：使用启动脚本（推荐）

```bash
cd /Users/Xiang/PersonalProjects/TransApp/python-engine
./start_api.sh
```

### 方法 2：手动启动

```bash
cd /Users/Xiang/PersonalProjects/TransApp/python-engine
source .venv/bin/activate
python api_server.py
```

服务器启动后访问：
- **API 文档：** http://127.0.0.1:5000/docs
- **ReDoc 文档：** http://127.0.0.1:5000/redoc

---

## 📡 API 接口

### 1. 系统状态

**接口：** `GET /`

**响应：**
```json
{
  "status": "ok",
  "version": "2.0.0",
  "features": ["语音识别", "多语言翻译", "自动语言检测"]
}
```

---

### 2. 健康检查

**接口：** `GET /health`

**响应：**
```json
{
  "status": "healthy",
  "system": {
    "python_version": "3.11.6",
    "platform": "darwin"
  },
  "features": {
    "transcription": "已安装",
    "translation": "已安装"
  }
}
```

---

### 3. 获取支持的语言

**接口：** `GET /api/languages`

**响应：**
```json
{
  "languages": [
    {
      "code": "zh",
      "name": "中文",
      "can_translate_to": ["en"]
    },
    {
      "code": "en",
      "name": "英文",
      "can_translate_to": ["zh", "ja", "ko", "fr", "de", "es"]
    }
  ]
}
```

---

### 4. 文本翻译 ⭐

**接口：** `POST /api/translate`

**请求：**
```json
{
  "text": "你好，世界！",
  "source_lang": "zh",
  "target_lang": "en"
}
```

**响应：**
```json
{
  "original_text": "你好，世界！",
  "translated_text": "Hello, world!",
  "source_lang": "zh",
  "target_lang": "en"
}
```

**支持的语言对：**
- 中文 (zh) ↔ 英文 (en)
- 英文 (en) → 日文、韩文、法文、德文、西班牙文
- 其他语言 → 英文

---

### 5. 批量翻译

**接口：** `POST /api/translate/batch`

**请求：**
```json
[
  {"text": "你好", "source_lang": "zh", "target_lang": "en"},
  {"text": "世界", "source_lang": "zh", "target_lang": "en"}
]
```

**响应：**
```json
{
  "total": 2,
  "results": [
    {"original": "你好", "translated": "Hello"},
    {"original": "世界", "translated": "World"}
  ]
}
```

---

### 6. 音频转录

**接口：** `POST /api/transcribe`

**请求：**
```json
{
  "audio_path": "/path/to/audio.mp3",
  "language": "auto",
  "task": "transcribe"
}
```

**响应：**
```json
{
  "text": "完整的转录文本",
  "language": "zh",
  "language_probability": 0.98,
  "duration": 10.5,
  "processing_time": 2.3,
  "segments": [
    {
      "start": 0.0,
      "end": 2.5,
      "text": "第一段文本"
    }
  ]
}
```

**支持格式：** MP3, WAV, M4A, FLAC, OGG

---

### 7. 音频转录 + 翻译（一步完成）⭐

**接口：** `POST /api/transcribe-and-translate`

**请求：**
```json
{
  "audio_path": "/path/to/audio.mp3",
  "source_lang": "auto",
  "target_lang": "en"
}
```

**响应：**
```json
{
  "original_text": "原始转录文本",
  "translated_text": "翻译后的文本",
  "detected_language": "zh",
  "target_language": "en",
  "language_probability": 0.98,
  "audio_duration": 10.5,
  "processing_time": 5.2
}
```

**使用场景：**
- 录音转文字并翻译
- 会议记录翻译
- 教学视频字幕翻译

---

## 🧪 测试 API

### 使用测试脚本

```bash
# 启动服务器
./start_api.sh

# 在另一个终端运行测试
python test_api_complete.py
```

### 使用 curl 测试

**测试翻译：**
```bash
curl -X POST "http://127.0.0.1:5000/api/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "你好，世界！",
    "source_lang": "zh",
    "target_lang": "en"
  }'
```

**测试音频转录：**
```bash
curl -X POST "http://127.0.0.1:5000/api/transcribe" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_path": "test_audio.mp3",
    "language": "auto"
  }'
```

### 使用 Swagger UI 测试

1. 访问 http://127.0.0.1:5000/docs
2. 选择要测试的接口
3. 点击 "Try it out"
4. 填写参数
5. 点击 "Execute"

---

## 📊 技术特性

### 完全离线
- ✅ 无需联网
- ✅ 模型本地运行
- ✅ 数据隐私保护

### 高性能
- ✅ Whisper small 模型（473 MB）
- ✅ OPUS-MT 翻译模型（~300 MB/语言对）
- ✅ Apple Silicon 优化

### 易用性
- ✅ RESTful API 设计
- ✅ 自动语言检测
- ✅ 支持批量处理

---

## 📝 注意事项

1. **首次使用**
   - 会自动下载模型文件
   - Whisper small: ~473 MB
   - 翻译模型: ~300 MB/语言对
   - 下载后永久缓存

2. **文件路径**
   - 支持绝对路径和相对路径
   - 相对路径相对于当前工作目录

3. **性能提示**
   - 音频转录：~1-2 秒/分钟音频
   - 文本翻译：<1 秒/句子
   - 首次运行需要加载模型（~5 秒）

---

## 🔧 故障排除

### 服务器无法启动

**问题：** 端口被占用
```bash
# 查看占用端口的进程
lsof -i :5000

# 杀死进程
kill -9 <PID>
```

### 模型下载失败

**问题：** 无法连接 Hugging Face
```bash
# 使用国内镜像
export HF_ENDPOINT=https://hf-mirror.com
python api_server.py
```

### 翻译结果不理想

**问题：** 翻译质量差
- 尝试分段翻译长文本
- 确认语言代码正确
- 查看支持的语言对

---

## 📚 相关文档

- [TRANSLATION_FEATURE_SUMMARY.md](../TRANSLATION_FEATURE_SUMMARY.md) - 翻译功能说明
- [FEATURES.md](../FEATURES.md) - 完整功能列表
- [DEVELOPMENT_SETUP.md](../DEVELOPMENT_SETUP.md) - 开发环境设置

---

**更新时间：** 2026-01-30
**版本：** 2.0.0
**状态：** ✅ 完成并可用
