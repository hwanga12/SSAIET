import { defineStore } from "pinia"
import axios from "axios"
import { useAuthStore } from "./auth"

export const useMypageStore = defineStore("mypage", {
    state: () => ({
        counts: null,
        posts: [],
        comments: [],
        likedPosts: [],
        isLoading: false,
        error: null,
    }),

    actions: {
        async fetchMypage() {
            const authStore = useAuthStore()
            this.isLoading = true
            this.error = null

            try {
                const res = await axios.get(
                    "http://localhost:8000/api/accounts/mypage/",
                    {
                        headers: {
                            Authorization: `Bearer ${authStore.accessToken}`,
                        },
                    }
                )

                this.counts = res.data.counts
                this.posts = res.data.posts
                this.comments = res.data.comments
                this.likedPosts = res.data.liked_posts
            } catch (err) {
                this.error = err.response?.data || "마이페이지 로딩 실패"
            } finally {
                this.isLoading = false
            }
        },
    },
})
