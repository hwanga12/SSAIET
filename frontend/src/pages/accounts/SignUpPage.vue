<template>
  <div class="signup-page">
    <div class="bg-decoration">
      <div class="blob blob-green"></div>
      <div class="blob blob-light"></div>
    </div>

    <div class="signup-container">
      <div class="signup-card">
        
        <div class="visual-side">
          <div class="visual-content">
            <div class="logo-area" @click="goHome">
              <span class="logo-text">SSAIET</span>
            </div>
            <h2 class="visual-title">
              Start Your<br />
              <span class="highlight">Healthy</span> Life.
            </h2>
            <p class="visual-text">
              SSAFY인의 건강한 식단 관리,<br />
              SSAIET와 함께라면 어렵지 않습니다.
            </p>
          </div>
          <div class="visual-pattern"></div>
        </div>

        <div class="form-side">
          <div class="form-inner">
            <div class="form-header">
              <h3 class="form-title">Join Us</h3>
              <p class="form-subtitle">
                이미 계정이 있으신가요? 
                <span class="login-link" @click="goLogin">로그인하기</span>
              </p>
            </div>

            <form @submit.prevent="submitSignup" class="input-group">
              <div class="input-field">
                <label>이름</label>
                <input 
                  v-model="form.name" 
                  placeholder="성함을 입력하세요"
                  class="custom-input"
                  :class="{ 'input-error': errors.name }"
                  @input="clearError('name')"
                />
                <p v-if="errors.name" class="error-msg">{{ errors.name }}</p>
              </div>

              <div class="input-field">
                <label>아이디</label>
                <input 
                  v-model="form.username" 
                  placeholder="영문 소문자와 숫자만 입력 가능합니다"
                  class="custom-input"
                  :class="{ 'input-error': errors.username }"
                  @input="clearError('username')"
                />
                <p v-if="errors.username" class="error-msg">{{ errors.username }}</p>
              </div>

              <div class="input-field">
                <label>비밀번호</label>
                <input 
                  type="password"
                  v-model="form.password" 
                  placeholder="8자 이상 입력하세요"
                  class="custom-input"
                  :class="{ 'input-error': errors.password }"
                  @input="clearError('password')"
                />
                <p v-if="errors.password" class="error-msg">{{ errors.password }}</p>
              </div>

              <div class="action-group">
                <button type="submit" class="signup-btn" :disabled="isLoading">
                  <span v-if="!isLoading" class="btn-text">가입 완료</span>
                  <span v-else class="btn-text">처리 중...</span>
                  <span class="material-icons">arrow_forward</span>
                </button>

                <button type="button" class="home-btn" @click="goHome">
                  <span class="material-icons">home</span>
                  <span class="btn-text">메인페이지로 돌아가기</span>
                </button>
              </div>
            </form>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import axios from "axios"

const router = useRouter()
const authStore = useAuthStore()
const isLoading = ref(false)

const form = reactive({
  username: "",
  password: "",
  name: "",
})

const errors = reactive({
  username: "",
  password: "",
  name: "",
})

const clearError = (field) => { errors[field] = "" }

const submitSignup = async () => {
  Object.keys(errors).forEach(key => errors[key] = "")
  isLoading.value = true

  try {
    await axios.post("http://localhost:8000/api/accounts/signup/", form)
    const loginSuccess = await authStore.fetchAndStoreToken(form.username, form.password)
    
    if (loginSuccess) {
      alert("회원가입이 완료되었습니다! 🥗")
      router.replace("/profile-setup")
    } else {
      router.push("/login")
    }
  } catch (err) {
    const data = err.response?.data
    if (!data) return
    
    Object.entries(data).forEach(([field, messages]) => {
      if (errors.hasOwnProperty(field)) {
        errors[field] = Array.isArray(messages) ? messages[0] : messages
      }
    })
  } finally {
    isLoading.value = false
  }
}

const goLogin = () => router.push("/login")
const goHome = () => router.push("/")
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

.signup-page {
  position: relative;
  width: 100%;
  height: 100vh;
  min-height: 900px;
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
.signup-container { position: relative; z-index: 1; width: 100%; max-width: 1100px; padding: 0 20px; }
.signup-card { 
  display: flex; 
  background: white; 
  border-radius: 40px; 
  border: 1px solid rgba(0,0,0,0.05);
  box-shadow: 0 40px 100px rgba(0, 0, 0, 0.08); 
  height: 750px; 
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
.visual-title { font-size: 3.8rem; font-weight: 900; color: #0f172a; line-height: 1.1; margin: 30px 0; letter-spacing: -2px; }
.highlight { color: #22c55e; }
.visual-text { font-size: 1.25rem; color: #64748b; line-height: 1.6; }

/* 오른쪽 폼 */
.form-side { flex: 1.2; background: white; display: flex; align-items: center; justify-content: center; padding: 40px; }
.form-inner { width: 100%; max-width: 400px; }
.form-header { margin-bottom: 30px; }
.form-title { font-size: 2.5rem; font-weight: 900; color: #0f172a; margin-bottom: 8px; }
.form-subtitle { font-size: 1rem; color: #64748b; }
.login-link { color: #22c55e; font-weight: 800; cursor: pointer; margin-left: 5px; }

/* 입력 필드 */
.input-group { display: flex; flex-direction: column; gap: 14px; margin-bottom: 24px; }
.input-field { display: flex; flex-direction: column; gap: 6px; }
.input-field label { font-size: 13px; font-weight: 700; color: #1e293b; margin-left: 4px; }

.custom-input {
  height: 50px;
  padding: 0 16px;
  border-radius: 12px;
  border: 1.5px solid #e2e8f0;
  font-size: 15px;
  transition: 0.2s;
}
.custom-input:focus { outline: none; border-color: #22c55e; box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.1); }

.input-error { border-color: #ef4444 !important; background: #fffcfc; }
.error-msg { font-size: 12px; color: #ef4444; font-weight: 600; margin-left: 4px; }

/* 버튼 그룹 */
.action-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 10px;
}

.signup-btn {
  width: 100%;
  height: 56px;
  background: #0f172a;
  color: white;
  border: none;
  border-radius: 14px;
  font-size: 17px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  cursor: pointer;
  transition: 0.3s;
}
.signup-btn:hover:not(:disabled) { background: #22c55e; transform: translateY(-2px); box-shadow: 0 10px 20px rgba(34, 197, 94, 0.2); }

.home-btn {
  width: 100%;
  height: 52px;
  background: white;
  color: #64748b;
  border: 1.5px solid #e2e8f0;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
}
.home-btn:hover {
  background: #f8fafc;
  color: #0f172a;
  border-color: #cbd5e1;
}

.terms-text { margin-top: 24px; font-size: 12px; color: #94a3b8; text-align: center; line-height: 1.5; }
.terms-text span { font-weight: 700; color: #64748b; text-decoration: underline; cursor: pointer; }
</style>