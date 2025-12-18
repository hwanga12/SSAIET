<template>
  <section class="hero-section">
    <div class="bg-decoration">
      <div class="blob blob-green"></div>
      <div class="blob blob-black"></div>
    </div>

    <div class="hero-container">
      <div class="hero-card">
        
        <div class="content-side">
          <div class="badge-wrapper">
            <span class="top-badge">Only for SSAFY</span>
          </div>
          
          <h1 class="hero-main-title">
            당신의 스마트한<br />
            식단 파트너,
            <span class="brand-green">SSAIET</span>
          </h1>

          <p class="hero-sub-text">
            <template v-if="isLoggedIn">
              <strong>{{ userName }}</strong>님, 환영합니다.<br />
              오늘의 최적화된 식단을 확인해보세요.
            </template>
            <template v-else>
              SSAFY에서의 바쁜 하루, 건강은 SSAIET이 책임집니다.<br />
              맞춤형 <strong>식단 · 영양 · 관리</strong>의 시작.
            </template>
          </p>

          <div class="action-group">
            <template v-if="isLoggedIn">
              <button class="primary-btn black-btn" @click="$emit('goRecommend')">
                <span class="material-icons">restaurant</span>
                식단 추천 받기
              </button>
            </template>
            <template v-else>
              <button class="primary-btn green-btn" @click="$emit('goSignup')">시작하기</button>
              <button class="primary-btn black-btn" @click="$emit('goLogin')">로그인</button>
            </template>
          </div>
        </div>

        <div class="image-side">
          <div class="image-wrapper">
            <img 
              :src="imageSrc || 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&q=80'" 
              alt="hero-image" 
              class="main-img" 
            />
            <div class="image-overlay"></div>
          </div>
          
          <div class="floating-badge">
            <div class="icon-box">🥗</div>
            <div class="text-box">
              <span class="label">Healthy Life</span>
              <span class="val">SSAIET Balance</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  userName: String,
  imageSrc: String,
  isLoggedIn: Boolean,
})
defineEmits(["goLogin", "goSignup", "goRecommend"])
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.hero-section {
  position: relative;
  width: 100%;
  min-height: 700px;
  max-height: 900px; 
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  padding: 40px 20px;
  overflow: hidden;
}

/* 배경 장식 */
.bg-decoration {
  position: absolute;
  inset: 0;
  z-index: 0;
}
.blob {
  position: absolute;
  filter: blur(120px);
  border-radius: 50%;
  opacity: 0.3;
}
.blob-green {
  width: 600px; height: 600px;
  background: #22c55e;
  top: -200px; left: -100px;
}
.blob-black {
  width: 500px; height: 500px;
  background: #0f172a;
  bottom: -150px; right: -50px;
}

.hero-container {
  width: 100%;
  max-width: 1200px; /* 카드가 커짐에 따라 컨테이너도 살짝 확장 */
  z-index: 1;
}

.hero-card {
  display: flex;
  background: #ffffff;
  border-radius: 40px;
  border: 1px solid #f1f5f9;
  box-shadow: 0 40px 80px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  height: 600px; /* 높이를 540에서 600으로 키움 */
}

/* --- 왼쪽 콘텐츠 --- */
.content-side {
  flex: 1; /* 이미지 비중을 위해 1.2에서 1로 조정 */
  padding: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  z-index: 2;
  background: white; /* 이미지가 겹칠 때 글씨 가독성 확보 */
}

.top-badge {
  background: #f1f5f9;
  color: #0f172a;
  padding: 7px 16px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 800;
}

.hero-main-title {
  font-size: 3.5rem;
  font-weight: 900;
  line-height: 1.1;
  color: #0f172a;
  margin: 25px 0;
  letter-spacing: -2px;
}

.brand-green {
  color: #22c55e;
  display: block;
}

.hero-sub-text {
  font-size: 1.15rem;
  line-height: 1.6;
  color: #64748b;
  margin-bottom: 40px;
}

/* --- 버튼 --- */
.action-group {
  display: flex;
  gap: 15px;
}

.primary-btn {
  padding: 16px 32px;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 800;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.2s ease-out;
}

.green-btn { background: #22c55e; color: white; box-shadow: 0 10px 20px rgba(34, 197, 94, 0.2); }
.green-btn:hover { background: #16a34a; transform: translateY(-3px); }

.black-btn { background: #0f172a; color: white; box-shadow: 0 10px 20px rgba(15, 23, 42, 0.2); }
.black-btn:hover { background: #1e293b; transform: translateY(-3px); }

/* --- 🔥 오른쪽 이미지 (비중 대폭 확대) --- */
.image-side {
  flex: 1.4; /* 1에서 1.4로 키워 이미지가 압도적으로 보이게 함 */
  position: relative;
  overflow: hidden;
}

.image-wrapper {
  width: 100%;
  height: 100%;
}

.main-img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 이미지가 잘리지 않고 꽉 차게 */
  transition: transform 0.5s ease;
}

.hero-card:hover .main-img {
  transform: scale(1.05); /* 호버 시 이미지 확대 효과 */
}

.image-overlay {
  position: absolute;
  inset: 0;
  /* 왼쪽 콘텐츠에서 이미지로 넘어갈 때 더 부드럽게 페이드 */
  background: linear-gradient(to right, #ffffff 0%, rgba(255, 255, 255, 0) 20%);
}

.floating-badge {
  position: absolute;
  bottom: 40px;
  right: 40px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 18px 28px;
  border-radius: 24px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.icon-box { font-size: 28px; }
.text-box .label { display: block; font-size: 12px; color: #94a3b8; font-weight: 700; }
.text-box .val { font-size: 16px; font-weight: 900; color: #0f172a; }

/* 반응형 */
@media (max-width: 1100px) {
  .hero-main-title { font-size: 2.8rem; }
  .hero-card { height: 550px; }
}

@media (max-width: 850px) {
  .hero-card { flex-direction: column; height: auto; }
  .image-side { height: 350px; order: -1; }
  .image-overlay {
    background: linear-gradient(to top, #ffffff 0%, transparent 30%);
  }
  .content-side { padding: 40px; text-align: center; align-items: center; }
  .action-group { width: 100%; justify-content: center; }
}
</style>