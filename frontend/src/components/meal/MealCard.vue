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
              <span class="material-icons">touch_app</span>
              <span>터치하여 구성 보기</span>
            </div>
          </div>
        </div>

        <div class="card-face card-back">
          <div class="back-header">
            <div class="header-main">
              <span class="back-type-label">{{ mealTypeLabel }} 코스</span>
              <h4 class="back-title">식단 상세 구성</h4>
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
              <span class="label">총 열량</span>
              <span class="val"><strong>{{ totalCalorie }}</strong> kcal</span>
            </div>
            <button class="return-btn" @click.stop="toggleFlip">
              <span class="material-icons">flip_camera_android</span>
              메뉴 사진 보기
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
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.meal-card-wrapper {
  --brand-green: #22c55e;
  --dark-slate: #0f172a;
  --light-bg: #f8fafc;
  width: 100%;
  max-width: 380px;
  margin: 0 auto;
}

.card-perspective { perspective: 2000px; height: 500px; }

.flip-card {
  position: relative; width: 100%; height: 100%;
  transform-style: preserve-3d;
  transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  cursor: pointer;
}
.flip-card.is-flipped { transform: rotateY(180deg); }

.card-face {
  position: absolute; inset: 0; backface-visibility: hidden;
  border-radius: 40px; background: white; overflow: hidden;
  box-shadow: 0 15px 45px rgba(0,0,0,0.06);
  border: 1px solid rgba(0,0,0,0.03);
  display: flex; flex-direction: column;
}

/* --- 앞면 디자인 (Visual) --- */
.card-top-bar {
  position: absolute; top: 24px; left: 24px; right: 24px;
  z-index: 10; display: flex; justify-content: space-between; align-items: flex-start;
}

.type-badge {
  display: flex; align-items: center; gap: 6px;
  padding: 8px 16px; border-radius: 14px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
  color: var(--dark-slate);
  font-size: 0.85rem; font-weight: 800;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.type-badge.A { color: #166534; }
.type-badge.B { color: #854d0e; }

.premium-pscore {
  background: var(--dark-slate);
  padding: 6px 14px; border-radius: 16px;
  display: flex; flex-direction: column; align-items: center;
  color: var(--brand-green);
  box-shadow: 0 8px 16px rgba(15, 23, 42, 0.2);
}
.premium-pscore .label { font-size: 0.55rem; font-weight: 900; color: white; opacity: 0.7; margin-bottom: 2px; }
.premium-pscore .value { font-size: 1.2rem; font-weight: 900; }

.meal-photo-area { 
  height: 65%; background-size: cover; background-position: center; 
  position: relative; background-color: #f1f5f9; 
}
.empty-photo { height: 100%; display: flex; align-items: center; justify-content: center; }
.empty-icon-box { 
  width: 60px; height: 60px; background: white; border-radius: 50%; 
  display: flex; align-items: center; justify-content: center; color: #cbd5e1;
}

.photo-overlay { 
  position: absolute; inset: 0; 
  background: linear-gradient(to bottom, transparent 30%, rgba(255,255,255,0.8) 70%, white 100%); 
}

.meal-content { flex: 1; padding: 0 30px 30px; display: flex; flex-direction: column; align-items: center; margin-top: -10px; z-index: 2; }
.calorie-pill {
  background: #f0fdf4; color: #166534; padding: 6px 16px; border-radius: 100px;
  font-size: 0.9rem; font-weight: 800; display: flex; align-items: center; gap: 5px; margin-bottom: 12px;
}
.calorie-pill .material-icons { font-size: 16px; color: var(--brand-green); }

.menu-title {
  font-size: 1.6rem; font-weight: 900; color: var(--dark-slate);
  margin: 0 0 15px; text-align: center; line-height: 1.25; letter-spacing: -0.5px;
}

.interaction-hint { 
  margin-top: auto; color: #94a3b8; font-size: 0.85rem; 
  display: flex; align-items: center; gap: 5px; font-weight: 700;
  background: #f8fafc; padding: 6px 14px; border-radius: 10px;
}

/* --- 뒷면 디자인 (Details) --- */
.card-back { transform: rotateY(180deg); background: white; }
.back-header {
  padding: 30px 24px; display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1px solid #f1f5f9; background: #fafafa;
}
.back-type-label { font-size: 0.8rem; color: var(--brand-green); font-weight: 900; letter-spacing: 1px; }
.back-title { font-size: 1.3rem; color: var(--dark-slate); margin: 4px 0 0; font-weight: 900; }
.s-label { font-size: 0.6rem; color: #94a3b8; font-weight: 900; text-align: right; }
.s-value { font-size: 1.4rem; color: var(--brand-green); font-weight: 900; }

.menu-list-container { 
  flex: 1; padding: 24px; display: flex; flex-direction: column; gap: 10px; 
  overflow-y: auto; background: white;
}
.menu-row { 
  display: flex; justify-content: space-between; align-items: center; 
  padding: 14px 18px; border-radius: 18px; background: #f8fafc;
  transition: 0.2s;
}
.is-main-row { background: #f0fdf4; border: 1px solid rgba(34, 197, 94, 0.2); }
.main-dot { width: 8px; height: 8px; background: var(--brand-green); border-radius: 50%; margin-right: 10px; }
.food-name { font-weight: 700; color: #475569; font-size: 1rem; }
.is-main-row .food-name { color: #166534; font-weight: 900; }
.food-cal { font-size: 0.85rem; color: #94a3b8; font-weight: 600; }

.back-footer { padding: 20px 24px 30px; background: white; }
.footer-summary { 
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 20px; font-size: 1rem; color: #64748b; font-weight: 700;
  padding: 0 10px;
}
.footer-summary strong { color: var(--dark-slate); font-size: 1.2rem; font-weight: 900; }

.return-btn {
  width: 100%; padding: 18px; border-radius: 20px; border: none;
  background: var(--dark-slate); color: white; font-weight: 900; font-size: 1rem;
  display: flex; align-items: center; justify-content: center; gap: 8px;
  cursor: pointer; transition: 0.3s;
}
.return-btn:hover { background: var(--brand-green); transform: scale(1.02); }

/* 스크롤바 커스텀 */
.menu-list-container::-webkit-scrollbar { width: 4px; }
.menu-list-container::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }
</style>