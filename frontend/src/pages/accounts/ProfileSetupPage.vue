<template>
  <div class="setup-page">
    <div class="bg-decoration">
      <div class="blob blob-green"></div>
      <div class="blob blob-light"></div>
    </div>

    <div class="setup-container">
      <div class="setup-card">
        <div class="visual-side">
          <div class="visual-content">
            <div class="logo-area" @click="handleCancel">
              <span class="logo-text">SSAIET</span>
            </div>
            <h2 class="visual-title">
              Complete Your<br />
              <span class="highlight">Analysis</span>.
            </h2>
            <p class="visual-text">
              정확한 인적사항을 입력해주시면<br />
              싸피 생활에 딱 맞는 <strong>맞춤형 식단</strong>과<br />
              <strong>건강 분석 리포트</strong>를 제공해드려요.
            </p>
          </div>
        </div>

        <div class="form-side">
          <div class="form-inner">
            <div class="form-header">
              <div class="step-indicator">마지막 단계예요! 🥗</div>
              <h3 class="form-title">Profile Setup</h3>
              <p class="form-subtitle">정확한 분석을 위해 필수 정보를 입력해주세요.</p>
            </div>
            
            <ProfileForm @saved="isSubmitted = true" />

            <div class="button-group">
              <button type="button" class="cancel-btn" @click="handleCancel">
                나중에 할래요 (로그아웃)
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter, onBeforeRouteLeave } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import ProfileForm from "@/components/auth/ProfileForm.vue" // 경로 확인 필요

const router = useRouter()
const authStore = useAuthStore()
const isSubmitted = ref(false)

// ⭐ [핵심] 페이지 이탈 방지 가드
onBeforeRouteLeave((to, from, next) => {
  if (isSubmitted.value) {
    next() // 저장 완료 시 통과
  } else {
    const leaveWarning = window.confirm(
      "잠시만요! 😢 지금 프로필 설정을 중단하시면 서비스를 이용하실 수 없어요.\n정말로 나중에 하시겠어요? (지금 나가시면 로그아웃됩니다.)"
    )
    
    if (leaveWarning) {
      authStore.logOut() // 이탈 시 로그아웃 처리
      next()
    } else {
      next(false) // 취소 시 잔류
    }
  }
})

// 취소 버튼 클릭 시
const handleCancel = () => {
  const cancelConfirm = window.confirm("설정을 중단하고 로그아웃 하시겠습니까?\n작성 중인 내용은 저장되지 않으며 로그인 페이지로 이동합니다.")
  if (cancelConfirm) {
    authStore.logOut()
    router.replace("/login")
  }
}
</script>

<style scoped>
/* 기존 스타일 유지하되 폼 관련 스타일은 ProfileForm으로 이동했으므로 필요 없는 부분 삭제 */
.setup-page { position: relative; width: 100%; min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #fcfdfd; padding: 40px 20px; }
.bg-decoration { position: absolute; inset: 0; z-index: 0; }
.blob { position: absolute; filter: blur(120px); border-radius: 50%; opacity: 0.2; }
.blob-green { width: 600px; height: 600px; background: #22c55e; top: -100px; right: -100px; }
.blob-light { width: 500px; height: 500px; background: #e2e8f0; bottom: -100px; left: -100px; }

.setup-container { position: relative; z-index: 1; width: 100%; max-width: 1050px; }
.setup-card { display: flex; background: white; border-radius: 40px; border: 1px solid rgba(0,0,0,0.05); box-shadow: 0 40px 100px rgba(0, 0, 0, 0.08); overflow: hidden; min-height: 700px; }

.visual-side { flex: 0.9; background: #f8fafc; padding: 60px; display: flex; flex-direction: column; justify-content: center; border-right: 1px solid #f1f5f9; }
.logo-text { font-size: 22px; font-weight: 900; color: #22c55e; letter-spacing: 4px; cursor: pointer; }
.visual-title { font-size: 3.2rem; font-weight: 900; color: #0f172a; line-height: 1.1; margin: 25px 0; letter-spacing: -2px; }
.highlight { color: #22c55e; }
.visual-text { font-size: 1.1rem; color: #64748b; line-height: 1.6; }

.form-side { flex: 1.1; background: white; padding: 50px 70px; display: flex; align-items: center; }
.form-inner { width: 100%; }
.form-header { margin-bottom: 25px; }
.step-indicator { color: #22c55e; font-weight: 800; font-size: 13px; margin-bottom: 5px; }
.form-title { font-size: 2.2rem; font-weight: 900; color: #0f172a; }

.button-group { display: flex; flex-direction: column; gap: 10px; margin-top: 15px; }
.cancel-btn { padding: 12px; background: none; border: none; color: #94a3b8; font-size: 14px; font-weight: 600; cursor: pointer; text-decoration: underline; transition: 0.2s; width: 100%; }
.cancel-btn:hover { color: #64748b; }
</style>