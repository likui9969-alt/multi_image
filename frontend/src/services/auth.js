import { defineStore } from 'pinia'
import api from './api.js'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userId: Number(localStorage.getItem('userId')) || 0,
    username: localStorage.getItem('username') || '',
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    async login(email, password) {
      const { data } = await api.post('/auth/login', { email, password })
      this._saveAuth(data)
    },
    async register(username, email, password) {
      const { data } = await api.post('/auth/register', { username, email, password })
      this._saveAuth(data)
    },
    _saveAuth(data) {
      this.token = data.access_token
      this.userId = data.user_id
      this.username = data.username
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('userId', data.user_id)
      localStorage.setItem('username', data.username)
    },
    logout() {
      this.token = ''
      this.userId = 0
      this.username = ''
      localStorage.removeItem('token')
      localStorage.removeItem('userId')
      localStorage.removeItem('username')
    },
  },
})
