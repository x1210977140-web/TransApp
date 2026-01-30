import axios from 'axios'

// API 基础地址
const API_BASE_URL = 'http://127.0.0.1:5000'

// 创建 axios 实例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

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
