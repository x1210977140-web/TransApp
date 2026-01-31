import { spawn } from 'child_process'
import path from 'path'
import { fileURLToPath } from 'url'
import fs from 'fs'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

class PythonBridge {
  constructor() {
    this.pythonProcess = null
    this.isReady = false
    this.port = 5000

    // 确定路径
    if (process.env.NODE_ENV === 'development') {
      // 开发环境：使用项目中的虚拟环境
      this.pythonPath = path.join(__dirname, '../../python-engine/.venv/bin/python')
      this.apiScript = path.join(__dirname, '../../python-engine/api_server.py')
    } else {
      // 生产环境：使用打包后的 Python 可执行文件
      const resourcesPath = process.resourcesPath
      this.pythonPath = path.join(resourcesPath, 'python-engine/QuickTrans-API')
      this.apiScript = ''  // 可执行文件不需要脚本路径
    }
  }

  /**
   * 启动 Python API 服务器
   */
  start() {
    return new Promise((resolve, reject) => {
      if (this.pythonProcess) {
        console.log('Python API 服务器已在运行')
        resolve()
        return
      }

      // 检查 Python 可执行文件是否存在
      if (!fs.existsSync(this.pythonPath)) {
        reject(new Error(`Python 可执行文件不存在: ${this.pythonPath}`))
        return
      }

      // 开发环境需要检查脚本文件
      if (process.env.NODE_ENV === 'development' && !fs.existsSync(this.apiScript)) {
        reject(new Error(`API 脚本不存在: ${this.apiScript}`))
        return
      }

      console.log('正在启动 Python API 服务器...')
      console.log(`环境: ${process.env.NODE_ENV || 'production'}`)
      console.log(`Python 可执行文件: ${this.pythonPath}`)
      if (this.apiScript) {
        console.log(`API 脚本: ${this.apiScript}`)
      }

      // 准备启动参数
      const args = this.apiScript ? [this.apiScript] : []

      // 启动 Python 进程
      this.pythonProcess = spawn(this.pythonPath, args, {
        env: {
          ...process.env,
          PYTHONUNBUFFERED: '1' // 确保 Python 输出不缓冲
        }
      })

      // 监听标准输出
      this.pythonProcess.stdout.on('data', (data) => {
        const message = data.toString().trim()
        console.log(`[Python] ${message}`)

        // 检测服务器是否启动成功
        if (message.includes('Uvicorn running on') || message.includes('Application startup complete')) {
          this.isReady = true
          console.log('✅ Python API 服务器启动成功')
          resolve()
        }
      })

      // 监听错误输出
      this.pythonProcess.stderr.on('data', (data) => {
        const message = data.toString().trim()
        console.error(`[Python Error] ${message}`)
      })

      // 监听进程退出
      this.pythonProcess.on('close', (code) => {
        console.log(`Python 进程退出，代码: ${code}`)
        this.pythonProcess = null
        this.isReady = false
      })

      // 监听进程错误
      this.pythonProcess.on('error', (error) => {
        console.error('Python 进程错误:', error)
        this.pythonProcess = null
        this.isReady = false
        reject(error)
      })

      // 等待服务器启动（最多 30 秒）
      setTimeout(() => {
        if (!this.isReady) {
          console.log('⏳ Python API 服务器正在初始化...')
          resolve() // 即使没有检测到启动消息也 resolve，因为可能需要更长时间
        }
      }, 3000)
    })
  }

  /**
   * 停止 Python API 服务器
   */
  stop() {
    if (this.pythonProcess) {
      console.log('正在停止 Python API 服务器...')
      this.pythonProcess.kill('SIGTERM')
      this.pythonProcess = null
      this.isReady = false
    }
  }

  /**
   * 检查服务器是否就绪
   */
  ready() {
    return this.isReady
  }

  /**
   * 获取 API 服务器地址
   */
  getApiUrl() {
    return `http://127.0.0.1:${this.port}`
  }
}

export default PythonBridge
