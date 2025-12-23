import { defineStore } from "pinia"
import axios from "axios"

export const useAuthStore = defineStore('auth', {
    state: () => ({
        // 토큰 키 이름을 'accessToken'으로 통일합니다.
        accessToken: localStorage.getItem('accessToken') || null,
        user: JSON.parse(localStorage.getItem('user') || 'null'),
        isLoggedIn: !!localStorage.getItem('accessToken'),
    }),

    getters: {
        // 🔥 사용자가 프로필(키, 몸무게 등)을 입력했는지 확인하는 게터
        // 필수 값인 height나 current_weight가 없으면 false를 반환합니다.
        isProfileComplete: (state) => {
            return !!(state.user && state.user.height && state.user.current_weight);
        }
    },

    actions: {
        // ----------------------------------------
        // ⭐ 1. 로그인 + 토큰 저장
        // ----------------------------------------
        async fetchAndStoreToken(username, password) {
            try {
                const res = await axios.post(
                    "http://localhost:8000/api/accounts/login/",
                    { username, password }
                )

                const token = res.data.access
                this.accessToken = token
                this.isLoggedIn = true
                localStorage.setItem("accessToken", token)

                // 🔥 로그인 직후의 유저 정보(res.data)를 바로 저장
                this.user = res.data
                localStorage.setItem("user", JSON.stringify(res.data))

                return true
            } catch (error) {
                console.error("로그인 실패:", error)
                this.logOut()
                return false
            }
        },

        // ----------------------------------------
        // ⭐ 2. 내 프로필 조회
        // ----------------------------------------
        async fetchMyProfile() {
            if (!this.accessToken) return

            try {
                const res = await axios.get(
                    "http://localhost:8000/api/accounts/me/",
                    { headers: this.getAuthHeader() }
                )

                this.user = res.data
                localStorage.setItem("user", JSON.stringify(res.data))
            } catch (error) {
                if (error.response?.status === 401) {
                    this.logOut()
                }
            }
        },

        // ----------------------------------------
        // ⭐ 3. 프로필 수정 (입력 완료 시 호출)
        // ----------------------------------------
        async updateProfile(payload) {
            try {
                const res = await axios.put(
                    "http://localhost:8000/api/accounts/me/update/",
                    payload,
                    { headers: this.getAuthHeader() }
                );

                // 🔥 수정 성공 후 최신 정보를 다시 가져와서 state 업데이트
                await this.fetchMyProfile();
                return res.data;
            } catch (error) {
                if (error.response?.status === 401) {
                    this.logOut();
                    window.location.href = "/login";
                }
                throw error;
            }
        },

        // ----------------------------------------
        // ⭐ 4. 로그아웃 (초기화)
        // ----------------------------------------
        logOut() {
            this.accessToken = null
            this.user = null
            this.isLoggedIn = false
            localStorage.removeItem("accessToken")
            localStorage.removeItem("user")
        },

        getAuthHeader() {
            const token = this.accessToken || localStorage.getItem("accessToken");
            return token ? { Authorization: `Bearer ${token}` } : {}
        },

        // ----------------------------------------
        // ⭐ 4. 인증 헤더
        // ----------------------------------------
        getAuthHeader() {
            return this.accessToken
                ? { Authorization: `Bearer ${this.accessToken}` }
                : {}
        },

        // ----------------------------------------
        // ⭐ 5. 프로필 수정
        // ----------------------------------------
        // ----------------------------------------
        // ⭐ 5. 프로필 수정
        // ----------------------------------------
        async updateProfile(payload) {
            try {
                // 1. 요청 직전 토큰 재확인 (state에 없으면 localStorage에서라도 가져옴)
                const token = this.accessToken || localStorage.getItem("accessToken");

                if (!token) {
                    throw new Error("인증 토큰이 없습니다. 다시 로그인해주세요.");
                }

                const res = await axios.put(
                    "http://localhost:8000/api/accounts/me/update/",
                    payload,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                );

                // 🔥 서버 기준으로 다시 동기화
                await this.fetchMyProfile();
                return res.data;

            } catch (error) {
                console.error("프로필 수정 에러 상세:", error.response);

                // 2. 만약 401(토큰 만료/잘못됨)이면 로그아웃 처리
                if (error.response?.status === 401) {
                    alert("인증이 만료되었습니다. 다시 로그인해주세요.");
                    this.logOut();
                    // 필요하다면 여기서 router.push('/login')을 호출하거나 페이지를 새로고침 하세요.
                    window.location.href = "/login";
                }
                throw error;
            }
        },

        // ----------------------------------------
        // ⭐ 6. 계정 정보 수정
        // ----------------------------------------
        async updateAccount(payload) {
            const res = await axios.put(
                "http://localhost:8000/api/accounts/me/account/",
                payload,
                { headers: this.getAuthHeader() }
            )

            await this.fetchMyProfile()
            return res.data
        },

        // ----------------------------------------
        // ⭐ 7. 회원 탈퇴
        // ----------------------------------------
        async withdraw() {
            if (!this.accessToken) {
                throw new Error("로그인 상태가 아닙니다.")
            }

            try {
                await axios.delete(
                    "http://localhost:8000/api/accounts/me/delete/",
                    { headers: this.getAuthHeader() }
                )

                this.logOut()
            } catch (error) {
                console.error("회원탈퇴 실패:", error)
                throw error
            }
        },
    },
})