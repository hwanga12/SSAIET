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

      <div class="profile-dashboard-grid">
        
        <aside class="dashboard-left">
          <div class="card-inner">
            <ProfileCard :user="user" />
          </div>

          <div class="health-tip-banner">
            <div class="tip-icon">
              <span class="material-icons">auto_awesome</span>
            </div>
            <div class="tip-text">
              <span class="tip-label">Health Tip</span>
              <p>주기적으로 업데이트하여 더 정확한 <br /><strong>AI 식단</strong>을 처방받으세요!</p>
            </div>
          </div>
        </aside>

        <div class="dashboard-right">
          <div class="activity-wrapper">
            <ActivitySection 
              :my-posts="myPosts" 
              :liked-posts="likedPosts" 
              @go-detail="goDetail"
            />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import { useCommunityStore } from "@/stores/community"

import BaseNavbar from "@/components/common/BaseNavbar.vue"
import ProfileCard from "@/components/profile/ProfileCard.vue"
import ActivitySection from "@/components/profile/ActivitySection.vue"

const router = useRouter()
const auth = useAuthStore()
const community = useCommunityStore()

const user = computed(() => auth.user)
const myPosts = computed(() => community.posts.filter(p => p.is_mine))
const likedPosts = computed(() => community.posts.filter(p => p.is_liked))

onMounted(async () => {
  if (!auth.user || !auth.user.height) {
    await auth.fetchMyProfile()
  }
  if (community.posts.length === 0) {
    await community.fetchPosts()
  }
  await community.fetchMyComments()
})

const goDetail = (id) => router.push(`/community/detail/${id}`)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.profile-layout {
  min-height: 100vh;
  background-color: #fcfdfd;
  position: relative;
  min-width: 1200px;
  overflow-x: auto;
}

.bg-decoration { position: absolute; inset: 0; z-index: 0; pointer-events: none; }
.blob { position: absolute; filter: blur(100px); border-radius: 50%; opacity: 0.15; }
.blob-green { width: 600px; height: 600px; background: #22c55e; top: -100px; right: -100px; }
.blob-light { width: 500px; height: 500px; background: #e2e8f0; bottom: -100px; left: -100px; }

.nav-fixed { position: sticky; top: 0; z-index: 100; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); }

.profile-container {
  position: relative;
  z-index: 1;
  width: 1100px;
  margin: 0 auto;
  padding: 60px 0 100px;
}

.profile-header { margin-bottom: 50px; }
.title-group { display: flex; align-items: center; gap: 16px; margin-bottom: 8px; }
.icon-circle { width: 48px; height: 48px; background: #f0fdf4; color: #22c55e; border-radius: 14px; display: flex; align-items: center; justify-content: center; }
.main-title { font-size: 2.2rem; font-weight: 900; color: #0f172a; letter-spacing: -1.5px; }
.highlight { color: #22c55e; }
.sub-title { color: #64748b; font-size: 1rem; font-weight: 500; margin-left: 64px; }

/* ✅ 대시보드 그리드: stretch로 설정하여 양쪽 높이를 맞춤 */
.profile-dashboard-grid {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 30px;
  align-items: stretch;
}

.dashboard-left {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card-inner {
  background: white;
  border-radius: 32px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
  border: 1px solid #f1f5f9;
}

.profile-action-group { display: flex; flex-direction: column; gap: 12px; }

.action-btn {
  display: flex; align-items: center; justify-content: center; gap: 10px;
  padding: 16px; border-radius: 18px; font-weight: 800; font-size: 0.95rem;
  cursor: pointer; transition: 0.3s; border: none; width: 100%;
}

.secondary-btn { background: #ffffff; color: #64748b; border: 1.5px solid #e2e8f0; }
.primary-btn { background: #0f172a; color: white; }
.primary-btn:hover { background: #22c55e; box-shadow: 0 10px 20px rgba(34, 197, 94, 0.2); }

.health-tip-banner {
  background: #f8fafc; border-radius: 24px; padding: 20px;
  display: flex; align-items: center; gap: 16px; border: 1px solid #f1f5f9;
}

/* ✅ 오른쪽 섹션 수정: 겹침 방지 핵심 */
.dashboard-right {
  width: 100%;
  display: flex;
}

.activity-wrapper {
  width: 100%;
  height: 100%;
  min-height: 600px; /* 고정 높이를 확보하여 출렁임 방지 */
}

/* ✅ 자식 컴포넌트 내부 애니메이션 가두기 */
:deep(.activity-section) {
  height: 100% !important;
  box-sizing: border-box;
  overflow: hidden; /* 밖으로 삐져나가는 애니메이션 차단 */
  position: relative;
}

/* 탭 바가 항상 최상단에 오도록 */
:deep(.activity-tabs) {
  position: relative;
  z-index: 10;
  background: white;
}
</style>