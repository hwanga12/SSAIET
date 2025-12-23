<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <Transition name="modal-pop" appear>
      <div class="modal-card" v-if="detail">
        <header class="modal-header">
          <div class="date-info">
            <span class="calendar-icon"></span>
            <h3>{{ formattedDate }} <span class="highlight">식단 상세</span></h3>
          </div>
          <button class="close-btn" @click="$emit('close')">
            <span class="material-icons">close</span>
          </button>
        </header>

        <div class="modal-body">
          <div v-if="detail.lunch" class="meal-group lunch">
            <div class="meal-content-wrapper">
              <div class="meal-info">
                <span class="tag">LUNCH</span>
                <h4 class="meal-name">{{ detail.lunch.meal_name }}</h4>
                <div class="location">
                  <span class="material-icons">place</span>
                  {{ detail.lunch.restaurant }}
                </div>
              </div>
              
              <div class="p-score-container">
                <div class="p-score-circle">
                  <span class="p-label">P-SCORE</span>
                  <span class="p-value">{{ detail.lunch.p_score }}</span>
                </div>
              </div>
            </div>
          </div>

          <div v-if="detail.dinner" class="meal-group dinner" :class="{ 'did-skip': detail.dinner.is_eaten === false }">
            <div class="tag-ai">
              <span class="sparkle">✨</span> AI RECOMMENDATION
            </div>
            <h4 class="meal-name">{{ detail.dinner.ai_menu_name }}</h4>
            
            <div class="ai-reason-box">
              <div class="ai-badge">
                <span class="material-icons">auto_awesome</span>
                <span>AI TIP</span>
              </div>
              <p class="reason-text">{{ detail.dinner.ai_reason_text }}</p>
            </div>

            <div class="action-buttons">
              <button 
                class="btn-action eat" 
                :class="{ active: detail.dinner.is_eaten === true }" 
                @click="$emit('eat', true)"
              >
                <span class="material-icons">{{ detail.dinner.is_eaten === true ? 'check_circle' : 'add_circle' }}</span>
                먹었어요
              </button>
              
              <button 
                class="btn-action skip" 
                :class="{ active: detail.dinner.is_eaten === false }" 
                @click="$emit('eat', false)"
              >
                <span class="material-icons">{{ detail.dinner.is_eaten === false ? 'unpublished' : 'highlight_off' }}</span>
                안 먹었어요
              </button>
            </div>
          </div>

          <div v-else class="empty-recommendation">
            <div class="empty-icon">🍽️</div>
            <p class="empty-title">아직 추천 식단이 없어요</p>
            <p class="empty-desc">
             아직 추천받은 식단이 없네요. <br/>
             AI 추천을 통해 메뉴 고민을 덜어드릴게요!
            </p>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  detail: Object
})

defineEmits(['close', 'eat'])

const formattedDate = computed(() => {
  if (!props.detail?.date) return ''
  const s = String(props.detail.date)
  const m = parseInt(s.substring(4, 6))
  const d = parseInt(s.substring(6, 8))
  return `${m}월 ${d}일`
})
</script>

<style scoped>
.modal-backdrop {
  position: fixed; inset: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(10px);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000; padding: 20px;
}

.modal-card {
  background: #ffffff;
  width: 100%; max-width: 420px;
  border-radius: 32px; padding: 30px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;
}
.date-info h3 { font-size: 1.25rem; font-weight: 800; color: #1e293b; margin: 0; }
.highlight { color: #059669; font-size: 0.9rem; font-weight: 600; margin-left: 4px; }

.close-btn {
  background: #f1f5f9; border: none; width: 34px; height: 34px;
  border-radius: 50%; cursor: pointer; color: #64748b;
  display: flex; align-items: center; justify-content: center;
}

.meal-group {
  padding: 20px; border-radius: 24px; margin-bottom: 16px;
  border: 1px solid #f1f5f9; transition: all 0.3s ease;
}

/* 점심 스타일 */
.lunch { background: #f8fafc; border: 1px solid #e2e8f0; }
.meal-content-wrapper { display: flex; justify-content: space-between; align-items: center; }

.p-score-circle {
  width: 64px; height: 64px;
  background: white; border: 4px solid #3b82f6;
  border-radius: 50%; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  box-shadow: 0 4px 10px rgba(59, 130, 246, 0.2);
}
.p-label { font-size: 0.55rem; font-weight: 900; color: #94a3b8; }
.p-value { font-size: 1.1rem; font-weight: 900; color: #1e40af; }

/* 저녁/AI 스타일 */
.dinner { background: #f0fdf4; border: 2px dashed #10b981; }
.dinner.did-skip {
  background: #fef2f2; border: 2px solid #ef4444;
  box-shadow: inset 0 0 12px rgba(239, 68, 68, 0.1);
}

.tag-ai {
  color: #059669; font-size: 0.75rem; font-weight: 900; margin-bottom: 12px;
  display: flex; align-items: center; gap: 4px;
}
.dinner.did-skip .tag-ai { color: #ef4444; }

.ai-reason-box {
  background: white; border: 1px solid #dcfce7;
  padding: 16px; border-radius: 20px; margin-top: 14px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}
.dinner.did-skip .ai-reason-box { border-color: #fee2e2; }

.ai-badge {
  display: inline-flex; align-items: center; gap: 4px;
  background: #10b981; color: white;
  padding: 4px 10px; border-radius: 8px;
  font-size: 0.7rem; font-weight: 800; margin-bottom: 10px;
}
.ai-badge .material-icons { font-size: 14px; }
.dinner.did-skip .ai-badge { background: #ef4444; }

.reason-text {
  font-size: 0.9rem; color: #334155; line-height: 1.6;
  margin: 0; word-break: keep-all;
}

/* 추천 데이터 없음 스타일 */
.empty-recommendation {
  padding: 40px 20px; text-align: center;
  background: #f8fafc; border-radius: 28px;
  border: 1.5px dashed #cbd5e1; margin-top: 8px;
}
.empty-icon { font-size: 2.5rem; margin-bottom: 12px; opacity: 0.5; }
.empty-title { font-size: 1.1rem; font-weight: 800; color: #64748b; margin-bottom: 6px; }
.empty-desc { font-size: 0.85rem; color: #94a3b8; line-height: 1.5; margin: 0; }

/* 공통 버튼 및 텍스트 */
.tag { font-size: 0.7rem; font-weight: 900; color: #94a3b8; display: block; margin-bottom: 4px; }
.meal-name { font-size: 1.2rem; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
.location { display: flex; align-items: center; gap: 4px; color: #64748b; font-size: 0.85rem; }

.action-buttons { display: flex; gap: 10px; margin-top: 24px; }
.btn-action {
  flex: 1; height: 56px; border-radius: 18px; border: 1.5px solid #e2e8f0;
  background: white; cursor: pointer; display: flex; align-items: center;
  justify-content: center; gap: 6px; font-weight: 800; color: #94a3b8;
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.btn-action.eat.active {
  background: #059669; color: white; border-color: #059669;
  box-shadow: 0 8px 20px rgba(5, 150, 105, 0.3);
}

.btn-action.skip.active {
  background: #dc2626; color: white; border-color: #b91c1c;
  box-shadow: 0 8px 20px rgba(220, 38, 38, 0.4);
  transform: scale(1.02);
}

.btn-action:hover:not(.active) { background: #f8fafc; transform: translateY(-2px); }

.modal-pop-enter-active { transition: all 0.3s ease-out; }
.modal-pop-enter-from { opacity: 0; transform: scale(0.9) translateY(30px); }
</style>