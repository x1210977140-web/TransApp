# Windows 打包指南

## 🎯 方案概述

由于你当前在 macOS 上，有以下几种方案可以打包 Windows 版本：

---

## 方案 A：使用 GitHub Actions 自动打包（推荐）✨

### 优点：
- ✅ 完全自动化
- ✅ 同时打包 Windows、macOS、Linux 三个版本
- ✅ 无需本地配置
- ✅ 免费使用

### 步骤：

1. **提交代码到 GitHub**
   ```bash
   cd /Users/Xiang/PersonalProjects/TransApp
   git add .
   git commit -m "feat: add Windows build support"
   git push origin main
   ```

2. **GitHub Actions 自动构建**
   - 访问：https://github.com/x1210977140-web/TransApp/actions
   - 查看自动构建进度
   - 构建完成后下载 Windows 版本

3. **获取安装包**
   - 构建完成后，在 Actions 页面下载 Artifacts
   - 文件名：`QuickTrans-windows-latest`
   - 包含：`QuickTrans Setup x.x.x.exe`

---

## 方案 B：在 Windows 机器上手动打包

### 前提条件：
- Windows 10/11 电脑（或虚拟机）
- Python 3.11+
- Node.js 20+

### 步骤：

1. **克隆项目到 Windows**
   ```cmd
   git clone https://github.com/x1210977140-web/TransApp.git
   cd TransApp
   ```

2. **安装 Python 依赖**
   ```cmd
   cd python-engine
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   pip install pyinstaller
   ```

3. **打包 Python 可执行文件**
   ```cmd
   pyinstaller --name=QuickTrans-API --onefile --console api_server.py
   ```

4. **复制到 frontend 目录**
   ```cmd
   mkdir frontend\python-engine
   copy dist\QuickTrans-API.exe frontend\python-engine\
   ```

5. **安装 Node 依赖并打包**
   ```cmd
   cd frontend
   npm install
   npm run build
   npm run build -- --win
   ```

6. **获取安装包**
   - 位置：`frontend/dist/QuickTrans Setup x.x.x.exe`
   - 大小：约 400-500 MB

---

## 方案 C：使用云端打包服务

### 选项 1：Electron Userland
- 网站：https://www.electron.userland.com/

### 选项 2：AppVeyor
- 网站：https://www.appveyor.com/

---

## 🎨 方案对比

| 方案 | 难度 | 时间 | 成本 | 推荐度 |
|------|------|------|------|--------|
| **GitHub Actions** | 低 | 30分钟 | 免费 | ⭐⭐⭐⭐⭐ |
| **Windows 手动打包** | 中 | 1小时 | 免费 | ⭐⭐⭐⭐ |
| **云端打包服务** | 低 | 1小时 | 付费 | ⭐⭐⭐ |

---

## 📝 推荐流程

**我推荐使用 GitHub Actions**，因为：

1. **一次配置，持续使用**
   - 每次推送代码自动构建
   - 同时支持三个平台

2. **完全免费**
   - GitHub Actions 对公开仓库免费

3. **专业级构建**
   - 在真实的 Windows/macOS/Linux 环境中构建
   - 避免跨平台兼容性问题

4. **自动化测试**
   - 可以添加测试步骤
   - 确保打包质量

---

## 🚀 快速开始（GitHub Actions）

1. **确保代码已提交**
   ```bash
   git status
   git add .
   git commit -m "Add cross-platform build support"
   git push origin main
   ```

2. **查看构建进度**
   - 访问：https://github.com/x1210977140-web/TransApp/actions
   - 等待构建完成（约 30-40 分钟）

3. **下载 Windows 版本**
   - 在 Actions 页面找到最新的构建
   - 下载 `QuickTrans-windows-latest` artifact
   - 解压获得 `.exe` 安装程序

---

## 💡 提示

- **Windows 安装包格式**：`.exe` (NSIS installer)
- **安装后大小**：约 500 MB
- **首次运行**：会自动下载 AI 模型（~2.6 GB）
- **系统要求**：Windows 10/11 64位

---

需要我帮你执行 git push 来触发 GitHub Actions 构建吗？
