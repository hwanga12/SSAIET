<template>
  <div class="meal-card-wrapper">
    <div class="card-perspective">
      <div 
        class="flip-card" 
        :class="{ 'is-flipped': isFlipped }"
        @click="toggleFlip"
      >
        <div class="card-face card-front">
          <div class="card-top-bar">
            <div class="type-badge" :class="props.mealType">
              <span class="material-icons">{{ props.mealType === 'A' ? 'flatware' : 'auto_awesome' }}</span>
              {{ mealTypeLabel }}
            </div>
            
            <div class="premium-pscore">
              <span class="label">P-SCORE</span>
              <span class="value">{{ props.mealData.p_score }}</span>
            </div>
          </div>

          <div 
            class="meal-photo-area"
            :style="{ backgroundImage: props.mealData.photoUrl ? `url(${props.mealData.photoUrl})` : 'none' }"
          >
            <div v-if="!props.mealData.photoUrl" class="empty-photo">
              <div class="empty-icon-box">
                <span class="material-icons">restaurant</span>
              </div>
            </div>
            <div class="photo-overlay"></div>
          </div>

          <div class="meal-content">
            <div class="calorie-pill">
              <span class="material-icons">bolt</span>
              {{ totalCalorie }} kcal
            </div>
            <h3 class="menu-title">{{ mainMenuName }}</h3>
            
            <div class="interaction-hint">
              <span class="material-icons">sync_alt</span>
              <span>식단 상세 확인</span>
            </div>
          </div>
        </div>

        <div class="card-face card-back">
          <div class="back-header">
            <div class="header-main">
              <span class="back-type-label">{{ mealTypeLabel }} 메뉴</span>
              <h4 class="back-title">식단 구성</h4>
            </div>
            <div class="back-score-summary">
              <span class="s-label">P-SCORE</span>
              <span class="s-value">{{ props.mealData.p_score }}</span>
            </div>
          </div>

          <div class="menu-list-container">
            <div
              v-for="(food, index) in props.mealData.foods"
              :key="index"
              class="menu-row"
              :class="{ 'is-main-row': food.is_main }"
            >
              <div class="row-left">
                <div v-if="food.is_main" class="main-dot"></div>
                <span class="food-name">{{ food.name }}</span>
              </div>
              <span class="food-cal">{{ food.calorie }} <small>kcal</small></span>
            </div>
          </div>

          <div class="back-footer">
            <div class="footer-summary">
              <span class="label">Total</span>
              <span class="val"><strong>{{ totalCalorie }}</strong> kcal</span>
            </div>
            <button class="return-btn">
              <span class="material-icons">refresh</span>
              사진으로 돌아가기
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"

const props = defineProps({
  mealData: { type: Object, required: true },
  mealType: { type: String, required: true },
})

const isFlipped = ref(false)
const toggleFlip = () => isFlipped.value = !isFlipped.value

const mealTypeLabel = computed(() => props.mealType === "A" ? "한식" : "일품")
const mainMenuName = computed(() => {
  const main = props.mealData.foods?.find(f => f.is_main)
  return main ? main.name : props.mealData.foods?.[0]?.name || "메뉴 준비 중"
})
const totalCalorie = computed(() => {
  return props.mealData.foods?.reduce((sum, f) => sum + (Number(f.calorie) || 0), 0) || 0
})
</script>

<style scoped>
/* 프리미엄 화이트 & 연초록 테마 변수 */
.meal-card-wrapper {
  --mint-green: #4ade80; /* 밝고 건강한 연초록 */
  --soft-green: #f0fdf4; /* 연초록 배경 */
  --deep-green: #166534; /* 텍스트 강조용 */
  --white: #ffffff;
  width: 100%;
  max-width: 380px;
  margin: 0 auto;
}

.card-perspective { perspective: 1500px; height: 500px; }
.flip-card {
  position: relative; width: 100%; height: 100%;
  transform-style: preserve-3d;
  transition: transform 0.6s cubic-bezier(0.23, 1, 0.32, 1);
  cursor: pointer;
}
.flip-card.is-flipped { transform: rotateY(180deg); }

.card-face {
  position: absolute; inset: 0; backface-visibility: hidden;
  border-radius: 32px; background: var(--white); overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.04);
  border: 1px solid #f0f0f0;
  display: flex; flex-direction: column;
}

/* --- 앞면 디자인 --- */
.card-top-bar {
  position: absolute; top: 20px; left: 20px; right: 20px;
  z-index: 10; display: flex; justify-content: space-between; align-items: center;
}

.type-badge {
  display: flex; align-items: center; gap: 5px;
  padding: 6px 14px; border-radius: 12px;
  background: var(--white); color: var(--deep-green);
  font-size: 0.8rem; font-weight: 800;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
  border: 1px solid var(--soft-green);
}

.premium-pscore {
  background: var(--mint-green);
  padding: 4px 12px; border-radius: 12px;
  display: flex; flex-direction: column; align-items: center;
  color: white;
}
.premium-pscore .label { font-size: 0.55rem; font-weight: 900; opacity: 0.9; }
.premium-pscore .value { font-size: 1.1rem; font-weight: 900; }

.meal-photo-area { height: 60%; background-size: cover; background-position: center; position: relative; background-color: var(--soft-green); }
.empty-photo { height: 100%; display: flex; align-items: center; justify-content: center; color: var(--mint-green); }
.empty-icon-box { width: 50px; height: 50px; background: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; }

.photo-overlay { position: absolute; inset: 0; background: linear-gradient(to bottom, transparent 40%, var(--white) 100%); }

.meal-content { flex: 1; padding: 0 24px 24px; display: flex; flex-direction: column; align-items: center; }
.calorie-pill {
  background: var(--soft-green); color: var(--deep-green); padding: 4px 12px; border-radius: 100px;
  font-size: 0.85rem; font-weight: 700; display: flex; align-items: center; gap: 4px; margin-bottom: 8px;
}
.calorie-pill .material-icons { font-size: 14px; }

.menu-title {
  font-size: 1.5rem; font-weight: 800; color: #1a1a1a;
  margin: 4px 0 10px; text-align: center; line-height: 1.3;
}

.interaction-hint { margin-top: auto; color: #aaa; font-size: 0.8rem; display: flex; align-items: center; gap: 4px; font-weight: 600; }

/* --- 뒷면 디자인 --- */
.card-back { transform: rotateY(180deg); background: var(--white); }
.back-header {
  padding: 24px; display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1px solid #f9f9f9;
}
.back-type-label { font-size: 0.75rem; color: var(--mint-green); font-weight: 800; }
.back-title { font-size: 1.2rem; color: #333; margin: 0; font-weight: 800; }
.s-label { display: block; font-size: 0.55rem; color: #ccc; font-weight: 800; text-align: right; }
.s-value { font-size: 1.2rem; color: var(--mint-green); font-weight: 900; }

.menu-list-container { flex: 1; padding: 16px 20px; display: flex; flex-direction: column; gap: 6px; overflow-y: auto; }
.menu-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; border-radius: 14px; background: #fcfcfc; }
.is-main-row { background: var(--soft-green); border: 1px solid #e2fbe9; }
.main-dot { width: 6px; height: 6px; background: var(--mint-green); border-radius: 50%; margin-right: 8px; }
.food-name { font-weight: 600; color: #555; font-size: 0.95rem; }
.is-main-row .food-name { color: var(--deep-green); font-weight: 800; }
.food-cal { font-size: 0.8rem; color: #bbb; }

.back-footer { padding: 16px 24px 24px; }
.footer-summary { display: flex; justify-content: space-between; margin-bottom: 16px; font-size: 0.95rem; color: #666; }
.footer-summary strong { color: #1a1a1a; font-weight: 800; }

.return-btn {
  width: 100%; padding: 14px; border-radius: 16px; border: none;
  background: #222; color: white; font-weight: 700;
  display: flex; align-items: center; justify-content: center; gap: 6px;
  cursor: pointer; transition: background 0.2s;
}
.return-btn:hover { background: var(--deep-green); }
</style>