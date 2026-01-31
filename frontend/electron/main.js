import { app, BrowserWindow } from 'electron'
import path from 'path'
import { fileURLToPath } from 'url'
import fs from 'fs'
import PythonBridge from './python-bridge.js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

let mainWindow = null
let pythonBridge = null

// 创建主窗口
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: false, // 允许加载本地资源
      preload: path.join(__dirname, 'preload.js')
    },
    titleBarStyle: 'default',
    show: false
  })

  // 开发模式加载 Vite 服务器，生产模式加载打包后的文件
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173')
    mainWindow.webContents.openDevTools()
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'))
  }

  mainWindow.once('ready-to-show', () => {
    mainWindow.show()
  })

  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

// 应用就绪时创建窗口并启动 Python
app.whenReady().then(async () => {
  // 创建 Python 桥接器
  pythonBridge = new PythonBridge()

  try {
    // 启动 Python API 服务器
    console.log('正在启动 Python API 服务器...')
    await pythonBridge.start()
    console.log('✅ Python API 服务器已就绪')
  } catch (error) {
    console.error('❌ Python API 服务器启动失败:', error)
    // 即使 Python 启动失败也继续启动应用
  }

  // 创建窗口
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

// 所有窗口关闭时退出应用（macOS 除外）
app.on('window-all-closed', () => {
  // 停止 Python 进程
  if (pythonBridge) {
    pythonBridge.stop()
  }

  if (process.platform !== 'darwin') {
    app.quit()
  }
})

// 应用退出前清理
app.on('before-quit', () => {
  if (pythonBridge) {
    pythonBridge.stop()
  }
})

// 开发模式下，监听 Vite 服务器的变化
if (process.env.NODE_ENV === 'development') {
  const viteServerPath = path.join(__dirname, '../node_modules/.bin/vite')

  if (fs.existsSync(viteServerPath)) {
    console.log('Vite 开发服务器将在渲染进程中启动')
  }
}

