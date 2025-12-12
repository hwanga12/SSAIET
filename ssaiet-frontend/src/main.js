import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()

// 🔥 pinia 먼저
app.use(pinia)

// 🔥 router 다음
app.use(router)

app.mount('#app')