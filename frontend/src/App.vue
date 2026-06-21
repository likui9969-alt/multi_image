<template>
  <div id="app-root" :data-theme="theme">
    <nav v-if="isLoggedIn" class="navbar">
      <div class="navbar-brand">
        <div class="logo-icon">
          <svg viewBox="0 0 32 32" fill="none">
            <defs>
              <linearGradient id="navLogoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#667eea"/>
                <stop offset="100%" style="stop-color:#764ba2"/>
              </linearGradient>
            </defs>
            <circle cx="16" cy="16" r="14" fill="url(#navLogoGradient)"/>
            <path d="M10 16 L16 10 L22 16 L16 22 Z" fill="white" opacity="0.9"/>
            <circle cx="16" cy="16" r="3" fill="white"/>
          </svg>
        </div>
        <span class="logo-text">AI Style Studio</span>
      </div>
      <div class="navbar-menu">
        <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">
          <span class="nav-icon">🎨</span>
          <span class="nav-text">创作</span>
        </router-link>
        <router-link to="/history" class="nav-link" :class="{ active: $route.path === '/history' }">
          <span class="nav-icon">📁</span>
          <span class="nav-text">历史</span>
        </router-link>
      </div>
      <div class="navbar-user">
        <button class="theme-toggle" @click="toggleTheme" :title="theme === 'dark' ? '切换到浅色模式' : '切换到深色模式'">
          <span v-if="theme === 'dark'" class="theme-icon">☀️</span>
          <span v-else class="theme-icon">🌙</span>
        </button>
        <div class="user-avatar">
          <span class="avatar-text">{{ avatarText }}</span>
        </div>
        <span class="username">{{ auth.username }}</span>
        <button class="btn ghost sm logout-btn" @click="logout">
          <span class="logout-icon">👋</span>
          <span class="logout-text">退出</span>
        </button>
      </div>
    </nav>
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <Toast ref="toastRef" />
    <ConfirmDialog ref="confirmRef" />
  </div>
</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from './services/auth.js'
import { unauthorizedEvent } from './services/api.js'
import { Toast, ConfirmDialog } from './components/index.js'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const toastRef = ref(null)
const confirmRef = ref(null)
const isLoggedIn = computed(() => auth.isLoggedIn)

// 深色模式
const theme = ref('light')

function toggleTheme() {
  theme.value = theme.value === 'dark' ? 'light' : 'dark'
  localStorage.setItem('theme', theme.value)
}

onMounted(() => {
  // 从 localStorage 读取用户偏好
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    theme.value = savedTheme
  } else {
    // 检测系统偏好
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      theme.value = 'dark'
    }
  }
})

const avatarText = computed(() => {
  const name = auth.username || 'User'
  return name.charAt(0).toUpperCase()
})

// 全局 Toast 和 Confirm 方法
window.$toast = (msg, type) => toastRef.value?.show(msg, type)
window.$toastSuccess = (msg) => toastRef.value?.success(msg)
window.$toastError = (msg) => toastRef.value?.error(msg)
window.$toastWarning = (msg) => toastRef.value?.warning(msg)
window.$confirm = (options) => confirmRef.value?.show(options)

// 监听 401 事件
watch(unauthorizedEvent, () => {
  if (unauthorizedEvent.value && route.path !== '/login') {
    auth.logout()
    toastRef.value?.warning('登录已过期，请重新登录')
    router.push('/login')
  }
})

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<style>
#app-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bg);
}

.navbar {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  padding: var(--spacing-md) var(--spacing-xl);
  background: var(--color-bg-white);
  border-bottom: 1px solid var(--color-border-light);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.logo-icon {
  width: 32px;
  height: 32px;
}

.logo-text {
  font-family: var(--font-family-display);
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.navbar-menu {
  display: flex;
  gap: var(--spacing-sm);
  margin-left: var(--spacing-xl);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
}

.nav-link:hover {
  color: var(--color-primary);
  background: var(--color-primary-bg);
}

.nav-link.active {
  color: var(--color-primary);
  background: var(--color-primary-bg);
}

.nav-icon {
  font-size: 16px;
}

.nav-text {
  font-size: var(--font-size-md);
}

.navbar-user {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.theme-toggle {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: var(--color-bg);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.theme-toggle:hover {
  background: var(--color-primary-bg);
}

.theme-icon {
  font-size: 18px;
  transition: transform var(--transition-fast);
}

.theme-toggle:hover .theme-icon {
  transform: scale(1.1);
}

.user-avatar {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-primary);
  border-radius: var(--radius-full);
  color: white;
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-md);
}

.username {
  color: var(--color-text-regular);
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-medium);
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.logout-icon {
  font-size: 14px;
}

.logout-text {
  font-size: var(--font-size-sm);
}

.main-content {
  flex: 1;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .navbar {
    padding: var(--spacing-sm) var(--spacing-md);
    gap: var(--spacing-md);
  }

  .logo-text {
    font-size: var(--font-size-md);
  }

  .navbar-menu {
    margin-left: var(--spacing-md);
    gap: var(--spacing-xs);
  }

  .nav-link {
    padding: var(--spacing-xs) var(--spacing-sm);
  }

  .nav-text {
    display: none;
  }

  .username {
    display: none;
  }

  .logout-text {
    display: none;
  }
}

@media (max-width: 480px) {
  .navbar-brand {
    gap: var(--spacing-xs);
  }

  .logo-icon {
    width: 28px;
    height: 28px;
  }

  .navbar-menu {
    margin-left: auto;
  }

  .navbar-user {
    margin-left: 0;
  }
}
</style>