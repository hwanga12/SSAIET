<template>
  <article v-if="post" class="post-card" @click="$emit('click')">
    <div class="card-header">
      <h3 class="title">{{ post?.title }}</h3>
      <p class="excerpt">{{ post?.content }}</p>
    </div>

    <div class="card-footer">
      <div class="user-meta">
        <div class="mini-avatar">🥗</div>
        <span class="author">{{ post?.author_name || '익명' }}</span>
      </div>
      
      <div class="stats-meta">
        <div class="stat-item" :class="{ 'is-liked': post?.is_liked }">
          <span class="material-icons">
            {{ post?.is_liked ? 'thumb_up' : 'thumb_up_off_alt' }}
          </span>
          <span class="count-num">{{ post?.likes_count || 0 }}</span>
        </div>

        <div class="stat-item is-comment">
          <span class="material-icons">chat_bubble_outline</span>
          <span class="count-num">{{ post?.comments_count || 0 }}</span>
        </div>
      </div>
    </div>
  </article>
</template>

<script setup>
defineProps({
  post: {
    type: Object,
    required: true
  }
})

defineEmits(['click'])
</script>

<style scoped>
.post-card {
  background: white; border-radius: 28px; padding: 28px;
  border: 1px solid #f1f5f9; cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex; flex-direction: column; justify-content: space-between;
  min-height: 220px; /* 댓글 배지 추가로 높이 살짝 보정 */
}

.post-card:hover {
  transform: translateY(-8px);
  border-color: #22c55e;
  box-shadow: 0 20px 40px rgba(34, 197, 94, 0.08);
}

.title { 
  font-size: 1.25rem; font-weight: 800; color: #0f172a; margin-bottom: 12px; line-height: 1.4; 
  overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; 
}

.excerpt { 
  font-size: 0.95rem; color: #64748b; line-height: 1.6; overflow: hidden; 
  text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; margin-bottom: 24px; 
}

.card-footer { 
  display: flex; justify-content: space-between; align-items: center; 
  padding-top: 16px; border-top: 1px solid #f8fafc; 
}

.user-meta { display: flex; align-items: center; gap: 8px; }
.mini-avatar { width: 24px; height: 24px; background: #f0fdf4; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 12px; }
.author { font-size: 0.85rem; font-weight: 700; color: #475569; }

.stats-meta { display: flex; align-items: center; gap: 10px; }

.stat-item { 
  display: flex; align-items: center; gap: 4px; font-size: 0.85rem; 
  font-weight: 800; color: #94a3b8; padding: 4px 10px; border-radius: 10px; transition: 0.2s;
}

.stat-item .material-icons { font-size: 16px; }

/* 좋아요 활성화 (그린) */
.stat-item.is-liked { color: #22c55e; background: #f0fdf4; }

/* 댓글 스타일 (블루 포인트) */
.stat-item.is-comment { color: #3b82f6; background: #eff6ff; }

.count-num { font-family: 'Pretendard', sans-serif; }
</style>