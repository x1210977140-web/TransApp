# Python 虚拟环境路径记录

**记录时间：** 2026-01-30
**记录目的：** 方便快速定位和删除虚拟环境

---

## 📍 核心路径（最重要）

### 完整绝对路径
```
/Users/Xiang/PersonalProjects/TransApp/python-engine/.venv
```

### 相对路径（从项目根目录）
```
python-engine/.venv
```

### 项目根目录
```
/Users/Xiang/PersonalProjects/TransApp/
```

---

## 🗂️ 虚拟环境内部结构

```
/Users/Xiang/PersonalProjects/TransApp/python-engine/.venv/
├── bin/                                    # 可执行文件
│   ├── python*                             # Python 解释器链接
│   ├── pip*                                # pip 包管理器
│   ├── activate*                           # 虚拟环境激活脚本
│   └── ...                                 # 其他工具
├── include/                                # C 头文件
│   └── python3.11/                         # Python 3.11 头文件
├── lib/                                    # Python 库
│   └── python3.11/
│       └── site-packages/                  # 已安装的包（63个，约 800 MB）
│           ├── torch/                      # 400 MB
│           ├── transformers/               # 96 MB
│           ├── onnxruntime/                # 68 MB
│           ├── av/                         # 53 MB
│           ├── numpy/                      # 36 MB
│           └── ...                         # 其他包
└── pyvenv.cfg                              # 虚拟环境配置文件
```

---

## ⚡ 快速命令（复制即可用）

### 查看虚拟环境路径
```bash
echo /Users/Xiang/PersonalProjects/TransApp/python-engine/.venv
```

### 检查虚拟环境是否存在
```bash
ls -la /Users/Xiang/PersonalProjects/TransApp/python-engine/.venv
```

### 查看虚拟环境大小
```bash
du -sh /Users/Xiang/PersonalProjects/TransApp/python-engine/.venv
# 预期输出：847M
```

### 完全删除虚拟环境（释放 847 MB）
```bash
rm -rf /Users/Xiang/PersonalProjects/TransApp/python-engine/.venv
```

### 进入虚拟环境目录
```bash
cd /Users/Xiang/PersonalProjects/TransApp/python-engine/.venv
```

### 激活虚拟环境
```bash
source /Users/Xiang/PersonalProjects/TransApp/python-engine/.venv/bin/activate
```

---

## 📋 路径记录在其他文档中的位置

### 1. CLEANUP_GUIDE.md
**位置：** 多处提及
- 第 10 行：快速清理命令
- 第 38 行：安装文件详细清单
- 第 60 行：核心 Python 包路径表格

### 2. INSTALLATION_SUMMARY.md
**位置：** 第 16 行
```
虚拟环境路径：/Users/Xiang/PersonalProjects/TransApp/python-engine/.venv
```

### 3. 本文件（VENV_PATH.md）
**专门记录路径信息的文档**

---

## 🔍 验证路径正确性

### 方法 1：使用 ls 命令
```bash
ls -la /Users/Xiang/PersonalProjects/TransApp/python-engine/.venv/bin/python
```
**预期输出：** 应该显示 python 可执行文件

### 方法 2：使用 realpath
```bash
realpath /Users/Xiang/PersonalProjects/TransApp/python-engine/.venv
```
**预期输出：** `/Users/Xiang/PersonalProjects/TransApp/python-engine/.venv`

### 方法 3：激活并检查
```bash
source /Users/Xiang/PersonalProjects/TransApp/python-engine/.venv/bin/activate
which python
```
**预期输出：** `/Users/Xiang/PersonalProjects/TransApp/python-engine/.venv/bin/python`

---

## 📊 空间占用详情

### 虚拟环境总体
```
/Users/Xiang/PersonalProjects/TransApp/python-engine/.venv
总大小：847 MB
```

### 最大占用子目录
```
.venv/lib/python3.11/site-packages/torch
大小：400 MB（47%）

.venv/lib/python3.11/site-packages/transformers
大小：96 MB（11%）
```

---

## 🛡️ 删除前确认清单

在删除虚拟环境前，请确认：

- [ ] 我不再需要这个 Python 环境
- [ ] 我已经备份了重要的代码
- [ ] 我知道如何重新安装（查看 CLEANUP_GUIDE.md）
- [ ] 我知道路径是：`/Users/Xiang/PersonalProjects/TransApp/python-engine/.venv`

---

## 📝 如果路径改变

如果你的项目移动到了其他位置，虚拟环境的路径也会改变：

### 示例：移动到 ~/Projects/
```bash
# 原路径
/Users/Xiang/PersonalProjects/TransApp/python-engine/.venv

# 新路径（如果移动项目）
~/Projects/TransApp/python-engine/.venv
```

**注意：** 移动项目后，虚拟环境可能需要重新创建，因为有些路径是硬编码的。

---

## 🎯 一键操作参考

### 查看路径
```bash
echo /Users/Xiang/PersonalProjects/TransApp/python-engine/.venv
```

### 复制路径到剪贴板（macOS）
```bash
echo /Users/Xiang/PersonalProjects/TransApp/python-engine/.venv | pbcopy
```

### 在 Finder 中打开
```bash
open /Users/Xiang/PersonalProjects/TransApp/python-engine/.venv
```

### 在终端中快速跳转
```bash
cd /Users/Xiang/PersonalProjects/TransApp/python-engine/.venv
```

---

## ✅ 总结

**虚拟环境的完整路径（重要）：**

```
/Users/Xiang/PersonalProjects/TransApp/python-engine/.venv
```

**大小：** 847 MB

**删除命令：**
```bash
rm -rf /Users/Xiang/PersonalProjects/TransApp/python-engine/.venv
```

---

**文档版本：** v1.0
**创建时间：** 2026-01-30
**路径验证：** ✅ 已确认正确
