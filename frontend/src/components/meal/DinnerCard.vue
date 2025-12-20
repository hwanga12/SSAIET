<template>
  <section class="dinner-card-wrapper">
    <!-- 🔹 STEP 1 : 점심 선택 -->
    <div v-if="step === 'select'" class="dinner-card">
      <h3 class="title">점심을 선택해주세요</h3>

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

    <div class="meal-name-text">
      {{ meal.meal_name }}
    </div>

    <span class="material-icons arrow">chevron_right</span>
  </div>
</div>


      <button class="retry-btn" @click="$emit('close')">
        닫기
      </button>
    </div>

    <!-- 🔹 STEP 2 : 로딩 -->
    <div v-else-if="step === 'loading'" class="dinner-card loading">
      <div class="pulse-loader"></div>
      <p class="loading-text">AI가 저녁 메뉴를 고민 중이에요</p>
    </div>

    <!-- 🔹 STEP 3 : 결과 -->
    <div v-else class="dinner-card result">
      <h3 class="title">🍽 추천 저녁 메뉴</h3>

      <p class="menu-name">{{ dinnerMenu }}</p>

      <div class="reason-box">
        <h4>추천 이유</h4>
        <p>{{ reason }}</p>
      </div>

      <button class="retry-btn" @click="step = 'select'">
        다른 점심으로 다시 추천
      </button>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue"
import axios from "axios"
import { useMealStore } from "@/stores/mealStore"
import { useAuthStore } from "@/stores/auth"

const mealStore = useMealStore()
const authStore = useAuthStore()

const step = ref("select")
const dinnerMenu = ref("")
const reason = ref("")

const selectLunch = async (mealId) => {
  step.value = "loading"

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

  dinnerMenu.value = dinnerRes.data.ai_menu
  reason.value = dinnerRes.data.reason
  step.value = "result"
}
</script>




<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.dinner-card-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 80px;
}

/* 공통 카드 */
.dinner-card {
  max-width: 620px;
  width: 100%;
  background: #ffffff;
  padding: 50px 40px;
  border-radius: 40px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.05);
  text-align: center;
}

/* 타이틀 */
.title {
  font-size: 1.6rem;
  font-weight: 900;
  color: #0f172a;
  margin-bottom: 20px;
}

/* 메뉴 이름 */
.menu-name {
  font-size: 1.4rem;
  font-weight: 800;
  color: #22c55e;
  margin-bottom: 30px;
}

/* 이유 */
.reason-box {
  background: #f8fafc;
  border-radius: 20px;
  padding: 24px;
  text-align: left;
  margin-bottom: 30px;
}

.reason-box h4 {
  font-size: 1rem;
  font-weight: 900;
  margin-bottom: 8px;
  color: #0f172a;
}

.reason-box p {
  color: #475569;
  font-weight: 600;
  line-height: 1.6;
}

/* 버튼 */
.retry-btn {
  padding: 14px 28px;
  border-radius: 20px;
  border: none;
  background: #0f172a;
  color: #fff;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s;
}

.retry-btn:hover {
  background: #22c55e;
}

/* 로딩 */
.loading-text {
  font-weight: 700;
  color: #64748b;
  margin-top: 14px;
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
  0% { transform: scale(0.8); opacity: 0.4; }
  50% { transform: scale(1.1); opacity: 1; }
  100% { transform: scale(0.8); opacity: 0.4; }
}

/* 에러 */
.error .material-icons {
  font-size: 48px;
  color: #ef4444;
  margin-bottom: 10px;
}

/* 점심 선택 리스트 */
.lunch-select-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
  margin: 30px 0 40px;
}

/* 선택 카드 */
.lunch-select-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 22px 26px;
  background: #ffffff;
  border-radius: 22px;
  border: 1px solid #f1f5f9;
  cursor: pointer;
  box-shadow: 0 10px 25px rgba(0,0,0,0.04);
  transition: all 0.3s ease;
}

.lunch-select-card:hover {
  transform: translateY(-4px);
  border-color: #22c55e;
  box-shadow: 0 18px 40px rgba(34,197,94,0.18);
}

/* 한식 / 일품 뱃지 */
.meal-type-badge {
  font-size: 0.75rem;
  font-weight: 900;
  padding: 6px 14px;
  border-radius: 999px;
  background: #f0fdf4;
  color: #22c55e;
}

/* 메뉴명 */
.meal-name-text {
  flex: 1;
  margin-left: 18px;
  text-align: left;
  font-size: 1.05rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.4;
}

/* 화살표 */
.lunch-select-card .arrow {
  color: #94a3b8;
  transition: transform 0.3s, color 0.3s;
}

.lunch-select-card:hover .arrow {
  transform: translateX(6px);
  color: #22c55e;
}


</style>
