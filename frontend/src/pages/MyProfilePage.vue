<template>
  <div class="profile-layout">
    <BaseNavbar class="nav-fixed" />

    <div class="bg-decoration">
      <div class="blob blob-green"></div>
      <div class="blob blob-light"></div>
    </div>

    <main class="profile-container">
      <header class="profile-header">
        <div class="title-group">
          <div class="icon-circle">
            <span class="material-icons">fingerprint</span>
          </div>
          <h1 class="main-title">나의 <span class="highlight">건강</span> 프로필</h1>
        </div>
        <p class="sub-title">SSAIET에 저장된 소중한 건강 데이터입니다.</p>
      </header>

      <div class="profile-content-wrapper">
        <div class="card-inner">
          <ProfileCard :user="user" />
        </div>

        <div class="profile-action-group">
          <button class="action-btn secondary-btn" @click="goAccountEdit">
            <span class="material-icons">manage_accounts</span>
            <span>계정 설정</span>
          </button>
          
          <button class="action-btn primary-btn" @click="goEdit">
            <span class="material-icons">settings</span>
            <span>정보 수정하기</span>
          </button>
        </div>
      </div>

      <div class="health-tip-banner">
        <div class="tip-icon">
          <span class="material-icons">auto_awesome</span>
        </div>
        <div class="tip-text">
          <span class="tip-label">Health Tip</span>
          <p>키와 몸무게를 주기적으로 업데이트하면 <br />더 정확한 <strong>AI 식단 처방</strong>이 가능합니다.</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import BaseNavbar from "@/components/common/BaseNavbar.vue"
import ProfileCard from "@/components/profile/ProfileCard.vue"

const router = useRouter()
const auth = useAuthStore()

const user = computed(() => auth.user)

onMounted(async () => {
  if (!auth.user || !auth.user.height) {
    await auth.fetchMyProfile()
  }
})

const goEdit = () => {
  router.push("/profile/edit")
}

const goAccountEdit = () => {
  router.push("/account/edit") // 계정 수정 경로에 맞게 조정하세요
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.profile-layout {
  min-height: 100vh;
  background-color: #fcfdfd;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.bg-decoration {
  position: absolute;
  inset: 0;
  z-index: 0;
}
.blob {
  position: absolute;
  filter: blur(100px);
  border-radius: 50%;
  opacity: 0.15;
}
.blob-green { width: 600px; height: 600px; background: #22c55e; top: -100px; right: -100px; }
.blob-light { width: 500px; height: 500px; background: #e2e8f0; bottom: -100px; left: -100px; }

.nav-fixed {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
}

.profile-container {
  position: relative;
  z-index: 1;
  max-width: 900px;
  width: 100%;
  margin: 0 auto;
  padding: 60px 20px 100px;
}

.profile-header {
  margin-bottom: 40px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title-group {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}

.icon-circle {
  width: 54px;
  height: 54px;
  background: #f0fdf4;
  color: #22c55e;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: -2px;
}

.highlight {
  color: #22c55e;
}

.sub-title {
  color: #64748b;
  font-size: 1.1rem;
  font-weight: 500;
}

.profile-content-wrapper {
  position: relative;
  width: 100%;
}

.card-inner {
  background: white;
  border-radius: 40px;
  overflow: hidden;
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.03);
  width: 100%;
}

/* ===== 🔥 하단 액션 버튼 그룹 ===== */
.profile-action-group {
  position: absolute;
  right: 40px;
  bottom: -28px;
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 28px;
  border-radius: 20px;
  font-weight: 800;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
}

/* 계정 설정 버튼 (세컨더리 - 화이트) */
.secondary-btn {
  background: #ffffff;
  color: #64748b;
  border: 1.5px solid #e2e8f0;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
}

.secondary-btn:hover {
  background: #f8fafc;
  color: #0f172a;
  border-color: #cbd5e1;
  transform: translateY(-5px);
}

/* 정보 수정 버튼 (프라이머리 - 블랙) */
.primary-btn {
  background: #0f172a;
  color: white;
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.2);
}

.primary-btn:hover {
  background: #22c55e;
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(34, 197, 94, 0.3);
}

.health-tip-banner {
  margin-top: 80px;
  background: #f8fafc;
  border-radius: 28px;
  padding: 30px;
  display: flex;
  align-items: center;
  gap: 24px;
  border: 1px solid #f1f5f9;
}

.tip-icon {
  width: 56px;
  height: 56px;
  background: #fff;
  color: #22c55e;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

.tip-label {
  display: inline-block;
  font-size: 12px;
  font-weight: 900;
  color: #22c55e;
  background: #f0fdf4;
  padding: 4px 10px;
  border-radius: 6px;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.tip-text p {
  font-size: 1rem;
  color: #475569;
  line-height: 1.6;
  margin: 0;
}

.tip-text strong {
  color: #0f172a;
  font-weight: 800;
}

@media (max-width: 768px) {
  .profile-container { padding-top: 40px; }
  .main-title { font-size: 2rem; }
  .profile-action-group { 
    position: relative;
    right: 0;
    bottom: 0;
    margin-top: 30px;
    flex-direction: column;
    width: 100%;
    align-items: center;
  }
  .action-btn { width: 100%; justify-content: center; }
  .health-tip-banner { flex-direction: column; text-align: center; padding: 20px; }
}
</style>