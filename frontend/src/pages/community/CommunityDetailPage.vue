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
            <input 
              v-model="editPostData.title" 
              class="edit-title-input" 
              placeholder="제목을 입력하세요"
            />
          </div>
        </header>

        <section class="post-body">
          <p v-if="!isEditingPost" class="content-text">{{ post.content }}</p>
          <textarea 
            v-else 
            v-model="editPostData.content" 
            class="edit-content-textarea" 
            rows="10"
          ></textarea>
        </section>

        <section v-if="hasExtraInfo && !isEditingPost" class="extra-info-section">
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
              <button class="save-btn" @click="submitEditPost">저장하기</button>
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

          <div class="comment-input-card">
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
// 1. 모든 도구들을 먼저 가져옵니다 (Import)
import { ref, reactive, computed, onMounted } from "vue" 
import { useRoute, useRouter } from "vue-router"
import { useCommunityStore } from "@/stores/community"
import BaseNavbar from "@/components/common/BaseNavbar.vue"

// 2. 외부 도구 설정
const route = useRoute()
const router = useRouter()
const store = useCommunityStore()
const postId = Number(route.params.id)

// 3. 상태 변수 선언 (데이터 보관함)
const isEditingPost = ref(false)
const editPostData = reactive({ title: "", content: "" })
const editingCommentId = ref(null)
const editCommentContent = ref("")
const newComment = ref("")

// 4. 데이터 계산 로직 (Computed)
const post = computed(() => store.posts.find(p => p.id === postId))
const comments = computed(() => store.comments || [])
const isLiked = computed(() => post.value?.is_liked || false)
const hasExtraInfo = computed(() => {
  if (!post.value) return false
  return ['RESTAURANT', 'REVIEW'].includes(post.value.category)
})

const startEditPost = () => {
  if (!post.value) return
  editPostData.title = post.value.title
  editPostData.content = post.value.content
  isEditingPost.value = true
}
// 5. 게시글 관련 함수 (수정/삭제)
const submitEditPost = async () => {
  if (!post.value) return;
  if (!editPostData.title.trim() || !editPostData.content.trim()) {
    alert("제목과 내용을 입력해주세요.");
    return;
  }

  try {
    // ✅ 서버 검증을 통과하기 위해 데이터가 있는 것만 전송하거나 구조를 맞춤
    const payload = {
      title: editPostData.title,
      content: editPostData.content,
      category: post.value.category,
    };

    // 데이터가 존재할 때만 포함 (null 대신 실제 객체 전송)
    if (post.value.restaurant_info) payload.restaurant_info = post.value.restaurant_info;
    if (post.value.review_info) payload.review_info = post.value.review_info;
    if (post.value.question_info) payload.question_info = post.value.question_info;

    console.log("최종 전송 payload:", payload);

    await store.updatePost(postId, payload);
    
    isEditingPost.value = false;
    alert("게시글이 성공적으로 수정되었습니다.");
  } catch (error) {
    // 상세 에러 내용을 더 자세히 출력해서 확인
    console.error("❌ 수정 실패 원인:", error.response?.data);
    alert("수정 실패: 입력 데이터를 확인해주세요.");
  }
};


const handleDeletePost = async () => {
  if (confirm("정말 이 게시물을 삭제하시겠습니까?")) {
    try {
      // 1. 이동할 경로를 미리 변수에 저장 (삭제 후에는 post.value가 사라질 수 있음)
      const targetCategory = post.value?.category?.toLowerCase() || 'free';
      
      // 2. 삭제 실행
      await store.deletePost(postId);
      
      // 3. 성공 시 즉시 이동 (다른 요청이 가기 전에)
      alert("게시글이 삭제되었습니다.");
      router.push(`/community/${targetCategory}`);
    } catch (error) {
      // 서버에서 이미 지워졌는데 404가 난 경우라면 에러로 처리하지 않음
      if (error.response?.status === 404) {
          router.push('/community');
          return;
      }
      console.error("삭제 실패 상세:", error);
      alert("삭제 중 오류가 발생했습니다.");
    }
  }
}

// 6. 댓글 관련 함수 (등록/수정/삭제)
const submitComment = async () => {
  if (!newComment.value.trim()) return
  try {
    await store.createComment(postId, newComment.value)
    newComment.value = ""
  } catch (error) {
    alert("댓글 등록 실패")
  }
}

const startEditComment = (comment) => {
  editingCommentId.value = comment.id
  editCommentContent.value = comment.content
}

const submitEditComment = async (commentId) => {
  // 1. 함수 호출 여부 확인
  console.log("=== 댓글 수정 시작 ===");
  console.log("전달받은 commentId:", commentId);
  console.log("게시글 ID(postId):", postId);
  console.log("수정할 내용(editCommentContent):", editCommentContent.value);

  // 2. 유효성 검사 로그
  if (!editCommentContent.value || !editCommentContent.value.trim()) {
    console.warn("내용이 비어있어 수정을 중단합니다.");
    alert("댓글 내용을 입력해주세요.");
    return;
  }

  try {
    console.log("3. store.updateComment 호출 시도 중...");
    
    // API 호출
    const result = await store.updateComment(postId, commentId, editCommentContent.value);
    
    console.log("4. 서버 응답 결과:", result);

    // 성공 시 상태 초기화
    editingCommentId.value = null;
    console.log("5. 수정 모드 종료 완료");
    
  } catch (error) {
    // 🚨 에러 상세 출력
    console.error("❌ 댓글 수정 중 에러 발생!");
    
    if (error.response) {
      // 서버가 에러 코드를 반환한 경우 (400, 404, 405, 500 등)
      console.error("서버 응답 에러 데이터:", error.response.data);
      console.error("HTTP 상태 코드:", error.response.status);
    } else if (error.request) {
      // 요청은 보냈으나 응답을 아예 못 받은 경우 (네트워크 에러 등)
      console.error("서버로부터 응답을 받지 못했습니다.");
    } else {
      // 코드 자체에 문제가 있는 경우 (오타 등)
      console.error("에러 메시지:", error.message);
    }
    
    alert("댓글 수정에 실패했습니다. 콘솔을 확인해주세요.");
  }
};

const removeComment = async (commentId) => {
  if (confirm("댓글을 삭제하시겠습니까?")) {
    await store.deleteComment(postId, commentId)
  }
}

// 7. 기타 기능 (좋아요, 뒤로가기, 날짜)
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

// CommunityDetailPage.vue 의 onMounted 수정
onMounted(async () => {
  try {
    // 1. 일단 전체 목록을 불러오거나 단일 게시글 정보를 불러옵니다.
    if (store.posts.length === 0) await store.fetchPosts();
    
    // 2. 불러온 뒤에도 현재 postId에 해당하는 글이 없다면?
    if (!post.value) {
      alert("존재하지 않는 게시글입니다.");
      router.push('/community'); // 또는 404 페이지로 이동
      return;
    }

    // 3. 글이 있을 때만 댓글 로드
    await store.fetchComments(postId);
  } catch (error) {
    console.error("데이터 로딩 중 에러:", error);
    router.push('/community');
  }
});
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
.extra-card.review { background: #f0fdf4; border-color: #dcfce7; }
.extra-header { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
.extra-header h3 { font-size: 1.1rem; font-weight: 800; margin: 0; }
.extra-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.info-item strong { display: block; font-size: 0.8rem; color: #94a3b8; margin-bottom: 4px; }
.info-item span { font-weight: 700; color: #1e293b; }
.tag { color: #22c55e; }

.review-stats { display: flex; gap: 16px; }
.stat-box { flex: 1; padding: 16px; background: white; border-radius: 16px; text-align: center; }
.stat-box.accent { background: #22c55e; color: white; }
.stat-box.accent .stat-label { color: rgba(255,255,255,0.8); }
.stat-label { font-size: 0.8rem; font-weight: 700; color: #94a3b8; display: block; margin-bottom: 4px; }
.stat-value { font-size: 1.1rem; font-weight: 900; }

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

.empty-placeholder { text-align: center; padding: 60px 0; color: #cbd5e1; }
.empty-bg { font-size: 3rem; margin-bottom: 12px; }

/* 애니메이션 */
.comment-list-enter-active, .comment-list-leave-active { transition: all 0.4s ease; }
.comment-list-enter-from, .comment-list-leave-to { opacity: 0; transform: translateX(30px); }

/* 게시글 수정 UI 스타일 */
.edit-title-input {
  width: 100%; font-size: 2.5rem; font-weight: 900; border: none;
  border-bottom: 2px solid #22c55e; outline: none; padding: 10px 0; margin-bottom: 20px;
}
.edit-content-textarea {
  width: 100%; font-size: 1.15rem; line-height: 1.8; border: 1px solid #e2e8f0;
  border-radius: 12px; padding: 20px; outline: none; resize: none; background: #fcfdfd;
}

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
</style>