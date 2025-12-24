import { ref, computed } from "vue"
import { defineStore } from "pinia"
import axios from "axios"

export const useAuthStore = defineStore("auth", () => {
    /* ===============================
       1️⃣ STATE
    =============================== */

    // 토큰 (로컬스토리지 우선)
    const token = ref(localStorage.getItem("accessToken") || null)

    // 유저 정보
    const storedUser = localStorage.getItem("user")
    const user = ref(storedUser ? JSON.parse(storedUser) : null)

    /* ===============================
       2️⃣ GETTERS
    =============================== */

    const isLoggedIn = computed(() => !!token.value)
    const accessToken = computed(() => token.value)

    /* ===============================
       3️⃣ AXIOS 기본 헤더 유지
    =============================== */

    if (token.value) {
        axios.defaults.headers.common["Authorization"] = `Bearer ${token.value}`
    }

    /* ===============================
       4️⃣ ACTIONS
    =============================== */

    // ✅ 공통 Authorization 헤더 반환 (🔥 핵심)
    const getAuthHeader = () => {
        if (!token.value) {
            console.warn("⚠️ accessToken 없음")
            return {}
        }
        return {
            Authorization: `Bearer ${token.value}`,
        }
    }

    // 로그인 성공 처리
    const loginSuccess = (newToken, newName, newUsername) => {
        token.value = newToken
        user.value = { name: newName, username: newUsername }

        localStorage.setItem("accessToken", newToken)
        localStorage.setItem("user", JSON.stringify(user.value))

        axios.defaults.headers.common["Authorization"] = `Bearer ${newToken}`
    }

    // 로그아웃
    const logOut = () => {
        token.value = null
        user.value = null

        localStorage.removeItem("accessToken")
        localStorage.removeItem("user")

        delete axios.defaults.headers.common["Authorization"]
    }

    // 로그인 요청
    const fetchAndStoreToken = async (username, password) => {
        try {
            const res = await axios.post(
                "http://localhost:8000/api/accounts/login/",
                { username, password }
            )

            const receivedToken =
                res.data.key || res.data.token || res.data.access
            const receivedName = res.data.name || username

            if (!receivedToken) {
                console.error("❌ 토큰 없음:", res.data)
                return false
            }

            loginSuccess(receivedToken, receivedName, username)
            return true

        } catch (err) {
            console.error("❌ 로그인 에러:", err)
            if (err.response) {
                console.error("📛 응답 데이터:", err.response.data)
            }
            return false
        }
    }

    // 회원 탈퇴
    const withdraw = async () => {
        try {
            await axios.delete(
                "http://localhost:8000/api/accounts/delete/",
                { headers: getAuthHeader() }
            )
            logOut()
        } catch (err) {
            console.error("❌ 회원 탈퇴 실패:", err)
            throw err
        }
    }

    // 계정 정보 수정 (추후 구현)
    const updateAccount = async (payload) => {
        // TODO
    }

    /* ===============================
       5️⃣ EXPORT
    =============================== */

    const updateProfile = async (payload) => {
    try {
        const res = await axios.patch(
            "http://localhost:8000/api/accounts/update-profile/",
            payload,
            { headers: getAuthHeader() }
        )

        // 🔄 로컬 user 정보 갱신
        user.value = {
            ...user.value,
            ...res.data,
        }
        localStorage.setItem("user", JSON.stringify(user.value))

        return res.data
    } catch (err) {
        console.error("❌ 프로필 수정 실패:", err)
        throw err
    }
    }

    return {
        // state
        token,
        user,

        // getters
        isLoggedIn,
        accessToken,

        // actions
        getAuthHeader,
        loginSuccess,
        logOut,
        fetchAndStoreToken,
        withdraw,
        updateAccount,
        updateProfile,
    }
})
