<template>
  <div class="auth-page">
    <!-- 左侧品牌展示区 -->
    <div class="brand-section">
      <div class="brand-content">
        <!-- Logo -->
        <div class="brand-logo">
          <div class="logo-icon">
            <svg viewBox="0 0 40 40" fill="none">
              <defs>
                <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#667eea"/>
                  <stop offset="100%" style="stop-color:#764ba2"/>
                </linearGradient>
              </defs>
              <circle cx="20" cy="20" r="18" fill="url(#logoGradient)"/>
              <path d="M12 20 L20 12 L28 20 L20 28 Z" fill="white" opacity="0.9"/>
              <circle cx="20" cy="20" r="4" fill="white"/>
            </svg>
          </div>
          <span class="logo-text">AI Style Studio</span>
        </div>

        <!-- 标题 -->
        <h1 class="brand-title">
          将你的图片<br>
          <span class="gradient-text">变成艺术作品</span>
        </h1>

        <!-- 描述 -->
        <p class="brand-desc">
          使用先进的 AI 技术，一键将普通照片转换为动漫、油画、素描等多种艺术风格
        </p>

        <!-- 特性列表 -->
        <div class="features">
          <div class="feature-item" v-for="(feature, index) in features" :key="index">
            <div class="feature-icon">{{ feature.icon }}</div>
            <div class="feature-content">
              <h3 class="feature-title">{{ feature.title }}</h3>
              <p class="feature-desc">{{ feature.desc }}</p>
            </div>
          </div>
        </div>

        <!-- 示例展示 -->
        <div class="showcase">
          <div class="showcase-label">风格示例</div>
          <div class="showcase-grid">
            <div class="showcase-item" v-for="style in showcaseStyles" :key="style.id">
              <img :src="style.img" :alt="style.name" class="showcase-img" />
              <span class="showcase-name">{{ style.name }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 背景装饰 -->
      <div class="brand-bg">
        <div class="bg-circle circle-1"></div>
        <div class="bg-circle circle-2"></div>
        <div class="bg-circle circle-3"></div>
      </div>
    </div>

    <!-- 右侧登录表单区 -->
    <div class="form-section">
      <div class="form-container">
        <!-- 切换动画 -->
        <Transition name="slide-fade" mode="out-in">
          <div :key="isRegister ? 'register' : 'login'" class="form-card">
            <!-- 表单头部 -->
            <div class="form-header">
              <h2 class="form-title">{{ isRegister ? '创建账号' : '欢迎回来' }}</h2>
              <p class="form-subtitle">
                {{ isRegister ? '开始你的艺术创作之旅' : '登录以继续使用' }}
              </p>
            </div>

            <!-- 表单内容 -->
            <form @submit.prevent="submit" class="form-body">
              <!-- 用户名（仅注册） -->
              <Transition name="field">
                <div v-if="isRegister" class="form-group">
                  <label class="form-label">用户名</label>
                  <div class="input-wrapper">
                    <input
                      v-model="username"
                      class="form-input"
                      :class="{ error: errors.username }"
                      placeholder="输入用户名"
                      @blur="validateUsername"
                      @input="errors.username = ''"
                    />
                    <span class="input-icon">👤</span>
                  </div>
                  <Transition name="error">
                    <p v-if="errors.username" class="error-msg">{{ errors.username }}</p>
                  </Transition>
                </div>
              </Transition>

              <!-- 邮箱 -->
              <div class="form-group">
                <label class="form-label">邮箱地址</label>
                <div class="input-wrapper">
                  <input
                    v-model="email"
                    class="form-input"
                    :class="{ error: errors.email }"
                    type="email"
                    placeholder="输入邮箱地址"
                    @blur="validateEmail"
                    @input="errors.email = ''"
                  />
                  <span class="input-icon">📧</span>
                </div>
                <Transition name="error">
                  <p v-if="errors.email" class="error-msg">{{ errors.email }}</p>
                </Transition>
              </div>

              <!-- 密码 -->
              <div class="form-group">
                <label class="form-label">密码</label>
                <div class="input-wrapper">
                  <input
                    v-model="password"
                    class="form-input"
                    :class="{ error: errors.password }"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="输入密码"
                    @blur="validatePassword"
                    @input="errors.password = ''"
                  />
                  <span class="input-icon" @click="showPassword = !showPassword">
                    {{ showPassword ? '👁️' : '🔒' }}
                  </span>
                </div>
                <Transition name="error">
                  <p v-if="errors.password" class="error-msg">{{ errors.password }}</p>
                </Transition>
              </div>

              <!-- 错误提示 -->
              <Transition name="error">
                <p v-if="error" class="form-error">{{ error }}</p>
              </Transition>

              <!-- 提交按钮 -->
              <button
                type="submit"
                class="btn primary lg full submit-btn"
                :disabled="loading || hasErrors"
              >
                <span v-if="loading" class="spinner"></span>
                <span v-else>{{ isRegister ? '创建账号' : '登录' }}</span>
              </button>
            </form>

            <!-- 分割线 -->
            <div class="divider text">或</div>

            <!-- 社交登录 -->
            <div class="social-login">
              <button class="btn secondary social-btn" type="button">
                <svg class="social-icon" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                <span>使用 Google 登录</span>
              </button>
              <button class="btn secondary social-btn" type="button">
                <svg class="social-icon" viewBox="0 0 24 24">
                  <path fill="#07C160" d="M8.691 2.188C3.891 2.188 0 5.476 0 9.49c0 2.372 1.523 4.435 3.789 5.616l-.637 2.289 2.672-1.312c.912.243 1.883.375 2.867.375.328 0 .652-.016.972-.047-.203-.641-.316-1.328-.316-2.031 0-3.875 3.523-7.031 7.867-7.031.328 0 .652.023.972.063-.875-3.422-4.203-5.813-8.289-5.813zm-2.031 4.125c.547 0 .992.445.992.992s-.445.992-.992.992-.992-.445-.992-.992.445-.992.992-.992zm4.062 0c.547 0 .992.445.992.992s-.445.992-.992.992-.992-.445-.992-.992.445-.992.992-.992z"/>
                  <path fill="#07C160" d="M23.992 14.188c0-3.422-3.141-6.188-7.023-6.188-3.883 0-7.023 2.766-7.023 6.188s3.141 6.188 7.023 6.188c.941 0 1.836-.156 2.664-.438l2.422 1.203-.578-2.063c1.844-1.063 3.016-2.828 3.016-4.89zm-9.023-1.125c.406 0 .734.328.734.734s-.328.734-.734.734-.734-.328-.734-.734.328-.734.734-.734zm4.023 0c.406 0 .734.328.734.734s-.328.734-.734.734-.734-.328-.734-.734.328-.734.734-.734z"/>
                </svg>
                <span>使用微信登录</span>
              </button>
            </div>

            <!-- 切换登录/注册 -->
            <div class="form-footer">
              <p class="switch-text">
                {{ isRegister ? '已有账号？' : '还没有账号？' }}
                <span class="switch-link" @click="toggleMode">
                  {{ isRegister ? '立即登录' : '立即注册' }}
                </span>
              </p>
            </div>
          </div>
        </Transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../services/auth.js'

const router = useRouter()
const auth = useAuthStore()
const isRegister = ref(false)
const username = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const showPassword = ref(false)

const errors = ref({
  username: '',
  email: '',
  password: '',
})

const features = [
  { icon: '✨', title: '智能转换', desc: 'AI 自动识别图片特征，精准应用风格' },
  { icon: '🎨', title: '多种风格', desc: '动漫、油画、素描、水彩等多种选择' },
  { icon: '⚡', title: '一键下载', desc: '转换完成后即可下载高清图片' },
]

const showcaseStyles = [
  { id: 1, name: '动漫', img: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=anime%20style%20portrait%20girl%20colorful%20vibrant&image_size=square' },
  { id: 2, name: '油画', img: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=oil%20painting%20landscape%20classical%20art&image_size=square' },
  { id: 3, name: '素描', img: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=pencil%20sketch%20portrait%20detailed&image_size=square' },
  { id: 4, name: '水彩', img: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=watercolor%20painting%20flowers%20soft&image_size=square' },
]

const hasErrors = computed(() => {
  return Object.values(errors.value).some((e) => e)
})

function validateUsername() {
  if (isRegister.value) {
    if (!username.value.trim()) {
      errors.value.username = '请输入用户名'
    } else if (username.value.length < 2) {
      errors.value.username = '用户名至少2个字符'
    } else if (username.value.length > 20) {
      errors.value.username = '用户名最多20个字符'
    } else {
      errors.value.username = ''
    }
  }
}

function validateEmail() {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!email.value.trim()) {
    errors.value.email = '请输入邮箱'
  } else if (!emailRegex.test(email.value)) {
    errors.value.email = '请输入有效的邮箱地址'
  } else {
    errors.value.email = ''
  }
}

function validatePassword() {
  if (!password.value) {
    errors.value.password = '请输入密码'
  } else if (password.value.length < 6) {
    errors.value.password = '密码至少6个字符'
  } else if (password.value.length > 32) {
    errors.value.password = '密码最多32个字符'
  } else {
    errors.value.password = ''
  }
}

function toggleMode() {
  isRegister.value = !isRegister.value
  error.value = ''
  errors.value = { username: '', email: '', password: '' }
  showPassword.value = false
}

async function submit() {
  validateUsername()
  validateEmail()
  validatePassword()

  if (hasErrors.value) return

  loading.value = true
  error.value = ''
  try {
    if (isRegister.value) {
      await auth.register(username.value, email.value, password.value)
      window.$toastSuccess?.('注册成功，欢迎加入！')
    } else {
      await auth.login(email.value, password.value)
      window.$toastSuccess?.('登录成功')
    }
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || '操作失败，请稍后重试'
    window.$toastError?.(error.value)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  min-height: 100vh;
  background: var(--color-bg);
}

/* 左侧品牌区 */
.brand-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-hero);
  padding: var(--spacing-3xl);
  position: relative;
  overflow: hidden;
}

.brand-content {
  max-width: 480px;
  color: white;
  z-index: 1;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-2xl);
}

.logo-icon {
  width: 48px;
  height: 48px;
}

.logo-text {
  font-family: var(--font-family-display);
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
}

.brand-title {
  font-family: var(--font-family-display);
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  line-height: 1.2;
  margin-bottom: var(--spacing-lg);
}

.brand-desc {
  font-size: var(--font-size-lg);
  opacity: 0.9;
  line-height: 1.6;
  margin-bottom: var(--spacing-2xl);
}

/* 特性列表 */
.features {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-2xl);
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-md);
  backdrop-filter: blur(10px);
}

.feature-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: var(--radius-md);
  font-size: 20px;
}

.feature-title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--spacing-xs);
}

.feature-desc {
  font-size: var(--font-size-sm);
  opacity: 0.8;
}

/* 示例展示 */
.showcase {
  margin-top: var(--spacing-xl);
}

.showcase-label {
  font-size: var(--font-size-sm);
  opacity: 0.7;
  margin-bottom: var(--spacing-md);
}

.showcase-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-sm);
}

.showcase-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: var(--radius-md);
  overflow: hidden;
}

.showcase-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-normal);
}

.showcase-item:hover .showcase-img {
  transform: scale(1.1);
}

.showcase-name {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: var(--spacing-sm);
  background: rgba(0, 0, 0, 0.5);
  font-size: var(--font-size-xs);
  text-align: center;
}

/* 背景装饰 */
.brand-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.bg-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 6s ease-in-out infinite;
}

.circle-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.circle-2 {
  width: 200px;
  height: 200px;
  bottom: 100px;
  left: -50px;
  animation-delay: 2s;
}

.circle-3 {
  width: 150px;
  height: 150px;
  top: 50%;
  right: 20%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-20px) scale(1.05);
  }
}

/* 右侧表单区 */
.form-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-3xl);
  background: var(--color-bg-white);
}

.form-container {
  width: 100%;
  max-width: 420px;
}

.form-card {
  background: var(--color-bg-white);
  border-radius: var(--radius-xl);
  padding: var(--spacing-2xl);
  box-shadow: var(--shadow-xl);
}

.form-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.form-title {
  font-family: var(--font-family-display);
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.form-subtitle {
  font-size: var(--font-size-md);
  color: var(--color-text-secondary);
}

.form-body {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.form-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-regular);
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.form-input {
  width: 100%;
  padding: 14px 44px 14px 16px;
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-normal);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-bg);
  color: var(--color-text-primary);
  transition: all var(--transition-fast);
  outline: none;
  z-index: 1;
}

.form-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-bg);
  background: var(--color-bg-white);
}

.form-input::placeholder {
  color: var(--color-text-placeholder);
}

.form-input.error {
  border-color: var(--color-danger);
  box-shadow: 0 0 0 3px var(--color-danger-bg);
}

.input-wrapper .input-icon {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 18px;
  cursor: pointer;
  transition: transform var(--transition-fast);
  z-index: 2;
  pointer-events: auto;
}

.input-wrapper .input-icon:hover {
  transform: translateY(-50%) scale(1.1);
}

.form-error {
  background: var(--color-danger-bg);
  color: var(--color-danger);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  text-align: center;
}

.submit-btn {
  margin-top: var(--spacing-sm);
}

/* 社交登录 */
.social-login {
  display: flex;
  gap: var(--spacing-md);
  margin-top: var(--spacing-md);
}

.social-btn {
  flex: 1;
  justify-content: flex-start;
  padding-left: var(--spacing-md);
}

.social-icon {
  width: 20px;
  height: 20px;
}

/* 表单底部 */
.form-footer {
  text-align: center;
  margin-top: var(--spacing-xl);
}

.switch-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.switch-link {
  color: var(--color-primary);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: color var(--transition-fast);
}

.switch-link:hover {
  color: var(--color-primary-light);
}

/* 过渡动画 */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s ease-in;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.field-enter-active,
.field-leave-active {
  transition: all 0.3s ease;
}

.field-enter-from,
.field-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.error-enter-active,
.error-leave-active {
  transition: all 0.2s ease;
}

.error-enter-from,
.error-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}

/* 响应式 */
@media (max-width: 1024px) {
  .auth-page {
    flex-direction: column;
  }

  .brand-section {
    padding: var(--spacing-xl);
    min-height: auto;
  }

  .brand-title {
    font-size: var(--font-size-3xl);
  }

  .features {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .feature-item {
    flex: 1;
    min-width: 200px;
  }

  .showcase-grid {
    grid-template-columns: repeat(4, 1fr);
  }

  .form-section {
    padding: var(--spacing-xl);
  }
}

@media (max-width: 768px) {
  .brand-section {
    padding: var(--spacing-lg);
  }

  .features {
    display: none;
  }

  .showcase {
    display: none;
  }

  .brand-title {
    font-size: var(--font-size-2xl);
  }

  .form-section {
    padding: var(--spacing-md);
  }

  .form-card {
    padding: var(--spacing-lg);
    border-radius: var(--radius-lg);
  }

  .social-login {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .brand-section {
    padding: var(--spacing-md);
  }

  .brand-logo {
    justify-content: center;
  }

  .brand-title {
    text-align: center;
  }

  .brand-desc {
    text-align: center;
    font-size: var(--font-size-md);
  }

  .form-card {
    padding: var(--spacing-md);
    box-shadow: none;
    border-radius: 0;
  }
}
</style>