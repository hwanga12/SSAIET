<template>
  <div class="map-layout">
    <BaseNavbar class="nav-fixed" />
    <main class="map-page">
      <div class="map-container">
        <header class="page-header">
          <div class="header-left">
            <div class="icon-circle"><span class="material-icons">near_me</span></div>
            <div class="title-group">
              <h1>주변 <span class="highlight">추천</span> 식당</h1>
              <p>싸피생의 건강을 책임질 주변 맛집!</p>
            </div>
          </div>
          <div class="location-badge">
            <span class="material-icons">location_on</span> SSAFY 멀티캠퍼스 역삼
          </div>
        </header>

        <div class="map-content-wrapper">
          <section class="map-section full-width">
            <div class="map-inner">
              <KakaoMap ref="kakaoMapRef" />
            </div>
          </section>
        </div>

        <footer class="map-footer">
          <span class="material-icons">info</span>
          <p>지도를 움직이거나 오른쪽 리스트를 통해 맛집을 탐색해보세요.</p>
        </footer>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BaseNavbar from '@/components/common/BaseNavbar.vue'
import KakaoMap from '@/components/map/KakaoMap.vue'

const kakaoMapRef = ref(null)
</script>

<style scoped>
.map-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 네브바 아래 실제 콘텐츠 영역 */
.map-page {
  flex: 1;
  background: #f8fafc;
  padding: 32px;
  padding-top: 96px; /* ⭐ 네비 높이 + 여유 */
  display: flex;
  justify-content: center;
}


.map-container {
  width: 100%;
  max-width: 1200px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ===== Header ===== */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0; /* ⭐ 절대 줄어들지 않게 */
}

.header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.icon-circle {
  width: 44px;
  height: 44px;
  background: #22c55e;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.title-group h1 {
  font-size: 24px;
  font-weight: 800;
  margin: 0;
  color: #1e293b;
}

.title-group p {
  margin: 4px 0 0;
  font-size: 14px;
  color: #64748b;
}

.highlight {
  color: #22c55e;
}

.location-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: white;
  border-radius: 12px;
  font-weight: 700;
  font-size: 14px;
  color: #475569;
  border: 1px solid #e2e8f0;
}

/* ===== Map ===== */
.map-section {
  flex: 1;           /* ⭐ 남은 공간을 지도에 */
  min-height: 420px; /* ⭐ 너무 작아지는 것 방지 */
}

.map-inner {
  height: 100%;
  background: white;
  border-radius: 28px;
  overflow: hidden;
  border: 1px solid #f1f5f9;
  box-shadow: 0 20px 40px rgba(0,0,0,0.06);
}

/* ===== Footer ===== */
.map-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: #94a3b8;
  font-size: 0.9rem;
  flex-shrink: 0;
}

</style>