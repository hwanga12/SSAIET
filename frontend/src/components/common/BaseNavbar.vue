<template>
  <header class="navbar">
    <!-- ================= LEFT ================= -->
    <div class="navbar-left">
      <div class="logo-wrapper" @click="goHome">
        <img src="@/assets/SSAIET_LOGO.png" alt="SSAIET Logo" class="logo-img" />
      </div>

      <nav class="main-nav" v-if="authStore.isLoggedIn">
        <button class="nav-link" @click="scrollToMeal">
          <span class="material-icons">restaurant</span>
          <span class="nav-text">오늘 식단</span>
        </button>
        <button class="nav-link" @click="router.push('/calendar')">
          <span class="material-icons">calendar_month</span>
          <span class="nav-text">영양 캘린더</span>
        </button>
        <button class="nav-link" @click="router.push('/community')">
          <span class="material-icons">forum</span>
          <span class="nav-text">커뮤니티</span>
        </button>
        <button class="nav-link status-link" @click="router.push('/status')">
          <span class="material-icons">groups</span>
          <span class="nav-text">식당 순서</span>
        </button>
      </nav>
    </div>

    <!-- ================= RIGHT ================= -->
    <div class="navbar-right">
      <!-- 🔹 비로그인 -->
      <template v-if="!authStore.isLoggedIn">
        <button class="btn ghost" @click="goLogin">로그인</button>
        <button class="btn primary" @click="goSignup">시작하기</button>
      </template>

      <!-- 🔹 로그인 -->
      <template v-else>
        <div class="profile-menu">
          <button
            class="profile-btn"
            :class="{ active: menuOpen }"
            @click.stop="toggleMenu"
          >
            <span class="user-avatar">🥗</span>
            <span class="user-name">{{ authStore.user?.name }}님</span>
            <span class="material-icons chevron-icon">expand_more</span>
          </button>

          <transition name="dropdown-pop">
            <div v-if="menuOpen" class="dropdown">
              <!-- 유저 정보 -->
              <div class="dropdown-user-info">
                <div class="info-avatar">🥗</div>
                <div class="info-text">
                  <span class="header-name">{{ authStore.user?.name }}님</span>
                </div>
              </div>

              <div class="divider"></div>

              <!-- 메뉴 -->
              <button class="menu-item" @click="goProfile">
                <span class="material-icons">person_outline</span>
                내 건강 정보
              </button>
              <button class="menu-item" @click="goSettings">
                <span class="material-icons">settings</span>
                계정 설정
              </button>

              <div class="divider"></div>

              <button class="menu-item danger" @click="logout">
                <span class="material-icons">logout</span>
                로그아웃
              </button>
            </div>
          </transition>
        </div>
      </template>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const menuOpen = ref(false)

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const closeMenu = () => {
  menuOpen.value = false
}

onMounted(() => window.addEventListener("click", closeMenu))
onUnmounted(() => window.removeEventListener("click", closeMenu))

const scrollToMeal = () => {
  if (route.path === "/") {
    document.getElementById("today-meal-section")?.scrollIntoView({ behavior: "smooth" })
  } else {
    router.push({ path: "/", hash: "#today-meal-section" })
  }
}

const goHome = () => router.push("/")
const goProfile = () => { closeMenu(); router.push("/profile") }
const goSettings = () => { closeMenu(); router.push("/account/edit") }
const goLogin = () => router.push("/login")
const goSignup = () => router.push("/signup")

const logout = () => {
  authStore.logOut()
  router.replace("/")
}
</script>

<style scoped>
@import url("https://fonts.googleapis.com/icon?family=Material+Icons");

/* ================= NAVBAR ================= */
.navbar {
  position: fixed;
  top: 0;
  width: 100%;
  height: 76px;
  padding: 0 40px;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 1000;
  box-sizing: border-box;
}

/* ================= LEFT ================= */
.navbar-left {
  display: flex;
  align-items: center;
  gap: 36px;
}

.logo-img {
  height: 40px;
  cursor: pointer;
}

.main-nav {
  display: flex;
  gap: 8px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 12px;
  border: none;
  background: none;
  font-weight: 800;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.nav-link:hover {
  background: #f0fdf4;
  color: #22c55e;
}

/* ================= RIGHT (버튼 스타일 수정) ================= */
.navbar-right {
  display: flex;
  align-items: center;
  gap: 14px; /* 버튼 간격 소폭 확대 */
}

/* 공통 버튼 베이스 */
.btn {
  padding: 12px 24px;
  border-radius: 14px; /* 다른 카드들과 곡률 통일 */
  font-size: 15px;
  font-weight: 800; /* 더 굵고 까리하게 */
  border: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 🔹 시작하기 (Primary) : 딥 블랙 -> 그린 변신 */
.btn.primary {
  background: #0f172a; /* SSAIET 딥 블랙 */
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.1);
}

.btn.primary:hover {
  background: #22c55e; /* 호버 시 SSAIET 그린 */
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(34, 197, 94, 0.25);
}

.btn.primary:active {
  transform: translateY(0);
}

/* 🔹 로그인 (Ghost) : 깔끔하고 선명한 스타일 */
.btn.ghost {
  background: transparent;
  color: #64748b;
  border: 1.5px solid #e2e8f0;
  padding: 10.5px 22px; /* 보더 두께만큼 패딩 미세 조정 */
}

.btn.ghost:hover {
  background: #ffffff;
  color: #0f172a;
  border-color: #0f172a; /* 딥 블랙 보더로 포인트 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
/* ================= PROFILE ================= */
.profile-menu {
  position: relative;
}

.profile-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 18px;
  border-radius: 999px;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  cursor: pointer;
  transition: 0.2s;
}

.profile-btn.active {
  background: #f0fdf4;
  border-color: #22c55e;
}

.chevron-icon {
  transition: transform 0.2s;
}

.profile-btn.active .chevron-icon {
  transform: rotate(180deg);
}

/* ================= DROPDOWN ================= */
/* ================= DROPDOWN ================= */
.dropdown {
  position: absolute;
  top: calc(100% + 12px);
  right: 0;
  width: 240px; /* 너비 살짝 조정 */
  padding: 8px; /* 패딩 최적화 */
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  z-index: 2000;
}

/* 유저 정보 영역 스타일링 */
.dropdown-user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 8px;
  margin-bottom: 4px;
}

.info-avatar {
  font-size: 24px;
  background: #f0fdf4;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.info-text {
  display: flex;
  flex-direction: column;
}

.header-name {
  font-size: 16px;
  font-weight: 800;
  color: #1e293b;
}

/* 메뉴 아이템 스타일 보완 */
.menu-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  border: none;
  background: none;
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
}

.menu-item .material-icons {
  font-size: 20px;
  color: #94a3b8;
}

.menu-item:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.menu-item:hover .material-icons {
  color: #22c55e;
}

.menu-item.danger {
  color: #ef4444;
  margin-top: 4px;
}

.menu-item.danger:hover {
  background: #fef2f2;
}

.menu-item.danger .material-icons {
  color: #ef4444;
}

.divider {
  height: 1px;
  background: #f1f5f9;
  margin: 6px 0;
}

/* 애니메이션 */
.dropdown-pop-enter-active,
.dropdown-pop-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.dropdown-pop-enter-from,
.dropdown-pop-leave-to {
  opacity: 0;
  transform: translateY(-8px) scale(0.95);
}

/* 메뉴 */
.menu-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 10px;
  border: none;
  background: none;
  cursor: pointer;
}

.menu-item:hover {
  background: #f8fafc;
}

.menu-item.danger {
  color: #ef4444;
}

.divider {
  height: 1px;
  background: #e5e7eb;
  margin: 8px 0;
}
</style>
