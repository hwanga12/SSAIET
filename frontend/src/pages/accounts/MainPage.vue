<template>
  <div class="main-layout">
    <BaseNavbar class="fixed-navbar" />

    <main class="main-content">
      <HeroSection
        :userName="authStore.isLoggedIn ? authStore.user?.name : '싸피생'"
        :imageSrc="heroImage"
        :isLoggedIn="authStore.isLoggedIn"
        @goLogin="router.push('/login')"
        @goSignup="router.push('/signup')"
        @goRecommend="scrollToMeal"
      />

      <Transition name="section-fade">
        <div id="today-meal-section" class="meal-wrapper">
          <div class="premium-divider">
            <div class="line"></div>
            <div class="divider-content">
              <span class="top-tag">DAILY MENU</span>
              <h2 class="divider-title">오늘의 영양 큐레이션</h2>
              <div class="leaf-icon">
                <span class="material-icons">eco</span>
              </div>
            </div>
            <div class="line"></div>
          </div>

          <div class="section-inner">
            <MealSection />
          </div>
        </div>
      </Transition>
    </main>
  </div>
</template>

<script setup>
/* 로직 100% 동일 */
import { onMounted } from "vue"
import { useAuthStore } from "@/stores/auth"
import { useRouter, useRoute } from "vue-router"

import BaseNavbar from "@/components/common/BaseNavbar.vue"
import HeroSection from "@/components/common/HeroSection.vue"
import MealSection from "@/components/meal/MealSection.vue"
import heroImage from "@/assets/ssafy_study.png"

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const formatDateLocal = (date) => {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, "0")
  const d = String(date.getDate()).padStart(2, "0")
  return `${y}-${m}-${d}`
}

onMounted(() => {
  if (!route.query.date) {
    const todayStr = formatDateLocal(new Date())
    router.replace({ query: { ...route.query, date: todayStr } })
  }
})

const scrollToMeal = () => {
  const element = document.getElementById('today-meal-section');
  if (element) {
    // 🛠 네비바 높이를 고려하여 스크롤 오프셋을 120으로 조정 (안 가려지게)
    const offset = 120; 
    const elementPosition = element.getBoundingClientRect().top + window.pageYOffset;
    window.scrollTo({
      top: elementPosition - offset,
      behavior: 'smooth'
    });
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.main-layout {
  min-height: 100vh;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  color: #1a1a1a;
}

/* 🛠 Navbar 고정 설정 */
.fixed-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #f2f2f2;
}

/* 🛠 중요: 고정된 네비바의 높이(약 70px~80px)만큼 컨텐츠를 아래로 밀어줌 */
.main-content { 
  flex: 1; 
  padding-top: 80px; 
}

.meal-wrapper {
  padding: 80px 0 120px;
  background-color: #f8fafc;
}

.section-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.premium-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 60px;
  padding: 0 40px;
}

.line {
  flex: 1;
  height: 2px;
  background: linear-gradient(to right, #164e33, #22c55e, #164e33);
}

.divider-content {
  text-align: center;
  padding: 0 40px;
}

.top-tag {
  display: block;
  font-size: 0.85rem;
  font-weight: 800;
  color: #22c55e;
  letter-spacing: 4px;
  margin-bottom: 8px;
}

.divider-title {
  font-size: 2.2rem;
  font-weight: 900;
  color: #0f172a;
  margin: 0;
  letter-spacing: -1px;
}

.leaf-icon {
  margin-top: 15px;
  color: #22c55e;
}

.section-fade-enter-active {
  transition: all 1.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.section-fade-enter-from {
  opacity: 0;
  transform: translateY(50px);
}
</style>