<template>
  <section class="dinner-card-wrapper">
    <div class="dinner-card-relative">
      <button class="close-icon-btn" @click="emit('close')" aria-label="닫기">
        <span class="material-icons">close</span>
      </button>

      <div v-if="step === 'select'" class="dinner-card">
        <div class="card-header">
          <div class="icon-badge">
            <span class="material-icons">lunch_dining</span>
          </div>
          <h3 class="title">점심을 선택해주세요</h3>
          <p class="sub-title">오늘 드신 점심에 맞춰 AI가 저녁을 추천해드려요.</p>
        </div>

        <div class="lunch-select-list">
          <div
            v-for="meal in mealStore.menus"
            :key="meal.id"
            class="lunch-select-card"
            @click="selectLunch(meal.id)"
          >
            <div class="meal-type-badge" :class="meal.course_type">
              {{ meal.course_type === 'A' ? '한식' : '일품' }}
            </div>
            <div class="meal-name-text">{{ meal.meal_name }}</div>
            <span class="material-icons arrow">chevron_right</span>
          </div>
        </div>
        
        <button class="footer-close-btn" @click="emit('close')">다음에 할게요</button>
      </div>

      <div v-else-if="step === 'loading'" class="dinner-card loading">
        <div class="loader-container">
          <div class="pulse-loader"></div>
          <div class="pulse-loader-ring"></div>
        </div>
        <p class="loading-text">AI가 완벽한 저녁 메뉴를<br/>고민하고 있습니다...</p>
      </div>

      <div v-else class="dinner-card result">
        <div class="card-header">
          <div class="icon-badge ai-badge">
            <span class="material-icons">auto_fix_high</span>
          </div>
          <h3 class="title">AI 추천 저녁 메뉴</h3>
        </div>

        <div class="menu-highlight-box">
          <p class="menu-name">{{ dinnerMenu }}</p>
        </div>

        <div class="reason-box">
          <div class="reason-header">
            <span class="material-icons">info</span>
            <h4>추천 이유</h4>
          </div>
          <p>{{ reason }}</p>
        </div>

        <div class="status-message-area">
          <Transition name="fade-slide">
            <p v-if="isEaten === true" class="eat-status success">
              <span class="material-icons">check_circle</span>
              목표에 한걸음 더 다가갔어요!
            </p>
            <p v-else-if="isEaten === false" class="eat-status skip">
              <span class="material-icons">pause_circle</span>
              오늘은 저녁을 건너뛰었어요
            </p>
            <p v-else class="eat-status guide">이 메뉴를 드실 건가요?</p>
          </Transition>
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

        <button class="footer-close-btn result-close" @click="emit('close')">닫기</button>
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
  padding: 20px;
  margin-bottom: 60px;
}

.dinner-card-relative {
  position: relative;
  max-width: 520px;
  width: 100%;
}

.dinner-card {
  background: #ffffff;
  padding: 50px 40px 30px;
  border-radius: 40px;
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.12);
  text-align: center;
  border: 1px solid rgba(0,0,0,0.03);
  transition: all 0.3s ease;
}

/* 닫기 아이콘 버튼 */
.close-icon-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: #f1f5f9;
  color: #94a3b8;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  transition: 0.2s;
}
.close-icon-btn:hover { background: #fee2e2; color: #ef4444; transform: rotate(90deg); }

.card-header { margin-bottom: 30px; }
.icon-badge {
  width: 56px; height: 56px; background: #f0fdf4; color: #22c55e;
  border-radius: 18px; display: flex; align-items: center; justify-content: center;
  margin: 0 auto 16px;
}
.icon-badge.ai-badge { background: #0f172a; color: #22c55e; }

.title { font-size: 1.6rem; font-weight: 900; color: #0f172a; margin-bottom: 10px; letter-spacing: -0.5px; }
.sub-title { font-size: 1rem; color: #64748b; font-weight: 500; }

/* 메뉴 강조 */
.menu-highlight-box {
  background: #f0fdf4; padding: 25px; border-radius: 24px; margin-bottom: 24px;
  border: 1px dashed #22c55e;
}
.menu-name { font-size: 1.8rem; font-weight: 900; color: #166534; margin: 0; }

.reason-box {
  background: #f8fafc; border-radius: 24px; padding: 24px;
  text-align: left; margin-bottom: 24px; border: 1px solid #f1f5f9;
}
.reason-header { display: flex; align-items: center; gap: 6px; margin-bottom: 8px; color: #0f172a; }
.reason-header .material-icons { font-size: 18px; color: #22c55e; }
.reason-box h4 { font-size: 1rem; font-weight: 800; margin: 0; }
.reason-box p { color: #475569; font-size: 0.95rem; line-height: 1.6; font-weight: 500; margin: 0; }

/* 점심 선택 리스트 */
.lunch-select-list { display: grid; gap: 14px; margin-bottom: 20px; }
.lunch-select-card {
  display: flex; align-items: center; padding: 20px 24px;
  background: #fff; border: 2px solid #f1f5f9; border-radius: 20px;
  cursor: pointer; transition: 0.2s;
}
.lunch-select-card:hover { border-color: #22c55e; background: #f0fdf4; transform: scale(1.02); }
.meal-type-badge {
  padding: 4px 10px; border-radius: 8px; font-size: 0.8rem; font-weight: 800;
}
.meal-type-badge.A { background: #dcfce7; color: #166534; }
.meal-type-badge.B { background: #fef9c3; color: #854d0e; }
.meal-name-text { flex: 1; margin-left: 16px; text-align: left; font-weight: 800; color: #1e293b; font-size: 1.05rem; }
.arrow { color: #cbd5e1; }

/* 상태 메시지 */
.status-message-area { height: 48px; display: flex; align-items: center; justify-content: center; margin-bottom: 12px; }
.eat-status { font-weight: 800; font-size: 1rem; display: flex; align-items: center; gap: 6px; }
.eat-status.success { color: #166534; }
.eat-status.skip { color: #64748b; }
.eat-status.guide { color: #94a3b8; }

/* 버튼 액션 */
.eat-actions { display: flex; gap: 12px; margin-bottom: 15px; }
.eat-btn { 
  flex: 1; padding: 18px; border-radius: 18px; border: none; font-weight: 900; font-size: 1.05rem;
  cursor: pointer; transition: 0.3s; 
}
.eat-btn.yes { background: #e2e8f0; color: #64748b; }
.eat-btn.no { background: #f1f5f9; color: #94a3b8; }

.eat-btn.yes.active { background: #22c55e; color: white; box-shadow: 0 10px 20px rgba(34, 197, 94, 0.25); }
.eat-btn.no.active { background: #0f172a; color: white; box-shadow: 0 10px 20px rgba(15, 23, 42, 0.2); }

/* 하단 닫기 버튼 */
.footer-close-btn {
  background: none; border: none; color: #94a3b8; font-weight: 700; font-size: 0.9rem;
  text-decoration: underline; cursor: pointer; padding: 10px; transition: 0.2s;
}
.footer-close-btn:hover { color: #64748b; }
.result-close { margin-top: 10px; }

/* 로더 */
.loading { padding: 80px 40px; }
.loader-container { position: relative; width: 60px; height: 60px; margin: 0 auto 30px; }
.pulse-loader { 
  width: 100%; height: 100%; background: #22c55e; border-radius: 50%; 
  animation: pulse 1.5s infinite ease-in-out; 
}
.pulse-loader-ring {
  position: absolute; inset: -10px; border: 2px solid #22c55e; border-radius: 50%;
  animation: pulse-ring 1.5s infinite ease-out; opacity: 0;
}
.loading-text { font-size: 1.1rem; font-weight: 800; color: #1e293b; line-height: 1.6; }

@keyframes pulse { 0%, 100% { transform: scale(0.8); } 50% { transform: scale(1.1); } }
@keyframes pulse-ring { 0% { transform: scale(0.7); opacity: 0.5; } 100% { transform: scale(1.3); opacity: 0; } }

.fade-slide-enter-active { transition: all 0.3s ease-out; }
.fade-slide-enter-from { opacity: 0; transform: translateY(10px); }
</style>