<template>
  <section class="meal-page">
    <div class="header-container">
      <div class="date-nav-bar">
        <button class="nav-arrow-btn" @click="goPrevDay" aria-label="이전 날짜">
          <span class="material-icons">chevron_left</span>
        </button>

        <div class="main-date-selector" @click="openDatePicker">
          <div class="calendar-icon-box">
            <span class="material-icons">calendar_today</span>
          </div>
          <div class="date-info">
            <h2 class="display-date">{{ formattedDate }}</h2>
            <div class="weekday-badge" :class="`is-${currentDate.getDay()}`">
              {{ weekdayLabel }}요일
            </div>
          </div>
          <input
            ref="dateInputRef"
            type="date"
            class="hidden-picker"
            v-model="dateInput"
            @change="onDatePick"
          />
        </div>

        <button class="nav-arrow-btn" @click="goNextDay" aria-label="다음 날짜">
          <span class="material-icons">chevron_right</span>
        </button>

        <button class="today-jump-btn" @click="goToday">오늘</button>
      </div>
    </div>

    <div class="meal-cards-grid">
      <div class="card-wrapper">
        <MealCard v-if="koreanMeal" :meal-data="koreanMeal" meal-type="A" />
        <div v-else class="empty-state-card">
          <div class="empty-icon-circle">
            <span class="material-icons">restaurant</span>
          </div>
          <h4>한식 준비 중</h4>
          <p>정성 가득한 한식 식단을 준비하고 있습니다.</p>
        </div>
      </div>

      <div class="card-wrapper">
        <MealCard v-if="singleMeal" :meal-data="singleMeal" meal-type="B" />
        <div v-else class="empty-state-card">
          <div class="empty-icon-circle">
            <span class="material-icons">auto_awesome</span>
          </div>
          <h4>일품 준비 중</h4>
          <p>맛있는 특식 메뉴를 곧 공개합니다.</p>
        </div>
      </div>
    </div>

    <div v-if="hasMealData" class="recommend-section" ref="scrollTarget">
      <div class="recommend-container">
        <div class="recommend-guide">
          <p class="guide-text">오늘의 영양 상태를 분석하여</p>
          <h3 class="guide-title">완벽한 <span class="highlight">저녁 메뉴</span>를 추천해드릴까요?</h3>
        </div>
        
        <button 
          class="action-pill-btn" 
          :class="{ 'is-active': showDinner }"
          @click="onClickDinnerRecommend"
        >
          <div class="btn-content">
            <span class="material-icons">
              {{ showDinner ? "keyboard_arrow_up" : "auto_fix_high" }}
            </span>
            <span class="btn-text">
              {{ showDinner ? "추천 닫기" : (hasDinner ? "오늘 저녁 메뉴 보기" : "저녁 메뉴 추천 받기") }}
            </span>
          </div>
        </button>
      </div>
    </div>

    <DinnerCard
      v-if="showDinner && hasMealData"
      :key="apiDate"
      :date="apiDate"
      @close="showDinner = false"
    />
  </section>
</template>

<script setup>
/* 로직은 그대로 유지 */
import { ref, computed, watch, nextTick } from "vue"
import axios from "axios"
import { useMealStore } from "@/stores/mealStore"
import { useAuthStore } from "@/stores/auth"
import { useRouter, useRoute } from "vue-router"

import MealCard from "./MealCard.vue"
import DinnerCard from "./DinnerCard.vue"

const mealStore = useMealStore()
const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const showDinner = ref(false)
const dateInputRef = ref(null)
const scrollTarget = ref(null)
const hasDinner = ref(false)

const today = new Date()
today.setHours(0, 0, 0, 0)

const formatDateLocal = (date) => {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, "0")
  const d = String(date.getDate()).padStart(2, "0")
  return `${y}-${m}-${d}`
}

const formatDateForAPI = (date) => formatDateLocal(date).replace(/-/g, "")

const getInitialDate = () => {
  const queryDate = route.query.date
  if (queryDate && /^\d{4}-\d{2}-\d{2}$/.test(queryDate)) {
    return new Date(queryDate)
  }
  return new Date(today)
}

const currentDate = ref(getInitialDate())
const dateInput = ref(formatDateLocal(currentDate.value))
const apiDate = computed(() => formatDateForAPI(currentDate.value))

const formattedDate = computed(() => {
  const d = currentDate.value
  return `${d.getFullYear()}년 ${d.getMonth() + 1}월 ${d.getDate()}일`
})

const weekdays = ["일","월","화","수","목","금","토"]
const weekdayLabel = computed(() => weekdays[currentDate.value.getDay()])

const koreanMeal = computed(() => mealStore.menus.find(m => m.course_type === "A"))
const singleMeal = computed(() => mealStore.menus.find(m => m.course_type === "B"))
const hasMealData = computed(() => !!(koreanMeal.value || singleMeal.value))

const syncDateWithURL = (newDate) => {
  const dateStr = formatDateLocal(newDate)
  currentDate.value = newDate
  dateInput.value = dateStr
  router.replace({ query: { ...route.query, date: dateStr } })
}

const openDatePicker = () => dateInputRef.value?.showPicker()
const onDatePick = (e) => {
  const [y, m, d] = e.target.value.split("-").map(Number)
  syncDateWithURL(new Date(y, m - 1, d))
}

const goPrevDay = () => {
  const d = new Date(currentDate.value)
  d.setDate(d.getDate() - 1)
  syncDateWithURL(d)
}

const goNextDay = () => {
  const d = new Date(currentDate.value)
  d.setDate(d.getDate() + 1)
  syncDateWithURL(d)
}

const goToday = () => syncDateWithURL(new Date(today))

const checkDinnerExists = async () => {
  if (!authStore.isLoggedIn || !hasMealData.value) {
    hasDinner.value = false
    return
  }
  try {
    await axios.post(
      "http://localhost:8000/meal/recommend-dinner/",
      { date: apiDate.value },
      { headers: authStore.getAuthHeader() }
    )
    hasDinner.value = true
  } catch {
    hasDinner.value = false
  }
}

const onClickDinnerRecommend = async () => {
  if (!authStore.isLoggedIn) {
    router.push("/login")
    return
  }
  showDinner.value = !showDinner.value
  if (showDinner.value) {
    await nextTick()
    scrollTarget.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

watch(apiDate, async () => {
  showDinner.value = false
  await mealStore.fetchMeals(apiDate.value, "2")
  if (hasMealData.value) {
    await checkDinnerExists()
  } else {
    hasDinner.value = false
  }
}, { immediate: true })

watch(() => route.query.date, (newDateStr) => {
  if (newDateStr && newDateStr !== formatDateLocal(currentDate.value)) {
    currentDate.value = new Date(newDateStr)
    dateInput.value = newDateStr
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.meal-page {
  padding: 40px 20px 80px;
  background: transparent;
  font-family: 'Pretendard', -apple-system, sans-serif;
}

/* 상단 네비게이션 동일 */
.header-container { max-width: 800px; margin: 0 auto 50px; }
.date-nav-bar { display: flex; align-items: center; gap: 12px; }

.main-date-selector {
  flex: 1; display: flex; align-items: center; background: #ffffff;
  padding: 14px 28px; border-radius: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  cursor: pointer; position: relative; border: 1px solid #f1f5f9;
  transition: transform 0.2s;
}
.main-date-selector:hover { transform: translateY(-2px); }

.calendar-icon-box {
  width: 44px; height: 44px; background: #f0fdf4; color: #22c55e;
  border-radius: 14px; display: flex; align-items: center; justify-content: center;
  margin-right: 18px;
}

.display-date { margin: 0; font-size: 1.3rem; font-weight: 900; color: #0f172a; letter-spacing: -0.5px; }
.weekday-badge {
  font-size: 0.85rem; font-weight: 700; color: #64748b;
  background: #f1f5f9; padding: 4px 10px; border-radius: 8px;
}
.weekday-badge.is-0 { color: #ef4444; background: #fee2e2; }
.weekday-badge.is-6 { color: #2563eb; background: #dbeafe; }

.nav-arrow-btn {
  width: 52px; height: 52px; border-radius: 18px; border: none;
  background: white; color: #64748b; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05); transition: 0.2s;
}
.nav-arrow-btn:hover { background: #f8fafc; color: #0f172a; }

.today-jump-btn {
  padding: 0 20px; height: 52px; border-radius: 18px; border: none;
  background: #0f172a; color: white; font-weight: 800; cursor: pointer;
  transition: 0.2s;
}
.today-jump-btn:hover { background: #22c55e; box-shadow: 0 8px 20px rgba(34, 197, 94, 0.2); }

/* ⭐ [핵심 수정] 식단 카드 그리드 확장 */
.meal-cards-grid {
  display: grid; 
  /* 🛠 최소 너비를 340px -> 420px로 확장하여 카드가 커질 공간을 확보합니다 */
  grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
  gap: 40px; 
  /* 🛠 전체 폭을 1100px -> 1200px로 확장하여 시원한 느낌을 줍니다 */
  max-width: 1200px; 
  margin: 0 auto;
}

.empty-state-card {
  height: 520px; /* MealCard의 바뀐 높이에 맞춰 조절 */
  background: white; border-radius: 32px;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  border: 1px solid #f1f5f9; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.03);
}
.empty-icon-circle {
  width: 70px; height: 70px; background: #f8fafc; border-radius: 50%;
  display: flex; align-items: center; justify-content: center; margin-bottom: 20px;
}
.empty-icon-circle .material-icons { color: #cbd5e1; font-size: 32px; }
.empty-state-card h4 { font-size: 1.4rem; color: #1e293b; font-weight: 900; margin: 0; }
.empty-state-card p { font-size: 1rem; color: #94a3b8; margin-top: 10px; }

/* 저녁 추천 섹션 */
.recommend-section { 
  display: flex; justify-content: center; 
  margin-top: 100px; margin-bottom: 40px; 
}
.recommend-container { text-align: center; width: 100%; }
.recommend-guide { margin-bottom: 25px; }
.guide-text { font-size: 0.95rem; color: #64748b; font-weight: 600; margin-bottom: 6px; }
.guide-title { font-size: 1.8rem; font-weight: 900; color: #0f172a; }
.highlight { color: #22c55e; }

.action-pill-btn {
  position: relative; padding: 20px 50px; border-radius: 50px;
  border: none; background: #0f172a; color: white;
  cursor: pointer; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 15px 30px rgba(15, 23, 42, 0.2);
}
.action-pill-btn:hover { 
  transform: translateY(-5px) scale(1.02); 
  background: #22c55e; 
  box-shadow: 0 20px 40px rgba(34, 197, 94, 0.3); 
}
.btn-content { display: flex; align-items: center; gap: 10px; }
.btn-text { font-weight: 800; font-size: 1.2rem; letter-spacing: -0.3px; }
.action-pill-btn.is-active { background: #64748b; transform: scale(0.98); }

.hidden-picker { position: absolute; inset: 0; opacity: 0; cursor: pointer; }
</style>