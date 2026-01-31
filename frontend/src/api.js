import axios from 'axios'

// API 基础地址
const API_BASE_URL = 'http://127.0.0.1:5000'

// 创建 axios 实例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 增加到 60 秒，首次运行模型加载需要时间
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加重试逻辑
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    // 如果是网络错误或连接被拒绝，尝试重试
    if (!error.response && !originalRequest._retry) {
      originalRequest._retry = true
      const maxRetries = 3
      const retryDelay = 2000 // 2秒

      for (let i = 0; i < maxRetries; i++) {
        console.log(`请求失败，${retryDelay/1000}秒后重试 (${i+1}/${maxRetries})...`)

        await new Promise(resolve => setTimeout(resolve, retryDelay))

        try {
          const response = await api(originalRequest)
          return response
        } catch (retryError) {
          if (i === maxRetries - 1) {
            console.error('重试失败，API 服务器可能未启动')
            throw new Error('网络错误：无法连接到 Python API 服务器。请确保应用已完全启动。')
          }
        }
      }
    }

    // 其他错误直接抛出
    throw error
  }
)

// ==================== 系统接口 ====================

export const getSystemStatus = async () => {
  const response = await api.get('/')
  return response.data
}

export const getHealth = async () => {
  const response = await api.get('/health')
  return response.data
}

export const getSupportedLanguages = async () => {
  const response = await api.get('/api/languages')
  return response.data
}

// ==================== 翻译接口 ====================

export const translateText = async (text, sourceLang, targetLang) => {
  const response = await api.post('/api/translate', {
    text,
    source_lang: sourceLang,
    target_lang: targetLang
  })
  return response.data
}

export const translateBatch = async (requests) => {
  const response = await api.post('/api/translate/batch', requests)
  return response.data
}

// ==================== 音频转录接口 ====================

export const transcribeAudio = async (audioPath, language = 'auto') => {
  const response = await api.post('/api/transcribe', {
    audio_path: audioPath,
    language,
    task: 'transcribe'
  })
  return response.data
}

export const transcribeAndTranslate = async (audioPath, sourceLang = 'auto', targetLang = 'en') => {
  const response = await api.post('/api/transcribe-and-translate', {
    audio_path: audioPath,
    source_lang: sourceLang,
    target_lang: targetLang
  })
  return response.data
}

export default api
