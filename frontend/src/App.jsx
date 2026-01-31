import { useState, useEffect } from 'react'
import './App.css'
import { getSystemStatus, getSupportedLanguages, translateText, transcribeAudio, transcribeAndTranslate } from './api'
import FileDropZone from './FileDropZone'

function App() {
  const [activeTab, setActiveTab] = useState('translate')
  const [systemStatus, setSystemStatus] = useState(null)
  const [supportedLanguages, setSupportedLanguages] = useState([])

  useEffect(() => {
    loadSystemInfo()
  }, [])

  const loadSystemInfo = async () => {
    try {
      const [status, languages] = await Promise.all([
        getSystemStatus(),
        getSupportedLanguages()
      ])
      setSystemStatus(status)
      setSupportedLanguages(languages.languages)
    } catch (error) {
      console.error('Failed to load system info:', error)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>QuickTrans</h1>
        <p>本地音频转录与文本翻译引擎</p>
        {systemStatus && (
          <div className="status-badge">
            <span className="status-dot"></span>
            系统正常
          </div>
        )}
      </header>

      <nav className="app-nav">
        <button
          className={activeTab === 'translate' ? 'active' : ''}
          onClick={() => setActiveTab('translate')}
        >
          文本翻译
        </button>
        <button
          className={activeTab === 'transcribe' ? 'active' : ''}
          onClick={() => setActiveTab('transcribe')}
        >
          音频转录
        </button>
        <button
          className={activeTab === 'both' ? 'active' : ''}
          onClick={() => setActiveTab('both')}
        >
          转录并翻译
        </button>
      </nav>

      <main className="app-main">
        {activeTab === 'translate' && <TranslationTab languages={supportedLanguages} />}
        {activeTab === 'transcribe' && <TranscriptionTab />}
        {activeTab === 'both' && <CombinedTab languages={supportedLanguages} />}
      </main>

      <footer className="app-footer">
        <p>QuickTrans v2.0.0 | 完全离线运行 | 保护您的隐私</p>
      </footer>
    </div>
  )
}

// ==================== 文本翻译组件 ====================

function TranslationTab({ languages }) {
  const [sourceText, setSourceText] = useState('')
  const [translatedText, setTranslatedText] = useState('')
  const [sourceLang, setSourceLang] = useState('zh')
  const [targetLang, setTargetLang] = useState('en')
  const [loading, setLoading] = useState(false)

  const handleTranslate = async () => {
    if (!sourceText.trim()) return

    setLoading(true)
    try {
      const result = await translateText(sourceText, sourceLang, targetLang)
      setTranslatedText(result.translated_text)
    } catch (error) {
      console.error('Translation failed:', error)
      alert('翻译失败：' + error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="tab-content">
      <div className="translation-container">
        <div className="language-selector">
          <select
            value={sourceLang}
            onChange={(e) => setSourceLang(e.target.value)}
          >
            {languages.map(lang => (
              <option key={lang.code} value={lang.code}>
                {lang.name}
              </option>
            ))}
          </select>
          <span className="arrow">→</span>
          <select
            value={targetLang}
            onChange={(e) => setTargetLang(e.target.value)}
          >
            {languages
              .filter(l => l.code === sourceLang)
              .flatMap(l => l.can_translate_to)
              .map(code => {
                const lang = languages.find(l => l.code === code)
                return lang ? (
                  <option key={lang.code} value={lang.code}>
                    {lang.name}
                  </option>
                ) : null
              })}
          </select>
        </div>

        <div className="text-areas">
          <div className="text-area">
            <textarea
              placeholder="输入要翻译的文本..."
              value={sourceText}
              onChange={(e) => setSourceText(e.target.value)}
            />
            <div className="char-count">{sourceText.length} 字符</div>
          </div>

          <div className="text-area">
            <textarea
              placeholder="翻译结果将显示在这里..."
              value={translatedText}
              readOnly
            />
            <button
              className="copy-btn"
              onClick={() => navigator.clipboard.writeText(translatedText)}
              disabled={!translatedText}
            >
              复制
            </button>
          </div>
        </div>

        <button
          className="action-btn"
          onClick={handleTranslate}
          disabled={loading || !sourceText.trim()}
        >
          {loading ? '翻译中...' : '开始翻译'}
        </button>
      </div>
    </div>
  )
}

// ==================== 音频转录组件 ====================

function TranscriptionTab() {
  const [audioPath, setAudioPath] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleTranscribe = async () => {
    if (!audioPath.trim()) return

    setLoading(true)
    try {
      const transcription = await transcribeAudio(audioPath)
      setResult(transcription)
    } catch (error) {
      console.error('Transcription failed:', error)
      alert('转录失败：' + error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="tab-content">
      <div className="transcription-container">
        <FileDropZone
          onFileSelect={setAudioPath}
          placeholder="拖拽音频文件到此处或点击选择"
        />

        <button
          className="action-btn"
          onClick={handleTranscribe}
          disabled={loading || !audioPath.trim()}
        >
          {loading ? '转录中...' : '开始转录'}
        </button>

        {result && (
          <div className="result-area">
            <h3>转录结果</h3>
            <div className="result-info">
              <p><strong>检测语言：</strong>{result.language}</p>
              <p><strong>置信度：</strong>{(result.language_probability * 100).toFixed(1)}%</p>
              <p><strong>音频时长：</strong>{result.duration.toFixed(1)} 秒</p>
              <p><strong>处理时间：</strong>{result.processing_time.toFixed(1)} 秒</p>
            </div>
            <div className="result-text">
              <p>{result.text}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

// ==================== 转录+翻译组件 ====================

function CombinedTab({ languages }) {
  const [audioPath, setAudioPath] = useState('')
  const [targetLang, setTargetLang] = useState('en')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleProcess = async () => {
    if (!audioPath.trim()) return

    setLoading(true)
    try {
      const processed = await transcribeAndTranslate(audioPath, 'auto', targetLang)
      setResult(processed)
    } catch (error) {
      console.error('Processing failed:', error)
      alert('处理失败：' + error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="tab-content">
      <div className="combined-container">
        <FileDropZone
          onFileSelect={setAudioPath}
          placeholder="拖拽音频文件到此处或点击选择"
        />

        <select
          value={targetLang}
          onChange={(e) => setTargetLang(e.target.value)}
          className="lang-select"
        >
          {languages.map(lang => (
            <option key={lang.code} value={lang.code}>
              翻译成{lang.name}
            </option>
          ))}
        </select>

        <button
          className="action-btn"
          onClick={handleProcess}
          disabled={loading || !audioPath.trim()}
        >
          {loading ? '处理中...' : '转录并翻译'}
        </button>

        {result && (
          <div className="result-area">
            <h3>处理结果</h3>
            <div className="result-info">
              <p><strong>检测语言：</strong>{result.detected_language}</p>
              <p><strong>目标语言：</strong>{result.target_language}</p>
              <p><strong>音频时长：</strong>{result.audio_duration.toFixed(1)} 秒</p>
              <p><strong>处理时间：</strong>{result.processing_time.toFixed(1)} 秒</p>
            </div>
            <div className="result-text-section">
              <div>
                <h4>原文：</h4>
                <p>{result.original_text}</p>
              </div>
              <div>
                <h4>译文：</h4>
                <p>{result.translated_text}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
