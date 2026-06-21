import axios from 'axios'
import { ref } from 'vue'

// 全局事件：用于通知 401 登出
const unauthorizedEvent = ref(null)

// 重试配置
const MAX_RETRY = 3 // 最大重试次数（不含首次请求）
const RETRY_BASE_DELAY = 500 // 基础延迟（毫秒）
const RETRYABLE_METHODS = ['get', 'head', 'options', 'put', 'delete']
const RETRYABLE_STATUS = [408, 429, 500, 502, 503, 504]

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

/**
 * 判断错误是否可重试
 */
function isRetryable(error) {
  // 网络错误 / 超时
  if (!error.response) return true
  // 仅对幂等或安全方法重试
  const method = (error.config?.method || '').toLowerCase()
  if (!RETRYABLE_METHODS.includes(method)) return false
  return RETRYABLE_STATUS.includes(error.response.status)
}

/**
 * 指数退避延迟（带抖动）
 */
function getRetryDelay(attempt) {
  const exp = RETRY_BASE_DELAY * Math.pow(2, attempt)
  // 加入 ±20% 抖动，避免惊群
  const jitter = exp * 0.2 * (Math.random() * 2 - 1)
  return Math.max(0, exp + jitter)
}

/**
 * 带重试的请求执行
 */
async function requestWithRetry(config, attempt = 0) {
  try {
    return await api.request(config)
  } catch (error) {
    // 401 直接触发登出，不重试
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('userId')
      localStorage.removeItem('username')
      unauthorizedEvent.value = Date.now()
      throw error
    }

    if (attempt >= MAX_RETRY || !isRetryable(error)) {
      throw error
    }

    const delay = getRetryDelay(attempt)
    await new Promise((resolve) => setTimeout(resolve, delay))
    return requestWithRetry(config, attempt + 1)
  }
}

// 对外暴露带重试的便捷方法
const http = {
  get(url, config = {}) {
    return requestWithRetry({ ...config, method: 'get', url })
  },
  post(url, data = undefined, config = {}) {
    return requestWithRetry({ ...config, method: 'post', url, data })
  },
  put(url, data = undefined, config = {}) {
    return requestWithRetry({ ...config, method: 'put', url, data })
  },
  delete(url, config = {}) {
    return requestWithRetry({ ...config, method: 'delete', url })
  },
  request(config) {
    return requestWithRetry(config)
  },
  // 暴露原始 axios 实例（如需直接访问拦截器等）
  _axios: api,
}

// 订阅 401 事件
export function onUnauthorized(callback) {
  const stop = (unauthorizedEvent) => {
    if (unauthorizedEvent.value) {
      callback()
    }
  }
  return stop
}

export { unauthorizedEvent }
export default http
