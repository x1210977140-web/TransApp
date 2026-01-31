import { app as r, BrowserWindow as P } from "electron";
import e from "path";
import { fileURLToPath as d } from "url";
import p from "fs";
import { spawn as f } from "child_process";
const u = d(import.meta.url), c = e.dirname(u);
class g {
  constructor() {
    if (this.pythonProcess = null, this.isReady = !1, this.port = 5e3, process.env.NODE_ENV === "development")
      this.pythonPath = e.join(c, "../../python-engine/.venv/bin/python"), this.apiScript = e.join(c, "../../python-engine/api_server.py");
    else {
      const s = process.resourcesPath;
      this.pythonPath = e.join(s, "python-engine/QuickTrans-API"), this.apiScript = "";
    }
  }
  /**
   * 启动 Python API 服务器
   */
  start() {
    return new Promise((s, l) => {
      if (this.pythonProcess) {
        console.log("Python API 服务器已在运行"), s();
        return;
      }
      if (!p.existsSync(this.pythonPath)) {
        l(new Error(`Python 可执行文件不存在: ${this.pythonPath}`));
        return;
      }
      if (process.env.NODE_ENV === "development" && !p.existsSync(this.apiScript)) {
        l(new Error(`API 脚本不存在: ${this.apiScript}`));
        return;
      }
      console.log("正在启动 Python API 服务器..."), console.log(`环境: ${process.env.NODE_ENV || "production"}`), console.log(`Python 可执行文件: ${this.pythonPath}`), this.apiScript && console.log(`API 脚本: ${this.apiScript}`);
      const m = this.apiScript ? [this.apiScript] : [];
      this.pythonProcess = f(this.pythonPath, m, {
        env: {
          ...process.env,
          PYTHONUNBUFFERED: "1"
          // 确保 Python 输出不缓冲
        }
      }), this.pythonProcess.stdout.on("data", (o) => {
        const i = o.toString().trim();
        console.log(`[Python] ${i}`), (i.includes("Uvicorn running on") || i.includes("Application startup complete")) && (this.isReady = !0, console.log("✅ Python API 服务器启动成功"), s());
      }), this.pythonProcess.stderr.on("data", (o) => {
        const i = o.toString().trim();
        console.error(`[Python Error] ${i}`);
      }), this.pythonProcess.on("close", (o) => {
        console.log(`Python 进程退出，代码: ${o}`), this.pythonProcess = null, this.isReady = !1;
      }), this.pythonProcess.on("error", (o) => {
        console.error("Python 进程错误:", o), this.pythonProcess = null, this.isReady = !1, l(o);
      }), setTimeout(() => {
        this.isReady || (console.log("⏳ Python API 服务器正在初始化..."), s());
      }, 3e3);
    });
  }
  /**
   * 停止 Python API 服务器
   */
  stop() {
    this.pythonProcess && (console.log("正在停止 Python API 服务器..."), this.pythonProcess.kill("SIGTERM"), this.pythonProcess = null, this.isReady = !1);
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
}
const w = d(import.meta.url), a = e.dirname(w);
let t = null, n = null;
function y() {
  t = new P({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: !1,
      contextIsolation: !0,
      preload: e.join(a, "preload.js")
    },
    titleBarStyle: "default",
    show: !1
  }), process.env.NODE_ENV === "development" ? (t.loadURL("http://localhost:5173"), t.webContents.openDevTools()) : t.loadFile(e.join(a, "../dist/index.html")), t.once("ready-to-show", () => {
    t.show();
  }), t.on("closed", () => {
    t = null;
  });
}
r.whenReady().then(async () => {
  n = new g();
  try {
    console.log("正在启动 Python API 服务器..."), await n.start(), console.log("✅ Python API 服务器已就绪");
  } catch (h) {
    console.error("❌ Python API 服务器启动失败:", h);
  }
  y(), r.on("activate", () => {
    P.getAllWindows().length === 0 && y();
  });
});
r.on("window-all-closed", () => {
  n && n.stop(), process.platform !== "darwin" && r.quit();
});
r.on("before-quit", () => {
  n && n.stop();
});
if (process.env.NODE_ENV === "development") {
  const h = e.join(a, "../node_modules/.bin/vite");
  p.existsSync(h) && console.log("Vite 开发服务器将在渲染进程中启动");
}
