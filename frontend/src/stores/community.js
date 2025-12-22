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
        // 1. 게시글 작성
        async addPost(payload) {
            const auth = useAuthStore()
            this.isLoading = true
            try {
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

        // ⭐ 2. 게시글 수정 (반응성 강화)
        async updatePost(postId, payload) {
            const auth = useAuthStore()
            try {
                const res = await axios.put(
                    `${API_URL}/posts/${postId}/`,
                    payload,
                    {
                        headers: { Authorization: `Bearer ${auth.accessToken}` },
                    }
                )

                // ✅ Vue 3에서 배열 내부 객체 변경을 확실히 감지하도록 splice 사용
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

        // 3. 카테고리별 게시글 조회
        async fetchPostsByCategory(category) {
            const auth = useAuthStore()
            this.isLoading = true
            try {
                const res = await axios.get(
                    `${API_URL}/category/${category.toLowerCase()}/`,
                    { headers: { Authorization: `Bearer ${auth.accessToken}` } }
                )
                this.posts = res.data
            } catch (error) {
                console.error("카테고리 로드 실패:", error)
                this.handleAuthError(error)
            } finally {
                this.isLoading = false
            }
        },

        // 4. 전체 게시글 조회
        async fetchPosts() {
            const auth = useAuthStore()
            if (!auth.accessToken) return
            try {
                const res = await axios.get(`${API_URL}/posts/`, {
                    headers: { Authorization: `Bearer ${auth.accessToken}` },
                })
                this.posts = res.data
            } catch (error) {
                this.handleAuthError(error)
            }
        },

        // 5. 좋아요 토글
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
                this.handleAuthError(error)
            }
        },

        // 6. 댓글 조회
        async fetchComments(postId) {
            const auth = useAuthStore()
            try {
                const res = await axios.get(
                    `${API_URL}/posts/${postId}/comments/`,
                    { headers: { Authorization: `Bearer ${auth.accessToken}` } }
                )
                this.comments = res.data
            } catch (error) {
                console.error("댓글 로드 실패:", error)
            }
        },

        // 7. 댓글 작성
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

        // ✅ 인자를 3개 받도록 수정: postId, commentId, content
        async updateComment(postId, commentId, content) {
            const auth = useAuthStore()
            try {
                console.log("스토어 내부 데이터 확인:", { postId, commentId, content })

                const res = await axios.put(
                    `${API_URL}/comments/${commentId}/`, // commentId(14)가 여기로 가야 함
                    { content: content },               // content("222222")가 여기로 가야 함
                    { headers: { Authorization: `Bearer ${auth.accessToken}` } }
                )

                // 로컬 상태 반영
                const idx = this.comments.findIndex(c => c.id === commentId)
                if (idx !== -1) {
                    this.comments.splice(idx, 1, res.data)
                }

                return res.data; // ✅ 이걸 해야 콘솔에 undefined가 안 뜹니다!
            } catch (error) {
                console.error("댓글 수정 실패:", error)
                this.handleAuthError(error)
                throw error
            }
        },

        // 9. 댓글 삭제
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

        // 10. 게시글 삭제
        async deletePost(postId) {
            const auth = useAuthStore()
            try {
                const res = await axios.delete(
                    `${API_URL}/posts/${postId}/`,
                    { headers: { Authorization: `Bearer ${auth.accessToken}` } }
                )

                console.log("1. 서버 응답 성공:", res.status);

                // ✅ 만약 this.posts가 로드되지 않은 상태라면 filter에서 에러가 납니다.
                if (this.posts && this.posts.length > 0) {
                    this.posts = this.posts.filter(p => p.id !== postId)
                }

                console.log("2. 로컬 상태 업데이트 완료");
                return res; // 성공 리턴
            } catch (error) {
                // 실제 서버 에러인지, 위 로직(filter 등)에서 난 에러인지 구분
                console.error("삭제 함수 내부에서 문제 발생:", error);
                throw error
            }
        },

        // 11. 인증 에러 공통 처리
        handleAuthError(error) {
            if (error.response?.status === 401) {
                const auth = useAuthStore()
                alert("세션이 만료되었습니다. 다시 로그인해주세요.")
                auth.logOut()
                window.location.href = "/login"
            }
        },
        async fetchMyComments() {
            const auth = useAuthStore()
            try {
                const res = await axios.get(`${API_URL}/my-comments/`, {
                    headers: { Authorization: `Bearer ${auth.accessToken}` },
                })
                this.myComments = res.data
                console.log("내 댓글 목록 로드 성공:", res.data)
            } catch (error) {
                console.error("내 댓글 로드 실패:", error)
                this.handleAuthError(error)
            }
        },
    },
})