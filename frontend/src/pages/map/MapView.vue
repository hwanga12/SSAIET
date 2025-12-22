<template>
  <div class="map-layout">
    <BaseNavbar class="nav-fixed" />

    <div class="bg-decoration">
      <div class="blob blob-green"></div>
      <div class="blob blob-light"></div>
    </div>

    <main class="map-page">
      <div class="container">
        <header class="page-header">
          <div class="header-text">
            <div class="icon-circle">
              <span class="material-icons">near_me</span>
            </div>
            <div class="title-group">
              <h1>주변 <span class="highlight">추천</span> 식당</h1>
              <p>싸피생의 건강을 책임질 주변 맛집을 찾아보세요.</p>
            </div>
          </div>
          
          <div class="header-actions">
            <div class="location-badge">
              <span class="material-icons">location_on</span>
              <span>SSAFY 멀티 캠퍼스 주변</span>
            </div>
          </div>
        </header>

        <section class="map-section">
          <div class="map-inner">
            <KakaoMap />
          </div>
        </section>

        <footer class="map-footer">
          <span class="material-icons">info</span>
          <p>지도를 움직여 더 많은 식당을 찾아보세요. 마커를 클릭하면 상세 정보를 확인할 수 있습니다.</p>
        </footer>
      </div>
    </main>
  </div>
</template>

<script setup>
import BaseNavbar from '@/components/common/BaseNavbar.vue'
import KakaoMap from '@/components/map/KakaoMap.vue'
</script>

<style scoped>
@import url("https://fonts.googleapis.com/icon?family=Material+Icons");

.map-layout {
  min-height: 100vh;
  background-color: #f8fafc; /* 눈이 편한 미색 */
  position: relative;
  overflow-x: hidden;
}

/* ✅ 배경 데코레이션 */
.bg-decoration {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}
.blob {
  position: absolute;
  filter: blur(120px);
  border-radius: 50%;
  opacity: 0.07;
}
.blob-green {
  width: 500px; height: 500px;
  background: #22c55e;
  top: -50px; right: -100px;
}
.blob-light {
  width: 400px; height: 400px;
  background: #94a3b8;
  bottom: -50px; left: -100px;
}

.nav-fixed {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
}

.map-page {
  position: relative;
  z-index: 1;
  padding: 60px 0 100px;
}

.container {
  max-width: 1100px; /* 커뮤니티 페이지와 통일 */
  margin: 0 auto;
  padding: 0 20px;
}

/* ================= HEADER ================= */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}

.header-text {
  display: flex;
  align-items: center;
  gap: 20px;
}

.icon-circle {
  width: 56px;
  height: 56px;
  background: white;
  color: #22c55e;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 20px rgba(0,0,0,0.04);
  border: 1px solid #f1f5f9;
}

.title-group h1 {
  font-size: 2.2rem;
  font-weight: 900;
  color: #1e293b;
  margin: 0;
  letter-spacing: -1.5px;
}

.highlight { color: #22c55e; }

.title-group p {
  color: #64748b;
  font-size: 1rem;
  margin-top: 4px;
  font-weight: 500;
}

.location-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #f1f5f9;
  padding: 8px 16px;
  border-radius: 12px;
  color: #475569;
  font-weight: 700;
  font-size: 0.9rem;
}

/* ================= MAP SECTION ================= */
.map-section {
  background: white;
  border-radius: 32px; /* 더 둥글게 */
  padding: 12px; /* 지도 주변에 살짝 액자 느낌의 여백 */
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.06);
  border: 1px solid #f1f5f9;
  transition: transform 0.3s ease;
}

.map-inner {
  border-radius: 24px;
  overflow: hidden;
  height: 600px; /* 지도 높이 확보 */
}

/* ================= FOOTER ================= */
.map-footer {
  margin-top: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #94a3b8;
  font-size: 0.9rem;
}

.map-footer .material-icons {
  font-size: 1.2rem;
}
</style>