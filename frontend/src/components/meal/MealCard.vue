<template>
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

    </div>
  </div>
</template>

<script setup>
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
});
</script>

<style scoped>
/* -------------------- 컨테이너 -------------------- */
.meal-card-container {
  perspective: 1000px;
  width: 350px;
  height: 400px;
  cursor: pointer;
}

.meal-card {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
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
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

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
