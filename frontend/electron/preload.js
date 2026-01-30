import { contextBridge, ipcRenderer } from 'electron'

// 暴露受保护的 API 给渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
  // 平台信息
  platform: process.platform,

  // 应用版本
  getVersion: () => {
    return '2.0.0'
  },

  // 文件操作（后续扩展）
  selectFile: () => {
    return ipcRenderer.invoke('dialog:openFile')
  },

  // Python API 调用（后续实现）
  callPythonAPI: (endpoint, data) => {
    return ipcRenderer.invoke('python:call', endpoint, data)
  }
})

// 暴露 Node.js 版本
contextBridge.exposeInMainWorld('nodeVersions', {
  node: process.versions.node,
  chrome: process.versions.chrome,
  electron: process.versions.electron
})
