<template>
  <div class="login-page">
    <h1>로그인</h1>

    <input 
      v-model="username" 
      placeholder="아이디"
      class="input"
    />

    <input 
      type="password"
      v-model="password"
      placeholder="비밀번호"
      class="input"
    />

    <button class="login-btn" @click="handleLogin">
      로그인
    </button>

    <!-- 🔥 회원가입 안내 영역 -->
    <div class="signup-box">
      <p>계정이 없으신가요?</p>
      <button class="signup-btn" @click="goSignup">회원가입 하러가기</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import axios from "axios"

const username = ref("")
const password = ref("")
const router = useRouter()
const authStore = useAuthStore()

const handleLogin = async () => {
  try {
    const res = await axios.post("http://localhost:8000/api/accounts/login/", {
      username: username.value,
      password: password.value,
    })

    // 토큰 저장
    authStore.accessToken = res.data.access
    localStorage.setItem("accessToken", res.data.access)
    authStore.isLoggedIn = true

    // 사용자 정보 저장
    authStore.user = {
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
    }
    localStorage.setItem("user", JSON.stringify(authStore.user))

    // 이동
    router.push("/")
  } catch (err) {
    console.error(err)
    alert("로그인 실패!")
  }
}

// 🔥 회원가입 페이지로 이동
const goSignup = () => {
  router.push("/signup")
}
</script>

<style scoped>
.login-page {
  width: 320px;
  margin: 60px auto;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.input {
  padding: 8px;
  border: 1px solid #ccc;
}

.login-btn {
  padding: 10px;
  cursor: pointer;
}

.signup-box {
  margin-top: 20px;
  text-align: center;
}

.signup-btn {
  margin-top: 5px;
  padding: 8px 12px;
  cursor: pointer;
  color: white;
  background-color: #4a90e2;
  border: none;
  border-radius: 6px;
}
</style>