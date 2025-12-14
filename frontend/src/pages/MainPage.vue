<template>
  <div>
    <h1>메인 페이지</h1>

    <!-- 🔥 로그인한 사용자 UI -->
    <div v-if="authStore.isLoggedIn">
      <p>{{ authStore.user?.name }}님 환영합니다!</p>

      <!-- 🔥 내 프로필 보기 버튼 -->
      <button @click="$router.push('/profile')">
        내 프로필 보기
      </button>

      <!-- 로그아웃 버튼 -->
      <button @click="logout">로그아웃</button>
    </div>

    <!-- 🔥 비로그인 사용자 UI -->
    <div v-else>
      <p>로그인하면 개인 맞춤 기능을 사용할 수 있어요!</p>

      <button @click="$router.push('/login')">로그인</button>
      <button @click="$router.push('/signup')">회원가입</button>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth"
import { useRouter } from "vue-router"

const authStore = useAuthStore()
const router = useRouter()

// 로그아웃 기능
const logout = () => {
  authStore.logOut()
  router.push("/")   // 로그아웃 후 메인으로 이동
}
</script>