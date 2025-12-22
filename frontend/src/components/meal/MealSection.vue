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
        <div class="btn-background"></div>
      </button>
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
/* 로직은 기존과 동일하므로 생략 (그대로 사용하시면 됩니다) */
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
  background: #f8fafc;
  min-height: 100vh;
  font-family: 'Pretendard', -apple-system, sans-serif;
}

/* 상단 네비게이션 */
.header-container { max-width: 800px; margin: 0 auto 50px; }
.date-nav-bar { display: flex; align-items: center; gap: 10px; }

.main-date-selector {
  flex: 1;
  display: flex;
  align-items: center;
  background: #ffffff;
  padding: 12px 24px;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  cursor: pointer;
  position: relative;
  border: 1px solid #f1f5f9;
}

.calendar-icon-box {
  width: 40px; height: 40px;
  background: #f1f5f9; color: #475569;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  margin-right: 15px;
}

.display-date { margin: 0; font-size: 1.2rem; font-weight: 800; color: #1e293b; }
.weekday-badge {
  font-size: 0.8rem; font-weight: 600; color: #64748b;
  background: #f1f5f9; padding: 2px 8px; border-radius: 6px; width: fit-content;
}
.weekday-badge.is-0 { color: #ef4444; background: #fee2e2; }
.weekday-badge.is-6 { color: #2563eb; background: #dbeafe; }

.nav-arrow-btn {
  width: 48px; height: 48px; border-radius: 16px; border: none;
  background: white; color: #94a3b8; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.03);
}

.today-jump-btn {
  padding: 0 16px; height: 48px; border-radius: 16px; border: none;
  background: #334155; color: white; font-weight: 700; cursor: pointer;
}

/* 식단 카드 그리드 */
.meal-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 30px; max-width: 1000px; margin: 0 auto;
}

.card-wrapper { position: relative; padding-top: 15px; }

/* 한식/일품 강조 태그 */

.empty-state-card {
  height: 420px; background: white; border-radius: 28px;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  border: 1px solid #edf2f7; text-align: center;
}
.empty-icon-circle {
  width: 64px; height: 64px; background: #f8fafc; border-radius: 50%;
  display: flex; align-items: center; justify-content: center; margin-bottom: 16px;
}
.empty-icon-circle .material-icons { color: #cbd5e1; font-size: 28px; }
.empty-state-card h4 { margin: 0; color: #475569; font-weight: 700; }
.empty-state-card p { font-size: 0.85rem; color: #94a3b8; margin-top: 6px; }

/* 저녁 추천 버튼 */
.recommend-section { display: flex; justify-content: center; margin-top: 50px; }
.action-pill-btn {
  position: relative; padding: 16px 32px; border-radius: 50px;
  border: none; background: #1e293b; color: white;
  cursor: pointer; overflow: hidden; transition: all 0.3s ease;
}
.action-pill-btn:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.15); }
.btn-content { display: flex; align-items: center; gap: 8px; position: relative; z-index: 2; }
.btn-text { font-weight: 700; font-size: 1rem; }
.action-pill-btn.is-active { background: #64748b; }

.hidden-picker { position: absolute; inset: 0; opacity: 0; cursor: pointer; }

@media (max-width: 600px) {
  .display-date { font-size: 1rem; }
  .meal-cards-grid { grid-template-columns: 1fr; }
}
</style>