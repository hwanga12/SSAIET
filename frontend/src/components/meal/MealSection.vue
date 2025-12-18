<template>
<<<<<<< HEAD
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

=======
  <section class="meal-page">
    <div class="header-container">
      <div class="date-nav-bar">
        <button class="glass-icon-btn" @click="goPrevDay" aria-label="이전날">
          <span class="material-icons">chevron_left</span>
        </button>

        <div class="main-date-selector" @click="openDatePicker">
          <div class="calendar-accent">
            <span class="material-icons">calendar_today</span>
          </div>
          <div class="date-content">
            <h2 class="display-date">{{ formattedDate }}</h2>
            <span class="display-weekday" :class="`type-${currentDate.getDay()}`">
              {{ weekdayLabel }}
            </span>
          </div>
          
          <input
            ref="dateInputRef"
            type="date"
            class="hidden-picker"
            v-model="dateInput"
            @change="onDatePick"
          />
        </div>

        <button class="glass-icon-btn" @click="goNextDay" aria-label="다음날">
          <span class="material-icons">chevron_right</span>
        </button>

        <button class="today-float-btn" @click="goToday">
          <span class="material-icons">event</span>
          <span>Today</span>
        </button>
      </div>
    </div>

    <main class="content-wrapper">
      <Transition name="fade" mode="out-in">
        <div v-if="mealStore.isLoading" class="state-card loading">
          <div class="pulse-loader"></div>
          <p class="loading-text">맛있는 메뉴를 구성하고 있어요</p>
        </div>

        <div v-else-if="mealStore.isClosed" class="state-card empty">
          <div class="icon-circle shadow-inner">
            <span class="material-icons">coffee_maker</span>
          </div>
          <h3>식당이 쉬어가는 날입니다</h3>
          <p>다른 날짜의 건강한 식단을 확인해보세요.</p>
        </div>

        <div v-else-if="mealStore.error" class="state-card error">
          <span class="material-icons">error_outline</span>
          <p>정보를 불러오는 데 실패했습니다.</p>
          <button @click="location.reload()" class="retry-btn">다시 시도</button>
        </div>

        <div v-else class="meal-cards-grid">
          <MealCard :meal-data="koreanMeal" meal-type="A" />
          <MealCard :meal-data="singleMeal" meal-type="B" />
        </div>
      </Transition>
    </main>
>>>>>>> FE_Mainpage_Herosection&Navbar
  </section>
</template>

<script setup>
<<<<<<< HEAD
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
=======
import { ref, computed, watch } from "vue"
import { useMealStore } from "@/stores/mealStore"
import MealCard from "./MealCard.vue"

const mealStore = useMealStore()
const dateInputRef = ref(null)

const formatDateToISO = (date) => date.toISOString().split('T')[0]
const currentDate = ref(new Date())
const dateInput = ref(formatDateToISO(currentDate.value))

const formattedDate = computed(() => {
  const d = currentDate.value
  return `${d.getFullYear()}년 ${String(d.getMonth() + 1).padStart(2, '0')}월 ${String(d.getDate()).padStart(2, '0')}일`
})

const weekdays = ["일요일","월요일","화요일","수요일","목요일","금요일","토요일"]
const weekdayLabel = computed(() => weekdays[currentDate.value.getDay()])

const apiDate = computed(() => formatDateToISO(currentDate.value).replace(/-/g, ""))

const goToday = () => { currentDate.value = new Date() }
const openDatePicker = () => {
  if (dateInputRef.value) {
    'showPicker' in dateInputRef.value ? dateInputRef.value.showPicker() : dateInputRef.value.click()
  }
}
const onDatePick = (e) => {
  if (!e.target.value) return
  const [y, m, d] = e.target.value.split("-").map(Number)
  currentDate.value = new Date(y, m - 1, d)
}
const goPrevDay = () => { currentDate.value = new Date(currentDate.value.setDate(currentDate.value.getDate() - 1)) }
const goNextDay = () => { currentDate.value = new Date(currentDate.value.setDate(currentDate.value.getDate() + 1)) }

watch(currentDate, (newDate) => { dateInput.value = formatDateToISO(newDate) })
const koreanMeal = computed(() => mealStore.menus.find(m => m.course_type === "A") || null)
const singleMeal = computed(() => mealStore.menus.find(m => m.course_type === "B") || null)

watch(apiDate, (val) => { mealStore.fetchMeals(val, "2") }, { immediate: true })
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.meal-page {
  padding: 60px 20px;
  background: #fcfdfd;
  min-height: 100vh;
}

.header-container {
  max-width: 900px;
  margin: 0 auto 60px;
}

/* ===== 날짜 선택기 바 ===== */
.date-nav-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
}

.main-date-selector {
  flex: 1;
  display: flex;
  align-items: center;
  background: #ffffff;
  padding: 16px 28px;
  border-radius: 28px;
  box-shadow: 0 15px 35px rgba(0,0,0,0.05);
  border: 1px solid #f1f5f9;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.main-date-selector:hover {
  transform: translateY(-3px);
  border-color: #22c55e;
  box-shadow: 0 20px 40px rgba(34, 197, 94, 0.1);
}

.calendar-accent {
  width: 48px;
  height: 48px;
  background: #f0fdf4;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #22c55e;
  margin-right: 18px;
}

.display-date {
  margin: 0;
  font-size: 1.35rem;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: -0.5px;
}

.display-weekday {
  font-size: 0.85rem;
  font-weight: 800;
  margin-top: 2px;
  padding: 2px 10px;
  border-radius: 8px;
  width: fit-content;
  background: #f1f5f9;
  color: #64748b;
}

.type-0 { color: #ef4444; background: #fef2f2; } /* 일요일 */
.type-6 { color: #3b82f6; background: #eff6ff; } /* 토요일 */

.hidden-picker {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
}

/* ===== 버튼 그룹 ===== */
.glass-icon-btn {
  width: 56px;
  height: 56px;
  border-radius: 20px;
  border: none;
  background: #ffffff;
  color: #94a3b8;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 15px rgba(0,0,0,0.03);
  cursor: pointer;
  transition: all 0.2s;
}

.glass-icon-btn:hover {
  background: #0f172a;
  color: #ffffff;
}

.today-float-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 24px;
  height: 56px;
  border-radius: 20px;
  border: none;
  background: #0f172a;
  color: #fff;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 10px 20px rgba(15, 23, 42, 0.1);
}

.today-float-btn:hover {
  background: #22c55e;
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(34, 197, 94, 0.2);
}

/* ===== 상태 카드 (로딩/비어있음) ===== */
.state-card {
  background: #ffffff;
  padding: 80px 40px;
  border-radius: 40px;
  text-align: center;
  box-shadow: 0 20px 50px rgba(0,0,0,0.04);
  max-width: 600px;
  margin: 0 auto;
}

.loading-text {
  font-weight: 700;
  color: #64748b;
  margin-top: 10px;
}

.pulse-loader {
  width: 50px;
  height: 50px;
  background: #22c55e;
  border-radius: 50%;
  margin: 0 auto 24px;
  animation: pulse 1.5s infinite ease-in-out;
}

@keyframes pulse {
  0% { transform: scale(0.8); opacity: 0.4; box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.4); }
  50% { transform: scale(1.1); opacity: 1; box-shadow: 0 0 0 20px rgba(34, 197, 94, 0); }
  100% { transform: scale(0.8); opacity: 0.4; }
}

.icon-circle {
  width: 80px;
  height: 80px;
  background: #f8fafc;
  color: #cbd5e1;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.icon-circle .material-icons { font-size: 40px; }

/* ===== 그리드 배율 ===== */
.meal-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 850px) {
  .meal-cards-grid { grid-template-columns: 1fr; max-width: 450px; }
  .today-float-btn span:not(.material-icons) { display: none; }
  .today-float-btn { padding: 0 16px; width: 56px; justify-content: center; }
>>>>>>> FE_Mainpage_Herosection&Navbar
}
</style>