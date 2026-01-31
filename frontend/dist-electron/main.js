import { app as o, BrowserWindow as l } from "electron";
import t from "path";
import { fileURLToPath as r } from "url";
import a from "fs";
const d = r(import.meta.url), n = t.dirname(d);
let e = null;
function i() {
  e = new l({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: !1,
      contextIsolation: !0,
      preload: t.join(n, "preload.js")
    },
    titleBarStyle: "default",
    show: !1
  }), process.env.NODE_ENV === "development" ? (e.loadURL("http://localhost:5173"), e.webContents.openDevTools()) : e.loadFile(t.join(n, "../dist/index.html")), e.once("ready-to-show", () => {
    e.show();
  }), e.on("closed", () => {
    e = null;
  });
}
o.whenReady().then(() => {
  i(), o.on("activate", () => {
    l.getAllWindows().length === 0 && i();
  });
});
o.on("window-all-closed", () => {
  process.platform !== "darwin" && o.quit();
});
if (process.env.NODE_ENV === "development") {
  const s = t.join(n, "../node_modules/.bin/vite");
  a.existsSync(s) && console.log("Vite 开发服务器将在渲染进程中启动");
}
