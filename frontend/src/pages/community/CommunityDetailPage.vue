<template>
  <div class="page-layout">
    <BaseNavbar />

    <div class="bg-decoration">
      <div class="blob blob-green"></div>
      <div class="blob blob-light"></div>
    </div>

    <main v-if="post" class="detail-container">
      <nav class="detail-nav">
        <button class="back-link" @click="goBack">
          <span class="material-icons">arrow_back</span>
          <span>커뮤니티 목록으로</span>
        </button>
        <div class="category-badge" :class="post.category.toLowerCase()">
          {{ post.category }}
        </div>
      </nav>

      <article class="post-card">
        <header class="post-header">
          <div v-if="!isEditingPost">
            <h1 class="post-title">{{ post.title }}</h1>
            <div class="post-meta">
              <div class="author-info">
                <div class="avatar-mini">🥗</div>
                <span class="author-name">{{ post.author_name }}</span>
              </div>
              <div class="meta-divider"></div>
              <span class="post-date">{{ formatDate(post.created_at) }}</span>
            </div>
          </div>
          <div v-else class="edit-post-header">
            <label class="edit-label">제목</label>
            <input 
              v-model="editPostData.title" 
              class="edit-title-input" 
              placeholder="제목을 입력하세요"
            />
          </div>
        </header>

        <section class="post-body">
          <p v-if="!isEditingPost" class="content-text">{{ post.content }}</p>
          <div v-else class="edit-content-wrapper">
            <label class="edit-label">내용</label>
            <textarea 
              v-model="editPostData.content" 
              class="edit-content-textarea" 
              rows="10"
            ></textarea>
          </div>
        </section>

        <section class="extra-info-section">
          
          <template v-if="!isEditingPost">
            <div v-if="post.category === 'RESTAURANT' && post.restaurant_info" class="extra-card restaurant">
              <div class="extra-header">
                <span class="material-icons tag">restaurant_menu</span>
                <h3>식당 상세 정보</h3>
              </div>
              <div class="extra-grid">
                <div class="info-item">
                  <strong>식당 이름</strong>
                  <span>{{ post.restaurant_info.restaurant_name }}</span>
                </div>
                <div class="info-item">
                  <strong>위치</strong>
                  <span>{{ post.restaurant_info.location }}</span>
                </div>
                <div class="info-item">
                  <strong>추천 메뉴</strong>
                  <span>{{ post.restaurant_info.recommended_menu }}</span>
                </div>
                <div class="info-item">
                  <strong>건강 태그</strong>
                  <span class="tag">{{ getHealthLabel(post.restaurant_info.health_tag) }}</span>
                </div>
              </div>
            </div>

            <div v-if="post.category === 'REVIEW' && post.review_info" class="extra-card review-modern">
              <div class="review-badges">
                <span class="badge period">
                  <span class="material-icons">calendar_today</span>
                  {{ getPeriodLabel(post.review_info.period) }} 동안
                </span>
                <span class="badge type">체중 변화</span>
              </div>

              <div class="weight-display">
                <div class="weight-icon-circle" :class="post.review_info.weight_diff < 0 ? 'loss' : 'gain'">
                  <span class="material-icons">
                    {{ post.review_info.weight_diff < 0 ? 'trending_down' : (post.review_info.weight_diff > 0 ? 'trending_up' : 'remove') }}
                  </span>
                </div>
                <div class="weight-text-group">
                  <span class="label-text">총 변화량</span>
                  <div class="value-text" :class="post.review_info.weight_diff < 0 ? 'loss-text' : 'gain-text'">
                    {{ post.review_info.weight_diff > 0 ? '+' : '' }}{{ post.review_info.weight_diff }}
                    <span class="unit">kg</span>
                  </div>
                </div>
              </div>
            </div>
          </template>

          <template v-else>
            <div v-if="post.category === 'RESTAURANT'" class="extra-card restaurant edit-mode">
              <div class="extra-header">
                <span class="material-icons tag">edit_note</span>
                <h3>식당 정보 수정</h3>
              </div>
              <div class="edit-grid">
                <div class="input-group">
                  <label>식당 이름</label>
                  <input v-model="editPostData.restaurant.restaurant_name" class="custom-input small" placeholder="식당 이름" />
                </div>
                <div class="input-group">
                  <label>위치</label>
                  <input v-model="editPostData.restaurant.location" class="custom-input small" placeholder="위치 (예: 역삼역)" />
                </div>
                <div class="input-group">
                  <label>추천 메뉴</label>
                  <input v-model="editPostData.restaurant.recommended_menu" class="custom-input small" placeholder="추천 메뉴" />
                </div>
                <div class="input-group">
                  <label>건강 태그</label>
                  <select v-model="editPostData.restaurant.health_tag" class="custom-select small">
                    <option value="BALANCED">🥗 균형식</option>
                    <option value="HIGH_PROTEIN">🥩 고단백</option>
                    <option value="LOW_FAT">🥑 저지방</option>
                    <option value="DIET">📉 다이어트</option>
                    <option value="OUT">🍜 외식 (치팅)</option>
                  </select>
                </div>
              </div>
            </div>

            <div v-if="post.category === 'REVIEW'" class="extra-card review edit-mode">
              <div class="extra-header">
                <span class="material-icons tag">monitor_weight</span>
                <h3>체중 변화 정보 수정</h3>
              </div>
              <div class="edit-grid">
                <div class="input-group">
                  <label>진행 기간</label>
                  <select v-model="editPostData.review.period" class="custom-select small">
                    <option value="1W">1주일 진행</option>
                    <option value="2W">2주일 진행</option>
                    <option value="1M">1개월 진행</option>
                  </select>
                </div>
                <div class="input-group">
                  <label>체중 변화량 (kg)</label>
                  <input 
                    type="number" 
                    v-model="editPostData.review.weight_diff" 
                    class="custom-input small no-spinner" 
                    placeholder="예: -2.5" 
                  />
                </div>
              </div>
              <p class="input-hint">* 변화량만 입력해주세요 (예: 감량시 -2, 증량시 2)</p>
            </div>
          </template>

        </section>

        <footer class="post-footer">
          <template v-if="!isEditingPost">
            <button class="like-btn" :class="{ active: isLiked }" @click="handleLike">
              <span class="material-icons">{{ isLiked ? 'thumb_up' : 'thumb_up_off_alt' }}</span>
              <span class="like-count">도움돼요 {{ post.likes_count }}</span>
            </button>
            
            <div v-if="post.is_mine" class="author-actions">
              <button class="edit-btn" @click="startEditPost">
                <span class="material-icons">edit</span>
                <span>수정</span>
              </button>
              <button class="delete-post-btn" @click="handleDeletePost">
                <span class="material-icons">delete_outline</span>
                <span>삭제</span>
              </button>
            </div>
          </template>

          <template v-else>
            <div class="edit-actions-group">
              <button class="save-btn" @click="submitEditPost">수정 완료</button>
              <button class="cancel-btn" @click="isEditingPost = false">취소</button>
            </div>
          </template>
        </footer>

        <section class="comment-section">
          <div class="comment-header">
            <div class="header-left">
              <span class="material-icons">chat_bubble_outline</span>
              <h3>댓글 <span class="comment-count">{{ comments.length }}</span></h3>
            </div>
          </div>

          <div v-if="!isEditingPost" class="comment-input-card">
            <textarea 
              v-model="newComment" 
              placeholder="따뜻한 댓글로 SSAFY 동료를 응원해주세요!"
              rows="3"
              class="styled-textarea"
            ></textarea>
            <div class="input-actions">
              <span class="guide-text">상대방을 존중하는 마음을 담아주세요.</span>
              <button class="comment-submit-btn" :disabled="!newComment.trim()" @click="submitComment">
                <span>등록</span>
                <span class="material-icons">send</span>
              </button>
            </div>
          </div>
          <div v-else class="empty-placeholder">
            ⚠️ 게시글 수정 중에는 댓글을 작성할 수 없습니다.
          </div>

          <TransitionGroup name="comment-list" tag="div" class="comment-list-container">
            <div v-for="comment in comments" :key="comment.id" class="comment-card">
              <div class="comment-main">
                <div class="comment-user-area">
                  <div class="user-avatar-circle"><span class="material-icons">person</span></div>
                  <div class="user-meta">
                    <span class="user-display-name">{{ comment.author_name }}</span>
                    <span class="comment-timestamp">{{ formatDate(comment.created_at) }}</span>
                  </div>
                </div>

                <div v-if="editingCommentId !== comment.id">
                  <p class="comment-text-body">{{ comment.content }}</p>
                </div>
                <div v-else class="comment-edit-area">
                  <textarea v-model="editCommentContent" class="styled-textarea edit-mode"></textarea>
                  <div class="edit-btn-group">
                    <button class="mini-save-btn" @click="submitEditComment(comment.id)">저장</button>
                    <button class="mini-cancel-btn" @click="editingCommentId = null">취소</button>
                  </div>
                </div>
              </div>

              <div v-if="comment.is_mine && editingCommentId !== comment.id" class="comment-actions">
                <button class="comment-mini-btn" @click="startEditComment(comment)">수정</button>
                <button class="comment-delete-icon-btn" @click="removeComment(comment.id)">삭제</button>
              </div>
            </div>
          </TransitionGroup>
        </section>
      </article>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue" 
import { useRoute, useRouter } from "vue-router"
import { useCommunityStore } from "@/stores/community"
import BaseNavbar from "@/components/common/BaseNavbar.vue"

const route = useRoute()
const router = useRouter()
const store = useCommunityStore()
const postId = Number(route.params.id)

const isEditingPost = ref(false)
const editPostData = reactive({ 
  title: "", 
  content: "",
  restaurant: {
    restaurant_name: "",
    location: "",
    recommended_menu: "",
    health_tag: "BALANCED"
  },
  review: {
    period: "1W",
    weight_diff: null,
    change_type: "WEIGHT"
  }
})
const editingCommentId = ref(null)
const editCommentContent = ref("")
const newComment = ref("")

const post = computed(() => store.posts.find(p => p.id === postId))
const comments = computed(() => store.comments || [])
const isLiked = computed(() => post.value?.is_liked || false)
const hasExtraInfo = computed(() => {
  if (!post.value) return false
  return ['RESTAURANT', 'REVIEW'].includes(post.value.category)
})

const HEALTH_TAG_MAP = {
  "BALANCED": "🥗 균형식",
  "HIGH_PROTEIN": "🥩 고단백",
  "LOW_FAT": "🥑 저지방",
  "DIET": "📉 다이어트",
  "OUT": "🍜 외식 (치팅)"
}
const getHealthLabel = (code) => HEALTH_TAG_MAP[code] || code

const getPeriodLabel = (code) => {
  const map = { '1W': '1주일', '2W': '2주일', '1M': '1개월' }
  return map[code] || code
}

const startEditPost = () => {
  if (!post.value) return
  editPostData.title = post.value.title
  editPostData.content = post.value.content
  
  if (post.value.category === 'RESTAURANT' && post.value.restaurant_info) {
    editPostData.restaurant = { ...post.value.restaurant_info }
  } 
  else if (post.value.category === 'REVIEW' && post.value.review_info) {
    editPostData.review = { 
        ...post.value.review_info,
        change_type: "WEIGHT"
    }
  }
  
  isEditingPost.value = true
}

const submitEditPost = async () => {
  if (!post.value) return;
  if (!editPostData.title.trim() || !editPostData.content.trim()) {
    alert("제목과 내용을 입력해주세요.");
    return;
  }

  try {
    const payload = {
      title: editPostData.title,
      content: editPostData.content,
      category: post.value.category,
    };

    if (post.value.category === 'RESTAURANT') {
      payload.restaurant_info = editPostData.restaurant;
    } 
    else if (post.value.category === 'REVIEW') {
      if (!editPostData.review.weight_diff) {
         alert("체중 변화량을 입력해주세요.");
         return;
      }
      payload.review_info = editPostData.review;
    }

    console.log("최종 수정 전송 데이터:", payload);

    await store.updatePost(postId, payload);
    
    isEditingPost.value = false;
    alert("게시글이 성공적으로 수정되었습니다.");
  } catch (error) {
    console.error("❌ 수정 실패 원인:", error.response?.data);
    alert("수정 실패: 입력 데이터를 확인해주세요.");
  }
};


const handleDeletePost = async () => {
  if (confirm("정말 이 게시물을 삭제하시겠습니까?")) {
    try {
      const targetCategory = post.value?.category?.toLowerCase() || 'free';
      await store.deletePost(postId);
      alert("게시글이 삭제되었습니다.");
      router.push(`/community/${targetCategory}`);
    } catch (error) {
      if (error.response?.status === 404) {
          router.push('/community');
          return;
      }
      console.error("삭제 실패 상세:", error);
      alert("삭제 중 오류가 발생했습니다.");
    }
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) return
  try {
    await store.createComment(postId, newComment.value)
    newComment.value = ""
  } catch (error) {
    alert("로그인 후 이용해주세요.")
  }
}

const startEditComment = (comment) => {
  editingCommentId.value = comment.id
  editCommentContent.value = comment.content
}

const submitEditComment = async (commentId) => {
  if (!editCommentContent.value || !editCommentContent.value.trim()) {
    alert("댓글 내용을 입력해주세요.");
    return;
  }
  try {
    await store.updateComment(postId, commentId, editCommentContent.value);
    editingCommentId.value = null;
  } catch (error) {
    console.error("❌ 댓글 수정 실패", error);
    alert("댓글 수정에 실패했습니다.");
  }
};

const removeComment = async (commentId) => {
  if (confirm("댓글을 삭제하시겠습니까?")) {
    await store.deleteComment(postId, commentId)
  }
}

const handleLike = async () => {
  if (post.value) await store.toggleLike(post.value.id)
}
const goBack = () => {
  const category = post.value?.category?.toLowerCase() || "free"
  router.push(`/community/${category}`)
}
const formatDate = (dateStr) => {
  if (!dateStr) return ""
  const date = new Date(dateStr)
  return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일 ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
}

onMounted(async () => {
  try {
    if (!post.value) {
      await store.fetchPostDetail(postId)
    }

    if (!post.value) {
      alert("존재하지 않는 게시글입니다.")
      router.push('/community')
      return
    }

    await store.fetchComments(postId)
  } catch (error) {
    router.push('/community')
  }
})

</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

/* --- 기본 레이아웃 --- */
.page-layout { min-height: 100vh; background-color: #fcfdfd; position: relative; }
.bg-decoration { position: absolute; inset: 0; z-index: 0; pointer-events: none; }
.blob { position: absolute; filter: blur(100px); border-radius: 50%; opacity: 0.15; }
.blob-green { width: 600px; height: 600px; background: #22c55e; top: -100px; right: -100px; }
.blob-light { width: 500px; height: 500px; background: #e2e8f0; bottom: -100px; left: -100px; }

.detail-container { position: relative; z-index: 1; max-width: 800px; margin: 0 auto; padding: 120px 20px 100px; }
.detail-nav { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.back-link { display: flex; align-items: center; gap: 8px; background: none; border: none; color: #64748b; font-weight: 700; cursor: pointer; }

/* --- 게시글 카드 스타일 --- */
.post-card { background: white; border-radius: 32px; padding: 50px; box-shadow: 0 30px 60px rgba(0, 0, 0, 0.05); border: 1px solid #f1f5f9; }
.post-header { margin-bottom: 40px; border-bottom: 1px solid #f1f5f9; padding-bottom: 30px; }
.post-title { font-size: 2.5rem; font-weight: 900; color: #0f172a; line-height: 1.2; }
.post-meta { display: flex; align-items: center; gap: 16px; color: #94a3b8; }
.author-info { display: flex; align-items: center; gap: 8px; }
.avatar-mini { font-size: 1.2rem; }
.author-name { font-weight: 800; color: #1e293b; }
.meta-divider { width: 1px; height: 14px; background: #e2e8f0; }

.category-badge { padding: 6px 14px; border-radius: 10px; font-size: 0.75rem; font-weight: 900; text-transform: uppercase; }
.category-badge.restaurant { background: #f0fdf4; color: #22c55e; }
.category-badge.review { background: #eff6ff; color: #3b82f6; }
.category-badge.free { background: #f1f5f9; color: #475569; }

.content-text { font-size: 1.15rem; line-height: 1.8; color: #334155; white-space: pre-wrap; margin-bottom: 40px; }

/* --- 추가 정보 섹션 (식당/리뷰) --- */
.extra-info-section { margin-top: 40px; }
.extra-card { border-radius: 24px; padding: 30px; margin-bottom: 20px; border: 1px solid #f1f5f9; }
.extra-card.restaurant { background: #f8fafc; }

.extra-header { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
.extra-header h3 { font-size: 1.1rem; font-weight: 800; margin: 0; }
.extra-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.info-item strong { display: block; font-size: 0.8rem; color: #94a3b8; margin-bottom: 4px; }
.info-item span { font-weight: 700; color: #1e293b; }
.tag { color: #22c55e; }

/* ✅ 새로운 리뷰 UI (review-modern) */
.extra-card.review-modern {
  background: white; border: 1px solid #e2e8f0; box-shadow: 0 10px 30px rgba(0,0,0,0.03);
  text-align: center; padding: 40px 30px;
}

.review-badges {
  display: flex; justify-content: center; gap: 8px; margin-bottom: 30px;
}
.badge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 700;
}
.badge.period { background: #f1f5f9; color: #64748b; }
.badge.type { background: #e0f2fe; color: #0284c7; }
.badge .material-icons { font-size: 16px; }

.weight-display {
  display: flex; flex-direction: column; align-items: center; gap: 16px;
}
.weight-icon-circle {
  width: 64px; height: 64px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 32px;
}
.weight-icon-circle.loss { background: #ecfdf5; color: #10b981; }
.weight-icon-circle.gain { background: #fef2f2; color: #ef4444; }

.weight-text-group { display: flex; flex-direction: column; align-items: center; }
.label-text { font-size: 0.9rem; font-weight: 700; color: #94a3b8; margin-bottom: 4px; }
.value-text { font-size: 3.5rem; font-weight: 900; line-height: 1; letter-spacing: -1px; }
.value-text.loss-text { color: #10b981; }
.value-text.gain-text { color: #ef4444; }
.value-text .unit { font-size: 1.2rem; color: #94a3b8; font-weight: 700; margin-left: 4px; }

/* --- 하단 버튼 액션 --- */
.post-footer { margin-top: 50px; display: flex; justify-content: center; gap: 16px; padding-bottom: 40px; border-bottom: 1px solid #f1f5f9; }
.like-btn { display: flex; align-items: center; gap: 8px; padding: 14px 30px; border-radius: 20px; border: 1.5px solid #e2e8f0; background: white; cursor: pointer; font-weight: 800; transition: 0.3s; }
.like-btn.active { border-color: #22c55e; color: #22c55e; background: #f0fdf4; }

.delete-post-btn {
  display: flex; align-items: center; gap: 8px; padding: 14px 24px; border-radius: 20px;
  border: 1.5px solid #fee2e2; background: white; color: #ef4444; font-weight: 800;
  cursor: pointer; transition: 0.3s;
}
.delete-post-btn:hover { border-color: #ef4444; background: #fef2f2; transform: translateY(-3px); }

/* --- 댓글 섹션 --- */
.comment-section { margin-top: 40px; padding-top: 20px; }
.comment-header { margin-bottom: 24px; }
.header-left { display: flex; align-items: center; gap: 10px; }
.header-left h3 { font-size: 1.25rem; font-weight: 800; color: #1e293b; margin: 0; }
.comment-count { color: #22c55e; }

.comment-input-card { background: #ffffff; border: 2px solid #f1f5f9; border-radius: 20px; padding: 16px; margin-bottom: 40px; transition: all 0.3s ease; }
.comment-input-card:focus-within { border-color: #22c55e; box-shadow: 0 10px 20px rgba(34, 197, 94, 0.08); }
.styled-textarea { width: 100%; border: none; resize: none; outline: none; font-size: 1rem; line-height: 1.6; color: #334155; min-height: 80px; }

.input-actions { display: flex; justify-content: space-between; align-items: center; margin-top: 12px; padding-top: 12px; border-top: 1px solid #f8fafc; }
.guide-text { font-size: 0.85rem; color: #94a3b8; }

.comment-submit-btn {
  display: flex; align-items: center; gap: 8px; background: #0f172a; color: #ffffff;
  padding: 12px 24px; border-radius: 14px; border: none; font-weight: 800; cursor: pointer; transition: 0.3s;
}
.comment-submit-btn:hover:not(:disabled) { background: #22c55e; transform: translateY(-2px); box-shadow: 0 8px 16px rgba(34, 197, 94, 0.2); }
.comment-submit-btn:disabled { background: #e2e8f0; color: #94a3b8; cursor: not-allowed; }

/* --- 댓글 아이템 카드 --- */
.comment-card { position: relative; display: flex; justify-content: space-between; align-items: flex-start; padding: 24px; background: #f8fafc; border-radius: 20px; margin-bottom: 16px; transition: all 0.3s ease; }
.comment-card:hover { background: #f1f5f9; }
.comment-user-area { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.user-avatar-circle { width: 36px; height: 36px; background: #e2e8f0; color: #94a3b8; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.user-display-name { font-weight: 800; font-size: 0.95rem; color: #1e293b; }
.comment-timestamp { font-size: 0.75rem; color: #94a3b8; margin-left: 8px; }
.comment-text-body { padding-left: 48px; font-size: 1rem; line-height: 1.6; color: #475569; white-space: pre-wrap; }

/* 댓글 삭제 버튼 */
.comment-delete-icon-btn {
  display: flex; align-items: center; gap: 4px; background: #fff5f5; border: 1px solid #fee2e2;
  color: #ef4444; padding: 6px 12px; border-radius: 10px; cursor: pointer;
  transition: all 0.2s; font-size: 0.8rem; font-weight: 700;
}
.comment-delete-icon-btn:hover { background: #ef4444; color: #ffffff; border-color: #ef4444; }

/* ================= 수정 모드 UI 스타일 ================= */
.edit-label {
  display: block; font-size: 0.9rem; font-weight: 800; color: #94a3b8; margin-bottom: 6px;
}
.edit-title-input {
  width: 100%; font-size: 2.2rem; font-weight: 900; border: none;
  border-bottom: 2px solid #e2e8f0; outline: none; padding: 10px 0;
  transition: 0.2s;
}
.edit-title-input:focus { border-bottom-color: #22c55e; }

.edit-content-wrapper { margin-bottom: 20px; }
.edit-content-textarea {
  width: 100%; font-size: 1.1rem; line-height: 1.8; border: 1px solid #e2e8f0;
  border-radius: 12px; padding: 20px; outline: none; resize: none; background: #fcfdfd;
}
.edit-content-textarea:focus { border-color: #22c55e; }

/* 식당 정보 수정 그리드 */
.edit-grid {
  display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-top: 16px;
}
.input-group label {
  display: block; font-size: 0.8rem; font-weight: 700; color: #94a3b8; margin-bottom: 4px;
}
.custom-input.small, .custom-select.small {
  width: 100%; height: 42px; border: 1px solid #e2e8f0; border-radius: 10px;
  padding: 0 12px; font-size: 0.9rem; outline: none; box-sizing: border-box;
}
.custom-input.small:focus, .custom-select.small:focus { border-color: #22c55e; }

/* ✅ 숫자 입력창 화살표(Spinner) 제거 스타일 */
.custom-input.no-spinner::-webkit-outer-spin-button,
.custom-input.no-spinner::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
.custom-input.no-spinner {
  -moz-appearance: textfield;
}

.input-hint { font-size: 0.8rem; color: #94a3b8; margin-top: 12px; text-align: right; }

/* 하단 버튼 그룹 */
.author-actions { display: flex; gap: 10px; margin-left: auto; }
.edit-btn {
  display: flex; align-items: center; gap: 4px; padding: 10px 20px;
  border-radius: 14px; border: 1.5px solid #e2e8f0; background: white;
  color: #64748b; font-weight: 800; cursor: pointer; transition: 0.2s;
}
.edit-btn:hover { background: #f8fafc; border-color: #cbd5e1; }

.edit-actions-group { display: flex; gap: 12px; }
.save-btn { background: #0f172a; color: white; padding: 12px 24px; border-radius: 14px; border: none; font-weight: 800; cursor: pointer; }
.cancel-btn { background: #f1f5f9; color: #64748b; padding: 12px 24px; border-radius: 14px; border: none; font-weight: 800; cursor: pointer; }

/* 댓글 수정 UI 스타일 */
.comment-actions { display: flex; gap: 8px; align-items: center; }
.comment-mini-btn { background: none; border: none; color: #94a3b8; font-size: 0.8rem; font-weight: 700; cursor: pointer; }
.comment-mini-btn:hover { color: #22c55e; text-decoration: underline; }

.comment-edit-area { margin-top: 10px; }
.edit-mode { border: 1.5px solid #22c55e !important; background: #fff !important; }
.edit-btn-group { display: flex; gap: 8px; justify-content: flex-end; margin-top: 8px; }
.mini-save-btn { background: #22c55e; color: white; border: none; padding: 4px 12px; border-radius: 8px; font-weight: 700; cursor: pointer; }
.mini-cancel-btn { background: #f1f5f9; color: #94a3b8; border: none; padding: 4px 12px; border-radius: 8px; font-weight: 700; cursor: pointer; }

.empty-placeholder { text-align: center; padding: 60px 0; color: #cbd5e1; font-weight: 700; }
</style>