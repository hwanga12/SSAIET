<template>
  <div id="map" style="width:100%; height:600px;"></div>
</template>

<script setup>
import { onMounted } from "vue";

// ✅ SSAFY 멀티캠퍼스 좌표
const SSAFY_CENTER = {
  lat: 37.501274,
  lng: 127.039585,
};

onMounted(() => {
  // SDK 중복 로드 방지
  if (!window.kakao) {
    const script = document.createElement("script");
    script.src =
      "https://dapi.kakao.com/v2/maps/sdk.js?appkey=" +
      import.meta.env.VITE_KAKAO_MAP_KEY +
      "&autoload=false";

    script.onload = () => {
      loadMap();
    };

    document.head.appendChild(script);
  } else {
    loadMap();
  }
});

function loadMap() {
  window.kakao.maps.load(() => {
    const kakao = window.kakao;

    const center = new kakao.maps.LatLng(
      SSAFY_CENTER.lat,
      SSAFY_CENTER.lng
    );

    const map = new kakao.maps.Map(
      document.getElementById("map"),
      {
        center,
        level: 3,
      }
    );

    // ✅ SSAFY 위치 마커
    new kakao.maps.Marker({
      map,
      position: center,
    });

    console.log("✅ SSAFY 멀티캠퍼스 기준 지도 로드 완료");
  });
}
</script>
