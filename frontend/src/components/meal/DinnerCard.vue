<template>
  <section class="dinner-card-wrapper">
    <div v-if="step === 'select'" class="dinner-card">
      <h3 class="title">점심을 선택해주세요</h3>
      <p class="sub-title">오늘 드신 점심에 맞춰 AI가 저녁을 추천해드려요.</p>

      <div class="lunch-select-list">
        <div
          v-for="meal in mealStore.menus"
          :key="meal.id"
          class="lunch-select-card"
          @click="selectLunch(meal.id)"
        >
          <div class="meal-type-badge">
            {{ meal.course_type === 'A' ? '한식' : '일품' }}
          </div>
          <div class="meal-name-text">{{ meal.meal_name }}</div>
          <span class="material-icons arrow">chevron_right</span>
        </div>
      </div>
      </div>

    <div v-else-if="step === 'loading'" class="dinner-card loading">
      <div class="pulse-loader"></div>
      <p class="loading-text">AI가 저녁 메뉴를 고민 중이에요</p>
    </div>

    <div v-else class="dinner-card result">
      <h3 class="title">🍽 추천 저녁 메뉴</h3>
      <p class="menu-name">{{ dinnerMenu }}</p>

      <div class="reason-box">
        <h4>추천 이유</h4>
        <p>{{ reason }}</p>
      </div>

      <div class="status-message-area">
        <p v-if="isEaten === true" class="eat-status success">✅ 목표에 한걸음 더 다가갔어요!</p>
        <p v-else-if="isEaten === false" class="eat-status skip">⏸ 오늘은 저녁을 건너뛰었어요</p>
        <p v-else class="eat-status guide">이 메뉴를 드실 건가요?</p>
      </div>

      <div class="eat-actions">
        <button
          class="eat-btn yes"
          :class="{ active: isEaten === true }"
          @click="updateDinner(true)"
        >
          먹을게요
        </button>
        <button
          class="eat-btn no"
          :class="{ active: isEaten === false }"
          @click="updateDinner(false)"
        >
          안 먹을게요
        </button>
      </div>
      </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"
import { useMealStore } from "@/stores/mealStore"
import { useAuthStore } from "@/stores/auth"

const props = defineProps({
  date: { type: String, required: true }
})

// emit('close')는 부모의 '추천 창 닫기' 버튼이 처리하므로 호출부가 없어도 무방함
const emit = defineEmits(['close'])

const mealStore = useMealStore()
const authStore = useAuthStore()

const step = ref("loading")
const dinnerMenu = ref("")
const reason = ref("")
const dinnerId = ref(null)
const isEaten = ref(null)

/* 기존 추천 조회 */
const fetchExistingDinner = async () => {
  try {
    const res = await axios.post(
      "http://localhost:8000/meal/recommend-dinner/",
      { date: props.date },
      { headers: authStore.getAuthHeader() }
    )

    if (res.data?.cached) {
      dinnerId.value = res.data.dinner_id
      dinnerMenu.value = res.data.ai_menu
      reason.value = res.data.reason
      isEaten.value = res.data.is_eaten
      step.value = "result"
      return
    }
  } catch (err) {
    console.error("추천 데이터 로드 실패")
  }
  step.value = "select"
}

/* 점심 선택 */
const selectLunch = async (mealId) => {
  step.value = "loading"
  try {
    const selectRes = await axios.post(
      "http://localhost:8000/meal/select-meal/",
      { meal_id: mealId },
      { headers: authStore.getAuthHeader() }
    )

    const dinnerRes = await axios.post(
      "http://localhost:8000/meal/recommend-dinner/",
      { user_selected_meal_id: selectRes.data.user_selected_meal_id },
      { headers: authStore.getAuthHeader() }
    )

    dinnerId.value = dinnerRes.data.dinner_id
    dinnerMenu.value = dinnerRes.data.ai_menu
    reason.value = dinnerRes.data.reason
    isEaten.value = dinnerRes.data.is_eaten ?? null
    step.value = "result"
  } catch (err) {
    console.error("추천 실패")
    step.value = "select"
  }
}

/* 상태 업데이트 */
const updateDinner = async (value) => {
  if (isEaten.value === value) return
  isEaten.value = value
  try {
    await axios.post(
      "http://localhost:8000/meal/dinner/status/",
      { dinner_id: dinnerId.value, is_eaten: value },
      { headers: authStore.getAuthHeader() }
    )
  } catch (err) {
    console.error("업데이트 에러")
  }
}

onMounted(fetchExistingDinner)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.dinner-card-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 80px;
}

.dinner-card {
  max-width: 500px;
  width: 100%;
  background: #ffffff;
  padding: 45px 35px;
  border-radius: 32px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.06);
  text-align: center;
}

.title { font-size: 1.5rem; font-weight: 900; color: #0f172a; margin-bottom: 8px; }
.sub-title { font-size: 0.95rem; color: #64748b; margin-bottom: 24px; font-weight: 500; }
.menu-name { font-size: 1.7rem; font-weight: 800; color: #22c55e; margin: 20px 0; }

.reason-box {
  background: #f8fafc;
  border-radius: 20px;
  padding: 20px;
  text-align: left;
  margin-bottom: 24px;
}
.reason-box h4 { font-size: 0.9rem; font-weight: 900; color: #0f172a; margin-bottom: 6px; }
.reason-box p { color: #475569; font-size: 0.95rem; line-height: 1.6; font-weight: 600; }

.lunch-select-list { display: grid; gap: 12px; margin-bottom: 24px; }
.lunch-select-card {
  display: flex; align-items: center; padding: 18px 22px;
  background: #fff; border: 1px solid #f1f5f9; border-radius: 18px;
  cursor: pointer; transition: 0.2s;
}
.lunch-select-card:hover { border-color: #22c55e; transform: translateY(-2px); }
.meal-name-text { flex: 1; margin-left: 14px; text-align: left; font-weight: 700; color: #1e293b; }

.status-message-area { height: 40px; display: flex; align-items: center; justify-content: center; margin-bottom: 8px; }
.eat-status { font-weight: 800; font-size: 0.95rem; }

.eat-actions { display: flex; gap: 10px; } /* margin-bottom 제거 */
.eat-btn { flex: 1; padding: 16px; border-radius: 14px; border: none; font-weight: 800; cursor: pointer; opacity: 0.4; transition: 0.2s; }
.eat-btn.active { opacity: 1; transform: scale(1.02); }
.eat-btn.yes { background: #22c55e; color: white; }
.eat-btn.no { background: #f1f5f9; color: #475569; }

.pulse-loader { width: 40px; height: 40px; background: #22c55e; border-radius: 50%; margin: 0 auto 20px; animation: pulse 1.2s infinite; }
@keyframes pulse { 0%, 100% { transform: scale(0.8); opacity: 0.5; } 50% { transform: scale(1.1); opacity: 1; } }
</style>