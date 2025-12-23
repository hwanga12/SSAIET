<template>
  <div class="login-page">
    <div class="bg-decoration">
      <div class="blob blob-green"></div>
      <div class="blob blob-light"></div>
    </div>

    <div class="login-container">
      <div class="login-card">
        
        <div class="visual-side">
          <div class="visual-content">
            <div class="logo-area" @click="goHome">
              <span class="logo-text">SSAIET</span>
            </div>
            <h2 class="visual-title">
              Welcome<br />
              <span class="highlight">Back</span>.
            </h2>
            <p class="visual-text">
              당신의 데이터는 더 건강한<br />
              내일을 향해 달리고 있습니다.
            </p>
          </div>
          <div class="visual-pattern"></div>
        </div>

        <div class="form-side">
          <div class="form-inner">
            <div class="form-header">
              <h3 class="form-title">Login</h3>
              <p class="form-subtitle">
                아직 계정이 없으신가요? 
                <span class="signup-link" @click="goSignup">회원가입 하기</span>
              </p>
            </div>

            <div class="input-group">
              <div class="input-field">
                <label>아이디</label>
                <input 
                  v-model="username" 
                  placeholder="아이디를 입력하세요"
                  class="custom-input"
                  :class="{ 'input-error': errorType === 'username' || errorType === 'all' }"
                  @input="clearError"
                  @keyup.enter="handleLogin"
                />
                <p v-if="errorType === 'username' || (errorType === 'all' && !username)" class="error-msg">
                  아이디를 입력해주세요.
                </p>
              </div>

              <div class="input-field">
                <label>비밀번호</label>
                <input 
                  type="password"
                  v-model="password" 
                  placeholder="비밀번호를 입력하세요"
                  class="custom-input"
                  :class="{ 'input-error': errorType === 'password' || errorType === 'all' }"
                  @input="clearError"
                  @keyup.enter="handleLogin"
                />
                <p v-if="errorType === 'password' || (errorType === 'all' && !password)" class="error-msg">
                  비밀번호를 입력해주세요.
                </p>
                <p v-if="loginFailed" class="error-msg mt-1">
                  아이디 또는 비밀번호가 일치하지 않습니다.
                </p>
              </div>
            </div>

            <div class="action-group">
              <button class="login-btn" @click="handleLogin">
                <span class="btn-text">로그인</span>
                <span class="material-icons">login</span>
              </button>
              
              <button class="home-btn" @click="goHome">
                <span class="material-icons">home</span>
                <span class="btn-text">메인페이지로 돌아가기</span>
              </button>
            </div>
          </div>
        </div>

      </div>
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
const errorType = ref("") 
const loginFailed = ref(false)

const router = useRouter()
const authStore = useAuthStore()

const clearError = () => {
  errorType.value = ""
  loginFailed.value = false
}

const handleLogin = async () => {
  clearError()

  if (!username.value && !password.value) {
    errorType.value = "all"
    return
  }
  if (!username.value) {
    errorType.value = "username"
    return
  }
  if (!password.value) {
    errorType.value = "password"
    return
  }
  
  try {
    const res = await axios.post("http://localhost:8000/api/accounts/login/", {
      username: username.value,
      password: password.value,
    })

    authStore.accessToken = res.data.access
    localStorage.setItem("accessToken", res.data.access)
    authStore.isLoggedIn = true

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

    router.push("/")
  } catch (err) {
    loginFailed.value = true 
  }
}

const goSignup = () => router.push("/signup")
const goHome = () => router.push("/")
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.login-page {
  position: relative;
  width: 100%;
  height: 100vh;
  min-height: 800px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fcfdfd;
}

/* 배경 장식 */
.bg-decoration {
  position: absolute;
  inset: 0;
  z-index: 0;
}
.blob {
  position: absolute;
  filter: blur(100px);
  border-radius: 50%;
  opacity: 0.2;
}
.blob-green { width: 600px; height: 600px; background: #22c55e; top: -100px; right: -100px; }
.blob-light { width: 500px; height: 500px; background: #e2e8f0; bottom: -100px; left: -100px; }

/* 카드 디자인 */
.login-container { position: relative; z-index: 1; width: 100%; max-width: 1050px; padding: 0 20px; }
.login-card { 
  display: flex; 
  background: white; 
  border-radius: 40px; 
  border: 1px solid rgba(0,0,0,0.05);
  box-shadow: 0 40px 100px rgba(0, 0, 0, 0.08); 
  height: 600px; 
  overflow: hidden; 
}

/* 왼쪽 비주얼 */
.visual-side { 
  flex: 1; 
  background: #f8fafc; 
  padding: 60px; 
  display: flex; 
  flex-direction: column; 
  justify-content: center; 
  position: relative;
  border-right: 1px solid #f1f5f9;
}
.logo-text { font-size: 22px; font-weight: 900; color: #22c55e; letter-spacing: 4px; cursor: pointer; }
.visual-title { font-size: 4rem; font-weight: 900; color: #0f172a; line-height: 1.1; margin: 30px 0; letter-spacing: -2px; }
.highlight { color: #22c55e; }
.visual-text { font-size: 1.2rem; color: #64748b; line-height: 1.6; }

/* 오른쪽 폼 */
.form-side { flex: 1.2; background: white; display: flex; align-items: center; justify-content: center; padding: 40px; }
.form-inner { width: 100%; max-width: 360px; }
.form-header { margin-bottom: 30px; }
.form-title { font-size: 2.5rem; font-weight: 900; color: #0f172a; margin-bottom: 8px; }
.form-subtitle { font-size: 1rem; color: #64748b; }
.signup-link { color: #22c55e; font-weight: 800; cursor: pointer; margin-left: 5px; }

/* 입력 필드 */
.input-group { display: flex; flex-direction: column; gap: 18px; margin-bottom: 25px; }
.input-field { display: flex; flex-direction: column; gap: 6px; }
.input-field label { font-size: 14px; font-weight: 700; color: #1e293b; margin-left: 4px; }

.custom-input {
  height: 52px;
  padding: 0 16px;
  border-radius: 12px;
  border: 1.5px solid #e2e8f0;
  font-size: 15px;
  transition: 0.2s;
}
.custom-input:focus { outline: none; border-color: #22c55e; box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.1); }

/* 에러 스타일 */
.input-error { border-color: #ef4444 !important; background: #fffcfc; }
.error-msg { font-size: 12px; color: #ef4444; font-weight: 600; margin-left: 4px; margin-top: 2px; }
.mt-1 { margin-top: 4px; }

/* 버튼 그룹 */
.action-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.login-btn {
  width: 100%;
  height: 54px;
  background: #0f172a;
  color: white;
  border: none;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  transition: 0.2s;
}
.login-btn:hover { background: #22c55e; transform: translateY(-2px); box-shadow: 0 10px 20px rgba(34, 197, 94, 0.2); }

/* 메인페이지 버튼 스타일 */
.home-btn {
  width: 100%;
  height: 50px;
  background: white;
  color: #64748b;
  border: 1.5px solid #e2e8f0;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s;
}
.home-btn:hover {
  background: #f8fafc;
  color: #0f172a;
  border-color: #cbd5e1;
}

.material-icons { font-size: 18px; }
</style>