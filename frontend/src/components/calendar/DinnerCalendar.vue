<template>
  <div class="calendar-wrapper">
    <div class="calendar-grid weekday-header">
      <div v-for="day in weekDays" :key="day" class="weekday">{{ day }}</div>
    </div>

    <div class="calendar-grid calendar-body">
      <div v-for="n in firstDayOffset" :key="'empty-'+n" class="cell empty"></div>
      <div 
        v-for="day in daysInMonth" :key="day" 
        class="cell day-cell"
        :class="[
          {'is-today': isToday(day)},
          getStatusClass(dayMap[dateKey(day)])
        ]"
        @click="$emit('select-date', dateKey(day))"
      >
        <div class="cell-top">
          <span class="day-num">{{ day }}</span>
          <span v-if="isToday(day)" class="today-badge">TODAY</span>
        </div>

        <div v-if="dayMap[dateKey(day)]" class="status-indicator">
          <template v-if="dayMap[dateKey(day)].dinner">
            <span v-if="dayMap[dateKey(day)].dinner.is_eaten === true" class="material-icons status-icon">check_circle</span>
            <span v-else-if="dayMap[dateKey(day)].dinner.is_eaten === false" class="material-icons status-icon">cancel</span>
            <span v-else class="material-icons status-icon">pending</span>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useMealCalendarStore } from "@/stores/mealCalendar"

const props = defineProps({ year: Number, month: Number })
const store = useMealCalendarStore()
const weekDays = ['일', '월', '화', '수', '목', '금', '토']

const firstDayOffset = computed(() => new Date(props.year, props.month - 1, 1).getDay())
const daysInMonth = computed(() => new Date(props.year, props.month, 0).getDate())

const dayMap = computed(() => {
  const map = {}
  store.monthData.forEach(item => { map[item.date] = item })
  return map
})

const isToday = (day) => {
  const now = new Date()
  return now.getFullYear() === props.year && now.getMonth() + 1 === props.month && now.getDate() === day
}

// 셀 자체에 클래스를 부여하여 전체 배경색을 바꿉니다.
const getStatusClass = (data) => {
  if (!data || !data.dinner) return ''
  if (data.dinner.is_eaten === true) return 'state-eaten'
  if (data.dinner.is_eaten === false) return 'state-skipped'
  return 'state-pending'
}

const dateKey = (day) => {
  const m = String(props.month).padStart(2, '0')
  const d = String(day).padStart(2, '0')
  return Number(`${props.year}${m}${d}`)
}
</script>

<style scoped>
.calendar-wrapper { padding: 10px; background: white; border-radius: 24px; }
.calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px; }

.weekday { 
  text-align: center; padding: 12px 0; 
  font-weight: 800; color: #94a3b8; font-size: 0.75rem; 
}

/* 기본 셀 스타일 */
.cell { 
  aspect-ratio: 1; border-radius: 18px; padding: 10px; 
  border: 1px solid #f8fafc; cursor: pointer; 
  display: flex; flex-direction: column; justify-content: space-between; 
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); 
  background: #f8fafc; 
}

.cell-top { display: flex; justify-content: space-between; align-items: flex-start; }
.day-num { font-weight: 700; color: #475569; font-size: 0.9rem; }
.today-badge { font-size: 0.5rem; background: #059669; color: white; padding: 2px 5px; border-radius: 4px; font-weight: 900; }

/* 상태별 디자인 강화 */
.state-eaten { 
  background: #ecfdf5; border-color: #10b981; 
}
.state-eaten .status-icon { color: #10b981; font-size: 1.2rem; }
.state-eaten .day-num { color: #064e3b; }

.state-skipped { 
  background: #fef2f2; border-color: #ef4444; 
}
.state-skipped .status-icon { color: #ef4444; font-size: 1.2rem; }
.state-skipped .day-num { color: #7f1d1d; }

.state-pending { 
  background: #f1f5f9; border-color: #e2e8f0; 
}
.state-pending .status-icon { color: #94a3b8; font-size: 1.2rem; }

/* 효과 */
.day-cell:hover { 
  transform: translateY(-4px); 
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); 
  z-index: 10;
}

.cell.empty { background: transparent; border: none; cursor: default; }

/* 오늘 날짜 강조 */
.is-today:not(.state-eaten):not(.state-skipped) {
  border: 2px solid #059669;
  background: white;
}

.status-indicator {
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
}
</style>