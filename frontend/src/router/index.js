import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import HomeView from '../views/HomeView.vue'
import HistoryView from '../views/HistoryView.vue'
import NotFoundView from '../views/NotFoundView.vue'
import { useAuthStore } from '../services/auth.js'

const routes = [
  { path: '/login', component: LoginView },
  { path: '/', component: HomeView, meta: { requiresAuth: true } },
  { path: '/history', component: HistoryView, meta: { requiresAuth: true } },
  { path: '/:pathMatch(.*)*', component: NotFoundView },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isLoggedIn) next('/login')
  else next()
})

export default router
