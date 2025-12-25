import { defineStore } from "pinia"
import axios from "axios"
import { useAuthStore } from "./auth"

const API_URL = "http://localhost:8000"

export const useMealCalendarStore = defineStore("mealCalendar", {
    state: () => ({
        monthData: [],
        dayDetail: null,
        isLoading: false,
        error: null,
    }),

    actions: {
        // 📅 월 캘린더
        async fetchMonth(year, month) {
            this.isLoading = true
            this.error = null
            try {
                const auth = useAuthStore()
                const res = await axios.get(
                    `${API_URL}/meal/calendar/month/`,
                    {
                        params: { year, month },
                        headers: {
                            Authorization: `Bearer ${auth.accessToken}`,
                        },
                    }
                )
                this.monthData = res.data
            } catch (err) {
                this.error = "캘린더 데이터를 불러오지 못했습니다."
            } finally {
                this.isLoading = false
            }
        },

        // 📄 날짜 상세
        async fetchDayDetail(date) {
            this.isLoading = true
            this.error = null
            try {
                const auth = useAuthStore()
                const res = await axios.get(
                    `${API_URL}/meal/calendar/day/${date}/`,
                    {
                        headers: {
                            Authorization: `Bearer ${auth.accessToken}`,
                        },
                    }
                )
                this.dayDetail = res.data
            } catch (err) {
                this.error = "상세 데이터를 불러오지 못했습니다."
            } finally {
                this.isLoading = false
            }
        },

        clearDayDetail() {
            this.dayDetail = null
        },

        // 🌙 저녁 먹음 / 안 먹음 업데이트 (🔥 핵심)
        async updateDinnerStatus(date, isEaten) {
            try {
                const auth = useAuthStore()
                await axios.post(
                    `${API_URL}/meal/dinner/eat/`,
                    {
                        date: date,
                        is_eaten: isEaten,
                    },
                    {
                        headers: {
                            Authorization: `Bearer ${auth.accessToken}`,
                        },
                    }
                )

                // 🔥 로컬 상태 즉시 반영 (모달)
                if (this.dayDetail && this.dayDetail.dinner) {
                    this.dayDetail.dinner.is_eaten = isEaten
                }

                // 🔥 월 캘린더에도 반영
                const day = this.monthData.find(d => d.date === date)
                if (day && day.dinner) {
                    day.dinner.is_eaten = isEaten
                }

            } catch (err) {
                console.error("저녁 상태 업데이트 실패", err)
            }
        },
    },
})
