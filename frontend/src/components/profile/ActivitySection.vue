<template>
  <section class="activity-section">
    <nav class="activity-tabs">
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'myPosts' }"
        @click="activeTab = 'myPosts'"
      >
        내 게시글 <span class="badge">{{ mypageStore.posts.length }}</span>
      </button>

      <button
        class="tab-btn"
        :class="{ active: activeTab === 'myComments' }"
        @click="activeTab = 'myComments'"
      >
        내 댓글 <span class="badge">{{ mypageStore.comments.length }}</span>
      </button>

      <button
        class="tab-btn"
        :class="{ active: activeTab === 'likedPosts' }"
        @click="activeTab = 'likedPosts'"
      >
        좋아요 한 글 <span class="badge">{{ mypageStore.likedPosts.length }}</span>
      </button>
    </nav>

    <div class="activity-content">
      <div v-if="mypageStore.isLoading" class="empty-activity">
        <span class="material-icons">hourglass_empty</span>
        <p>활동 내역을 불러오는 중입니다...</p>
      </div>
      <div v-else-if="mypageStore.error" class="empty-activity error">
        <span class="material-icons">error_outline</span>
        <p>마이페이지 로딩에 실패했습니다.</p>
      </div>

      <div v-else class="post-mini-list-wrapper">
        <TransitionGroup
          name="list-fade"
          tag="div"
          class="post-mini-list"
        >
          <div
            v-if="activeTab === 'myComments' ? mypageStore.comments.length === 0 : currentDisplayPosts.length === 0"
            key="empty"
            class="empty-activity"
          >
            <span class="material-icons">history_edu</span>
            <p>아직 기록된 활동이 없습니다.</p>
          </div>

          <template v-else-if="activeTab === 'myComments'">
            <div
              v-for="comment in mypageStore.comments"
              :key="`comment-${comment.id}`"
              class="post-mini-item comment-item"
              @click="emit('goDetail', comment.post_id)"
            >
              <div class="post-info">
                <span class="comment-label">💬 댓글</span>
                <h4 class="post-title">{{ comment.content }}</h4>
                <div class="origin-post-info">
                  <span class="origin-label">원문:</span> {{ comment.post_title }}
                </div>
              </div>
              <div class="post-meta">
                <span class="date">{{ formatDate(comment.created_at) }}</span>
              </div>
            </div>
          </template>

          <template v-else>
            <div
              v-for="post in currentDisplayPosts"
              :key="`post-${post.id}`"
              class="post-mini-item"
              @click="emit('goDetail', post.id)"
            >
              <div class="post-info">
                <span class="category-tag" :class="post.category?.toLowerCase()">
                  {{ post.category }}
                </span>
                <h4 class="post-title">{{ post.title }}</h4>
              </div>
              <div class="post-meta">
                <span class="material-icons">thumb_up</span>
                {{ post.likes_count }}
                <span class="date">{{ formatDate(post.created_at) }}</span>
              </div>
            </div>
          </template>
        </TransitionGroup>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { useMypageStore } from "@/stores/mypage"

const emit = defineEmits(["goDetail"])
const activeTab = ref("myPosts")
const mypageStore = useMypageStore()

onMounted(() => {
  mypageStore.fetchMypage()
})

const currentDisplayPosts = computed(() => {
  if (activeTab.value === "myPosts") return mypageStore.posts
  if (activeTab.value === "likedPosts") return mypageStore.likedPosts
  return []
})

const formatDate = (dateStr) => {
  if (!dateStr) return ""
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}/${date.getDate()}`
}
</script>

<style scoped>
/* 전체 레이아웃 */
.activity-section {
  background: white;
  border-radius: 32px;
  padding: 35px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.04);
  border: 1px solid #f1f5f9;
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* 탭: 상단 고정 및 레이어 우선순위 확보 */
.activity-tabs {
  display: flex;
  gap: 24px;
  margin-bottom: 25px;
  border-bottom: 2px solid #f1f5f9;
  position: relative;
  z-index: 10; /* 애니메이션 요소보다 위에 오도록 */
  background: white; /* 뒤로 지나가는 요소 가림 */
}

.tab-btn {
  background: none;
  border: none;
  font-size: 1rem;
  font-weight: 800;
  color: #94a3b8;
  cursor: pointer;
  padding: 12px 0;
  position: relative;
}

.tab-btn.active { color: #0f172a; }
.tab-btn.active::after {
  content: "";
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 3px;
  background: #22c55e;
  border-radius: 10px;
}

.badge {
  font-size: 0.7rem;
  background: #f1f5f9;
  padding: 2px 8px;
  border-radius: 6px;
  margin-left: 4px;
}

/* 콘텐츠 영역: 애니메이션 가둠 */
.activity-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden; /* 가로 애니메이션 튀어나감 방지 */
  position: relative; /* 자식 absolute의 기준점 */
  padding-right: 5px;
}

.post-mini-list-wrapper {
  position: relative;
  width: 100%;
}

.post-mini-list {
  padding-top: 6px;
  position: relative; /* TransitionGroup 기준점 */
  width: 100%;
}

.post-mini-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: #fcfdfd;
  border: 1px solid #f1f5f9;
  border-radius: 14px;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
  margin-bottom: 12px;
  min-height: 80px;
  box-sizing: border-box; /* 너비 계산 오류 방지 */
  width: 100%; 
}

.post-mini-item:hover {
  background: #f0fdf4;
  border-color: #22c55e;
  transform: translateY(-2px);
}

/* 태그 및 텍스트 스타일 */
.post-info { flex: 1; overflow: hidden; display: flex; flex-direction: column; gap: 4px; }
.post-title { font-size: 0.95rem; font-weight: 700; color: #1e293b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.category-tag { font-size: 0.65rem; font-weight: 900; padding: 3px 7px; border-radius: 5px; text-transform: uppercase; width: fit-content; }
.category-tag.restaurant { background: #f0fdf4; color: #22c55e; }
.category-tag.review { background: #eff6ff; color: #3b82f6; }
.category-tag.free { background: #f1f5f9; color: #64748b; }

.comment-item { border-left: 4px solid #22c55e; }
.comment-label { font-size: 0.65rem; font-weight: 900; color: #22c55e; background: #f0fdf4; padding: 2px 6px; border-radius: 4px; width: fit-content; }
.origin-post-info { font-size: 0.8rem; color: #94a3b8; }
.post-meta { font-size: 0.8rem; color: #94a3b8; display: flex; align-items: center; gap: 8px; white-space: nowrap; }

.empty-activity { text-align: center; padding: 60px 0; color: #cbd5e1; width: 100%; }

/* ================= 애니메이션 (핵심 수정) ================= */
.list-fade-enter-active,
.list-fade-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.list-fade-leave-active {
  position: absolute; /* 나가는 요소가 레이아웃에서 빠짐 */
  width: 100%;        /* 중요: absolute 시 너비 유지 */
  z-index: 1;
}

.list-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.list-fade-leave-to {
  opacity: 0;
  transform: translateX(-30px); /* 왼쪽으로 밀면서 사라짐 */
}

/* 리스트 항목들이 자리를 옮길 때 부드럽게 이동 */
.list-fade-move {
  transition: transform 0.4s ease;
}
</style>