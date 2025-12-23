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
            <div class="tip-icon"><span class="material-icons">auto_awesome</span></div>
            <div class="tip-text">
              <span class="tip-label">Health Tip</span>
              <p>주기적으로 업데이트하여 더 정확한 <br /><strong>AI 식단</strong>을 처방받으세요!</p>
            </div>
          </div>
        </aside>
        <div class="dashboard-right">
          <div class="activity-wrapper">
            <ActivitySection @go-detail="goDetail" />
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
onMounted(async () => {
  if (!auth.user?.height) await auth.fetchMyProfile()
  if (community.posts.length === 0) await community.fetchPosts()
})
const goDetail = (id) => router.push(`/community/detail/${id}`)
</script>

<style scoped>
.profile-layout { background-color: #fcfdfd; position: relative; min-width: 1200px; }
.nav-fixed { position: fixed; top: 0; left: 0; right: 0; z-index: 1000; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); }
.profile-container { position: relative; z-index: 1; width: 1100px; margin: 0 auto; padding: 120px 0 100px; }
.profile-dashboard-grid { display: grid; grid-template-columns: 360px 1fr; gap: 30px; align-items: start; }
.dashboard-left { position: sticky; top: 120px; display: flex; flex-direction: column; gap: 20px; }
.card-inner { background: white; border-radius: 32px; overflow: hidden; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05); border: 1px solid #f1f5f9; }
.dashboard-right { width: 100%; }

/* ⭐ 이중 스크롤 해결의 결정타: 자식의 모든 스크롤 강제 차단 */
.activity-wrapper :deep(.activity-section),
.activity-wrapper :deep(.activity-content) {
  height: auto !important;
  max-height: none !important;
  overflow: visible !important;
}

.bg-decoration { position: absolute; inset: 0; z-index: 0; pointer-events: none; }
.blob { position: absolute; filter: blur(100px); border-radius: 50%; opacity: 0.15; }
.blob-green { width: 600px; height: 600px; background: #22c55e; top: -100px; right: -100px; }
.blob-light { width: 500px; height: 500px; background: #e2e8f0; bottom: -100px; left: -100px; }
</style>