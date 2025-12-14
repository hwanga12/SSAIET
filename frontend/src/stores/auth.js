import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        accessToken: localStorage.getItem('accessToken') || null,
        isLoggedIn: !!localStorage.getItem('accessToken'),
        user: JSON.parse(localStorage.getItem('user')) || null,
    }),

    actions: {
        // ----------------------------------------
        // ⭐ 1. 로그인 + 사용자 정보 저장
        // ----------------------------------------
        async fetchAndStoreToken(username, password) {
            try {
                const res = await axios.post("http://localhost:8000/api/accounts/login/", {
                    username,
                    password,
                });

                // Access Token 저장
                const token = res.data.access;
                this.accessToken = token;
                this.isLoggedIn = true;
                localStorage.setItem('accessToken', token);

                // 🔥 사용자 정보 저장
                const userData = {
                    username: res.data.username,
                    name: res.data.name,
                    email: res.data.email,
                    height: res.data.height,
                    current_weight: res.data.current_weight,
                    target_weight: res.data.target_weight,
                    muscle_mass: res.data.muscle_mass,
                    body_fat: res.data.body_fat,
                    age: res.data.age,
                    gender: res.data.gender,
                    allergies: res.data.allergies,
                };

                this.user = userData;
                localStorage.setItem('user', JSON.stringify(userData));

                return true;

            } catch (error) {
                console.error("로그인/토큰 발급 실패:", error);
                this.logOut();
                return false;
            }
        },

        // ----------------------------------------
        // ⭐ 2. 로그아웃
        // ----------------------------------------
        logOut() {
            this.accessToken = null;
            this.user = null;
            this.isLoggedIn = false;

            localStorage.removeItem('accessToken');
            localStorage.removeItem('user');
        },

        // ----------------------------------------
        // ⭐ 3. 인증 헤더 (토큰 포함)
        // ----------------------------------------
        getAuthHeader() {
            return this.accessToken
                ? { Authorization: `Bearer ${this.accessToken}` }
                : {};
        },

        // ----------------------------------------
        // ⭐ 4. 프로필 수정 (이름/키/몸무게/목표/체지방 등등)
        // ----------------------------------------
        async updateProfile(payload) {
            const res = await axios.put(
                "http://localhost:8000/api/accounts/me/update/",
                payload,
                { headers: this.getAuthHeader() }
            );

            // store + localStorage 업데이트
            this.user = { ...this.user, ...payload };
            localStorage.setItem("user", JSON.stringify(this.user));

            return res.data;
        },

        // ----------------------------------------
        // ⭐ 5. 계정 수정 (username, email, password)
        // ----------------------------------------
        async updateAccount(payload) {
            const res = await axios.put(
                "http://localhost:8000/api/accounts/me/account/",
                payload,
                { headers: this.getAuthHeader() }
            );

            // 비밀번호 외에는 user 객체 수정 필요
            const updatedFields = { ...payload };
            delete updatedFields.password; // password는 user 데이터에서 제외

            this.user = { ...this.user, ...updatedFields };
            localStorage.setItem("user", JSON.stringify(this.user));

            return res.data;
        }
    }
});