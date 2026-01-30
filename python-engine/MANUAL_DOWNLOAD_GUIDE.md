# Whisper 模型手动下载指南

如果自动下载失败，可以使用手动下载方式。

---

## 📥 手动下载步骤

### 方法 1：使用 HF-Mirror 下载（推荐国内用户）

#### Step 1: 安装 huggingface-hub
```bash
cd /Users/Xiang/PersonalProjects/TransApp/python-engine
source .venv/bin/activate
pip install huggingface-hub
```

#### Step 2: 配置镜像
```bash
export HF_ENDPOINT=https://hf-mirror.com
```

#### Step 3: 下载模型
```bash
# 下载 medium 模型（~1.5 GB）
huggingface-cli download guillaumekln/faster-whisper-medium \
  --local-dir ~/Library/Application\ Support/faster-whisper/faster-whisper-medium

# 或下载 small 模型（~460 MB）
huggingface-cli download guillaumekln/faster-whisper-small \
  --local-dir ~/Library/Application\ Support/faster-whisper/faster-whisper-small
```

---

### 方法 2：浏览器下载

#### Step 1: 访问 HF-Mirror
```
https://hf-mirror.com/guillaumekln/faster-whisper-medium
```

#### Step 2: 下载文件
下载以下文件到 `~/Library/Application Support/faster-whisper/faster-whisper-medium/`:

1. `model.bin` (或 `pytorch_model.bin`)
2. `config.json`
3. `tokenizer.json`
4. `vocab.json`
5. `vocabulary.txt`
6. `tokenizer_config.json`
7. `special_tokens_map.json`
8. `generation_config.json`

#### Step 3: 移动文件到正确位置
```bash
# 创建目录
mkdir -p ~/Library/Application\ Support/faster-whisper/faster-whisper-medium

# 移动下载的文件到该目录
# （假设你下载到了 ~/Downloads/）
mv ~/Downloads/model.bin ~/Library/Application\ Support/faster-whisper/faster-whisper-medium/
mv ~/Downloads/*.json ~/Library/Application\ Support/faster-whisper/faster-whisper-medium/
mv ~/Downloads/*.txt ~/Library/Application\ Support/faster-whisper/faster-whisper-medium/
```

---

### 方法 3：使用 Git LFS

```bash
# 安装 git-lfs
brew install git-lfs

# 配置镜像
export HF_ENDPOINT=https://hf-mirror.com

# 克隆模型仓库
cd ~/Library/Application\ Support/faster-whisper/
git clone https://hf-mirror.com/guillaumekln/faster-whisper-medium
```

---

## ✅ 验证下载

### 检查文件完整性
```bash
# 查看下载的文件
ls -lh ~/Library/Application\ Support/faster-whisper/faster-whisper-medium/

# 查看总大小
du -sh ~/Library/Application\ Support/faster-whisper/faster-whisper-medium/
```

### 预期大小
- **small 模型**: ~460 MB
- **medium 模型**: ~1.5 GB

---

## 🧪 测试模型

下载完成后，运行测试：

```bash
cd /Users/Xiang/PersonalProjects/TransApp/python-engine
source .venv/bin/activate
export HF_ENDPOINT=https://hf-mirror.com

python test_model_loading.py
```

---

## 🔧 常见问题

### Q1: 下载速度慢？
**A:** 使用 HF-Mirror 镜像（国内）
```bash
export HF_ENDPOINT=https://hf-mirror.com
```

### Q2: 下载中断？
**A:** 重新下载，会自动断点续传

### Q3: 文件损坏？
**A:** 删除重新下载
```bash
rm -rf ~/Library/Application\ Support/faster-whisper/faster-whisper-medium
```

---

## 📊 模型选择建议

| 模型 | 大小 | 准确度 | 速度 | 适用场景 |
|------|------|--------|------|----------|
| **tiny** | ~40 MB | 低 | 最快 | 快速测试 |
| **base** | ~140 MB | 中等 | 快 | 日常使用 |
| **small** | ~460 MB | 高 | 较快 | 推荐 ⭐ |
| **medium** | ~1.5 GB | 很高 | 中等 | 高质量需求 |
| **large** | ~2.9 GB | 最高 | 慢 | 专业用途 |

---

**推荐：** 先下载 **small** 模型测试，工作正常后再考虑 medium
