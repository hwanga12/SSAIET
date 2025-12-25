// src/stores/mealStore.js
import { defineStore } from "pinia"
import axios from "axios"

const API_BASE_URL = "http://127.0.0.1:8000"

export const useMealStore = defineStore("meal", {
  state: () => ({
    // =========================
    // 기존 상태 (유지)
    // =========================
    menus: [],
    isLoading: false,
    error: null,
    isClosed: false,
    currentDateKey: null,

    // =========================
    // 🔥 저녁 관련 상태 (추가)
    // =========================
    dinnerId: null,
    aiMenu: null,
    dinnerReason: null,
    isEaten: null,
  }),

  actions: {
    // =========================
    // 기존 식단 조회 (유지)
    // =========================
    async fetchMeals(dateKey, mealTimeId = "2") {
      this.currentDateKey = dateKey
      this.isLoading = true
      this.error = null
      this.isClosed = false

      try {
        const response = await axios.post(
          `${API_BASE_URL}/meal/save/`,
          { date: dateKey, mealTimeId }
        )

        if (this.currentDateKey !== dateKey) return

        const { success, data } = response.data
        if (!success || !Array.isArray(data)) {
          throw new Error("INVALID_RESPONSE")
        }

        const hasA = data.some(m => m.course_type === "A")
        const hasB = data.some(m => m.course_type === "B")

        if (!hasA && !hasB) {
          this.menus = []
          this.isClosed = true
          return
        }

        this.menus = data
        this.isClosed = false

      } catch (err) {
        if (this.currentDateKey !== dateKey) return
        this.error = err.message || "FETCH_ERROR"
        this.isClosed = false
      } finally {
        if (this.currentDateKey === dateKey) {
          this.isLoading = false
        }
      }
    },

    // =========================
    // 🔥 저녁 추천 받기
    // =========================
    async recommendDinner(dateKey, token) {
      const res = await axios.post(
        `${API_BASE_URL}/meal/recommend-dinner/`,
        { date: dateKey },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      const data = res.data
      this.dinnerId = data.dinner_id
      this.aiMenu = data.ai_menu
      this.dinnerReason = data.reason
      this.isEaten = data.is_eaten
    },

    // =========================
    // 🔥 저녁 먹었어요 / 안 먹었어요
    // =========================
    async updateDinnerStatus({ isEaten, mealId, token }) {
      await axios.post(
        `${API_BASE_URL}/meal/update-dinner-status/`,
        {
          dinner_id: this.dinnerId,
          is_eaten: isEaten,
          meal_id: mealId ?? null,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      this.isEaten = isEaten
    },

    // =========================
    // 🔥 날짜 바뀌면 저녁 상태 초기화
    // =========================
    resetDinnerState() {
      this.dinnerId = null
      this.aiMenu = null
      this.dinnerReason = null
      this.isEaten = null
    },
  },
})
