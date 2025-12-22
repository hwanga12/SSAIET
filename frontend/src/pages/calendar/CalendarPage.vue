<template>
  <div class="calendar-layout">
    <BaseNavbar class="nav-fixed" />

    <div class="bg-decoration">
      <div class="blob blob-green"></div>
      <div class="blob blob-soft"></div>
    </div>

    <main class="calendar-page">
      <div class="container">
        <header class="page-header">
          <div class="header-left">
            <div class="icon-badge">
              <span class="material-icons">auto_awesome</span>
            </div>
            <div class="title-group">
              <span class="sub-title">Meal Management</span>
              <h1>나의 <span class="highlight">식단</span> 타임라인</h1>
              <p>AI가 분석한 최적의 영양 밸런스를 확인하세요.</p>
            </div>
          </div>

          <div class="header-right">
            <div class="summary-card">
              <div class="summary-info">
                <span class="label">이달의 식단 실천</span>
                <span class="value">
                  <strong>{{ eatenCount }}</strong>
                  <small>일 실천</small>
                </span>
              </div>
              <div class="summary-icon">🔥</div>
            </div>
          </div>
        </header>

        <section class="calendar-section">
          <div class="calendar-nav">
            <button @click="changeMonth(-1)" class="nav-btn">
              <span class="material-icons">chevron_left</span>
            </button>
            <h2 class="current-month">{{ year }}년 {{ month }}월</h2>
            <button @click="changeMonth(1)" class="nav-btn">
              <span class="material-icons">chevron_right</span>
            </button>
          </div>

          <div class="glass-card">
            <div class="calendar-inner">
               <DinnerCalendar :year="year" :month="month" @select-date="onSelectDate" />
            </div>
            
            <footer class="calendar-legend">
              <div class="legend-item"><span class="dot eaten"></span>식사 완료</div>
              <div class="legend-item"><span class="dot skipped"></span>거름/안먹음</div>
              <div class="legend-item"><span class="dot empty"></span>기록 없음</div>
            </footer>
          </div>
        </section>
      </div>
    </main>

    <DinnerDetailModal 
      v-if="isModalOpen" 
      :detail="calendarStore.dayDetail" 
      @close="closeModal" 
      @eat="handleEatUpdate" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue"
import { useMealCalendarStore } from "@/stores/mealCalendar"
import DinnerCalendar from "@/components/calendar/DinnerCalendar.vue"
import DinnerDetailModal from "@/components/calendar/DinnerDetailModal.vue"
import BaseNavbar from "@/components/common/BaseNavbar.vue"

/* ================= STORE & STATE ================= */
const calendarStore = useMealCalendarStore()
const today = new Date()
const year = ref(today.getFullYear())
const month = ref(today.getMonth() + 1)
const isModalOpen = ref(false)

/* ================= COMPUTED ================= */
// 이달의 실천 횟수 (is_eaten 필드 활용)
const eatenCount = computed(() => {
  if (!calendarStore.monthData) return 0
  return calendarStore.monthData.filter(day => day.dinner?.is_eaten === true).length
})

/* ================= METHODS ================= */
// 월 변경 로직
const changeMonth = (diff) => {
  const newDate = new Date(year.value, month.value - 1 + diff, 1)
  year.value = newDate.getFullYear()
  month.value = newDate.getMonth() + 1
}

// 날짜 선택 시 상세 정보 조회
const onSelectDate = async (dateKey) => {
  await calendarStore.fetchDayDetail(dateKey)
  isModalOpen.value = true
}

// 모달 닫기
const closeModal = () => {
  isModalOpen.value = false
  calendarStore.clearDayDetail()
}

// 식사 여부 업데이트 후 UI 갱신
const handleEatUpdate = async (status) => {
  // 실제 DB 업데이트는 각 프로젝트의 store 액션에 따라 다를 수 있습니다.
  // 업데이트 후 다시 데이터를 불러옵니다.
  await calendarStore.fetchMonth(year.value, month.value)
  if (calendarStore.dayDetail?.date) {
    await calendarStore.fetchDayDetail(calendarStore.dayDetail.date)
  }
}

/* ================= LIFECYCLE & WATCH ================= */
onMounted(() => {
  calendarStore.fetchMonth(year.value, month.value)
})

watch([year, month], () => {
  calendarStore.fetchMonth(year.value, month.value)
})
</script>

<style scoped>
/* 구글 마테리얼 아이콘 폰트 */
@import url("https://fonts.googleapis.com/icon?family=Material+Icons");

/* ===== Layout Base ===== */
.calendar-layout {
  min-height: 100vh;
  background: #fcfdfd;
  position: relative;
  overflow-x: hidden;
  padding-top: 80px;
}

.container {
  max-width: 1080px;
  margin: 0 auto;
  padding: 40px 24px;
  position: relative;
  z-index: 1;
}

/* ===== Header Layout ===== */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 48px;
  gap: 24px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.icon-badge {
  width: 52px;
  height: 52px;
  background: #064e3b;
  color: white;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 16px rgba(6, 78, 59, 0.2);
}

.title-group h1 {
  font-size: 2.4rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.2;
}

.title-group p {
  margin-top: 8px;
  color: #64748b;
  font-size: 1.05rem;
}

.highlight { color: #059669; }

/* ===== Summary Card ===== */
.header-right {
  flex-shrink: 0;
}

.summary-card {
  background: white;
  padding: 24px 32px;
  border-radius: 24px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  border: 1px solid #f1f5f9;
  display: flex;
  align-items: center;
  gap: 20px;
}

.summary-info {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.summary-info .label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 4px;
}

.summary-info .value {
  font-size: 2rem;
  font-weight: 800;
  color: #064e3b;
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.summary-info .value small {
  font-size: 1rem;
  font-weight: 600;
  color: #94a3b8;
}

.summary-icon {
  font-size: 2.2rem;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
}

/* ===== Calendar Navigation ===== */
.calendar-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  margin-bottom: 32px;
}

.current-month {
  font-size: 1.6rem;
  font-weight: 800;
  color: #064e3b;
  min-width: 200px;
  text-align: center;
}

.nav-btn {
  background: white;
  border: 1px solid #e2e8f0;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-btn:hover {
  background: #f0fdf4;
  border-color: #059669;
  color: #059669;
}

/* ===== Glass Card ===== */
.glass-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  border-radius: 32px;
  padding: 48px;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.calendar-legend {
  margin-top: 40px;
  display: flex;
  justify-content: center;
  gap: 32px;
  border-top: 1px solid #f1f5f9;
  padding-top: 32px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  color: #64748b;
}

.dot { width: 10px; height: 10px; border-radius: 50%; }
.dot.eaten { background: #059669; }
.dot.skipped { background: #f87171; }
.dot.empty { background: #e2e8f0; }

/* Background Blobs */
.bg-decoration { position: fixed; inset: 0; z-index: 0; pointer-events: none; }
.blob { position: absolute; filter: blur(100px); opacity: 0.35; border-radius: 50%; }
.blob-green { width: 500px; height: 500px; background: #059669; top: -150px; right: -100px; }
.blob-soft { width: 400px; height: 400px; background: #d1fae5; bottom: -100px; left: -100px; }

/* Responsive */
@media (max-width: 768px) {
  .page-header { flex-direction: column; align-items: flex-start; }
  .header-right { width: 100%; }
  .summary-card { justify-content: space-between; }
  .glass-card { padding: 24px; }
}
</style>