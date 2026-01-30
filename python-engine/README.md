# QuickTrans Python 引擎

**目录：** `python-engine/`
**Python 版本：** 3.11.6
**虚拟环境：** `.venv/`

---

## 📚 快速开始

### 1. 激活虚拟环境

```bash
cd /Users/Xiang/PersonalProjects/TransApp/python-engine
source .venv/bin/activate
```

### 2. 测试模型加载

```bash
python test_model_loading.py
```

**预期结果：**
- 首次运行会下载 Whisper medium 模型（~1.5 GB）
- 下载完成后显示"✅ 模型加载成功！"

### 3. 测试 FastAPI 接口

```bash
python test_api.py
```

然后在浏览器访问：
- http://localhost:5000 (健康检查)
- http://localhost:5000/docs (API 文档)

---

## 🧪 测试脚本说明

### test_model_loading.py
**用途：** 测试 Whisper 模型是否能正常加载

**功能：**
- 加载 Whisper medium 模型
- 验证 faster-whisper 和 PyTorch 工作正常
- 显示模型信息

**运行时间：**
- 首次：5-10 分钟（下载模型）
- 后续：5-10 秒

### test_api.py
**用途：** 测试 FastAPI Web 服务器

**功能：**
- 启动 FastAPI 开发服务器
- 提供基础 API 端点
- 自动生成 API 文档（Swagger UI）

**端点：**
- `GET /` - 健康检查
- `GET /health` - 详细信息
- `POST /api/transcribe` - 音频转录（待实现）

---

## 📦 已安装的包

### 核心依赖（requirements.txt）
- `faster-whisper` - Whisper 推理引擎
- `torch` - PyTorch 深度学习框架
- `transformers` - Hugging Face 模型库
- `fastapi` - Web 框架
- `uvicorn` - ASGI 服务器
- `pydantic` - 数据验证
- `numpy` - 数值计算
- `opencc` - 繁简转换
- `soundfile` - 音频处理

### 开发依赖（可选）
```bash
pip install -r requirements-dev.txt
```

---

## 🎯 开发步骤

### Step 1: 测试模型加载
```bash
python test_model_loading.py
```

### Step 2: 创建音频转录测试
准备一个音频文件（.mp3, .wav, .m4a），然后：
```bash
python test_transcription.py path/to/audio.mp3
```

### Step 3: 开发完整 API 接口
编辑 `main.py`，实现完整的音频转录功能

---

## 📂 文件结构

```
python-engine/
├── .venv/                          # 虚拟环境（847 MB）
├── test_model_loading.py           # 模型加载测试 ⭐
├── test_api.py                     # FastAPI 测试 ⭐
├── requirements.txt                # 核心依赖
├── requirements-dev.txt            # 开发依赖
├── installed_packages.txt          # 已安装包列表
├── main.py                         # 主应用（待创建）
└── README.md                       # 本文件
```

---

## ⚙️ 配置说明

### 模型配置

**可用模型：**
- `tiny` - 最快，准确度最低（~40 MB）
- `base` - 快速，基础准确度（~140 MB）
- `small` - 平衡（~460 MB）
- `medium` - 推荐，高准确度（~1.5 GB）⭐
- `large` - 最准确，最慢（~2.9 GB）

**修改模型大小：**
编辑 `test_model_loading.py`，修改：
```python
model_size = "medium"  # 改为 "small" 或 "large"
```

### 设备配置

**Apple Silicon 优化：**
```python
model = WhisperModel(
    model_size,
    device="cpu",        # 使用 CPU
    compute_type="float32"  # 或 "int8" 节省内存
)
```

**如果有 NVIDIA GPU：**
```python
model = WhisperModel(
    model_size,
    device="cuda",       # 使用 GPU
    compute_type="float16"  # GPU 推荐使用 float16
)
```

---

## 🔄 重新安装

如果需要重新创建虚拟环境：

```bash
# 1. 删除旧环境
rm -rf .venv

# 2. 创建新环境
python3.11 -m venv .venv

# 3. 激活并安装
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🧹 清理

### 删除虚拟环境（释放 847 MB）
```bash
rm -rf /Users/Xiang/PersonalProjects/TransApp/python-engine/.venv
```

### 删除 Whisper 模型缓存（释放 ~1.5 GB）
```bash
rm -rf ~/Library/Application\ Support/faster-whisper/
```

详细清理指南请查看：`../CLEANUP_GUIDE.md`

---

## 📖 下一步

1. ✅ 运行 `test_model_loading.py` 测试模型
2. ✅ 运行 `test_api.py` 测试 API 服务器
3. ⏳ 创建完整的 `main.py` 应用
4. ⏳ 实现音频转录功能
5. ⏳ 集成到 Electron 前端

---

**文档版本：** v1.0
**创建时间：** 2026-01-30
