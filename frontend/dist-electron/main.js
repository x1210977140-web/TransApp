import { app, BrowserWindow } from "electron";
import path from "path";
import { fileURLToPath } from "url";
import fs from "fs";
import { spawn } from "child_process";
const __filename$2 = fileURLToPath(import.meta.url);
const __dirname$2 = path.dirname(__filename$2);
class PythonBridge {
  constructor() {
    this.pythonProcess = null;
    this.isReady = false;
    this.port = 5e3;
    if (process.env.NODE_ENV === "development") {
      this.pythonPath = path.join(__dirname$2, "../../python-engine/.venv/bin/python");
      this.apiScript = path.join(__dirname$2, "../../python-engine/api_server.py");
    } else {
      const resourcesPath = process.resourcesPath;
      const exeName = process.platform === "win32" ? "QuickTrans-API.exe" : "QuickTrans-API";
      this.pythonPath = path.join(resourcesPath, "python-engine", exeName);
      this.apiScript = "";
    }
  }
  /**
   * 启动 Python API 服务器
   */
  start() {
    return new Promise((resolve, reject) => {
      if (this.pythonProcess) {
        console.log("Python API 服务器已在运行");
        resolve();
        return;
      }
      if (!fs.existsSync(this.pythonPath)) {
        const error = new Error(`Python 可执行文件不存在: ${this.pythonPath}`);
        console.error("❌", error.message);
        reject(error);
        return;
      }
      if (process.env.NODE_ENV === "development" && !fs.existsSync(this.apiScript)) {
        const error = new Error(`API 脚本不存在: ${this.apiScript}`);
        console.error("❌", error.message);
        reject(error);
        return;
      }
      console.log("🚀 正在启动 Python API 服务器...");
      console.log(`📍 平台: ${process.platform}`);
      console.log(`📍 环境: ${process.env.NODE_ENV || "production"}`);
      console.log(`📍 Python 可执行文件: ${this.pythonPath}`);
      if (this.apiScript) {
        console.log(`📍 API 脚本: ${this.apiScript}`);
      }
      const args = this.apiScript ? [this.apiScript] : [];
      try {
        this.pythonProcess = spawn(this.pythonPath, args, {
          env: {
            ...process.env,
            PYTHONUNBUFFERED: "1",
            // 确保 Python 输出不缓冲
            NODE_ENV: process.env.NODE_ENV || "production"
          }
        });
      } catch (error) {
        console.error("❌ 启动 Python 进程失败:", error);
        reject(error);
        return;
      }
      this.pythonProcess.stdout.on("data", (data) => {
        const message = data.toString().trim();
        console.log(`[Python stdout] ${message}`);
        if (message.includes("Uvicorn running on") || message.includes("Application startup complete")) {
          this.isReady = true;
          console.log("✅ Python API 服务器启动成功");
          resolve();
        }
      });
      this.pythonProcess.stderr.on("data", (data) => {
        const message = data.toString().trim();
        if (!message.includes("INFO:") || process.env.NODE_ENV === "development") {
          console.log(`[Python stderr] ${message}`);
        }
      });
      this.pythonProcess.on("close", (code) => {
        const exitMsg = `Python 进程退出，退出码: ${code}`;
        console.log(`⚠️  ${exitMsg}`);
        this.pythonProcess = null;
        this.isReady = false;
      });
      this.pythonProcess.on("error", (error) => {
        console.error("❌ Python 进程错误:", error);
        this.pythonProcess = null;
        this.isReady = false;
        reject(error);
      });
      const waitTime = process.platform === "win32" ? 45e3 : 15e3;
      console.log(`⏳ 等待 Python API 服务器启动（最长 ${waitTime / 1e3} 秒）...`);
      setTimeout(async () => {
        if (!this.isReady) {
          console.log("⏳ Python API 服务器正在初始化，尝试健康检查...");
          try {
            const isHealthy = await this.healthCheck();
            if (isHealthy) {
              this.isReady = true;
              console.log("✅ Python API 服务器健康检查通过");
              resolve();
            } else {
              console.warn("⚠️  Python API 服务器未就绪，但继续启动应用");
              this.isReady = true;
              resolve();
            }
          } catch (error) {
            console.warn("⚠️  健康检查失败，但继续启动应用:", error.message);
            this.isReady = true;
            resolve();
          }
        }
      }, waitTime);
    });
  }
  /**
   * 停止 Python API 服务器
   */
  stop() {
    if (this.pythonProcess) {
      console.log("正在停止 Python API 服务器...");
      const signal = process.platform === "win32" ? "SIGKILL" : "SIGTERM";
      this.pythonProcess.kill(signal);
      this.pythonProcess = null;
      this.isReady = false;
    }
  }
  /**
   * 检查服务器是否就绪
   */
  ready() {
    return this.isReady;
  }
  /**
   * 获取 API 服务器地址
   */
  getApiUrl() {
    return `http://127.0.0.1:${this.port}`;
  }
  /**
   * 健康检查 - 验证 API 是否真正可用
   */
  async healthCheck() {
    try {
      const response = await fetch(`${this.getApiUrl()}/`);
      const data = await response.json();
      return data.status === "ok";
    } catch (error) {
      console.error("健康检查失败:", error.message);
      return false;
    }
  }
}
const __filename$1 = fileURLToPath(import.meta.url);
const __dirname$1 = path.dirname(__filename$1);
let mainWindow = null;
let pythonBridge = null;
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: false,
      // 允许加载本地资源
      preload: path.join(__dirname$1, "preload.js")
    },
    titleBarStyle: "default",
    show: false
  });
  if (process.env.NODE_ENV === "development") {
    mainWindow.loadURL("http://localhost:5173");
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname$1, "../dist/index.html"));
  }
  mainWindow.once("ready-to-show", () => {
    mainWindow.show();
  });
  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}
app.whenReady().then(async () => {
  pythonBridge = new PythonBridge();
  try {
    console.log("正在启动 Python API 服务器...");
    await pythonBridge.start();
    console.log("✅ Python API 服务器已就绪");
  } catch (error) {
    console.error("❌ Python API 服务器启动失败:", error);
  }
  createWindow();
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});
app.on("window-all-closed", () => {
  if (pythonBridge) {
    pythonBridge.stop();
  }
  if (process.platform !== "darwin") {
    app.quit();
  }
});
app.on("before-quit", () => {
  if (pythonBridge) {
    pythonBridge.stop();
  }
});
if (process.env.NODE_ENV === "development") {
  const viteServerPath = path.join(__dirname$1, "../node_modules/.bin/vite");
  if (fs.existsSync(viteServerPath)) {
    console.log("Vite 开发服务器将在渲染进程中启动");
  }
}
