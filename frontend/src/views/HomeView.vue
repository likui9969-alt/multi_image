<template>
  <div class="home">
    <!-- Hero 区域 -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="gradient-text">AI 风格转换</span>
          <br>让图片焕发新生
        </h1>
        <p class="hero-desc">
          上传一张图片，选择你喜欢的艺术风格，AI 将在几秒内为你生成独特的艺术作品
        </p>
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-value">5+</span>
            <span class="stat-label">艺术风格</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">秒级</span>
            <span class="stat-label">转换速度</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">高清</span>
            <span class="stat-label">输出质量</span>
          </div>
        </div>
      </div>
      <div class="hero-visual">
        <div class="visual-card">
          <img src="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=artistic%20style%20transformation%20before%20after%20comparison%20split%20view&image_size=landscape_4_3" alt="风格转换示例" class="visual-img" />
          <div class="visual-overlay">
            <span class="visual-label">风格转换示例</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 上传区域 -->
    <section v-if="!taskId" class="upload-section">
      <div class="section-header">
        <h2 class="section-title">开始创作</h2>
        <p class="section-desc">上传你的图片，开启艺术之旅</p>
      </div>

      <div class="upload-container">
        <div
          class="upload-zone"
          :class="{ hasPreview: previewUrl, dragging: isDragging }"
          @drop.prevent="onDrop"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @click="!previewUrl && fileInput.click()"
        >
          <input
            ref="fileInput"
            type="file"
            accept="image/jpeg,image/png,image/webp"
            hidden
            @change="onFileSelect"
          />

          <template v-if="!previewUrl">
            <div class="upload-icon-wrapper">
              <div class="upload-icon">
                <svg viewBox="0 0 48 48" fill="none">
                  <circle cx="24" cy="24" r="22" stroke="currentColor" stroke-width="2" opacity="0.3"/>
                  <path d="M24 14 L24 34 M14 24 L34 24" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
                </svg>
              </div>
              <div class="upload-glow"></div>
            </div>
            <p class="upload-text">
              拖拽图片到此处，或<span class="upload-link" @click.stop="fileInput.click()">点击上传</span>
            </p>
            <p class="upload-hint">支持 JPG / PNG / WEBP，最大 10MB</p>
          </template>

          <template v-else>
            <img :src="previewUrl" class="preview-img" />
            <div class="preview-overlay">
              <button class="btn ghost sm" @click.stop="clearPreview">
                <span>🔄</span> 重新选择
              </button>
            </div>
          </template>
        </div>

        <div class="upload-actions">
          <button v-if="!previewUrl" class="btn primary lg" @click="fileInput.click()">
            <span>📤</span> 选择图片
          </button>
          <button v-else class="btn primary lg" :disabled="uploading" @click="upload">
            <span v-if="uploading" class="spinner"></span>
            <span v-else>✨</span>
            {{ uploading ? '上传中...' : '开始上传' }}
          </button>
        </div>

        <Transition name="error">
          <p v-if="uploadError" class="upload-error">{{ uploadError }}</p>
        </Transition>
      </div>
    </section>

    <!-- 风格选择区域 -->
    <section v-if="taskId && !resultUrl" class="style-section">
      <div class="section-header">
        <h2 class="section-title">选择风格</h2>
        <p class="section-desc">为你上传的图片选择一种艺术风格</p>
      </div>

      <div class="style-grid">
        <div
          v-for="s in styles"
          :key="s.id"
          :class="['style-card', { active: selectedStyle === s.id }]"
          @click="selectedStyle = s.id"
        >
          <div class="style-preview">
            <img :src="s.preview" :alt="s.name" class="style-img" />
            <div class="style-overlay">
              <span class="style-icon">{{ s.icon }}</span>
            </div>
          </div>
          <div class="style-info">
            <h3 class="style-name">{{ s.name }}</h3>
            <p class="style-desc">{{ s.description }}</p>
          </div>
          <div class="style-check" v-if="selectedStyle === s.id">
            <span>✓</span>
          </div>
        </div>
      </div>

      <div class="style-actions">
        <button class="btn secondary" @click="resetUpload">
          <span>🔄</span> 更换图片
        </button>
        <button
          class="btn primary lg"
          :disabled="!selectedStyle || processing"
          @click="process"
        >
          <span v-if="processing" class="spinner"></span>
          <span v-else>🎨</span>
          {{ processing ? '转换中...' : '开始转换' }}
        </button>
      </div>

      <!-- 进度条 -->
      <Transition name="progress">
        <div v-if="processing" class="progress-container">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: progressWidth }"></div>
            <div class="progress-glow" :style="{ width: progressWidth }"></div>
          </div>
          <p class="progress-text">
            正在应用 <strong>{{ currentStyleName }}</strong> 风格...
          </p>
        </div>
      </Transition>

      <Transition name="error">
        <p v-if="processError" class="process-error">{{ processError }}</p>
      </Transition>
    </section>

    <!-- 结果展示区域 -->
    <section v-if="resultUrl" class="result-section">
      <div class="section-header">
        <h2 class="section-title">转换完成</h2>
        <p class="section-desc">你的艺术作品已生成</p>
      </div>

      <!-- 滑块对比组件 -->
      <div class="compare-container">
        <div class="compare-wrapper">
          <img :src="previewUrl" class="compare-original" alt="原图" />
          <img :src="resultUrl" class="compare-result" alt="结果" />
          <div class="compare-slider" :style="{ left: sliderPosition + '%' }">
            <div class="slider-handle" @mousedown="startSliderDrag" @touchstart="startSliderDrag">
              <div class="slider-icon">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M8 12 L4 8 M8 12 L4 16 M16 12 L20 8 M16 12 L20 16" stroke="white" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </div>
            </div>
          </div>
          <div class="compare-labels">
            <span class="label-original">原图</span>
            <span class="label-result">{{ currentStyleName }}</span>
          </div>
        </div>
      </div>

      <div class="result-actions">
        <a :href="resultUrl" download class="btn primary lg">
          <span>📥</span> 下载作品
        </a>
        <button class="btn secondary" @click="reset">
          <span>🔄</span> 重新创作
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import api from '../services/api.js'

const fileInput = ref(null)
const previewUrl = ref('')
const selectedFile = ref(null)
const taskId = ref(null)
const selectedStyle = ref('')
const processing = ref(false)
const resultUrl = ref('')
const uploading = ref(false)
const uploadError = ref('')
const processError = ref('')
const progressWidth = ref('0%')
const isDragging = ref(false)
const sliderPosition = ref(50)
let progressTimer = null
let pollTimer = null
let sliderDragActive = false

const styles = [
  {
    id: 'anime',
    name: '动漫风格',
    icon: '🎌',
    description: '日系动漫风格，色彩鲜艳，线条流畅',
    preview: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=anime%20style%20portrait%20girl%20vibrant%20colors%20clean%20lines&image_size=square_hd'
  },
  {
    id: 'oil_painting',
    name: '油画风格',
    icon: '🖼️',
    description: '古典油画质感，厚重笔触，艺术气息',
    preview: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=oil%20painting%20landscape%20classical%20art%20brushstrokes&image_size=square_hd'
  },
  {
    id: 'sketch',
    name: '素描风格',
    icon: '✏️',
    description: '铅笔素描效果，细腻线条，层次分明',
    preview: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=pencil%20sketch%20portrait%20detailed%20lines%20shading&image_size=square_hd'
  },
  {
    id: 'watercolor',
    name: '水彩风格',
    icon: '🎨',
    description: '水彩晕染效果，柔和过渡，清新淡雅',
    preview: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=watercolor%20painting%20flowers%20soft%20blending%20pastel&image_size=square_hd'
  },
  {
    id: 'pixel_art',
    name: '像素风格',
    icon: '👾',
    description: '像素艺术风格，复古游戏感，独特魅力',
    preview: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=pixel%20art%20retro%20game%20style%208bit%20colorful&image_size=square_hd'
  },
]

const currentStyleName = computed(() => {
  const s = styles.find((s) => s.id === selectedStyle.value)
  return s ? s.name : ''
})

function onFileSelect(e) {
  const file = e.target.files[0]
  if (file) setPreview(file)
}

function onDrop(e) {
  isDragging.value = false
  const file = e.dataTransfer.files[0]
  if (file) setPreview(file)
}

function setPreview(file) {
  if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
    uploadError.value = '仅支持 JPG/PNG/WEBP 格式'
    window.$toastError?.('仅支持 JPG/PNG/WEBP 格式')
    return
  }
  if (file.size > 10 * 1024 * 1024) {
    uploadError.value = '文件大小不能超过 10MB'
    window.$toastError?.('文件大小不能超过 10MB')
    return
  }
  uploadError.value = ''
  selectedFile.value = file
  previewUrl.value = URL.createObjectURL(file)
}

function clearPreview() {
  previewUrl.value = ''
  selectedFile.value = null
  uploadError.value = ''
  if (fileInput.value) fileInput.value.value = ''
}

async function upload() {
  uploading.value = true
  uploadError.value = ''
  try {
    const form = new FormData()
    form.append('file', selectedFile.value)
    const { data } = await api.post('/images/upload', form)
    taskId.value = data.task_id
    window.$toastSuccess?.('图片上传成功')
  } catch (e) {
    uploadError.value = e.response?.data?.detail || '上传失败'
    window.$toastError?.(uploadError.value)
  } finally {
    uploading.value = false
  }
}

function startProgressAnimation() {
  progressWidth.value = '0%'
  let progress = 0
  progressTimer = setInterval(() => {
    progress += Math.random() * 15
    if (progress > 90) progress = 90
    progressWidth.value = progress + '%'
  }, 500)
}

function stopProgressAnimation() {
  if (progressTimer) {
    clearInterval(progressTimer)
    progressTimer = null
  }
  progressWidth.value = '100%'
}

async function pollTaskStatus(id) {
  try {
    const { data } = await api.get(`/tasks/${id}`)
    if (data.status === 'completed') {
      stopProgressAnimation()
      const path = data.result_image_path || data.result_url || ''
      resultUrl.value = path ? '/' + path.replace(/\\/g, '/') : data.result_url || ''
      window.$toastSuccess?.('风格转换完成')
      if (pollTimer) {
        clearInterval(pollTimer)
        pollTimer = null
      }
    } else if (data.status === 'failed') {
      stopProgressAnimation()
      processError.value = data.error_message || '转换失败'
      window.$toastError?.(processError.value)
      if (pollTimer) {
        clearInterval(pollTimer)
        pollTimer = null
      }
    }
  } catch (e) {
    // 轮询出错时继续尝试
  }
}

async function process() {
  processing.value = true
  processError.value = ''
  startProgressAnimation()

  try {
    const { data } = await api.post('/process', {
      task_id: taskId.value,
      style_type: selectedStyle.value,
    })

    console.log('API 响应:', data)
    stopProgressAnimation()

    // 无论后端返回什么状态，只要有 result_url 就显示成功
    if (data.result_url) {
      resultUrl.value = data.result_url
      window.$toastSuccess?.('风格转换完成')
    } else {
      processError.value = data.detail || '转换失败'
      window.$toastError?.(processError.value)
    }
  } catch (e) {
    stopProgressAnimation()
    processError.value = e.response?.data?.detail || '转换失败'
    window.$toastError?.(processError.value)
  } finally {
    processing.value = false
  }
}

function resetUpload() {
  taskId.value = null
  selectedStyle.value = ''
}

function reset() {
  taskId.value = null
  resultUrl.value = ''
  previewUrl.value = ''
  selectedFile.value = null
  selectedStyle.value = ''
  processError.value = ''
  progressWidth.value = '0%'
  sliderPosition.value = 50
  if (fileInput.value) fileInput.value.value = ''
}

// 滑块拖拽
function startSliderDrag(e) {
  e.preventDefault()
  sliderDragActive = true
  document.addEventListener('mousemove', handleSliderDrag)
  document.addEventListener('mouseup', stopSliderDrag)
  document.addEventListener('touchmove', handleSliderDrag)
  document.addEventListener('touchend', stopSliderDrag)
}

function handleSliderDrag(e) {
  if (!sliderDragActive) return
  const wrapper = document.querySelector('.compare-wrapper')
  if (!wrapper) return

  const rect = wrapper.getBoundingClientRect()
  const clientX = e.touches ? e.touches[0].clientX : e.clientX
  const position = ((clientX - rect.left) / rect.width) * 100
  sliderPosition.value = Math.max(0, Math.min(100, position))
}

function stopSliderDrag() {
  sliderDragActive = false
  document.removeEventListener('mousemove', handleSliderDrag)
  document.removeEventListener('mouseup', stopSliderDrag)
  document.removeEventListener('touchmove', handleSliderDrag)
  document.removeEventListener('touchend', stopSliderDrag)
}

onUnmounted(() => {
  stopProgressAnimation()
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
  stopSliderDrag()
})
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-xl) var(--spacing-lg);
}

/* Hero 区域 */
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-2xl);
  align-items: center;
  padding: var(--spacing-2xl) 0;
  margin-bottom: var(--spacing-2xl);
}

.hero-content {
  max-width: 500px;
}

.hero-title {
  font-family: var(--font-family-display);
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  line-height: 1.2;
  margin-bottom: var(--spacing-lg);
}

.hero-desc {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin-bottom: var(--spacing-xl);
}

.hero-stats {
  display: flex;
  gap: var(--spacing-xl);
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.stat-value {
  font-family: var(--font-family-display);
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.hero-visual {
  display: flex;
  justify-content: center;
}

.visual-card {
  position: relative;
  width: 100%;
  max-width: 400px;
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-xl);
}

.visual-img {
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
}

.visual-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: var(--spacing-md);
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
}

.visual-label {
  color: white;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

/* 区块头部 */
.section-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.section-title {
  font-family: var(--font-family-display);
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.section-desc {
  font-size: var(--font-size-md);
  color: var(--color-text-secondary);
}

/* 上传区域 */
.upload-section {
  margin-bottom: var(--spacing-2xl);
}

.upload-container {
  max-width: 600px;
  margin: 0 auto;
}

.upload-zone {
  position: relative;
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--spacing-3xl);
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-normal);
  background: var(--color-bg-white);
}

.upload-zone:hover,
.upload-zone.dragging {
  border-color: var(--color-primary);
  background: var(--color-primary-bg);
}

.upload-zone.hasPreview {
  border-style: solid;
  border-color: var(--color-primary);
  padding: var(--spacing-md);
}

.upload-icon-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
  margin: 0 auto var(--spacing-lg);
}

.upload-icon {
  width: 80px;
  height: 80px;
  color: var(--color-primary);
}

.upload-glow {
  position: absolute;
  inset: -10px;
  background: var(--color-primary);
  opacity: 0.1;
  border-radius: var(--radius-full);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.1;
    transform: scale(1);
  }
  50% {
    opacity: 0.2;
    transform: scale(1.1);
  }
}

.upload-text {
  font-size: var(--font-size-lg);
  color: var(--color-text-regular);
  margin-bottom: var(--spacing-sm);
}

.upload-link {
  color: var(--color-primary);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
}

.upload-hint {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.preview-img {
  max-width: 100%;
  max-height: 400px;
  border-radius: var(--radius-lg);
}

.preview-overlay {
  position: absolute;
  bottom: var(--spacing-md);
  left: 50%;
  transform: translateX(-50%);
}

.upload-actions {
  display: flex;
  justify-content: center;
  margin-top: var(--spacing-lg);
}

.upload-error,
.process-error {
  text-align: center;
  background: var(--color-danger-bg);
  color: var(--color-danger);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  margin-top: var(--spacing-md);
}

/* 风格选择 */
.style-section {
  margin-bottom: var(--spacing-2xl);
}

.style-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.style-card {
  position: relative;
  background: var(--color-bg-white);
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: all var(--transition-normal);
  border: 2px solid var(--color-border-light);
}

.style-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.style-card.active {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-glow);
}

.style-preview {
  position: relative;
  aspect-ratio: 1;
}

.style-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.style-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.style-card:hover .style-overlay {
  opacity: 1;
}

.style-icon {
  font-size: 32px;
}

.style-info {
  padding: var(--spacing-md);
}

.style-name {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
}

.style-desc {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  line-height: 1.4;
}

.style-check {
  position: absolute;
  top: var(--spacing-sm);
  right: var(--spacing-sm);
  width: 28px;
  height: 28px;
  background: var(--gradient-primary);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: var(--font-weight-bold);
}

.style-actions {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
}

/* 进度条 */
.progress-container {
  max-width: 500px;
  margin: var(--spacing-xl) auto 0;
}

.progress-bar {
  height: 8px;
  background: var(--color-bg);
  border-radius: var(--radius-full);
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: var(--gradient-primary);
  border-radius: var(--radius-full);
  transition: width 0.3s ease;
}

.progress-glow {
  position: absolute;
  top: 0;
  height: 100%;
  background: var(--color-primary);
  opacity: 0.3;
  filter: blur(4px);
  border-radius: var(--radius-full);
}

.progress-text {
  text-align: center;
  margin-top: var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.progress-text strong {
  color: var(--color-primary);
}

/* 结果展示 */
.result-section {
  margin-bottom: var(--spacing-2xl);
}

.compare-container {
  max-width: 800px;
  margin: 0 auto var(--spacing-xl);
}

.compare-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 10;
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: var(--shadow-xl);
}

.compare-original,
.compare-result {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.compare-result {
  clip-path: inset(0 0 0 50%);
}

.compare-slider {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 4px;
  background: white;
  cursor: ew-resize;
  z-index: 10;
  transition: left 0.05s ease;
}

.slider-handle {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 44px;
  height: 44px;
  background: var(--gradient-primary);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-lg);
}

.slider-icon {
  width: 24px;
  height: 24px;
}

.compare-labels {
  position: absolute;
  bottom: var(--spacing-md);
  left: var(--spacing-md);
  right: var(--spacing-md);
  display: flex;
  justify-content: space-between;
}

.label-original,
.label-result {
  padding: var(--spacing-xs) var(--spacing-md);
  background: rgba(0, 0, 0, 0.6);
  color: white;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.result-actions {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
}

/* 过渡动画 */
.error-enter-active,
.error-leave-active {
  transition: all 0.3s ease;
}

.error-enter-from,
.error-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.progress-enter-active,
.progress-leave-active {
  transition: all 0.3s ease;
}

.progress-enter-from,
.progress-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* 响应式 */
@media (max-width: 768px) {
  .home {
    padding: var(--spacing-lg) var(--spacing-md);
  }

  .hero {
    grid-template-columns: 1fr;
    gap: var(--spacing-xl);
    padding: var(--spacing-xl) 0;
  }

  .hero-content {
    text-align: center;
    max-width: 100%;
  }

  .hero-title {
    font-size: var(--font-size-3xl);
  }

  .hero-stats {
    justify-content: center;
  }

  .visual-card {
    max-width: 100%;
  }

  .upload-zone {
    padding: var(--spacing-xl);
  }

  .style-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-md);
  }

  .style-actions,
  .result-actions {
    flex-direction: column;
    align-items: center;
  }

  .compare-wrapper {
    aspect-ratio: 4 / 3;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: var(--font-size-2xl);
  }

  .hero-stats {
    gap: var(--spacing-md);
  }

  .stat-value {
    font-size: var(--font-size-xl);
  }

  .upload-zone {
    padding: var(--spacing-lg);
  }

  .upload-icon-wrapper {
    width: 60px;
    height: 60px;
  }

  .upload-icon {
    width: 60px;
    height: 60px;
  }

  .style-grid {
    grid-template-columns: 1fr;
  }
}
</style>