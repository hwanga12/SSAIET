// src/stores/mealStore.js
<<<<<<< HEAD
import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000' 

export const useMealStore = defineStore('meal', {
  state: () => ({
    menus: [], 
    isLoading: false,
    error: null,
  }),
  actions: {
    async fetchMeals(date = null, mealTimeId = '2') {
      this.isLoading = true
      this.error = null
      this.menus = []

      // 백엔드 요청 바디 준비 (날짜가 null이면 백엔드가 오늘 날짜를 사용함)
      const requestBody = {
          date: date ? date.replace(/-/g, '') : undefined, // YYYY-MM-DD -> YYYYMMDD 변환
          mealTimeId: mealTimeId,
      }

      try {
        const response = await axios.post(`${API_BASE_URL}/meal/save/`, requestBody)
        
        if (response.data.success && response.data.data) {
          this.menus = response.data.data
        } else {
          this.error = "식단 데이터를 불러오는데 실패했습니다."
        }
      } catch (err) {
        this.error = "서버 통신 중 오류가 발생했습니다."
        console.error("Meal Fetch Error:", err)
      } finally {
        this.isLoading = false
      }
    },
  },
})
=======
import { defineStore } from "pinia"
import axios from "axios"

const API_BASE_URL = "http://127.0.0.1:8000"

export const useMealStore = defineStore("meal", {
  state: () => ({
    menus: [],
    isLoading: false,
    error: null,
    isClosed: false,
    currentDateKey: null, // 🔥 현재 유효한 날짜
  }),

  actions: {
    async fetchMeals(dateKey, mealTimeId = "2") {
      // 🔐 이 요청의 날짜를 기록
      this.currentDateKey = dateKey

      this.isLoading = true
      this.error = null
      this.isClosed = false

      try {
        const response = await axios.post(
          `${API_BASE_URL}/meal/save/`,
          { date: dateKey, mealTimeId }
        )

        const { success, data } = response.data

        // ❌ 응답 도착 시점에 날짜가 바뀌었으면 무조건 무시
        if (this.currentDateKey !== dateKey) {
          return
        }

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
        // 날짜 바뀐 후 에러면 무시
        if (this.currentDateKey !== dateKey) return

        this.error = err.message || "FETCH_ERROR"
        this.isClosed = false

      } finally {
        if (this.currentDateKey === dateKey) {
          this.isLoading = false
        }
      }
    },
  },
})
>>>>>>> FE_Mainpage_Herosection&Navbar
