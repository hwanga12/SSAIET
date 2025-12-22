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
            <div class="logo-area" @click="goHome">
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
            
            <div class="visual-badge">
              <span class="material-icons">security</span>
              데이터는 암호화되어 안전하게 보관됩니다.
            </div>
          </div>
          <div class="visual-pattern"></div>
        </div>

        <div class="form-side">
          <div class="form-inner">
            <div class="form-header">
              <h3 class="form-title">Profile Setup</h3>
              <p class="form-subtitle">더 정확한 추천을 위해 상세 정보를 입력해주세요.</p>
            </div>
            
            <div class="form-wrapper">
              <ProfileForm />
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router"
import ProfileForm from "@/components/auth/ProfileForm.vue"

const router = useRouter()
const goHome = () => router.push("/")
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.setup-page {
  position: relative;
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fcfdfd;
  padding: 40px 20px;
}

/* ===== 배경 장식 ===== */
.bg-decoration {
  position: absolute;
  inset: 0;
  z-index: 0;
}
.blob {
  position: absolute;
  filter: blur(120px);
  border-radius: 50%;
  opacity: 0.2;
}
.blob-green { width: 600px; height: 600px; background: #22c55e; top: -100px; right: -100px; }
.blob-light { width: 500px; height: 500px; background: #e2e8f0; bottom: -100px; left: -100px; }

/* ===== 카드 레이아웃 ===== */
.setup-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1100px;
}

.setup-card {
  display: flex;
  background: white;
  border-radius: 40px;
  border: 1px solid rgba(0,0,0,0.05);
  box-shadow: 0 40px 100px rgba(0, 0, 0, 0.08);
  min-height: 800px; /* 입력 필드가 많으므로 높이를 여유있게 설정 */
  overflow: hidden;
}

/* --- 왼쪽 비주얼 영역 --- */
.visual-side {
  flex: 1;
  background: #f8fafc;
  padding: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  border-right: 1px solid #f1f5f9;
}

.logo-text { font-size: 22px; font-weight: 900; color: #22c55e; letter-spacing: 4px; cursor: pointer; }
.visual-title { font-size: 3.5rem; font-weight: 900; color: #0f172a; line-height: 1.1; margin: 30px 0; letter-spacing: -2px; }
.highlight { color: #22c55e; }
.visual-text { font-size: 1.2rem; color: #64748b; line-height: 1.7; margin-bottom: 40px; }

.visual-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #94a3b8;
  background: #fff;
  padding: 12px 20px;
  border-radius: 12px;
  width: fit-content;
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

/* --- 오른쪽 폼 영역 --- */
.form-side {
  flex: 1.2;
  background: white;
  padding: 60px;
  display: flex;
  align-items: flex-start; /* 스크롤 가능성을 위해 상단 정렬 */
  justify-content: center;
}

.form-inner {
  width: 100%;
  max-width: 440px;
}

.form-header {
  margin-bottom: 40px;
}

.form-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: #0f172a;
  margin-bottom: 8px;
}

.form-subtitle {
  font-size: 1rem;
  color: #64748b;
  line-height: 1.5;
}

.form-wrapper {
  /* ProfileForm.vue 내부의 스타일과 결합됩니다 */
}

/* 애니메이션 */
.setup-card {
  animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 1024px) {
  .setup-card { flex-direction: column; height: auto; }
  .visual-side { padding: 40px; }
  .form-side { padding: 40px 20px; }
}
</style>