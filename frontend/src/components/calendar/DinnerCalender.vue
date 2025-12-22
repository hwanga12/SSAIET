<template>
  <section class="calendar-wrapper">
    <h2 class="calendar-title">🍽 저녁 식단 캘린더</h2>

    <div class="calendar-grid">
      <div
        v-for="day in days"
        :key="day.dateKey"
        class="calendar-day"
        :class="statusClass(day.status)"
        @click="emit('select-date', day.dateKey)"
      >
        <span class="day-number">{{ day.day }}</span>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import axios from "axios"
import { useAuthStore } from "@/stores/auth"

const emit = defineEmits(["select-date"])
const authStore = useAuthStore()

/* ===== 현재 보여줄 년/월 (나중에 props로 빼도 됨) ===== */
const year = 2025
const month = 12

/* ===== 서버에서 받은 상태 맵 =====
{
  "20251201": "eaten",
  "20251202": "skipped"
}
*/
const calendarMap = ref({})

/* ===== 달력 셀 생성 ===== */
const days = computed(() => {
  const lastDay = new Date(year, month, 0).getDate()
  const result = []

  for (let d = 1; d <= lastDay; d++) {
    const dateKey =
      `${year}${String(month).padStart(2, "0")}${String(d).padStart(2, "0")}`

    result.push({
      day: d,
      dateKey,
      status: calendarMap.value[dateKey] || null
    })
  }

  return result
})

/* ===== 상태 → CSS ===== */
const statusClass = (status) => {
  if (status === "eaten") return "eaten"
  if (status === "skipped") return "not-eaten"
  return ""
}

/* ===== 캘린더 데이터 요청 ===== */
const fetchCalendar = async () => {
  const res = await axios.post(
    "http://localhost:8000/meal/calendar/",
    { year, month },
    { headers: authStore.getAuthHeader() }
  )

  calendarMap.value = res.data.calendar || {}
}

onMounted(fetchCalendar)
</script>

<style scoped>
.calendar-wrapper {
  max-width: 1000px;
  margin: 80px auto;
}

.calendar-title {
  font-size: 1.7rem;
  font-weight: 900;
  margin-bottom: 36px;
  text-align: center;
  color: #0f172a;
}

/* ===== Grid ===== */
.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 16px;
}

/* ===== Day Cell ===== */
.calendar-day {
  height: 110px;
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #f1f5f9;
  padding: 12px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.05);

  cursor: pointer;
  transition: all 0.25s ease;

  display: flex;
  align-items: flex-start;
}

/* 클릭 방해 제거 */
.calendar-day * {
  pointer-events: none;
}

.calendar-day:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.08);
}

/* 날짜 숫자 */
.day-number {
  font-weight: 900;
  font-size: 1rem;
  color: #0f172a;
}

/* ===== 상태 ===== */
.eaten {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
}

.not-eaten {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

.eaten .day-number,
.not-eaten .day-number {
  color: white;
}
</style>
