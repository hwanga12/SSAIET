<template>
<<<<<<< HEAD
  <div class="meal-card-container" @click="toggleFlip">
    <div class="meal-card" :class="{ 'is-flipped': isFlipped }">

      <!-- ================= 앞면 ================= -->
      <div class="card-face card-front">

        <!-- 이미지 영역 -->
        <div
          class="meal-image"
          :style="{
            backgroundImage: mealData.photoUrl
              ? `url(${mealData.photoUrl})`
              : 'linear-gradient(135deg, #e5e7eb, #f9fafb)'
          }"
        >
          <div class="image-overlay"></div>

          <div class="meal-header">
            <span class="course-badge" :class="mealData.course_type">
              {{ mealData.course_type === 'A' ? '한식' : '일품' }}
            </span>

            <span class="p-score-badge">
              P-Score {{ mealData.p_score }}
            </span>
          </div>
        </div>

        <!-- 텍스트 영역 -->
        <div class="meal-info">
          <p class="meal-title">{{ mealData.subMenuTxt }}</p>
        </div>
      </div>

      <!-- ================= 뒷면 ================= -->
      <div class="card-face card-back">
        <div class="back-header">
          <h5>총 영양 정보 ({{ mealData.meal_name }})</h5>
        </div>

        <ul class="nutrition-summary">
          <li><span>총 칼로리:</span> <strong>{{ totalNutrition.calorie }} kcal</strong></li>
          <li><span>탄수화물:</span> {{ totalNutrition.carbohydrate }} g</li>
          <li><span>단백질:</span> {{ totalNutrition.protein }} g</li>
          <li><span>지방:</span> {{ totalNutrition.fat }} g</li>
        </ul>

        <div class="food-details">
          <h6>세부 음식 구성</h6>
          <div
            v-for="(food, index) in mealData.foods"
            :key="index"
            class="food-item"
          >
            <span :class="{ 'main-food': food.is_main }">
              {{ food.name }}
            </span>
            <span>({{ food.calorie }} kcal)</span>
          </div>
        </div>

        <button class="back-button" @click.stop="toggleFlip">
          돌아가기
        </button>
      </div>

=======
  <div class="meal-card-wrapper">
    <div class="card-perspective">
      <div v-if="isClosed || !mealData" class="status-card" :class="{ 'closed': isClosed }">
        <div class="status-icon">
          <span class="material-icons">{{ isClosed ? 'event_busy' : 'pending_actions' }}</span>
        </div>
        <h4>{{ isClosed ? '오늘은 식당이 쉬어갑니다' : '메뉴 준비 중' }}</h4>
        <p>{{ isClosed ? '운영 정보가 없습니다.' : emptyGuideText }}</p>
      </div>

      <div 
        v-else 
        class="flip-card" 
        :class="{ 'is-flipped': isFlipped }"
        @click="toggleFlip"
      >
        <div class="card-face card-front">
          <div class="inner-badge" :class="mealType">
            <span class="material-icons">{{ mealType === 'A' ? 'rice_bowl' : 'auto_awesome' }}</span>
            {{ mealTypeLabel }}
          </div>

          <div 
            class="meal-photo"
            :style="{ backgroundImage: mealData.photoUrl ? `url(${mealData.photoUrl})` : 'none' }"
          >
            <div v-if="!mealData.photoUrl" class="no-image-placeholder">
              <span class="material-icons">restaurant</span>
            </div>
            
            <div class="p-score-chip">
              <span class="material-icons">star</span>
              P {{ mealData.p_score }}
            </div>
          </div>

          <div class="meal-body">
            <div class="calorie-tag">Total {{ totalCalorie }} kcal</div>
            <h3 class="main-menu-name">{{ mainMenuName }}</h3>
            
            <div class="info-hint">
              <span>상세 구성 보기</span>
              <span class="material-icons">arrow_right_alt</span>
            </div>
          </div>
        </div>

        <div class="card-face card-back">
          <div class="back-header">
            <div class="back-type-label">{{ mealTypeLabel }} 구성</div>
            <h5>오늘의 건강한 식단</h5>
          </div>
          
          <div class="food-list-container">
            <div 
              v-for="(food, index) in mealData.foods" 
              :key="index" 
              class="food-row"
              :class="{ 'is-main': food.is_main }"
            >
              <div class="food-info">
                <span v-if="food.is_main" class="main-dot"></span>
                <span class="food-name">{{ food.name }}</span>
              </div>
              <span class="food-cal">{{ food.calorie }} kcal</span>
            </div>
          </div>

          <div class="back-footer">
            <div class="back-hint">
              <span class="material-icons">refresh</span>
              탭하여 이미지 보기
            </div>
          </div>
        </div>
      </div>
>>>>>>> FE_Mainpage_Herosection&Navbar
    </div>
  </div>
</template>

<script setup>
<<<<<<< HEAD
import { ref, computed } from 'vue';

const props = defineProps({
  mealData: {
    type: Object,
    required: true,
  }
});

const isFlipped = ref(false);
const toggleFlip = () => {
  isFlipped.value = !isFlipped.value;
};

const totalNutrition = computed(() => {
  if (!props.mealData.foods) {
    return { calorie: 0, carbohydrate: 0, protein: 0, fat: 0 };
  }

  const summary = {
    calorie: 0,
    carbohydrate: 0,
    protein: 0,
    fat: 0,
  };

  props.mealData.foods.forEach(food => {
    summary.calorie += food.calorie || 0;
    summary.carbohydrate += food.carbohydrate || 0;
    summary.protein += food.protein || 0;
    summary.fat += food.fat || 0;
  });

  summary.calorie = Math.round(summary.calorie);
  return summary;
=======
import { ref, computed } from "vue";

const props = defineProps({
  mealData: Object,
  mealType: { type: String, required: true },
  isClosed: Boolean,
});

const isFlipped = ref(false);
const toggleFlip = () => (isFlipped.value = !isFlipped.value);

const mealTypeLabel = computed(() => props.mealType === "A" ? "한식 코스" : "일품 요리");
const emptyGuideText = computed(() => 
  props.mealType === "A" ? "오늘은 일품 요리만 제공됩니다." : "오늘은 한식 코스만 제공됩니다."
);

const mainMenuName = computed(() => {
  if (!props.mealData) return "";
  const main = props.mealData.foods?.find(f => f.is_main);
  return main ? main.name : props.mealData.foods?.[0]?.name || "준비된 메뉴";
});

const totalCalorie = computed(() => {
  if (!props.mealData?.foods) return 0;
  return props.mealData.foods.reduce((acc, food) => acc + (Number(food.calorie) || 0), 0);
>>>>>>> FE_Mainpage_Herosection&Navbar
});
</script>

<style scoped>
<<<<<<< HEAD
/* -------------------- 컨테이너 -------------------- */
.meal-card-container {
  perspective: 1000px;
  width: 350px;
  height: 400px;
  cursor: pointer;
}

.meal-card {
=======
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.meal-card-wrapper {
  width: 100%;
  padding: 10px;
}

.card-perspective {
  perspective: 1200px;
  height: 480px;
  width: 100%;
}

/* ===== 상태 카드 (준비 중/휴무) ===== */
.status-card {
  width: 100%;
  height: 100%;
  background: #ffffff;
  border-radius: 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px dashed #e2e8f0;
  color: #94a3b8;
  box-shadow: 0 4px 20px rgba(0,0,0,0.02);
}

.status-icon .material-icons {
  font-size: 56px;
  color: #f1f5f9;
  margin-bottom: 16px;
}

.status-card h4 { color: #475569; font-weight: 800; margin-bottom: 4px; }

/* ===== 플립 카드 공통 ===== */
.flip-card {
>>>>>>> FE_Mainpage_Herosection&Navbar
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
<<<<<<< HEAD
  transition: transform 0.8s, box-shadow 0.3s;
  border-radius: 14px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}

.meal-card-container:hover .meal-card {
  box-shadow: 0 12px 24px rgba(0,0,0,0.25);
}

.meal-card.is-flipped {
  transform: rotateY(180deg);
}

/* -------------------- 공통 -------------------- */
.card-face {
  position: absolute;
  inset: 0;
  background: #fff;
  border-radius: 14px;
  backface-visibility: hidden;
=======
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.flip-card.is-flipped {
  transform: rotateY(180deg);
}

.card-face {
  position: absolute;
  inset: 0;
  backface-visibility: hidden;
  border-radius: 32px;
  background: #ffffff;
  box-shadow: 0 20px 40px rgba(0,0,0,0.06);
  border: 1px solid #f1f5f9;
>>>>>>> FE_Mainpage_Herosection&Navbar
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

<<<<<<< HEAD
.card-back {
  transform: rotateY(180deg);
}

/* -------------------- 앞면 -------------------- */
.meal-image {
  position: relative;
  height: 55%;
  background-size: cover;
  background-position: center;
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(0,0,0,0.15),
    rgba(0,0,0,0.65)
  );
}

.meal-header {
  position: absolute;
  top: 12px;
  left: 12px;
  right: 12px;
  display: flex;
  justify-content: space-between;
  z-index: 2;
}

.course-badge {
  padding: 6px 12px;
  border-radius: 999px;
  color: #fff;
  font-weight: 700;
  font-size: 13px;
}

.course-badge.A { background: #2563eb; }
.course-badge.B { background: #059669; }

.p-score-badge {
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(0,0,0,0.7);
  color: #facc15;
  font-weight: 800;
  font-size: 13px;
}

.meal-info {
  padding: 20px;
  flex-grow: 1;
  display: flex;
  align-items: center;
}

.meal-title {
  font-size: 18px;
  font-weight: 800;
  color: #111827;
  line-height: 1.4;
}

/* -------------------- 뒷면 -------------------- */
.card-back {
  padding: 16px;
}

.back-header {
  background: #f3f4f6;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 10px;
}

.nutrition-summary {
  list-style: none;
  padding: 0;
  margin-bottom: 10px;
}

.nutrition-summary li {
  font-size: 14px;
  padding: 4px 0;
  border-bottom: 1px dotted #e5e7eb;
}

.food-details {
  flex-grow: 1;
  overflow-y: auto;
}

.food-item {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  padding: 2px 0;
}

.main-food {
  font-weight: 700;
  color: #10b981;
}

.back-button {
  margin-top: auto;
  padding: 12px;
  background: #4f46e5;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-weight: 600;
}
</style>
=======
/* ===== 앞면 (Front) ===== */
.inner-badge {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 5;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 14px;
  font-size: 0.85rem;
  font-weight: 800;
  color: white;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
/* SSAIET 테마 컬러 적용 */
.inner-badge.A { background: #0f172a; } /* 딥 블랙 */
.inner-badge.B { background: #22c55e; } /* 그린 */

.meal-photo {
  height: 55%;
  position: relative;
  background-size: cover;
  background-position: center;
  background-color: #f8fafc;
}

.p-score-chip {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(4px);
  color: #0f172a;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 4px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.p-score-chip .material-icons { color: #22c55e; font-size: 16px; }

.meal-body {
  flex: 1;
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.calorie-tag {
  color: #22c55e;
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
  text-transform: uppercase;
}

.main-menu-name {
  font-size: 1.4rem;
  font-weight: 900;
  color: #0f172a;
  line-height: 1.25;
  margin-bottom: 20px;
  word-break: keep-all;
}

.info-hint {
  margin-top: auto;
  display: flex;
  align-items: center;
  gap: 6px;
  color: #64748b;
  font-size: 0.85rem;
  font-weight: 700;
  transition: 0.2s;
}

.flip-card:hover .info-hint { color: #22c55e; }

/* ===== 뒷면 (Back) ===== */
.card-back {
  transform: rotateY(180deg);
  padding: 32px 28px;
  background: #fcfdfd;
}

.back-type-label {
  font-size: 0.75rem;
  font-weight: 900;
  color: #22c55e;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.back-header h5 {
  font-size: 1.25rem;
  font-weight: 900;
  margin: 4px 0 24px;
  color: #0f172a;
}

.food-list-container {
  flex: 1;
  overflow-y: auto;
  padding-right: 4px;
}

/* 스크롤바 커스텀 */
.food-list-container::-webkit-scrollbar { width: 4px; }
.food-list-container::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }

.food-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 0;
  border-bottom: 1px solid #f1f5f9;
}

.food-info { display: flex; align-items: center; gap: 8px; }
.main-dot { width: 6px; height: 6px; background: #22c55e; border-radius: 50%; }

.food-name { font-size: 0.95rem; font-weight: 600; color: #475569; }
.food-row.is-main .food-name { color: #0f172a; font-weight: 800; }

.food-cal { color: #94a3b8; font-size: 0.85rem; font-weight: 500; }

.back-footer {
  margin-top: 24px;
}

.back-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 0.8rem;
  color: #94a3b8;
  font-weight: 700;
}
</style>
>>>>>>> FE_Mainpage_Herosection&Navbar
