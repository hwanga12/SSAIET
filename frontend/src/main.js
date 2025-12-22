import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'   // ⭐ 추가

// ==========================
// 🔐 axios JWT 설정 (핵심)
// ==========================
axios.defaults.baseURL = 'http://127.0.0.1:8000'

axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// ==========================

const app = createApp(App)
const pinia = createPinia()

// 🔥 pinia 먼저
app.use(pinia)

// 🔥 router 다음
app.use(router)

app.mount('#app')
