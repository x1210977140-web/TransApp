# QuickTrans 快速启动指南

## 最简单的启动方式

在项目根目录运行启动脚本：
```bash
./start.sh
```

应用会自动打开：http://localhost:5173

---

## 手动启动（开发模式）

### 步骤 1：启动 Python API 服务器
```bash
cd python-engine
source .venv/bin/activate
python api_server.py
```

保持这个终端窗口运行，你会看到：
```
QuickTrans API 服务器
🚀 正在启动服务器...
📍 服务地址: http://127.0.0.1:5000
```

### 步骤 2：启动前端应用（新开一个终端）
```bash
cd frontend
npm run dev
```

前端会启动在：http://localhost:5173

---

## 如何使用

1. **文本翻译**
   - 选择源语言和目标语言
   - 输入要翻译的文本
   - 点击"开始翻译"

2. **音频转录**
   - 输入音频文件的完整路径
   - 点击"开始转录"
   - 支持格式：MP3, WAV, M4A, FLAC, OGG

3. **转录并翻译**
   - 输入音频文件路径
   - 选择目标语言
   - 点击"转录并翻译"

---

## 停止服务

在运行的终端窗口按 `Ctrl + C` 停止服务。

---

## 系统要求

- Python 3.10+
- Node.js 18+
- 首次运行需要下载 AI 模型（约 800 MB）

---

## 常见问题

**Q: 如何知道自己系统上的 Python 和 Node.js 版本？**
```bash
python3 --version
node --version
```

**Q: 首次运行很慢？**
A: 首次使用需要下载 AI 模型，请耐心等待。下载完成后会缓存到本地，后续使用完全离线。

**Q: 支持批量处理吗？**
A: 目前支持单个文件处理，批量功能开发中。

---

## 版本

v2.0.0 - Apple 风格 UI 设计
