<template>
  <section class="dinner-card-wrapper">
    <!-- 🔹 STEP 1: 점심 선택 -->
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

      <button class="retry-btn" @click="$emit('close')">닫기</button>
    </div>

    <!-- 🔹 STEP 2: 로딩 -->
    <div v-else-if="step === 'loading'" class="dinner-card loading">
      <div class="pulse-loader"></div>
      <p class="loading-text">AI가 저녁 메뉴를 고민 중이에요</p>
    </div>

    <!-- 🔹 STEP 3: 결과 -->
    <div v-else class="dinner-card result">
      <h3 class="title">🍽 추천 저녁 메뉴</h3>

      <p class="menu-name">{{ dinnerMenu }}</p>

      <div class="reason-box">
        <h4>추천 이유</h4>
        <div v-html="renderedReason"></div> <!-- 마크다운을 HTML로 변환하여 출력 -->
      </div>

      <p v-if="isEaten === true" class="eat-status success">
        ✅ 목표에 한걸음 더 다가갔어요!
      </p>

      <p v-else-if="isEaten === false" class="eat-status skip">
        ⏸ 오늘은 저녁을 건너뛰었어요
      </p>

      <div class="eat-actions">
        <button
          class="eat-btn yes"
          :class="{ active: isEaten === true }"
          @click="updateDinner(true)"
        >
          먹을래요!
        </button>

        <button
          class="eat-btn no"
          :class="{ active: isEaten === false }"
          @click="updateDinner(false)"
        >
          오늘은 스킵할래요!
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import { useMealStore } from "@/stores/mealStore";
import { useAuthStore } from "@/stores/auth";
import MarkdownIt from "markdown-it"; // markdown-it 라이브러리 불러오기

const props = defineProps({
  date: {
    type: String,
    required: true
  }
});

const mealStore = useMealStore();
const authStore = useAuthStore();

const step = ref("loading");
const dinnerMenu = ref("");
const reason = ref("");
const cardNews = ref(""); // 카드뉴스 데이터 저장
const dinnerId = ref(null);
const isEaten = ref(null);

// 마크다운을 HTML로 변환하는 computed 속성
const renderedReason = computed(() => {
  const md = new MarkdownIt();
  return md.render(reason.value); // 마크다운을 HTML로 변환하여 반환
});

// 카드뉴스 마크다운 변환
const renderedCardNews = computed(() => {
  const md = new MarkdownIt();
  return md.render(cardNews.value); // 카드뉴스 마크다운을 HTML로 변환하여 반환
});

/* 🔥 이미 추천된 저녁 조회 */
const fetchExistingDinner = async () => {
  try {
    const res = await axios.post(
      "http://localhost:8000/meal/recommend-dinner/",
      { date: props.date },
      { headers: authStore.getAuthHeader() }
    );

    // 기존 추천 데이터가 있다면
    if (res.data?.cached) {
      // 중복되지 않게 기존 데이터를 상태에 할당
      dinnerId.value = res.data.dinner_id;
      dinnerMenu.value = res.data.ai_menu;
      reason.value = res.data.reason;
      cardNews.value = res.data.card_news; // 백엔드에서 받은 카드뉴스 추가
      isEaten.value = res.data.is_eaten;
      step.value = "result";
      return;  // 이미 데이터가 있으면 그만 실행
    }
  } catch (error) {
    console.error("추천 데이터를 가져오는 데 실패했습니다.", error);
  }

  step.value = "select";  // 기존 데이터가 없으면 점심 선택 화면으로
};

/* 점심 선택 */
const selectLunch = async (mealId) => {
  step.value = "loading";  // 로딩 화면 표시

  const selectRes = await axios.post(
    "http://localhost:8000/meal/select-meal/",
    { meal_id: mealId },
    { headers: authStore.getAuthHeader() }
  );

  const dinnerRes = await axios.post(
    "http://localhost:8000/meal/recommend-dinner/",
    { user_selected_meal_id: selectRes.data.user_selected_meal_id },
    { headers: authStore.getAuthHeader() }
  );

  // 새로 받은 추천 데이터로 상태 업데이트
  dinnerId.value = dinnerRes.data.dinner_id;
  dinnerMenu.value = dinnerRes.data.ai_menu;
  reason.value = dinnerRes.data.reason;
  isEaten.value = dinnerRes.data.is_eaten ?? null;

  step.value = "result";  // 추천 결과 화면으로 변경
};

/* 먹었음 / 안 먹었음 */
const updateDinner = async (value) => {
  // 이미 같은 값이면 그냥 리턴 (UX 안정화)
  if (isEaten.value === value) return;

  isEaten.value = value;

  await axios.post(
    "http://localhost:8000/meal/dinner/status/",
    {
      dinner_id: dinnerId.value,
      is_eaten: value
    },
    { headers: authStore.getAuthHeader() }
  );
};

onMounted(fetchExistingDinner);
</script>

<style scoped>
/* 기존 스타일 유지 + 버튼만 정리 */

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

/* 카드뉴스 */
.card-news {
  background: #f0fdf4;
  border-radius: 20px;
  padding: 24px;
  text-align: left;
  margin-bottom: 30px;
}

.card-news h3 {
  font-size: 1rem;
  font-weight: 900;
  color: #0f172a;
}

.card-news p {
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

.eat-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.eat-btn {
  padding: 14px 22px;
  border-radius: 16px;
  border: none;
  font-weight: 800;
  cursor: pointer;
}

.eat-btn.yes {
  background: #22c55e;
  color: white;
}

.eat-btn.no {
  background: #e5e7eb;
  color: #0f172a;
}

.eat-status {
  margin: 20px 0 10px;
  font-weight: 800;
  font-size: 0.95rem;
}

.eat-status.success {
  color: #16a34a;
}

.eat-status.skip {
  color: #64748b;
}
</style>
