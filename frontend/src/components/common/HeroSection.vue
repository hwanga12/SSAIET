<template>
  <section class="hero">
    <div class="hero-inner">

      <!-- 이미지 -->
      <div class="hero-right">
        <div class="image-overlay"></div>
        <img :src="imageSrc" alt="hero" />
      </div>

      <!-- 텍스트 -->
      <div class="hero-left">
        <h1 class="hero-title">
          SSAFY생을 위한 플래너<br />
          <span class="hero-title-accent">SSAIET</span> 입니다
        </h1>

        <p class="hero-desc">
          {{ userName }}님 환영합니다.<br />
          건강한 SSAFY 생활을 위해 만들어진<br />
          똑똑한 건강 관리 파트너입니다.
        </p>

        <!-- <button class="hero-btn">
          오늘 식단 추천 받기
        </button> -->
      </div>

    </div>
  </section>
</template>

<script setup>
defineProps({
  userName: String,
  imageSrc: String,
})
</script>

<style scoped>
/* 바깥 영역 */
.hero {
  padding: 40px;
  background: #f9fafb;
}

/* 🔥 완전 고정 카드 */
.hero-inner {
  position: relative;
  width: 1280px;
  height: 420px;
  margin: 0 auto;

  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  overflow: hidden;
}

/* 🔥 텍스트 영역 */
.hero-left {
  position: absolute;
  top: 15px;
  left: 0;

  width: 520px;
  padding-left: 64px;

  z-index: 10;

  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 제목 */
.hero-title {
  font-size: 42px;
  font-weight: 800;
  line-height: 1.22;
  color: #111827;

  letter-spacing: -0.025em;   /* 🔥 세련된 자간 */
}

/* SSAIET 강조 */
.hero-title-accent {
  background: linear-gradient(
  90deg,
  rgb(187, 201, 110)
);

  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 설명 */
.hero-desc {
  font-size: 17px;
  line-height: 1.75;
  color: #374151;

  max-width: 460px;           /* 🔥 줄 길이 제한 */
}

/* 버튼 (그대로 유지) */
.hero-btn {
  margin-top: 12px;

  padding: 14px 28px;
  font-size: 16px;

  background: #2563eb;
  color: white;
  border-radius: 8px;
  font-weight: 600;
  border: none;
  cursor: pointer;

  align-self: flex-start;
  white-space: nowrap;
}

/* 🔥 이미지 영역 */
.hero-right {
  position: absolute;
  top: 0;
  right: 0;

  width: 760px;
  height: 100%;
}

/* 이미지 */
.hero-right img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 🔥 왼쪽 페이드 오버레이 */
.image-overlay {
  position: absolute;
  inset: 0;

  z-index: 5;
  pointer-events: none;

  background: linear-gradient(
    to right,
    rgba(255, 255, 255, 0.95) 0%,
    rgba(255, 255, 255, 0.85) 30%,
    rgba(255, 255, 255, 0.4) 55%,
    rgba(255, 255, 255, 0) 70%
  );
}
</style>