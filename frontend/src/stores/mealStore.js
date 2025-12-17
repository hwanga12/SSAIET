// src/stores/mealStore.js
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
