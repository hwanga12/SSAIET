<template>
  <header class="navbar">
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
          <div class="status-dot"></div>
          <span class="material-icons">groups</span>
          <span class="nav-text">식당 순서</span>
        </button>
      </nav>
    </div>

<<<<<<< HEAD
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
=======
    <div class="navbar-right">
      <template v-if="!authStore.isLoggedIn">
        <button class="btn ghost" @click="goLogin">로그인</button>
        <button class="btn primary" @click="goSignup">시작하기</button>
      </template>

      <template v-else>
        <div class="profile-menu">
          <button class="profile-btn" @click="toggleMenu" :class="{ active: menuOpen }">
            <span class="user-avatar">🥗</span>
            <span class="user-name">{{ authStore.user?.name }}님</span>
            <span class="material-icons chevron-icon">expand_more</span>
          </button>

          <transition name="dropdown-pop">
            <div v-if="menuOpen" class="dropdown" @click.stop>
              <div class="dropdown-user-info">
                <div class="info-avatar">🥗</div>
                <div class="info-text">
                  <span class="header-name">{{ authStore.user?.name }}님</span>
                  <span class="header-email">{{ authStore.user?.email }}</span>
                </div>
              </div>
              
              <div class="divider"></div>
              
              <div class="menu-list">
                <button class="menu-item" @click="goProfile">
                  <span class="material-icons menu-icon">person_outline</span>
                  <span class="menu-text">내 건강 정보</span>
                </button>
                <button class="menu-item" @click="goSettings">
                  <span class="material-icons menu-icon">settings</span>
                  <span class="menu-text">계정 설정</span>
                </button>
              </div>
              
              <div class="divider"></div>
              
              <div class="menu-list">
                <button class="menu-item danger" @click="logout">
                  <span class="material-icons menu-icon">logout</span>
                  <span class="menu-text">로그아웃</span>
                </button>
                <button class="menu-item withdraw" @click="withdraw">회원탈퇴</button>
              </div>
            </div>
          </transition>
        </div>
      </template>
    </div>
>>>>>>> FE_Mainpage_Herosection&Navbar
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

const scrollToMeal = () => {
  if (route.path === '/') {
    const mealSection = document.getElementById('today-meal-section');
    if (mealSection) mealSection.scrollIntoView({ behavior: 'smooth' });
  } else {
    router.push({ path: '/', hash: '#today-meal-section' });
  }
}

const toggleMenu = (e) => {
  e.stopPropagation()
  menuOpen.value = !menuOpen.value
}

const closeMenu = () => { menuOpen.value = false }
onMounted(() => window.addEventListener('click', closeMenu))
onUnmounted(() => window.removeEventListener('click', closeMenu))

const goHome = () => router.push("/")
const goProfile = () => { closeMenu(); router.push("/profile"); }
const goSettings = () => { closeMenu(); router.push("/account/edit"); }
const goLogin = () => router.push("/login")
const goSignup = () => router.push("/signup")

const logout = () => {
  authStore.logOut()
  router.replace("/")
}

<<<<<<< HEAD
const goLogin = () => {
  router.push("/login")
}

const goSignup = () => {
  router.push("/signup")
}

=======
const withdraw = async () => {
  if (!confirm("정말 회원탈퇴 하시겠습니까?")) return
  await authStore.withdraw()
  alert("그동안 이용해주셔서 감사합니다. 🌱")
  router.replace("/")
}
>>>>>>> FE_Mainpage_Herosection&Navbar
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
  height: 76px;
  padding: 0 40px;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-left { display: flex; align-items: center; gap: 35px; }
.logo-img { height: 46px; cursor: pointer; }
.main-nav { display: flex; gap: 8px; }

/* 네브바 링크 가독성 유지 */
.nav-link {
  background: none; border: none; padding: 10px 16px;
  font-size: 15px; font-weight: 800; color: #64748b;
  cursor: pointer; border-radius: 12px;
  display: flex; align-items: center; gap: 8px;
  white-space: nowrap; /* 글자 줄바꿈 방지 */
}

.nav-link:hover { color: #22c55e; background: #f0fdf4; }
.nav-link .material-icons { font-size: 20px; color: #94a3b8; }
.nav-link:hover .material-icons { color: #22c55e; }

/* 프로필 버튼 */
.profile-menu { position: relative; }
.profile-btn {
  display: flex; align-items: center; gap: 10px;
  background: #f8fafc; border: 1.5px solid #e2e8f0;
  padding: 8px 18px; border-radius: 999px;
  cursor: pointer; transition: all 0.2s;
  white-space: nowrap;
}

.profile-btn.active, .profile-btn:hover { border-color: #22c55e; background: #fff; }
.user-name { font-size: 14px; font-weight: 800; color: #0f172a; }
.chevron-icon { font-size: 18px; color: #94a3b8; transition: transform 0.3s; }
.profile-btn.active .chevron-icon { transform: rotate(180deg); color: #22c55e; }

/* 🚀 드롭다운: 절대 깨지지 않는 구조 */
.dropdown {
  position: absolute;
  top: calc(100% + 12px);
  right: 0;
  width: 260px; /* 너비 고정 */
  background: #ffffff;
  border-radius: 24px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(0, 0, 0, 0.05);
  padding: 16px;
  z-index: 1100;
  transform-origin: top right;
}

/* 드롭다운 상단 정보부 */
.dropdown-user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 4px;
}

.info-avatar {
  width: 44px; height: 44px;
  background: #f0fdf4; border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px; flex-shrink: 0;
}

.info-text {
  display: flex; flex-direction: column;
  overflow: hidden; /* 텍스트 넘침 제어 */
}

.header-name {
  font-size: 16px; font-weight: 900; color: #0f172a;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

.header-email {
  font-size: 12px; color: #94a3b8; font-weight: 500;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

/* 드롭다운 메뉴 아이템 */
.menu-list { display: flex; flex-direction: column; gap: 4px; }

.menu-item {
  width: 100%; padding: 12px;
  display: flex; align-items: center; gap: 12px;
  border: none; background: none; border-radius: 12px;
  font-size: 14px; font-weight: 700; color: #475569;
  cursor: pointer; transition: 0.2s;
  white-space: nowrap;
}

.menu-item:hover { background: #f0fdf4; color: #22c55e; }
.menu-icon { font-size: 20px; color: #94a3b8; flex-shrink: 0; }
.menu-item:hover .menu-icon { color: #22c55e; }

.menu-item.danger { color: #ef4444; }
.menu-item.danger:hover { background: #fef2f2; }
.menu-item.danger .menu-icon { color: #fca5a5; }

.menu-item.withdraw {
  font-size: 11px; color: #cbd5e1; text-decoration: underline;
  justify-content: center; margin-top: 8px;
}

.divider { height: 1px; background: #f1f5f9; margin: 12px 0; }

/* 팝 애니메이션 */
.dropdown-pop-enter-active { transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.dropdown-pop-leave-active { transition: all 0.2s ease; }
.dropdown-pop-enter-from { opacity: 0; transform: translateY(10px) scale(0.9); }
.dropdown-pop-leave-to { opacity: 0; transform: translateY(5px) scale(0.95); }

/* 모바일 대응 제외 (기존 미디어쿼리 삭제 및 단순화) */
@media (max-width: 950px) {
  .nav-text { display: none; } /* 글자만 숨김 */
  .navbar-left { gap: 15px; }
}
</style>