import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import SignUpPage from "@/pages/accounts/SignUpPage.vue"
import ProfileSetupPage from "@/pages/accounts/ProfileSetupPage.vue"
import MainPage from "@/pages/accounts/MainPage.vue"
import LoginPage from "@/pages/accounts/LoginPage.vue"
import NotFoundView from "@/pages/accounts/NotFoundView.vue"
import MapView from '@/pages/map/MapView.vue'

// ✅ 커뮤니티 페이지 (상세 페이지와 리스트 페이지 분류 명확화)
const CommunityListPage = () => import("@/pages/community/CommunityPage.vue")
const CommunityDetailPage = () => import("@/pages/community/CommunityDetailPage.vue")
const CommunityWritePage = () => import("@/pages/community/CommunityWritePage.vue")

const routes = [
  { path: "/", name: "Main", component: MainPage },
  { path: "/login", name: "Login", component: LoginPage },
  { path: "/signup", name: "Signup", component: SignUpPage },
  // router/index.js
  {
    path: "/calendar",
    component: () => import("@/pages/calendar/CalendarPage.vue"),
  },

  {
    path: "/profile-setup",
    name: "ProfileSetup",
    component: ProfileSetupPage,
    meta: { requiresAuth: true },
  },
  {
    path: "/profile",
    name: "profile",
    component: () => import("@/pages/accounts/MyProfilePage.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/profile/edit",
    name: "profile-edit",
    component: () => import("@/pages/accounts/EditProfilePage.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/account/edit",
    name: "account-edit",
    component: () => import("@/pages/accounts/EditAccountPage.vue"),
    meta: { requiresAuth: true },
  },

  // ==========================
  // 🌱 Community (수정된 섹션)
  // ==========================

  // 1. 기본 경로 접근 시 restaurant로 자동 이동
  {
    path: "/community",
    redirect: "/community/restaurant",
  },

  // 2. 카테고리별 목록 페이지 (restaurant, review, qna, free)
  {
    path: "/community/:category(restaurant|review|qna|free)",
    name: "community",
    component: CommunityListPage,
    meta: { requiresAuth: true },
  },

  // 3. 게시글 작성 (상세 페이지보다 위에 있어야 우선순위가 밀리지 않음)
  {
    path: "/community/write",
    name: "community-write",
    component: CommunityWritePage,
    meta: { requiresAuth: true },
  },

  // 4. 게시글 상세
  {
    path: "/community/detail/:id", // 주소가 겹치지 않게 detail을 넣어주는 것이 안전함
    name: "community-detail",
    component: CommunityDetailPage,
    meta: { requiresAuth: true },
  },

  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundView
  },

  {
    path: '/map',
    name: 'Map',
    component: MapView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// ==========================
// ✅ Navigation Guard
// ==========================
// router/index.js 수정
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  const isLoggedIn = !!authStore.accessToken

  if (to.meta.requiresAuth && !isLoggedIn) {
    return next({ name: 'Login' })
  }

  // 기존의 '무조건 리다이렉트' 로직을 제거하거나 주석 처리합니다.
  // 사용자가 메인으로 가고 싶다면 일단 보내줍니다.
  next()
})

export default router