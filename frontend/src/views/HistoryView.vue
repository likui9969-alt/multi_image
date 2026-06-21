<template>
  <div class="history-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">
        <span class="title-icon">📁</span>
        历史记录
      </h1>
      <p class="page-desc">查看和管理你的所有转换记录</p>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section">
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <span class="stat-value">{{ stats.total }}</span>
          <span class="stat-label">总转换数</span>
        </div>
      </div>
      <div class="stat-card success">
        <div class="stat-icon">✅</div>
        <div class="stat-content">
          <span class="stat-value">{{ stats.successRate }}%</span>
          <span class="stat-label">成功率</span>
        </div>
      </div>
      <div class="stat-card primary">
        <div class="stat-icon">🎨</div>
        <div class="stat-content">
          <span class="stat-value">{{ stats.favoriteStyle }}</span>
          <span class="stat-label">最常用风格</span>
        </div>
      </div>
    </div>

    <!-- 工具栏 -->
    <div class="toolbar">
      <div class="filters">
        <select v-model="filterStyle" class="filter-select">
          <option value="">全部风格</option>
          <option v-for="s in styleOptions" :key="s.id" :value="s.id">{{ s.name }}</option>
        </select>
        <select v-model="filterStatus" class="filter-select">
          <option value="">全部状态</option>
          <option value="completed">已完成</option>
          <option value="processing">处理中</option>
          <option value="failed">失败</option>
          <option value="uploaded">已上传</option>
        </select>
        <select v-model="filterTime" class="filter-select">
          <option value="">全部时间</option>
          <option value="today">今天</option>
          <option value="week">本周</option>
          <option value="month">本月</option>
        </select>
      </div>
      <div class="view-actions">
        <div class="view-toggle">
          <button 
            class="view-btn" 
            :class="{ active: viewMode === 'grid' }"
            @click="viewMode = 'grid'"
            title="网格视图"
          >
            <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
              <rect x="3" y="3" width="7" height="7" rx="1"/>
              <rect x="14" y="3" width="7" height="7" rx="1"/>
              <rect x="3" y="14" width="7" height="7" rx="1"/>
              <rect x="14" y="14" width="7" height="7" rx="1"/>
            </svg>
          </button>
          <button 
            class="view-btn" 
            :class="{ active: viewMode === 'list' }"
            @click="viewMode = 'list'"
            title="列表视图"
          >
            <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
              <rect x="3" y="4" width="18" height="4" rx="1"/>
              <rect x="3" y="10" width="18" height="4" rx="1"/>
              <rect x="3" y="16" width="18" height="4" rx="1"/>
            </svg>
          </button>
        </div>
        <button 
          v-if="selectedTasks.length > 0"
          class="btn danger sm"
          @click="batchDelete"
        >
          <span>🗑️</span>
          删除选中 ({{ selectedTasks.length }})
        </button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="skeleton-grid">
      <div v-for="i in 6" :key="i" class="skeleton-card">
        <div class="skeleton-img"></div>
        <div class="skeleton-info">
          <div class="skeleton-line"></div>
          <div class="skeleton-line short"></div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else-if="!filteredTasks.length" class="empty-state">
      <div class="empty-illustration">
        <svg viewBox="0 0 200 200" fill="none">
          <circle cx="100" cy="100" r="80" stroke="var(--color-border)" stroke-width="4" opacity="0.3"/>
          <path d="M70 80 L130 80 M70 100 L130 100 M70 120 L100 120" stroke="var(--color-border)" stroke-width="4" stroke-linecap="round"/>
          <circle cx="130" cy="120" r="15" fill="var(--color-primary-bg)"/>
          <path d="M125 120 L135 120 M130 115 L130 125" stroke="var(--color-primary)" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </div>
      <h3 class="empty-title">{{ filterStyle || filterStatus || filterTime ? '没有符合条件的记录' : '暂无历史记录' }}</h3>
      <p class="empty-desc">开始上传图片并转换风格，记录将在这里显示</p>
      <router-link to="/" class="btn primary lg">
        <span>🎨</span>
        开始创作
      </router-link>
    </div>

    <!-- 网格视图 -->
    <div v-else-if="viewMode === 'grid'" class="task-grid">
      <div 
        v-for="t in filteredTasks" 
        :key="t.id" 
        class="task-card-grid"
        :class="{ selected: selectedTasks.includes(t.id) }"
        @click="toggleSelect(t.id)"
      >
        <div class="card-checkbox">
          <input type="checkbox" :checked="selectedTasks.includes(t.id)" @click.stop />
        </div>
        <div class="card-image">
          <img 
            v-if="t.status === 'completed'" 
            :src="imgUrl(t)" 
            class="result-img"
            @click.stop="previewImage(imgUrl(t))"
          />
          <div v-else class="placeholder-img">
            <span v-if="t.status === 'processing'" class="status-icon">⏳</span>
            <span v-else-if="t.status === 'failed'" class="status-icon">❌</span>
            <span v-else class="status-icon">📤</span>
          </div>
        </div>
        <div class="card-info">
          <h4 class="card-title">{{ t.original_filename }}</h4>
          <div class="card-tags">
            <span class="tag" :class="getTagClass(t.status)">{{ statusLabel(t.status) }}</span>
            <span class="tag primary">{{ styleLabel(t.style_type) }}</span>
          </div>
          <p class="card-time">{{ formatTime(t.created_at) }}</p>
        </div>
        <div class="card-actions">
          <button 
            v-if="t.status === 'completed'"
            class="btn ghost sm"
            @click.stop="downloadResult(t)"
            title="下载"
          >
            ⬇️
          </button>
          <button 
            class="btn danger sm"
            @click.stop="remove(t.id)"
            :disabled="t.deleting"
          >
            <span v-if="t.deleting" class="spinner dark"></span>
            <span v-else>🗑️</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 列表视图 -->
    <div v-else class="task-list">
      <div 
        v-for="t in filteredTasks" 
        :key="t.id" 
        class="task-card-list"
        :class="{ selected: selectedTasks.includes(t.id) }"
        @click="toggleSelect(t.id)"
      >
        <div class="list-checkbox">
          <input type="checkbox" :checked="selectedTasks.includes(t.id)" @click.stop />
        </div>
        <div class="list-thumb">
          <img 
            v-if="t.status === 'completed'" 
            :src="imgUrl(t)" 
            class="thumb-img"
            @click.stop="previewImage(imgUrl(t))"
          />
          <div v-else class="thumb-placeholder">
            <span v-if="t.status === 'processing'" class="status-icon">⏳</span>
            <span v-else-if="t.status === 'failed'" class="status-icon">❌</span>
            <span v-else class="status-icon">📤</span>
          </div>
        </div>
        <div class="list-info">
          <h4 class="list-title">{{ t.original_filename }}</h4>
          <div class="list-meta">
            <span class="tag" :class="getTagClass(t.status)">{{ statusLabel(t.status) }}</span>
            <span class="tag primary">{{ styleLabel(t.style_type) }}</span>
            <span class="meta-time">{{ formatTime(t.created_at) }}</span>
          </div>
        </div>
        <div class="list-actions">
          <button 
            v-if="t.status === 'completed'"
            class="btn ghost sm"
            @click.stop="downloadResult(t)"
          >
            ⬇️ 下载
          </button>
          <button 
            class="btn danger sm"
            @click.stop="remove(t.id)"
            :disabled="t.deleting"
          >
            <span v-if="t.deleting" class="spinner dark"></span>
            <span v-else>🗑️</span>
            {{ t.deleting ? '' : '删除' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 图片预览弹窗 -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="previewVisible" class="preview-modal" @click="closePreview">
          <div class="preview-container" @click.stop>
            <img :src="previewSrc" class="preview-img" />
            <div class="preview-actions">
              <button class="btn primary" @click="downloadPreview">
                ⬇️ 下载图片
              </button>
              <button class="btn secondary" @click="closePreview">
                ✖ 关闭
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api.js'

const tasks = ref([])
const loading = ref(true)
const filterStyle = ref('')
const filterStatus = ref('')
const filterTime = ref('')
const viewMode = ref('grid')
const selectedTasks = ref([])
const previewVisible = ref(false)
const previewSrc = ref('')
const previewFilename = ref('')

// 分页
const currentPage = ref(1)
const pageSize = ref(20)
const pagination = ref({ total: 0, page: 1, page_size: 20, total_pages: 1 })

const styleOptions = [
  { id: 'anime', name: '动漫' },
  { id: 'oil_painting', name: '油画' },
  { id: 'sketch', name: '素描' },
  { id: 'watercolor', name: '水彩' },
  { id: 'pixel_art', name: '像素' },
]

const styleMap = {
  anime: '动漫',
  oil_painting: '油画',
  sketch: '素描',
  watercolor: '水彩',
  pixel_art: '像素',
}

const statusMap = {
  uploaded: '已上传',
  processing: '处理中',
  completed: '已完成',
  failed: '失败',
}

// 统计数据
const stats = computed(() => {
  const total = tasks.value.length
  const completed = tasks.value.filter(t => t.status === 'completed').length
  const successRate = total > 0 ? Math.round((completed / total) * 100) : 0
  
  // 计算最常用风格
  const styleCounts = {}
  tasks.value.forEach(t => {
    if (t.style_type) {
      styleCounts[t.style_type] = (styleCounts[t.style_type] || 0) + 1
    }
  })
  
  let favoriteStyle = '无'
  let maxCount = 0
  Object.entries(styleCounts).forEach(([style, count]) => {
    if (count > maxCount) {
      maxCount = count
      favoriteStyle = styleMap[style] || style
    }
  })
  
  return { total, successRate, favoriteStyle }
})

function styleLabel(s) {
  return styleMap[s] || s || '未知'
}

function statusLabel(s) {
  return statusMap[s] || s
}

function getTagClass(status) {
  const classMap = {
    completed: 'success',
    processing: 'warning',
    failed: 'danger',
    uploaded: '',
  }
  return classMap[status] || ''
}

function imgUrl(t) {
  const p = (t.result_image_path || '').replace(/\\/g, '/')
  return p ? '/' + p : ''
}

function formatTime(time) {
  if (!time) return ''
  const d = new Date(time)
  return d.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 时间筛选
function isInTimeRange(time, range) {
  if (!time || !range) return true
  const d = new Date(time)
  const now = new Date()
  
  switch (range) {
    case 'today':
      return d.toDateString() === now.toDateString()
    case 'week':
      const weekStart = new Date(now)
      weekStart.setDate(now.getDate() - now.getDay())
      return d >= weekStart
    case 'month':
      return d.getMonth() === now.getMonth() && d.getFullYear() === now.getFullYear()
    default:
      return true
  }
}

const filteredTasks = computed(() => {
  return tasks.value.filter((t) => {
    if (filterStyle.value && t.style_type !== filterStyle.value) return false
    if (filterStatus.value && t.status !== filterStatus.value) return false
    if (filterTime.value && !isInTimeRange(t.created_at, filterTime.value)) return false
    return true
  })
})

// 选择功能
function toggleSelect(id) {
  const index = selectedTasks.value.indexOf(id)
  if (index === -1) {
    selectedTasks.value.push(id)
  } else {
    selectedTasks.value.splice(index, 1)
  }
}

async function load() {
  loading.value = true
  try {
    const { data } = await api.get('/history', {
      params: { page: currentPage.value, page_size: pageSize.value },
    })
    // 兼容分页响应（items）和旧版响应（tasks）
    tasks.value = (data.items || data.tasks || []).map((t) => ({ ...t, deleting: false }))
    pagination.value = {
      total: data.total || 0,
      page: data.page || 1,
      page_size: data.page_size || pageSize.value,
      total_pages: data.total_pages || 1,
    }
  } catch (e) {
    window.$toastError?.('加载历史记录失败')
  } finally {
    loading.value = false
  }
}

async function remove(id) {
  const confirmed = await window.$confirm?.({
    title: '删除确认',
    message: '确定要删除这条记录吗？删除后无法恢复。',
    confirmText: '删除',
  })

  if (!confirmed) return

  const task = tasks.value.find((t) => t.id === id)
  if (task) task.deleting = true

  try {
    await api.delete(`/history/${id}`)
    tasks.value = tasks.value.filter((t) => t.id !== id)
    selectedTasks.value = selectedTasks.value.filter(tId => tId !== id)
    window.$toastSuccess?.('删除成功')
  } catch (e) {
    window.$toastError?.('删除失败')
    if (task) task.deleting = false
  }
}

async function batchDelete() {
  const confirmed = await window.$confirm?.({
    title: '批量删除确认',
    message: `确定要删除选中的 ${selectedTasks.value.length} 条记录吗？删除后无法恢复。`,
    confirmText: '删除',
  })

  if (!confirmed) return

  const idsToDelete = [...selectedTasks.value]
  
  // 标记所有选中任务为删除中
  tasks.value.forEach(t => {
    if (idsToDelete.includes(t.id)) t.deleting = true
  })

  try {
    // 逐个删除
    for (const id of idsToDelete) {
      await api.delete(`/history/${id}`)
    }
    tasks.value = tasks.value.filter((t) => !idsToDelete.includes(t.id))
    selectedTasks.value = []
    window.$toastSuccess?.(`成功删除 ${idsToDelete.length} 条记录`)
  } catch (e) {
    window.$toastError?.('批量删除失败')
    // 恢复删除状态
    tasks.value.forEach(t => {
      if (idsToDelete.includes(t.id)) t.deleting = false
    })
  }
}

function previewImage(src) {
  previewSrc.value = src
  previewVisible.value = true
}

function closePreview() {
  previewVisible.value = false
  previewSrc.value = ''
  previewFilename.value = ''
}

function downloadResult(t) {
  const url = imgUrl(t)
  if (!url) return
  
  const link = document.createElement('a')
  link.href = url
  link.download = t.original_filename || 'result.jpg'
  link.click()
}

function downloadPreview() {
  if (!previewSrc.value) return
  
  const link = document.createElement('a')
  link.href = previewSrc.value
  link.download = previewFilename.value || 'result.jpg'
  link.click()
}

onMounted(load)
</script>

<style scoped>
.history-page {
  padding: var(--spacing-lg);
  max-width: 1200px;
  margin: 0 auto;
}

/* 页面标题 */
.page-header {
  margin-bottom: var(--spacing-xl);
}

.page-title {
  font-family: var(--font-family-display);
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.title-icon {
  font-size: 28px;
}

.page-desc {
  color: var(--color-text-secondary);
  margin-top: var(--spacing-xs);
}

/* 统计卡片 */
.stats-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.stat-card {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  background: var(--color-bg-white);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  transition: all var(--transition-fast);
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.stat-card.success {
  border-color: var(--color-success);
  background: var(--color-success-bg);
}

.stat-card.primary {
  border-color: var(--color-primary);
  background: var(--color-primary-bg);
}

.stat-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-primary);
  border-radius: var(--radius-md);
  font-size: 24px;
}

.stat-card.success .stat-icon {
  background: var(--color-success);
}

.stat-card.primary .stat-icon {
  background: var(--gradient-primary);
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-family: var(--font-family-display);
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

/* 工具栏 */
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  padding: var(--spacing-md);
  background: var(--color-bg-white);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
}

.filters {
  display: flex;
  gap: var(--spacing-sm);
}

.filter-select {
  padding: 8px 12px;
  font-size: var(--font-size-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-bg);
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.filter-select:focus {
  border-color: var(--color-primary);
  outline: none;
}

.view-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.view-toggle {
  display: flex;
  gap: var(--spacing-xs);
  padding: 4px;
  background: var(--color-bg);
  border-radius: var(--radius-md);
}

.view-btn {
  padding: 8px;
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.view-btn:hover {
  color: var(--color-primary);
}

.view-btn.active {
  background: var(--color-primary);
  color: white;
}

/* 骨架屏 */
.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
}

.skeleton-card {
  background: var(--color-bg-white);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.skeleton-img {
  height: 200px;
  background: linear-gradient(90deg, var(--color-bg) 25%, var(--color-border-light) 50%, var(--color-bg) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton-info {
  padding: var(--spacing-md);
}

.skeleton-line {
  height: 16px;
  background: linear-gradient(90deg, var(--color-bg) 25%, var(--color-border-light) 50%, var(--color-bg) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-sm);
  margin-bottom: var(--spacing-sm);
}

.skeleton-line.short {
  width: 60%;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: var(--spacing-3xl) var(--spacing-lg);
}

.empty-illustration {
  width: 200px;
  height: 200px;
  margin: 0 auto var(--spacing-lg);
}

.empty-title {
  font-size: var(--font-size-lg);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.empty-desc {
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-lg);
}

/* 网格视图 */
.task-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
}

.task-card-grid {
  position: relative;
  background: var(--color-bg-white);
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 2px solid var(--color-border-light);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.task-card-grid:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.task-card-grid.selected {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-glow);
}

.card-checkbox {
  position: absolute;
  top: var(--spacing-sm);
  left: var(--spacing-sm);
  z-index: 10;
}

.card-checkbox input {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: var(--color-primary);
}

.card-image {
  position: relative;
  height: 200px;
  background: var(--color-bg);
}

.result-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: zoom-in;
  transition: transform var(--transition-fast);
}

.result-img:hover {
  transform: scale(1.05);
}

.placeholder-img {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg);
}

.status-icon {
  font-size: 48px;
  opacity: 0.5;
}

.card-info {
  padding: var(--spacing-md);
}

.card-title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-tags {
  display: flex;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-sm);
}

.card-time {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.card-actions {
  display: flex;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  border-top: 1px solid var(--color-border-light);
}

/* 列表视图 */
.task-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.task-card-list {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--color-bg-white);
  border-radius: var(--radius-lg);
  border: 2px solid var(--color-border-light);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.task-card-list:hover {
  box-shadow: var(--shadow-md);
}

.task-card-list.selected {
  border-color: var(--color-primary);
  background: var(--color-primary-bg);
}

.list-checkbox {
  flex-shrink: 0;
}

.list-checkbox input {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: var(--color-primary);
}

.list-thumb {
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--color-bg);
}

.thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: zoom-in;
}

.thumb-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.thumb-placeholder .status-icon {
  font-size: 32px;
  opacity: 0.5;
}

.list-info {
  flex: 1;
}

.list-title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
}

.list-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.meta-time {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.list-actions {
  display: flex;
  gap: var(--spacing-sm);
}

/* 图片预览弹窗 */
.preview-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.preview-container {
  text-align: center;
  max-width: 90vw;
  max-height: 90vh;
}

.preview-img {
  max-width: 100%;
  max-height: 80vh;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
}

.preview-actions {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .preview-container,
.modal-leave-to .preview-container {
  transform: scale(0.9);
}

/* 响应式 */
@media (max-width: 1024px) {
  .task-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-section {
    grid-template-columns: 1fr;
  }

  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .filters {
    flex-wrap: wrap;
  }

  .filter-select {
    flex: 1;
    min-width: 120px;
  }

  .view-actions {
    justify-content: space-between;
  }

  .task-grid {
    grid-template-columns: 1fr;
  }

  .task-card-list {
    flex-wrap: wrap;
  }

  .list-thumb {
    order: -1;
    width: 100%;
    height: 150px;
    margin-bottom: var(--spacing-sm);
  }

  .list-actions {
    width: 100%;
    justify-content: flex-end;
    margin-top: var(--spacing-sm);
  }
}

@media (max-width: 480px) {
  .history-page {
    padding: var(--spacing-md);
  }

  .page-title {
    font-size: var(--font-size-xl);
  }

  .stat-card {
    padding: var(--spacing-md);
  }

  .stat-icon {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }

  .stat-value {
    font-size: var(--font-size-lg);
  }
}
</style>