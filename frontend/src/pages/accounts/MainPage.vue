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

    <footer class="main-footer">
      <div class="footer-inner">
        <div class="footer-top">
          <img src="@/assets/1.png" alt="SSAIET" class="footer-logo" />
          <nav class="footer-nav">
            <a href="#">ABOUT</a>
            <a href="#">TERMS</a>
            <a href="#">PRIVACY</a>
            <a href="#">CONTACT</a>
          </nav>
        </div>
        <div class="footer-bottom">
          <p class="copyright">&copy; 2025 SSAIET. Dedicated to SSAFY Excellence.</p>
          <div class="social-icons">
            <span class="material-icons">share</span>
            <span class="material-icons">language</span>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
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

/* 레이아웃 기본: 프리미엄 화이트 */
.main-layout {
  min-height: 100vh;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  color: #1a1a1a;
}

.fixed-navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #f2f2f2;
}

.main-content { flex: 1; }

/* 식단 섹션 스타일 */
.meal-wrapper {
  padding: 80px 0 120px;
  background-color: #fcfcfc; /* 미세한 화이트 대비 */
}

.section-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 프리미엄 구분선 디자인 */
.premium-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 60px;
  padding: 0 40px;
}

.line {
  flex: 1;
  height: 1px;
  background: #e5e5e5;
}

.divider-content {
  text-align: center;
  padding: 0 40px;
  position: relative;
}

.top-tag {
  display: block;
  font-size: 0.75rem;
  font-weight: 800;
  color: #164e33; /* 프리미엄 그린 */
  letter-spacing: 4px;
  margin-bottom: 8px;
}

.divider-title {
  font-size: 1.85rem;
  font-weight: 900;
  color: #000;
  margin: 0;
  letter-spacing: -0.5px;
}

.leaf-icon {
  margin-top: 15px;
  color: #164e33;
}

.leaf-icon .material-icons { font-size: 24px; opacity: 0.8; }

/* 푸터 디자인: 프리미엄 화이트 & 그레이 */
.main-footer {
  padding: 100px 0 60px;
  background: #ffffff;
  border-top: 1px solid #f0f0f0;
}

.footer-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 60px;
}

.footer-logo {
  height: 32px;
  filter: contrast(0.1); /* 로고 무채색화 */
  opacity: 0.6;
}

.footer-nav {
  display: flex;
  gap: 30px;
}

.footer-nav a {
  text-decoration: none;
  color: #888;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 1px;
  transition: color 0.3s;
}

.footer-nav a:hover { color: #164e33; }

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 40px;
  border-top: 1px solid #f7f7f7;
}

.copyright {
  color: #b0b0b0;
  font-size: 0.8rem;
  font-weight: 500;
}

.social-icons {
  display: flex;
  gap: 20px;
  color: #d0d0d0;
}

.social-icons .material-icons {
  font-size: 20px;
  cursor: pointer;
}

/* 애니메이션 */
.section-fade-enter-active {
  transition: all 1.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.section-fade-enter-from {
  opacity: 0;
  transform: translateY(50px);
}

@media (max-width: 768px) {
  .footer-top { flex-direction: column; gap: 40px; }
  .divider-title { font-size: 1.4rem; }
  .footer-nav { gap: 15px; }
}
</style>