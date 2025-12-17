<template>
  <header class="navbar">
    <!-- 🔥 왼쪽: 로고 (항상 보임) -->
    <div class="navbar-left" @click="goHome">
      <img
        src="@/assets/SSAIET_LOGO.png"
        alt="SSAIET Logo"
        class="logo-img"
      />
    </div>

    <!-- 🔥 로그인한 사용자 -->
    <nav class="navbar-right" v-if="authStore.isLoggedIn">
      <button @click="goProfile">내 프로필</button>
      <button @click="goSettings">계정 설정</button>
      <button class="logout" @click="logout">로그아웃</button>
    </nav>

    <!-- 🔥 비로그인 사용자 -->
    <nav class="navbar-right" v-else>
      <button @click="goLogin">로그인</button>
      <button @click="goSignup">회원가입</button>
    </nav>
  </header>
</template>


<script setup>
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const router = useRouter()
const authStore = useAuthStore()

/* 로고 클릭 → 무조건 메인 */
const goHome = () => {
  if (router.currentRoute.value.path !== "/") {
    router.push("/")
  }
}

const goProfile = () => {
  router.push("/profile")
}

const goSettings = () => {
  router.push("/settings")
}

const logout = () => {
  authStore.logOut()
  router.replace("/")
}

const goLogin = () => {
  router.push("/login")
}

const goSignup = () => {
  router.push("/signup")
}

</script>

<style scoped>
/* 🔥 Navbar 전체 */

/* 왼쪽 로고 영역 */
.navbar-left {
  display: flex;
  align-items: center;
  cursor: pointer;
}

/* 🔥 로고 이미지 크게 */
.logo-img {
  height: 48px;
  margin-bottom: 6px;   /* ⬅️ 로고 아래 공간 */
}

/* 🔥 Navbar 전체 */
.navbar {
  height: 50px;                 /* 여기서 최종 높이 결정 */
  padding: 0 24px 10px;
  background-color: #ffffff;
  border-bottom: 1px solid #e5e7eb;

  display: flex;
  align-items: center;
  justify-content: space-between;

  font-family:
    -apple-system,
    BlinkMacSystemFont,
    "Inter",
    "Pretendard",
    "Apple SD Gothic Neo",
    sans-serif;
}

.navbar-right button {
  background: none;
  border: none;
  font-size: 18px;
  font-weight: 500;
  letter-spacing: -0.01em;
  color: #374151;
  cursor: pointer;
  padding: 6px 8px;
  border-radius: 6px;
  transition: color 0.2s ease, background-color 0.2s ease;
}

.navbar-right button:hover {
  background-color: #f3f4f6;
  color: #111827;
}

.logout {
  color: #dc2626;
  font-weight: 600;
}

.logout:hover {
  background-color: #fee2e2;
}

</style>