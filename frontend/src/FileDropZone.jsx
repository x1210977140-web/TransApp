import { useState } from 'react'

function FileDropZone({ onFileSelect, accept = '.mp3,.wav,.m4a,.flac,.ogg', placeholder = '拖拽音频文件到此处或点击选择' }) {
  const [isDragging, setIsDragging] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)

    const files = e.dataTransfer.files
    if (files.length > 0) {
      const file = files[0]
      setSelectedFile(file)
      onFileSelect(file.path || file.name)
    }
  }

  const handleClick = () => {
    // 触发文件选择对话框
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = accept
    input.onchange = (e) => {
      const file = e.target.files[0]
      if (file) {
        setSelectedFile(file)
        onFileSelect(file.path || file.name)
      }
    }
    input.click()
  }

  return (
    <div
      className={`file-drop-zone ${isDragging ? 'dragging' : ''}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={handleClick}
    >
      <div className="drop-zone-content">
        <svg className="upload-icon" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="17 8 12 3 7 8"/>
          <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
        <p className="drop-zone-text">{placeholder}</p>
        {selectedFile && (
          <p className="selected-file-name">已选择: {selectedFile.name}</p>
        )}
        <p className="drop-zone-hint">支持格式: MP3, WAV, M4A, FLAC, OGG</p>
      </div>
    </div>
  )
}

export default FileDropZone
