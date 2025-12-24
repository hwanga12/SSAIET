<template>
  <header class="navbar">
    <div class="navbar-left">
      <div class="logo-wrapper" @click="goHome">
        <img src="@/assets/1.png" alt="SSAIET Logo" class="logo-img" />
      </div>

      <nav class="main-nav">
        <button class="nav-link" @click="scrollToMeal">
          <span class="material-icons">restaurant</span>
          <span class="nav-text">오늘 식단</span>
        </button>
        
        <button class="nav-link" @click="handleProtectedMove('/calendar')">
          <span class="material-icons">calendar_month</span>
          <span class="nav-text">영양 캘린더</span>
        </button>

          <!-- ✅ 체중 변화 예측 -->
        <button
          class="nav-link prediction-link"
          @click="handleProtectedMove('/weight-prediction')"
        >
          <span class="material-icons">insights</span>
          <span class="nav-text">체중 예측</span>
        </button>
              
        <button class="nav-link" @click="router.push('/community')">
          <span class="material-icons">forum</span>
          <span class="nav-text">커뮤니티</span>
        </button>
        
        <button class="nav-link status-link" @click="router.push('/map')">
          <span class="material-icons">map</span>
          <span class="nav-text">주변 식당</span>
        </button>

      </nav>
    </div>

    <div class="navbar-right">
      <template v-if="!authStore.isLoggedIn">
        <button class="btn ghost" @click="goLogin">로그인</button>
        <button class="btn primary" @click="goSignup">시작하기</button>
      </template>

      <template v-else>
        <div class="profile-menu">
          <button
            class="profile-btn"
            :class="{ active: menuOpen }"
            @click.stop="toggleMenu"
          >
            <span class="user-name">{{ authStore.user?.name || '사용자' }}님</span>
            <span class="material-icons chevron-icon">expand_more</span>
          </button>

          <transition name="dropdown-pop">
            <div v-if="menuOpen" class="dropdown">
              <div class="dropdown-user-info">
                <div class="info-avatar">🥗</div>
                <div class="info-text">
                  <span class="header-name">{{ authStore.user?.name }}님</span>
                </div>
              </div>

              <div class="divider"></div>

              <button class="menu-item" @click="goProfile">
                <span class="material-icons">person_outline</span>
                내 프로필
              </button>
              <button class="menu-item" @click="goSettings">
                <span class="material-icons">settings</span>
                계정 설정
              </button>

              <div class="divider"></div>

              <button class="menu-item withdraw-btn" @click="handleWithdraw">
                <span class="material-icons">person_remove</span>
                계정 탈퇴
              </button>

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

// 🔒 로그인 필요한 페이지 이동 함수 (현재 캘린더에만 적용)
const handleProtectedMove = (path) => {
  if (!authStore.isLoggedIn) {
    if (confirm("로그인 후 이용 가능한 서비스입니다.\n로그인 페이지로 이동하시겠습니까? 🔒")) {
      router.push("/login")
    }
    return
  }
  router.push(path)
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

const handleWithdraw = async () => {
  const isConfirmed = window.confirm(
    "정말로 SSAIET을 떠나시겠어요? 😢\n탈퇴 시 모든 건강 데이터와 활동 기록이 삭제되며 복구할 수 없습니다."
  )

  if (isConfirmed) {
    const finalCheck = window.confirm("마지막 확인입니다. 정말로 계정을 삭제할까요?")
    if (finalCheck) {
      try {
        await authStore.withdraw()
        alert("계정 탈퇴가 완료되었습니다. 그동안 이용해주셔서 감사합니다.")
        router.replace("/")
      } catch (err) {
        console.error("탈퇴 오류:", err)
        alert("탈퇴 처리 중 문제가 발생했습니다. 다시 시도해주세요.")
      }
    }
  }
}
</script>

<style scoped>
@import url("https://fonts.googleapis.com/icon?family=Material+Icons");

/* ================= NAVBAR BASE ================= */
.navbar {
  position: fixed;
  top: 0;
  width: 100%;
  min-width: 1280px; /* PC 레이아웃 고정 */
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

.navbar * { white-space: nowrap; }

/* ================= LEFT ================= */
.navbar-left {
  display: flex;
  align-items: center;
  gap: 36px;
  flex-shrink: 0;
}

.logo-img {
  height: 80px;
  cursor: pointer;
  flex-shrink: 0;
}

.main-nav {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
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

/* ================= RIGHT ================= */
.navbar-right {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-shrink: 0;
}

.btn {
  padding: 12px 24px;
  border-radius: 14px;
  font-size: 15px;
  font-weight: 800;
  border: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn.primary {
  background: #0f172a;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.1);
}

.btn.primary:hover {
  background: #22c55e;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(34, 197, 94, 0.25);
}

.btn.ghost {
  background: transparent;
  color: #64748b;
  border: 1.5px solid #e2e8f0;
  padding: 10.5px 22px;
}

.btn.ghost:hover {
  background: #ffffff;
  color: #0f172a;
  border-color: #0f172a;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* ================= PROFILE & DROPDOWN ================= */
.profile-menu { position: relative; }

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

.profile-btn.active { background: #f0fdf4; border-color: #22c55e; }
.chevron-icon { transition: transform 0.2s; }
.profile-btn.active .chevron-icon { transform: rotate(180deg); }

.dropdown {
  position: absolute;
  top: calc(100% + 12px);
  right: 0;
  width: 240px;
  padding: 8px;
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  z-index: 2000;
}

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

.header-name { font-size: 16px; font-weight: 800; color: #1e293b; }

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

.menu-item .material-icons { font-size: 20px; color: #94a3b8; }
.menu-item:hover { background: #f1f5f9; color: #1e293b; }
.menu-item:hover .material-icons { color: #22c55e; }

/* 탈퇴 버튼 전용 스타일 */
.withdraw-btn { color: #94a3b8; margin-top: 4px; }
.withdraw-btn:hover { color: #64748b; background: #f8fafc; }
.withdraw-btn:hover .material-icons { color: #64748b; }

.menu-item.danger { color: #ef4444; margin-top: 4px; }
.menu-item.danger:hover { background: #fef2f2; }
.menu-item.danger .material-icons { color: #ef4444; }

.divider { height: 1px; background: #f1f5f9; margin: 6px 0; }

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
/* ================= PC 고정 레이아웃 ================= */

.navbar {
  position: fixed;
  top: 0;
  width: 100%;
  min-width: 1280px;   /* 🔥 핵심 */
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

/* 줄바꿈 완전 차단 */
.navbar * {
  white-space: nowrap;
}

/* 줄어들지 않게 고정 */
.navbar-left,
.navbar-right,
.main-nav,
.logo-img {
  flex-shrink: 0;
}



</style>
