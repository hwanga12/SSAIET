<template>
  <div>
    <!-- 🔥 Navbar (항상 보임) -->
    <BaseNavbar />

    <!-- 🔥 로그인한 사용자 -->
    <HeroSection
      
      :userName="authStore.user?.name || '사용자'"
      :imageSrc="heroImage"
    />

    <!-- 🔥 비로그인 사용자 -->
    <!-- <section v-else class="guest-section">
      <p class="guest-text">
        로그인하면 개인 맞춤 기능을 사용할 수 있어요!
      </p>

      <div class="guest-buttons">
        <button @click="router.push('/login')">로그인</button>
        <button @click="router.push('/signup')">회원가입</button>
      </div>
    </section> -->
  </div>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth"
import { useRouter } from "vue-router"

import BaseNavbar from "@/components/common/BaseNavbar.vue"
import HeroSection from "@/components/common/HeroSection.vue"

// 🔹 이미지 import (중요)
import heroImage from "@/assets/ssafy_study.png"

const authStore = useAuthStore()
const router = useRouter()
</script>

<style scoped>
/* 비로그인 사용자 영역 */
.guest-section {
  min-height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: #f9fbfd;
}

.guest-text {
  font-size: 18px;
  margin-bottom: 24px;
  color: #374151;
}

.guest-buttons {
  display: flex;
  gap: 12px;
}

.guest-buttons button {
  padding: 10px 20px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: 600;
}

.guest-buttons button:first-child {
  background: #2563eb;
  color: white;
}

.guest-buttons button:last-child {
  background: #e5e7eb;
}
</style>