<template>
  <Teleport to="body">
    <div class="toast-container">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="['toast', toast.type]"
        >
          <span class="toast-icon">{{ iconMap[toast.type] }}</span>
          <span class="toast-message">{{ toast.message }}</span>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'

const toasts = ref([])
let toastId = 0

const iconMap = {
  success: '✓',
  error: '✕',
  warning: '!',
  info: 'i',
}

function show(message, type = 'info', duration = 3000) {
  const id = ++toastId
  toasts.value.push({ id, message, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }, duration)
}

function success(message, duration) {
  show(message, 'success', duration)
}

function error(message, duration) {
  show(message, 'error', duration)
}

function warning(message, duration) {
  show(message, 'warning', duration)
}

function info(message, duration) {
  show(message, 'info', duration)
}

defineExpose({ show, success, error, warning, info })
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 8px;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: var(--radius-md);
  background: var(--color-bg-white);
  box-shadow: var(--shadow-md);
  pointer-events: auto;
  min-width: 200px;
  max-width: 400px;
}

.toast-icon {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  flex-shrink: 0;
}

.toast-message {
  font-size: var(--font-size-md);
  color: var(--color-text-primary);
}

.toast.success .toast-icon {
  background: var(--color-success-bg);
  color: var(--color-success);
}

.toast.error .toast-icon {
  background: var(--color-danger-bg);
  color: var(--color-danger);
}

.toast.warning .toast-icon {
  background: var(--color-warning-bg);
  color: var(--color-warning);
}

.toast.info .toast-icon {
  background: var(--color-primary-bg);
  color: var(--color-primary);
}

/* 过渡动画 */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>