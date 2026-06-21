<template>
  <div class="not-found-page">
    <div class="not-found-content">
      <div class="error-illustration">
        <svg viewBox="0 0 400 300" fill="none">
          <!-- 背景 -->
          <rect x="50" y="50" width="300" height="200" rx="20" fill="var(--color-bg-white)" stroke="var(--color-border)" stroke-width="2"/>
          
          <!-- 404 文字 -->
          <text x="200" y="130" text-anchor="middle" font-family="var(--font-family-display)" font-size="60" font-weight="700" fill="var(--color-primary)">404</text>
          
          <!-- 问号装饰 -->
          <circle cx="100" cy="80" r="15" fill="var(--color-primary-bg)" opacity="0.5"/>
          <text x="100" y="85" text-anchor="middle" font-size="20" fill="var(--color-primary)">?</text>
          
          <circle cx="300" cy="80" r="15" fill="var(--color-primary-bg)" opacity="0.5"/>
          <text x="300" y="85" text-anchor="middle" font-size="20" fill="var(--color-primary)">?</text>
          
          <!-- 迷路的小人 -->
          <circle cx="200" cy="200" r="20" fill="var(--color-secondary)"/>
          <ellipse cx="200" cy="230" rx="15" ry="25" fill="var(--color-secondary)"/>
          <!-- 眼睛 -->
          <circle cx="195" cy="195" r="3" fill="white"/>
          <circle cx="205" cy="195" r="3" fill="white"/>
          <!-- 问号表情 -->
          <text x="200" y="210" text-anchor="middle" font-size="12" fill="white">?</text>
          
          <!-- 路径线 -->
          <path d="M80 250 Q120 230 160 250 Q200 270 240 250 Q280 230 320 250" stroke="var(--color-border)" stroke-width="3" stroke-linecap="round" fill="none" opacity="0.5"/>
        </svg>
      </div>
      
      <h1 class="error-title">页面未找到</h1>
      <p class="error-desc">抱歉，您访问的页面不存在或已被移除</p>
      
      <div class="error-actions">
        <router-link to="/" class="btn primary lg">
          <span class="btn-icon">🏠</span>
          返回首页
        </router-link>
        <router-link to="/history" class="btn secondary lg">
          <span class="btn-icon">📁</span>
          查看历史
        </router-link>
      </div>
      
      <div class="error-suggestions">
        <h3 class="suggestions-title">您可以尝试：</h3>
        <ul class="suggestions-list">
          <li>检查网址是否正确</li>
          <li>返回首页重新开始</li>
          <li>查看历史记录中的作品</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  background: var(--color-bg);
}

.not-found-content {
  text-align: center;
  max-width: 500px;
}

.error-illustration {
  width: 100%;
  max-width: 400px;
  margin: 0 auto var(--spacing-xl);
}

.error-title {
  font-family: var(--font-family-display);
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.error-desc {
  font-size: var(--font-size-md);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-xl);
}

.error-actions {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.btn-icon {
  font-size: 18px;
}

.error-suggestions {
  padding: var(--spacing-lg);
  background: var(--color-bg-white);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
}

.suggestions-title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}

.suggestions-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.suggestions-list li {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  padding: var(--spacing-xs) 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.suggestions-list li::before {
  content: '•';
  color: var(--color-primary);
  font-weight: bold;
}

@media (max-width: 480px) {
  .not-found-page {
    padding: var(--spacing-md);
  }

  .error-title {
    font-size: var(--font-size-xl);
  }

  .error-actions {
    flex-direction: column;
  }

  .error-actions .btn {
    width: 100%;
  }
}
</style>