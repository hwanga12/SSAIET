import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import SignUpPage from "@/pages/SignUpPage.vue"
import ProfileSetupPage from "@/pages/ProfileSetupPage.vue"
import MainPage from "@/pages/MainPage.vue"
import LoginPage from "@/pages/LoginPage.vue"
import NutritionCalendar from "@/components/calendar/DinnerCalendar.vue"
// import CalendarPage from "@/pages/CalendarPage.vue"


const routes = [
  { path: "/", name: "Main", component: MainPage },
  { path: "/login", name: "Login", component: LoginPage },
  { path: "/signup", name: "Signup", component: SignUpPage },
  {
    path: "/calendar",
    name: "NutritionCalendar",
    component: NutritionCalendar,
    meta: { requiresAuth: true }
  },
  {
    path: "/profile-setup",
    name: "ProfileSetup",
    component: ProfileSetupPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/pages/MyProfilePage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile/edit',
    name: 'profile-edit',
    component: () => import('@/pages/EditProfilePage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/account/edit',
    name: 'account-edit',
    component: () => import('@/pages/EditAccountPage.vue'),
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})


// ==========================
// ✅ Navigation Guard (수정 완료)
// ==========================
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isLoggedIn = authStore.accessToken !== null

  // 1️⃣ 인증이 필요한 페이지인데 로그인 안 됨 → signup으로 보내기
  if (to.meta.requiresAuth && !isLoggedIn) {
    return next({ name: "Login", replace: true })
  }

  // 2️⃣ 로그인한 상태에서 login/signup 접근 → 그냥 허용
  //    (막아버리면 login 페이지가 안 뜨는 문제가 발생)

  return next()
})


export default router