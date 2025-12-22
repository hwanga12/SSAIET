<template>
  <div class="community-layout">
    <BaseNavbar />

    <div class="bg-decoration">
      <div class="blob blob-green"></div>
      <div class="blob blob-light"></div>
    </div>

    <section class="community-page">
      <header class="page-header">
        <div class="header-text">
          <h2 class="page-title">싸피 <span class="highlight">광장</span></h2>
          <p class="page-subtitle">SSAFY인들과 건강한 정보를 공유해보세요.</p>
        </div>

        <button class="create-btn" @click="goCreate">
          <span class="material-icons">add_circle</span>
          <span>새 글 작성</span>
        </button>
      </header>

      <nav class="tab-bar">
        <button
          class="tab-item"
          :class="{ active: currentCategory === 'RESTAURANT' }"
          @click="handleTabChange('RESTAURANT')"
        >
          <span class="tab-emoji">🍽️</span> 식당 추천
        </button>
        <button
          class="tab-item"
          :class="{ active: currentCategory === 'REVIEW' }"
          @click="handleTabChange('REVIEW')"
        >
          <span class="tab-emoji">📈</span> 변화 후기
        </button>
        <button
          class="tab-item"
          :class="{ active: currentCategory === 'QNA' }"
          @click="handleTabChange('QNA')"
        >
          <span class="tab-emoji">❓</span> Q&A
        </button>
        <button
          class="tab-item"
          :class="{ active: currentCategory === 'FREE' }"
          @click="handleTabChange('FREE')"
        >
          <span class="tab-emoji">💬</span> 잡담
        </button>
      </nav>

      <main class="content-area">
        <Transition name="list-fade" mode="out-in">
          <div v-if="store.isLoading" class="status-container">
            <div class="pulse-loader"></div>
            <p>이야기 꾸러미를 가져오고 있어요...</p>
          </div>

          <div v-else-if="store.posts.length === 0" class="status-container empty">
            <div class="empty-icon">📂</div>
            <h3>아직 게시글이 없습니다</h3>
            <p>이 카테고리의 첫 번째 주인공이 되어보세요!</p>
          </div>

          <div v-else class="card-grid">
            <CommunityPostCard
              v-for="post in store.posts"
              :key="post.id"
              :post="post"
              @click="goDetail(post.id)"
            />
          </div>
        </Transition>
      </main>
    </section>
  </div>
</template>

<script setup>
import { computed, watch, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useCommunityStore } from "@/stores/community"
import BaseNavbar from "@/components/common/BaseNavbar.vue"
import CommunityPostCard from "@/components/community/CommunityPostCard.vue"

const route = useRoute()
const router = useRouter()
const store = useCommunityStore()

// 1. URL 파라미터에서 현재 카테고리 추출 (예: restaurant, free)
const currentCategory = computed(() => (route.params.category || 'RESTAURANT').toUpperCase())

// 2. 핵심 로직: URL 카테고리가 바뀔 때마다 서버에 해당 데이터 요청
watch(
  () => route.params.category,
  (newCategory) => {
    if (newCategory) {
      store.fetchPostsByCategory(newCategory)
    }
  },
  { immediate: true } // 페이지 진입 시 즉시 실행
)

// 탭 변경 시 URL 이동 (라우터 이동)
const handleTabChange = (target) => {
  router.push(`/community/${target.toLowerCase()}`)
}

// 상세 페이지 이동 (아까 라우터에서 설정한 detail 경로로 수정)
const goDetail = (id) => router.push(`/community/detail/${id}`)

// 글쓰기 페이지 이동
const goCreate = () => {
  router.push({
    path: "/community/write",
    query: { category: currentCategory.value },
  })
}
</script>

<style scoped>
@import url("https://fonts.googleapis.com/icon?family=Material+Icons");

.community-layout {
  min-height: 100vh;
  background-color: #fcfdfd;
  position: relative;
  overflow-x: auto; /* 🔥 가로 스크롤 허용 */
}

.bg-decoration {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.blob {
  position: absolute;
  filter: blur(100px);
  border-radius: 50%;
  opacity: 0.15;
}

.blob-green {
  width: 500px;
  height: 500px;
  background: #22c55e;
  top: -50px;
  right: -100px;
}

.blob-light {
  width: 400px;
  height: 400px;
  background: #e2e8f0;
  bottom: -50px;
  left: -100px;
}

/* ================= PAGE ================= */
.community-page {
  position: relative;
  z-index: 1;
  max-width: 1000px;
  min-width: 1000px; /* 🔥 PC 고정 */
  margin: 0 auto;
  padding: 120px 20px 100px;
}

/* ================= HEADER ================= */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 40px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #0f172a;
  margin: 0;
  letter-spacing: -1.5px;
}

.highlight {
  color: #22c55e;
}

.page-subtitle {
  font-size: 1.1rem;
  color: #64748b;
  margin-top: 8px;
  font-weight: 500;
}

/* ================= CREATE BUTTON ================= */
.create-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 24px;
  border-radius: 16px;
  border: none;
  background: #0f172a;
  color: white;
  font-weight: 800;
  cursor: pointer;
  transition: 0.3s;
  box-shadow: 0 10px 20px rgba(15, 23, 42, 0.15);
}

.create-btn:hover {
  background: #22c55e;
  transform: translateY(-3px);
}

/* ================= TAB ================= */
.tab-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
  background: #f1f5f9;
  padding: 8px;
  border-radius: 20px;
  width: fit-content;
  flex-wrap: nowrap;          /* 🔥 줄바꿈 제거 */
  white-space: nowrap;
}

.tab-item {
  padding: 12px 24px;
  border-radius: 14px;
  border: none;
  background: transparent;
  color: #64748b;
  font-weight: 800;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: 0.2s;
}

.tab-item.active {
  background: white;
  color: #22c55e;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* ================= GRID ================= */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

/* ================= STATUS ================= */
.status-container {
  text-align: center;
  padding: 100px 0;
  color: #94a3b8;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 16px;
  opacity: 0.5;
}

/* ================= TRANSITION ================= */
.list-fade-enter-active,
.list-fade-leave-active {
  transition: all 0.3s ease;
}

.list-fade-enter-from,
.list-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>