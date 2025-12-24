<template>
  <div class="kakao-map-container">
    <div id="map" class="map-canvas"></div>

    <button class="sidebar-toggle-btn" @click="isListOpen = !isListOpen">
      <span class="material-icons">{{ isListOpen ? 'chevron_left' : 'menu' }}</span>
    </button>

    <Transition name="slide-side">
      <div v-show="isListOpen" class="side-overlay">
        
        <div class="control-header">
          <div class="mode-switch">
            <button 
              :class="['mode-btn', { active: !isSearchMode }]" 
              @click="isSearchMode = false"
            >카테고리</button>
            <button 
              :class="['mode-btn', { active: isSearchMode }]" 
              @click="isSearchMode = true"
            >검색</button>
          </div>
        </div>

        <div v-if="!isSearchMode" class="category-scroll">
          <button 
            v-for="cat in categories" 
            :key="cat.code" 
            :class="['cat-btn', { active: selectedCat === cat.code }]"
            @click="filterByCategory(cat.code)"
          >
            {{ cat.name }}
          </button>
        </div>

        <div v-else class="search-area">
          <div class="search-box">
            <input 
              v-model="searchKeyword" 
              placeholder="장소, 맛집 검색 (Enter)" 
              @keyup.enter="performSearch"
            />
            <button @click="performSearch">
              <span class="material-icons">search</span>
            </button>
          </div>
        </div>

        <div class="list-wrapper" id="list-scroll">
          <div v-if="placeList.length === 0" class="no-data">
            {{ isSearchMode ? '검색 결과가 없습니다.' : '주변 맛집 탐색 중...' }}
          </div>
          <div 
            v-for="(item, idx) in placeList" 
            :key="idx" 
            class="recommend-card"
            @click="focusPlace(item)"
          >
            <div class="card-num">{{ idx + 1 }}</div>
            <div class="card-content">
              <div class="card-top">
                <span class="tag">{{ item.category_name.split(' > ').pop() }}</span>
                <span class="dist">{{ item.distance ? item.distance + 'm' : '' }}</span>
              </div>
              <h3 class="place-name">{{ item.place_name }}</h3>
              <p class="place-addr">{{ item.road_address_name || item.address_name }}</p>
              <a :href="item.place_url" target="_blank" class="review-link" @click.stop>
                평점/리뷰 <span class="material-icons">chevron_right</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <button class="re-center-btn" @click="goBackToCampus">
      <div class="btn-icon"><span class="material-icons">near_me</span></div>
      <span>멀캠 중심으로</span>
    </button>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";

const placeList = ref([]);
const selectedCat = ref("FD6");
const categories = [
  { name: "전체", code: "FD6" },
  { name: "한식", code: "한식" },
  { name: "일식", code: "일식" },
  { name: "카페", code: "CE7" },
];

// ✅ 추가된 상태 변수들
const isListOpen = ref(true); // 리스트 패널 열림/닫힘
const isSearchMode = ref(false); // 검색 모드 여부
const searchKeyword = ref(""); // 검색어

let map, ps, markers = [], infowindow, campusOverlay;
const CAMPUS_POS = { lat: 37.501286, lng: 127.039603 };

// 기존 로직: 카테고리 필터
const filterByCategory = (code) => {
  selectedCat.value = code;
  const options = { 
    location: new kakao.maps.LatLng(CAMPUS_POS.lat, CAMPUS_POS.lng), 
    radius: 700, 
    sort: kakao.maps.services.SortBy.DISTANCE 
  };
  code === "FD6" || code === "CE7" ? ps.categorySearch(code, searchCB, options) : ps.keywordSearch(code, searchCB, options);
};

// ✅ 추가 로직: 키워드 검색 실행
const performSearch = () => {
  if (!searchKeyword.value.trim()) {
    alert("검색어를 입력해주세요.");
    return;
  }
  // 검색 시에는 지도 중심 기준으로 검색하거나, 멀캠 중심으로 검색 (여기선 멀캠 중심 유지)
  const options = {
    location: new kakao.maps.LatLng(CAMPUS_POS.lat, CAMPUS_POS.lng),
    radius: 1000, // 검색은 반경을 좀 더 넓게 1km
    sort: kakao.maps.services.SortBy.DISTANCE 
  };
  ps.keywordSearch(searchKeyword.value, searchCB, options);
};

const searchCB = (data, status) => {
  if (status === kakao.maps.services.Status.OK) {
    displayPlaces(data);
    const scrollContainer = document.getElementById('list-scroll');
    if(scrollContainer) scrollContainer.scrollTop = 0;
  } else {
    placeList.value = [];
    clearMarkers();
  }
};

const clearMarkers = () => { markers.forEach(m => m.setMap(null)); markers = []; };

const displayPlaces = (data) => {
  clearMarkers();
  placeList.value = data;
  data.forEach(place => {
    const marker = new kakao.maps.Marker({
      map,
      position: new kakao.maps.LatLng(place.y, place.x)
    });
    markers.push(marker);
    kakao.maps.event.addListener(marker, "click", () => focusPlace(place));
  });
};

const focusPlace = (place) => {
  // 모바일/좁은 화면 대응: 리스트가 열려있으면 지도 보기 편하게 닫아주거나 유지 (여기선 유지)
  const moveLatLon = new kakao.maps.LatLng(place.y, place.x);
  
  map.setCenter(moveLatLon);
  
  // 리스트가 열려있을 땐 패널에 가리지 않게 약간 왼쪽으로 이동 (PC 기준)
  if (isListOpen.value) {
    map.panBy(-150, 0); 
  }

  infowindow.setContent(`
    <div style="padding:12px; font-weight:700; color:#1e293b; border:none; min-width:150px;">
      ${place.place_name}
    </div>
  `);
  infowindow.open(map, markers.find(m => m.getPosition().getLat().toFixed(6) === parseFloat(place.y).toFixed(6)));
};

const goBackToCampus = () => {
  map.setCenter(new kakao.maps.LatLng(CAMPUS_POS.lat, CAMPUS_POS.lng));
  map.setLevel(3);
};

onMounted(() => {
  const script = document.createElement("script");
  script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_KEY}&autoload=false&libraries=services`;
  script.onload = () => {
    window.kakao.maps.load(() => {
      map = new kakao.maps.Map(document.getElementById("map"), {
        center: new kakao.maps.LatLng(CAMPUS_POS.lat, CAMPUS_POS.lng),
        level: 3,
      });
      ps = new kakao.maps.services.Places(map);
      infowindow = new kakao.maps.InfoWindow({ zIndex: 10 });

      const content = `
        <div class="custom-campus-label">
          <div class="pulse"></div>
          <div class="text">SSAFY 멀티캠퍼스</div>
        </div>`;
      campusOverlay = new kakao.maps.CustomOverlay({
        position: new kakao.maps.LatLng(CAMPUS_POS.lat, CAMPUS_POS.lng),
        content: content,
        yAnchor: 1.2
      });
      campusOverlay.setMap(map);

      filterByCategory("FD6");
    });
  };
  document.head.appendChild(script);
});
</script>

<style scoped>
.kakao-map-container {
  position: relative;
  width: 100%;
  height: 600px;
  display: flex;
  overflow: hidden; /* 오버레이가 밖으로 나갈 때 스크롤 방지 */
}

.map-canvas {
  flex: 1;
  height: 100%;
}

/* 📋 사이드바 토글 버튼 */
.sidebar-toggle-btn {
  position: absolute;
  top: 20px; right: 20px;
  z-index: 20;
  width: 44px; height: 44px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  color: #1e293b;
  transition: 0.3s;
}
.sidebar-toggle-btn:hover { background: #f8fafc; color: #22c55e; }

/* 📋 사이드 오버레이 (리스트 패널) */
.side-overlay {
  position: absolute;
  top: 0; right: 0; bottom: 0;
  width: 340px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  border-left: 1px solid #e2e8f0;
  z-index: 15;
  display: flex;
  flex-direction: column;
  box-shadow: -10px 0 30px rgba(0,0,0,0.05);
}

/* 전환 애니메이션 */
.slide-side-enter-active,
.slide-side-leave-active {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-side-enter-from,
.slide-side-leave-to {
  transform: translateX(100%);
}

/* 🎮 제어 헤더 */
.control-header {
  padding: 16px 16px 8px;
  border-bottom: 1px solid #f1f5f9;
  /* 우측 상단 토글 버튼 공간 확보 */
  padding-right: 70px; 
}

.mode-switch {
  display: flex;
  background: #f1f5f9;
  padding: 4px;
  border-radius: 10px;
}

.mode-btn {
  flex: 1;
  padding: 8px;
  border: none;
  background: transparent;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 700;
  color: #64748b;
  cursor: pointer;
  transition: 0.2s;
}

.mode-btn.active {
  background: white;
  color: #22c55e;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

/* 카테고리 스크롤 영역 */
.category-scroll {
  padding: 12px 16px;
  display: flex;
  gap: 6px;
  overflow-x: auto;
  border-bottom: 1px solid #f1f5f9;
}
.category-scroll::-webkit-scrollbar { display: none; }

.cat-btn {
  padding: 8px 14px; border-radius: 12px; border: 1px solid #e2e8f0;
  background: white; white-space: nowrap; font-size: 13px; font-weight: 700;
  color: #64748b; cursor: pointer; transition: 0.2s;
}
.cat-btn.active { background: #22c55e; color: white; border-color: #22c55e; }

/* 🔍 검색 영역 */
.search-area {
  padding: 12px 16px;
  border-bottom: 1px solid #f1f5f9;
}
.search-box {
  display: flex;
  gap: 8px;
}
.search-box input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  outline: none;
  font-size: 14px;
}
.search-box input:focus { border-color: #22c55e; }
.search-box button {
  width: 44px;
  background: #22c55e;
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
}

/* 리스트 영역 */
.list-wrapper {
  flex: 1; overflow-y: auto; padding: 16px;
}
.list-wrapper::-webkit-scrollbar { width: 5px; }
.list-wrapper::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }
.no-data { text-align: center; color: #94a3b8; padding-top: 40px; font-size: 14px; }

/* 카드 디자인 */
.recommend-card {
  background: white; border-radius: 16px; padding: 16px; margin-bottom: 12px;
  display: flex; gap: 14px; cursor: pointer; transition: 0.2s;
  border: 1px solid #f1f5f9;
}
.recommend-card:hover { 
  transform: translateY(-3px); 
  box-shadow: 0 8px 20px rgba(0,0,0,0.06); 
  border-color: #22c55e; 
}

.card-num { font-size: 18px; font-weight: 900; color: #22c55e; opacity: 0.5; }
.card-content { flex: 1; }
.card-top { display: flex; justify-content: space-between; margin-bottom: 4px; }
.tag { font-size: 11px; color: #94a3b8; font-weight: 600; }
.dist { font-size: 11px; color: #22c55e; font-weight: 800; }
.place-name { font-size: 15px; font-weight: 800; color: #1e293b; margin: 2px 0; }
.place-addr { font-size: 12px; color: #64748b; line-height: 1.4; }
.review-link {
  margin-top: 10px; display: flex; align-items: center; gap: 4px;
  font-size: 12px; font-weight: 700; color: #22c55e; text-decoration: none;
}

/* 버튼 위치 조정 */
.re-center-btn {
  position: absolute; bottom: 30px; left: 30px;
  display: flex; align-items: center; gap: 10px;
  padding: 10px 20px; background: white; border-radius: 18px;
  border: none; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  font-weight: 800; color: #1e293b; cursor: pointer; z-index: 10;
  transition: 0.2s;
}
.re-center-btn:hover { transform: scale(1.05); color: #22c55e; }
.btn-icon { color: #22c55e; }

</style>

<style>
/* 전역 스타일 */
.custom-campus-label {
  display: flex; flex-direction: column; align-items: center;
}
.custom-campus-label .text {
  background: #22c55e; color: white; padding: 6px 14px; border-radius: 12px;
  font-weight: 800; font-size: 13px; box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4);
}
.custom-campus-label .pulse {
  width: 12px; height: 12px; background: #22c55e; border-radius: 50%;
  margin-top: 4px; border: 2px solid white;
  animation: pulse-animation 2s infinite;
}
@keyframes pulse-animation {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(34, 197, 94, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
}
</style>