<template>
  <section class="meal-section">
    <h2 class="section-title">
      🗓️ {{ todayFormatted }}의 점심 메뉴
    </h2>
    
    <div v-if="mealStore.isLoading" class="status-message loading">
      <p>🍽️ 식단 정보를 불러오는 중...</p>
    </div>
    <div v-else-if="mealStore.error" class="status-message error">
      <p>🚨 식단 로딩 실패: {{ mealStore.error }}</p>
    </div>
    <div v-else-if="mealStore.menus.length === 0" class="status-message no-data">
      <p>⚠️ 오늘 점심 식단 정보가 없습니다.</p>
    </div>
    
    <div v-else class="meal-list-wrapper">
      <MealCard 
        v-for="(meal, index) in mealStore.menus" 
        :key="index"
        :meal-data="meal"
      />
    </div>

  </section>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useMealStore } from '@/stores/mealStore';
import MealCard from './MealCard.vue'; // 3단계에서 만들 카드 컴포넌트

const mealStore = useMealStore();

// 오늘의 날짜를 보기 좋게 포맷하는 computed 속성
const todayFormatted = computed(() => {
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth() + 1;
    const day = today.getDate();
    return `${year}년 ${month}월 ${day}일`;
});

// 컴포넌트가 마운트될 때 데이터 요청
onMounted(() => {
  // 날짜(null: 오늘)와 점심 시간(2)으로 요청
  mealStore.fetchMeals(null, '2'); 
});
</script>

<style scoped>
.meal-section {
  padding: 30px 20px;
  background-color: #f9fbfd;
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 25px;
  text-align: center;
}

.status-message {
  text-align: center;
  padding: 40px;
  border-radius: 8px;
  margin: 20px auto;
  max-width: 600px;
}
.loading {
    background-color: #e0f2fe;
    color: #0369a1;
}
.error {
    background-color: #fee2e2;
    color: #b91c1c;
}
.no-data {
    background-color: #fffbeb;
    color: #b45309;
}

.meal-list-wrapper {
  display: flex;
  justify-content: center; /* 카드들을 가운데 정렬 */
  gap: 20px; /* 카드 사이 간격 */
  flex-wrap: wrap; /* 화면이 좁아지면 줄 바꿈 */
}
</style>