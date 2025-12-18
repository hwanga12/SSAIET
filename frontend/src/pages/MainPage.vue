<template>
<<<<<<< HEAD
  <div>
    <!-- 🔥 Navbar (항상 보임) -->
    <BaseNavbar />
    
    <!-- 🔥 로그인한 사용자 -->
    <HeroSection
      
      :userName="authStore.user?.name || '사용자'"
      :imageSrc="heroImage"
    />
    <MealSection />
    

    <!-- 🔥 비로그인 사용자 -->
    <!-- <section v-else class="guest-section">
      <p class="guest-text">
        로그인하면 개인 맞춤 기능을 사용할 수 있어요!
      </p>
=======
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
        <div v-if="authStore.isLoggedIn" id="today-meal-section" class="meal-wrapper">
          <div class="section-divider">
            <span class="divider-text">Today's Nutrition</span>
          </div>
          <MealSection />
        </div>
      </Transition>
>>>>>>> FE_Mainpage_Herosection&Navbar

      <Transition name="section-fade">
        <section v-if="!authStore.isLoggedIn" class="preview-section">
          <div class="preview-banner">
            <div class="banner-icon">🌱</div>
            <h2>지금 바로 시작해서 <br/>건강한 <span class="highlight">SSAFY</span> 생활을 만드세요!</h2>
            <p>식단 기록부터 식단 추천까지 SSAIET이 도와드립니다.</p>
            <button class="banner-btn" @click="router.push('/signup')">3초만에 시작하기</button>
          </div>
        </section>
      </Transition>
    </main>

    <footer class="main-footer">
      <div class="footer-content">
        <img src="@/assets/SSAIET_LOGO.png" alt="SSAIET" class="footer-logo" />
        <p>&copy; 2025 SSAIET. All rights reserved for SSAFY Students.</p>
      </div>
<<<<<<< HEAD
    </section> -->
=======
    </footer>
>>>>>>> FE_Mainpage_Herosection&Navbar
  </div>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth"
import { useRouter } from "vue-router"

import BaseNavbar from "@/components/common/BaseNavbar.vue"
import HeroSection from "@/components/common/HeroSection.vue"
import MealSection from "@/components/meal/MealSection.vue"

import heroImage from "@/assets/ssafy_study.png"

import MealSection from "@/components/meal/MealSection.vue"

const authStore = useAuthStore()
const router = useRouter()

// 추천 식단 클릭 시 식단 섹션으로 부드럽게 스크롤
const scrollToMeal = () => {
  const element = document.getElementById('today-meal-section');
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
}
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  background-color: #fcfdfd; /* 프리미엄 화이트 톤으로 변경 */
  display: flex;
  flex-direction: column;
}

.fixed-navbar {
  position: sticky;
  top: 0;
  z-index: 100;
}

.main-content {
  flex: 1;
}

/* ===== 🍱 식단 섹션 스크롤 위치 보정 ===== */
.meal-wrapper {
  scroll-margin-top: 90px; /* 네브바 높이만큼 여백을 주어 제목이 가려지지 않게 함 */
  padding-bottom: 60px;
}

/* ===== 섹션 구분선 디자인 (SSAIET 그린 포인트) ===== */
.section-divider {
  max-width: 1200px;
  margin: 80px auto 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.section-divider::before {
  content: "";
  position: absolute;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
}

.divider-text {
  background: #fcfdfd;
  padding: 0 24px;
  color: #22c55e; /* 그린으로 포인트 */
  font-size: 0.85rem;
  font-weight: 800;
  letter-spacing: 3px;
  text-transform: uppercase;
  position: relative;
  z-index: 1;
}

/* ===== 비로그인 안내 배너 (디자인 고도화) ===== */
.preview-section {
  padding: 100px 20px;
  text-align: center;
}

.preview-banner {
  max-width: 700px;
  margin: 0 auto;
  padding: 60px 40px;
  background: white;
  border-radius: 40px;
  border: 1px solid #f1f5f9;
  box-shadow: 0 30px 60px rgba(0,0,0,0.05);
}

.banner-icon { font-size: 40px; margin-bottom: 20px; }

.preview-banner h2 {
  font-size: 2rem;
  font-weight: 900;
  color: #0f172a;
  line-height: 1.3;
  margin-bottom: 16px;
}

.highlight { color: #22c55e; }

.preview-banner p {
  color: #64748b;
  font-size: 1.1rem;
  margin-bottom: 32px;
}

.banner-btn {
  background: #0f172a;
  color: white;
  padding: 16px 36px;
  border-radius: 16px;
  font-weight: 800;
  border: none;
  cursor: pointer;
  transition: 0.3s;
}

.banner-btn:hover {
  background: #22c55e;
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(34, 197, 94, 0.2);
}

/* ===== 애니메이션 ===== */
.section-fade-enter-active,
.section-fade-leave-active {
  transition: all 0.8s cubic-bezier(0.22, 1, 0.36, 1);
}

.section-fade-enter-from {
  opacity: 0;
  transform: translateY(40px);
}

/* ===== 푸터 ===== */
.main-footer {
  padding: 60px 40px;
  text-align: center;
  background: #f8fafc;
  border-top: 1px solid #f1f5f9;
}

.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.footer-logo {
  height: 36px;
  opacity: 0.6;
  filter: grayscale(1);
}

.main-footer p {
  color: #94a3b8;
  font-size: 0.85rem;
  font-weight: 500;
}
</style>