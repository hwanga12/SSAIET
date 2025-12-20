<template>
  <section class="meal-page">
    <!-- ===== 날짜 헤더 (기존 그대로) ===== -->
    <div class="header-container">
      <div class="date-nav-bar">
        <button class="glass-icon-btn" @click="goPrevDay">
          <span class="material-icons">chevron_left</span>
        </button>

        <div class="main-date-selector" @click="openDatePicker">
          <div class="calendar-accent">
            <span class="material-icons">calendar_today</span>
          </div>
          <div class="date-content">
            <h2 class="display-date">{{ formattedDate }}</h2>
            <span class="display-weekday">{{ weekdayLabel }}</span>
          </div>
          <input
            ref="dateInputRef"
            type="date"
            class="hidden-picker"
            v-model="dateInput"
            @change="onDatePick"
          />
        </div>

        <button class="glass-icon-btn" @click="goNextDay">
          <span class="material-icons">chevron_right</span>
        </button>
      </div>
    </div>

    <!-- ===== 점심 카드 영역 (그대로) ===== -->
    <div class="meal-cards-grid">
      <MealCard :meal-data="koreanMeal" meal-type="A" />
      <MealCard :meal-data="singleMeal" meal-type="B" />
    </div>

    <!-- ===== 저녁 추천 버튼 (기존 스타일 유지) ===== -->
    <div class="recommend-action-section">
      <button class="ai-recommend-btn" @click="onClickDinnerRecommend">
        <span class="material-icons">restaurant_menu</span>
        저녁 추천받기
      </button>
    </div>

    <!-- ===== 저녁 추천 카드 ===== -->
    <DinnerCard
      v-if="showDinner"
      :date="apiDate"
      @close="showDinner = false"
    />
  </section>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import { useMealStore } from "@/stores/mealStore"
import MealCard from "./MealCard.vue"
import DinnerCard from "./DinnerCard.vue"
import { useAuthStore } from "@/stores/auth"
import { useRouter } from "vue-router"

const authStore = useAuthStore()
const router = useRouter()

const onClickDinnerRecommend = () => {
  if (!authStore.isLoggedIn) {
    router.push("/login")
    return
  }
  showDinner.value = true
}


const mealStore = useMealStore()
const dateInputRef = ref(null)
const showDinner = ref(false)

/* =========================
   🔥 날짜 유틸 (로컬 기준)
   ========================= */
const formatDateLocal = (date) => {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, "0")
  const d = String(date.getDate()).padStart(2, "0")
  return `${y}-${m}-${d}`
}

const formatDateForAPI = (date) => {
  return formatDateLocal(date).replace(/-/g, "")
}

/* ===== 현재 날짜 ===== */
const currentDate = ref(new Date())
const dateInput = ref(formatDateLocal(currentDate.value))

/* ===== 화면 표시 ===== */
const formattedDate = computed(() => {
  const d = currentDate.value
  return `${d.getFullYear()}년 ${d.getMonth() + 1}월 ${d.getDate()}일`
})

const weekdays = ["일","월","화","수","목","금","토"]
const weekdayLabel = computed(() => weekdays[currentDate.value.getDay()])

/* ===== API 날짜 ===== */
const apiDate = computed(() => formatDateForAPI(currentDate.value))

/* =========================
   날짜 이동
   ========================= */
const openDatePicker = () => dateInputRef.value?.showPicker()

const onDatePick = (e) => {
  const [y, m, d] = e.target.value.split("-").map(Number)
  currentDate.value = new Date(y, m - 1, d)
  dateInput.value = formatDateLocal(currentDate.value)
  showDinner.value = false
}

const goPrevDay = () => {
  const d = new Date(currentDate.value)
  d.setDate(d.getDate() - 1)
  currentDate.value = d
  dateInput.value = formatDateLocal(d)
  showDinner.value = false
}

const goNextDay = () => {
  const d = new Date(currentDate.value)
  d.setDate(d.getDate() + 1)
  currentDate.value = d
  dateInput.value = formatDateLocal(d)
  showDinner.value = false
}

/* =========================
   점심 데이터
   ========================= */
const koreanMeal = computed(() =>
  mealStore.menus.find(m => m.course_type === "A")
)

const singleMeal = computed(() =>
  mealStore.menus.find(m => m.course_type === "B")
)

/* 날짜 바뀌면 점심 다시 조회 */
watch(apiDate, (val) => {
  mealStore.fetchMeals(val, "2")
}, { immediate: true })
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
}


/* 🔥 [추가] 저녁 추천 버튼 스타일 */
.recommend-action-section {
  display: flex;
  justify-content: center;
  margin-top: 50px;
  padding-bottom: 50px;
}

.ai-recommend-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 18px 36px;
  background: #0f172a;
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1.1rem;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.ai-recommend-btn:hover {
  background: #22c55e;
  transform: translateY(-3px);
  box-shadow: 0 15px 30px rgba(34, 197, 94, 0.2);
}

</style>

