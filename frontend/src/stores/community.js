import { defineStore } from "pinia"
import axios from "axios"
import { useAuthStore } from "@/stores/auth"

const API_URL = "http://localhost:8000/api/community"

export const useCommunityStore = defineStore("community", {
    state: () => ({
        posts: [],
        comments: [],
        myComments: [],
        isLoading: false,
    }),

    actions: {
        // ✅ [유틸] 헤더 생성기: 토큰이 있으면 넣고, 없으면 빈 객체 반환
        getHeaders() {
            const auth = useAuthStore()
            if (auth.accessToken) {
                return { headers: { Authorization: `Bearer ${auth.accessToken}` } }
            }
            return {} // 비로그인 요청 (헤더 없음)
        },

        // 1. 게시글 작성 (로그인 필수)
        async addPost(payload) {
            this.isLoading = true
            try {
                // 작성은 무조건 토큰이 필요하므로 직접 헤더 생성
                const auth = useAuthStore()
                const res = await axios.post(`${API_URL}/posts/`, payload, {
                    headers: { Authorization: `Bearer ${auth.accessToken}` },
                })
                return res.data
            } catch (error) {
                console.error("게시글 작성 실패:", error)
                this.handleAuthError(error)
                throw error
            } finally {
                this.isLoading = false
            }
        },

        // 2. 게시글 수정 (로그인 필수)
        async updatePost(postId, payload) {
            const auth = useAuthStore()
            try {
                const res = await axios.put(
                    `${API_URL}/posts/${postId}/`,
                    payload,
                    { headers: { Authorization: `Bearer ${auth.accessToken}` } }
                )

                const idx = this.posts.findIndex(p => p.id === postId)
                if (idx !== -1) {
                    this.posts.splice(idx, 1, res.data)
                }

                return res.data
            } catch (error) {
                console.error("게시글 수정 실패:", error)
                this.handleAuthError(error)
                throw error
            }
        },

        // ✅ 3. 카테고리별 게시글 조회 (누구나 가능)
        async fetchPostsByCategory(category) {
            this.isLoading = true
            try {
                // getHeaders()를 사용하여 비로그인 유저도 요청 가능하게 변경
                const res = await axios.get(
                    `${API_URL}/category/${category.toLowerCase()}/`,
                    this.getHeaders()
                )
                this.posts = res.data
            } catch (error) {
                console.error("카테고리 로드 실패:", error)
                // 조회 실패는 인증 에러 처리를 하지 않음 (또는 401이 아닐 때만 처리)
            } finally {
                this.isLoading = false
            }
        },

        // ✅ 4. 전체 게시글 조회 (누구나 가능)
        async fetchPosts() {
            try {
                // getHeaders() 사용 -> 토큰 없으면 그냥 요청 보냄
                const res = await axios.get(`${API_URL}/posts/`, this.getHeaders())
                this.posts = res.data
            } catch (error) {
                console.error("전체 게시글 로드 실패:", error)
            }
        },

        // 5. 좋아요 토글 (로그인 필수)
        async toggleLike(postId) {
            const auth = useAuthStore()
            try {
                const res = await axios.post(
                    `${API_URL}/posts/${postId}/like/`,
                    {},
                    { headers: { Authorization: `Bearer ${auth.accessToken}` } }
                )

                const targetPost = this.posts.find(p => p.id === postId)
                if (targetPost) {
                    if (res.data.liked) {
                        targetPost.likes_count += 1
                        targetPost.is_liked = true
                    } else {
                        targetPost.likes_count -= 1
                        targetPost.is_liked = false
                    }
                }
            } catch (error) {
                // 401 에러(비로그인)일 경우 처리
                this.handleAuthError(error)
            }
        },

        // ✅ 6. 댓글 조회 (누구나 가능)
        async fetchComments(postId) {
            try {
                const res = await axios.get(
                    `${API_URL}/posts/${postId}/comments/`,
                    this.getHeaders()
                )
                this.comments = res.data
            } catch (error) {
                console.error("댓글 로드 실패:", error)
            }
        },

        // 7. 댓글 작성 (로그인 필수)
        async createComment(postId, content) {
            const auth = useAuthStore()
            try {
                await axios.post(
                    `${API_URL}/posts/${postId}/comments/`,
                    { content },
                    { headers: { Authorization: `Bearer ${auth.accessToken}` } }
                )
                await this.fetchComments(postId)
            } catch (error) {
                console.error("댓글 등록 실패:", error)
                throw error
            }
        },

        // 8. 댓글 수정 (로그인 필수)
        async updateComment(postId, commentId, content) {
            const auth = useAuthStore()
            try {
                const res = await axios.put(
                    `${API_URL}/comments/${commentId}/`,
                    { content: content },
                    { headers: { Authorization: `Bearer ${auth.accessToken}` } }
                )

                const idx = this.comments.findIndex(c => c.id === commentId)
                if (idx !== -1) {
                    this.comments.splice(idx, 1, res.data)
                }

                return res.data
            } catch (error) {
                console.error("댓글 수정 실패:", error)
                this.handleAuthError(error)
                throw error
            }
        },

        // 9. 댓글 삭제 (로그인 필수)
        async deleteComment(postId, commentId) {
            const auth = useAuthStore()
            try {
                await axios.delete(
                    `${API_URL}/comments/${commentId}/`,
                    { headers: { Authorization: `Bearer ${auth.accessToken}` } }
                )
                await this.fetchComments(postId)
            } catch (error) {
                console.error("댓글 삭제 실패:", error)
            }
        },

        // 10. 게시글 삭제 (로그인 필수)
        async deletePost(postId) {
            const auth = useAuthStore()
            try {
                const res = await axios.delete(
                    `${API_URL}/posts/${postId}/`,
                    { headers: { Authorization: `Bearer ${auth.accessToken}` } }
                )

                if (this.posts && this.posts.length > 0) {
                    this.posts = this.posts.filter(p => p.id !== postId)
                }
                return res
            } catch (error) {
                console.error("게시글 삭제 실패:", error)
                throw error
            }
        },

        // 11. 인증 에러 공통 처리
        handleAuthError(error) {
            if (error.response?.status === 401) {
                alert("로그인이 필요한 기능입니다.")
                
            }
        },

        // 12. 내 댓글 조회 (로그인 필수)
        async fetchMyComments() {
            const auth = useAuthStore()
            try {
                const res = await axios.get(`${API_URL}/my-comments/`, {
                    headers: { Authorization: `Bearer ${auth.accessToken}` },
                })
                this.myComments = res.data
            } catch (error) {
                console.error("내 댓글 로드 실패:", error)
                this.handleAuthError(error)
            }
        },
        // ✅ 게시글 단건 조회 (상세 페이지용)
        async fetchPostDetail(postId) {
        try {
            const res = await axios.get(
            `${API_URL}/posts/${postId}/`,
            this.getHeaders()
            )

            const post = res.data

            const exists = this.posts.find(p => p.id === post.id)
            if (!exists) {
            this.posts.push(post)
            }

            return post
        } catch (error) {
            console.error("게시글 단건 조회 실패:", error)
            throw error
        }
        }

    },
})